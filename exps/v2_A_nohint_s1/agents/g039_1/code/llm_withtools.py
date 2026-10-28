import ast
import json
import re
import anthropic
import backoff
import openai
import copy
import traceback

from llm import create_client, get_response_from_llm
from prompts.tooluse_prompt import get_tooluse_prompt
from tools import load_all_tools

CLAUDE_MODEL = 'claude-3-5-sonnet-20241022'
OPENAI_MODEL = 'claude-3-5-sonnet-20241022'

class EmptyResponseError(Exception):
    """Raised by chat_with_agent(raise_on_empty=True) when the final assistant message is empty
    (no non-whitespace text and no tool_use), or when the API call failed before producing a reply."""
    def __init__(self, message, msg_history=None):
        super().__init__(message)
        self.msg_history = msg_history if msg_history is not None else []

def _history_has_nonempty_reply(msg_history):
    """True if the final assistant message has non-whitespace text or a tool_use block."""
    for msg in reversed(msg_history or []):
        if not isinstance(msg, dict):
            continue
        if msg.get('role') != 'assistant':
            continue
        content = msg.get('content', [])
        if isinstance(content, str):
            return bool(content.strip())
        for b in content:
            if isinstance(b, dict):
                if b.get('type') == 'tool_use':
                    return True
                if b.get('type') == 'text' and (b.get('text') or '').strip():
                    return True
            elif getattr(b, 'type', None) == 'tool_use':
                return True
        return False
    # No assistant message at all (e.g. the API call failed) counts as empty
    return False

def _serialize_response(response):
    """Best-effort full serialization of an SDK response object for logs."""
    try:
        if hasattr(response, 'model_dump_json'):
            return response.model_dump_json(indent=2)
        if hasattr(response, 'model_dump'):
            return json.dumps(response.model_dump(), indent=2, default=str)
    except Exception:
        pass
    return repr(response)

def _block_type(block):
    if isinstance(block, dict):
        return block.get('type')
    return getattr(block, 'type', None)

def _response_has_text_or_tool(response, model=''):
    """True if a raw SDK response contains non-empty text or a tool call."""
    if response is None:
        return False
    if 'claude' in model:
        for block in (getattr(response, 'content', None) or []):
            if _block_type(block) == 'tool_use':
                return True
            if _block_type(block) == 'text' and (getattr(block, 'text', '') or '').strip():
                return True
        return False
    if model.startswith('o3-'):
        for item in (getattr(response, 'output', None) or []):
            if getattr(item, 'type', None) == 'function_call':
                return True
            if getattr(item, 'type', None) == 'message':
                for c in (getattr(item, 'content', None) or []):
                    if (getattr(c, 'text', '') or '').strip():
                        return True
        try:
            return bool((getattr(response, 'output_text', '') or '').strip())
        except Exception:
            return False
    return bool(str(response).strip())

def log_response_diagnostics(response, model='', logging=print, label='Response'):
    """Log stop_reason, content block types, usage and, if the response has no text and
    no tool call, an explicit EMPTY RESPONSE line with the full serialized response."""
    try:
        stop_reason = getattr(response, 'stop_reason', None)
        status = getattr(response, 'status', None)
        incomplete = getattr(response, 'incomplete_details', None)
        if 'claude' in model:
            block_types = [_block_type(b) for b in (getattr(response, 'content', None) or [])]
        elif model.startswith('o3-'):
            block_types = [getattr(i, 'type', None) for i in (getattr(response, 'output', None) or [])]
        else:
            block_types = []
        usage = getattr(response, 'usage', None)
        logging(f"[diag] {label}: model={model} stop_reason={stop_reason} status={status} "
                f"incomplete={incomplete} block_types={block_types} usage={usage}")
        if not _response_has_text_or_tool(response, model=model):
            logging(f"EMPTY RESPONSE from {model} ({label}): stop_reason={stop_reason} "
                    f"block_types={block_types}\nFull response:\n{_serialize_response(response)}")
    except Exception:
        logging(f"[diag] failed to log diagnostics: {traceback.format_exc()}")

def process_tool_call(tools_dict, tool_name, tool_input):
    try:
        if tool_name in tools_dict:
            return tools_dict[tool_name]['function'](**tool_input)
        else:
            return f"Error: Tool '{tool_name}' not found"
    except Exception as e:
        return f"Error executing tool '{tool_name}': {str(e)}"

DEFAULT_MAX_TOKENS = 16384
MAX_TOKENS_CAP = 65536
THINKING_BUDGET = 4000  # must stay strictly below max_tokens

def _normalize_thinking(thinking, max_tokens):
    """Return a valid thinking config for the request, or None (omit the parameter).
    An enabled budget must be >=1024 and strictly smaller than max_tokens; otherwise thinking is dropped."""
    if not isinstance(thinking, dict):
        return None
    if thinking.get('type') == 'disabled':
        return {'type': 'disabled'}
    if thinking.get('type') == 'enabled':
        budget = int(thinking.get('budget_tokens', 0))
        if budget >= 1024 and budget < max_tokens:
            return {'type': 'enabled', 'budget_tokens': budget}
    return None

@backoff.on_exception(
    backoff.expo,
    (openai.RateLimitError, openai.APITimeoutError, anthropic.RateLimitError, anthropic.APIStatusError),
    max_time=600,
    max_value=60,
)
def get_response_withtools(
    client, model, messages, tools, tool_choice,
    logging=print, max_retry=3,
    max_tokens=DEFAULT_MAX_TOKENS, thinking=None,
):
    try:
        if 'claude' in model:
            kwargs = dict(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                tool_choice=tool_choice,
                tools=tools,
            )
            thinking_cfg = _normalize_thinking(thinking, max_tokens)
            if thinking_cfg is not None:
                kwargs['thinking'] = thinking_cfg
            response = client.messages.create(**kwargs)
        elif model.startswith('o3-'):
            response = client.responses.create(
                model=model,
                input=messages,
                tool_choice=tool_choice,
                tools=tools,
                parallel_tool_calls=False
            )
            response = response
        else:
            raise ValueError(f"Unsupported model: {model}")
        return response
    except Exception as e:
        logging(f"Error in get_response_withtools: {type(e).__name__}: {str(e)}\n{traceback.format_exc()}")
        if max_retry > 0:
            return get_response_withtools(client, model, messages, tools, tool_choice,
                                          logging=logging, max_retry=max_retry - 1,
                                          max_tokens=max_tokens, thinking=thinking)

        # Hitting the context window limit
        if 'Input is too long for requested model' in str(e):
            pass

        raise  # Re-raise the exception after logging

def _stop_reason_max_tokens_empty(response, model='claude'):
    """True if the response was cut off at max_tokens with no non-empty text and no tool_use
    (typically all output budget was consumed by hidden thinking)."""
    if response is None:
        return False
    return getattr(response, 'stop_reason', None) == 'max_tokens' and not _response_has_text_or_tool(response, model=model)

def _call_claude_with_escalation(client, model, messages, tools, tool_choice, logging, label,
                                 max_tokens=DEFAULT_MAX_TOKENS, thinking=None):
    """One Claude request. If the reply is empty and stop_reason == 'max_tokens' (output budget
    consumed by hidden thinking), immediately re-issue it: first with max_tokens doubled,
    then with thinking disabled and max_tokens doubled again (capped). Bounded, no sleeping."""
    response = get_response_withtools(
        client=client, model=model, messages=messages, tool_choice=tool_choice, tools=tools,
        logging=logging, max_tokens=max_tokens, thinking=thinking,
    )
    cur_tokens, cur_thinking = max_tokens, thinking
    for step in range(2):
        if not _stop_reason_max_tokens_empty(response, model=model):
            break
        if step == 0:
            new_tokens, new_thinking = min(cur_tokens * 2, MAX_TOKENS_CAP), thinking
            why = 'doubling max_tokens'
        else:
            new_tokens, new_thinking = min(cur_tokens * 2, MAX_TOKENS_CAP), {'type': 'disabled'}
            why = 'disabling thinking and doubling max_tokens'
        logging(f"[escalate] {label}: empty reply with stop_reason=max_tokens at max_tokens={cur_tokens}; "
                f"retrying ({why}) -> max_tokens={new_tokens}, thinking={new_thinking}")
        cur_tokens, cur_thinking = new_tokens, new_thinking
        response = get_response_withtools(
            client=client, model=model, messages=messages, tool_choice=tool_choice, tools=tools,
            logging=logging, max_tokens=cur_tokens, thinking=cur_thinking,
        )
    return response

def check_for_tool_use(response, model=''):
    """
    Checks if the response contains a tool call.
    """
    if 'claude' in model:
        # Claude, check for stop_reason in response
        if response.stop_reason == "tool_use":
            tool_use_block = next(block for block in response.content if block.type == "tool_use")
            return {
                'tool_id': tool_use_block.id,
                'tool_name': tool_use_block.name,
                'tool_input': tool_use_block.input,
            }

    elif model.startswith('o3-'):
        # OpenAI, check for tool_calls in response
        for tool_call in response.output:
            if tool_call.type == "function_call":
                break

        if tool_call:
            return {
                'tool_id': tool_call.call_id,
                'tool_name': tool_call.name,
                'tool_input': json.loads(tool_call.arguments),
            }

    else:
        # Any other LLM, response is str, check for <tool_use> tag in response
        pattern = r'<tool_use>(.*?)</tool_use>'
        match = re.search(pattern, response, re.DOTALL)
        if match:
            tool_use_str = match.group(1).strip()
            try:
                tool_use_dict = ast.literal_eval(tool_use_str)
                if isinstance(tool_use_dict, dict) and 'tool_name' in tool_use_dict and 'tool_input' in tool_use_dict:
                    return tool_use_dict
            except Exception:
                pass

    # No tool use found
    return None

def convert_tool_info(tool_info, model=None):
    """
    Converts tool_info from Claude format to the given model's format.
    """
    if 'claude' in model:
        # should have no change
        return {
            'name': tool_info['name'],
            'description': tool_info['description'],
            'input_schema': tool_info['input_schema'],
        }
    elif model.startswith('o3-'):
        def add_additional_properties(d):
            if isinstance(d, dict):
                if 'properties' in d:
                    d['additionalProperties'] = False
                for k, v in d.items():
                    add_additional_properties(v)
        add_additional_properties(tool_info['input_schema'])
        for p in tool_info['input_schema']['properties'].keys():
            if not p in tool_info['input_schema']['required']:
                tool_info['input_schema']['required'].append(p)
                t = copy.deepcopy(tool_info['input_schema']['properties'][p]["type"])
                if isinstance(t, str):
                    tool_info['input_schema']['properties'][p]["type"] = [t, "null"]
                elif isinstance(t, list):
                    tool_info['input_schema']['properties'][p]["type"] = t + ["null"]
                
        return {
            'type': 'function',
            'name': tool_info['name'],
            'description': tool_info['description'],
            'parameters': tool_info['input_schema'],
            "strict": True,
        }
    else:
        return tool_info

def convert_block_claude(block):
    """
    Convert a single block of content from Claude into a standard format.
    """
    if isinstance(block, dict):
        block_type = block.get('type')
        text = block.get('text')
        tool_name = block.get('name')
        tool_input = block.get('input')
        tool_result = block.get('content')
    else:
        block_type = getattr(block, 'type', None)
        text = getattr(block, 'text', None)
        tool_name = getattr(block, 'name', None)
        tool_input = getattr(block, 'input', None)
        tool_result = getattr(block, 'content', None)

    text = text or ""

    if block_type == "text":
        return {
            "type": "text",
            "text": text
        }
    elif block_type == "tool_use":
        # Convert to the manual tool calling format
        return {
            "type": "text",
            "text": f"<tool_use>\n{{'tool_name': {tool_name}, 'tool_input': {tool_input}}}\n</tool_use>"
        }
    elif block_type == "tool_result":
        return {
            "type": "text",
            "text": f"Tool Result: {tool_result}"
        }
    else:
        # Fallback if we ever encounter an unknown block type
        return {
            "type": "text",
            "text": str(block)
        }

def convert_msg_history_claude(msg_history):
    """
    Convert Claude-style message history into a generic format.
    """
    new_msg_history = []

    for msg in msg_history:
        role = msg.get('role', '')
        content_blocks = msg.get('content', [])
        new_content = []

        for block in content_blocks:
            new_content.append(convert_block_claude(block))

        new_msg_history.append({
            "role": role,
            "content": new_content
        })

    return new_msg_history

def convert_msg_history_openai(msg_history):
    """
    Convert OpenAI-style message history into a generic format.
    """
    new_msg_history = []

    for msg in msg_history:
        if isinstance(msg, dict):
            role = msg.get('role', '')
            content = msg.get('content', '')

            if role == 'tool':
                new_msg = {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Tool Result: {content}",
                        }
                    ],
                }
            else:
                new_msg = {
                    "role": role,
                    "content": content,
                }
        else:
            role = getattr(msg, 'role', None)
            content = getattr(msg, 'content', None)
            tool_calls = getattr(msg, 'tool_calls', None)

            if tool_calls:
                tool_call = tool_calls[0]
                function_name = getattr(tool_call.function, 'name', '')
                function_args = getattr(tool_call.function, 'arguments', '')
                # Convert to the manual tool calling format
                new_msg = {
                    "role": role,
                    "content": [
                        {
                            "type": "text",
                            "text": f"<tool_use>\n{{'tool_name': {function_name}, 'tool_input': {function_args}}}\n</tool_use>",
                        }
                    ],
                }
            else:
                new_msg = {
                    "role": role,
                    "content": [
                        {
                            "type": "text",
                            "text": content,
                        }
                    ],
                }

        new_msg_history.append(new_msg)

    return new_msg_history

def convert_msg_history(msg_history, model=None):
    """
    Convert message history from the model-specific format to a generic format.
    """
    if 'claude' in model:
        return convert_msg_history_claude(msg_history)
    elif model.startswith('o3-'):
        return convert_msg_history_openai(msg_history)
    else:
        return msg_history

def chat_with_agent_manualtools(msg, model, msg_history=None, logging=print):
    # Construct message
    if msg_history is None:
        msg_history = []
    system_message = f'You are a coding agent.\n\n{get_tooluse_prompt()}'
    new_msg_history = msg_history

    try:
        # Load all tools
        all_tools = load_all_tools(logging=logging)
        tools_dict = {tool['info']['name']: tool for tool in all_tools}
        
        # Create client
        client, client_model = create_client(model)

        # Call API
        logging(f"Input: {msg}")
        response, new_msg_history = get_response_from_llm(
            msg=msg,
            client=client,
            model=client_model,
            system_message=system_message,
            print_debug=False,
            msg_history=new_msg_history,
        )
        logging(f"Output: {response}")
        if not _response_has_text_or_tool(response, model=client_model):
            logging(f"EMPTY RESPONSE from {client_model} (manual tools, first turn): {response!r}")

        # Tool use
        tool_use = check_for_tool_use(response, model=client_model)
        while tool_use:
            # Process tool call
            tool_name = tool_use['tool_name']
            tool_input = tool_use['tool_input']
            tool_result = process_tool_call(tools_dict, tool_name, tool_input)

            # Get tool response
            tool_msg = f'Tool Used: {tool_name}\nTool Input: {tool_input}\nTool Result: {tool_result}'
            logging(tool_msg)
            response, new_msg_history = get_response_from_llm(
                msg=tool_msg,
                client=client,
                model=client_model,
                system_message=system_message,
                print_debug=False,
                msg_history=new_msg_history,
            )
            logging(f"Output: {response}")
            if not _response_has_text_or_tool(response, model=client_model):
                logging(f"EMPTY RESPONSE from {client_model} (manual tools, tool turn): {response!r}")

            # Check for next tool use
            tool_use = check_for_tool_use(response, model=client_model)

    except Exception as e:
        logging(f"Error in chat_with_agent_manualtools: {type(e).__name__}: {e}\n{traceback.format_exc()}")

    return new_msg_history

def chat_with_agent_claude(
        msg,
        model='bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0',
        msg_history=None,
        logging=print,
        max_tokens=DEFAULT_MAX_TOKENS,
        thinking=None,
    ):
    # Construct message
    if msg_history is None:
        msg_history = []
    new_msg_history = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": msg,
                }
            ],
        }
    ]

    try:
        # Create client
        client, client_model = create_client(model)

        # Load all tools
        all_tools = load_all_tools(logging=logging)
        tools_dict = {tool['info']['name']: tool for tool in all_tools}
        tools = [convert_tool_info(tool['info'], model=client_model) for tool in all_tools]

        # Call API
        response = _call_claude_with_escalation(
            client, client_model, msg_history + new_msg_history, tools, {"type": "auto"}, logging,
            label='claude first turn', max_tokens=max_tokens, thinking=thinking,
        )
        log_response_diagnostics(response, model=client_model, logging=logging, label='claude first turn')

        # Check for tool use
        tool_use = check_for_tool_use(response, model=client_model)
        while tool_use:
            # Process tool call
            tool_name = tool_use['tool_name']
            tool_input = tool_use['tool_input']
            tool_result = process_tool_call(tools_dict, tool_name, tool_input)

            # Get tool response
            new_msg_history.append({"role": "assistant", "content": response.content})
            new_msg_history.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use['tool_id'],
                        "content": tool_result,
                    }
                ],
            })
            response = _call_claude_with_escalation(
                client, client_model, msg_history + new_msg_history, tools, {"type": "auto"}, logging,
                label='claude tool turn', max_tokens=max_tokens, thinking=thinking,
            )
            log_response_diagnostics(response, model=client_model, logging=logging, label='claude tool turn')

            # Check for next tool use
            tool_use = check_for_tool_use(response, model=client_model)

        # Get final response
        final_response = next((block.text for block in response.content if hasattr(block, "text")), None)
        new_msg_history.append({
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": final_response or "",
                }
            ],
        })

    except Exception as e:
        logging(f"Error in chat_with_agent_claude: {type(e).__name__}: {e}\n{traceback.format_exc()}")

    return new_msg_history

def get_plain_code_response_claude(prompt, model=CLAUDE_MODEL, logging=print,
                                   max_tokens=16384, thinking=None):
    """No-tools single-turn Claude request. Returns the concatenated text ('' on failure).
    Escalates max_tokens (doubling, capped) and disables thinking if the reply is empty at max_tokens."""
    client, client_model = create_client(model)
    cur_tokens, cur_thinking = max_tokens, thinking
    for step in range(3):
        kwargs = dict(model=client_model, messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
                      max_tokens=cur_tokens)
        cfg = _normalize_thinking(cur_thinking, cur_tokens)
        if cfg is not None:
            kwargs['thinking'] = cfg
        try:
            response = client.messages.create(**kwargs)
        except Exception as e:
            logging(f"[plain] request failed: {type(e).__name__}: {e}")
            return ''
        text = "\n".join(getattr(b, 'text', '') or '' for b in (response.content or []) if _block_type(b) == 'text')
        if text.strip():
            return text
        if getattr(response, 'stop_reason', None) != 'max_tokens' or step == 2:
            logging(f"[plain] empty reply, stop_reason={getattr(response, 'stop_reason', None)}")
            return ''
        cur_tokens = min(cur_tokens * 2, MAX_TOKENS_CAP)
        cur_thinking = {'type': 'disabled'}
        logging(f"[escalate] plain code request: empty reply at max_tokens; retrying with "
                f"max_tokens={cur_tokens}, thinking disabled")
    return ''

def chat_with_agent_openai(
        msg,
        model='o3-mini-2025-01-31',
        msg_history=None,
        logging=print,
    ):
    # Construct message
    if msg_history is None:
        msg_history = []
    new_msg_history = [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": msg,
                }
            ],
        }
    ]
    separator = '=' * 10
    logging(f"\n{separator} User Instruction {separator}\n{msg}")
    try:
        # Create client
        client, client_model = create_client(model)

        # Load all tools
        all_tools = load_all_tools(logging=logging)
        tools_dict = {tool['info']['name']: tool for tool in all_tools}
        tools = [convert_tool_info(tool['info'], model=client_model) for tool in all_tools]

        # Call API
        response = get_response_withtools(
            client=client,
            model=client_model,
            messages=msg_history + new_msg_history,
            tool_choice="auto",
            tools=tools,
            logging=logging,
        )
        logging(f"\n{separator} Agent Response {separator}\n{response}")
        log_response_diagnostics(response, model=client_model, logging=logging, label='openai first turn')

        # Check for tool use
        tool_use = check_for_tool_use(response, model=client_model)
        logging(tool_use)
        while tool_use:
            # Process tool call
            tool_name = tool_use['tool_name']
            tool_input = tool_use['tool_input']
            tool_result = process_tool_call(tools_dict, tool_name, tool_input)

            logging(f"Tool Used: {tool_name}")
            logging(f"Tool Input: {tool_input}")
            logging(f"Tool Result: {tool_result}")

            # Get tool response
            for tool_call in response.output:
                if tool_call.type == "function_call":
                    break
            new_msg_history.append(tool_call)
            new_msg_history.append({
                "type": "function_call_output",
                "call_id": tool_use['tool_id'],
                "output": tool_result,
            })
            response = get_response_withtools(
                client=client,
                model=client_model,
                messages=msg_history + new_msg_history,
                tool_choice="auto",
                tools=tools,
                logging=logging,
            )

            # Check for next tool use
            tool_use = check_for_tool_use(response, model=client_model)

            logging(f"Tool Response: {response}")
            log_response_diagnostics(response, model=client_model, logging=logging, label='openai tool turn')

        # Get final response
        new_msg_history.append(response)

    except Exception as e:
        logging(f"Error in chat_with_agent_openai: {type(e).__name__}: {e}\n{traceback.format_exc()}")

    return new_msg_history

def chat_with_agent(
    msg,
    model=CLAUDE_MODEL,
    msg_history=None,
    logging=print,
    convert=False,  # Convert the message history to a generic format, so that msg_history can be used across models
    raise_on_empty=False,  # If True, raise EmptyResponseError when the final assistant reply is empty or the call failed
    max_tokens=DEFAULT_MAX_TOKENS,  # Claude output budget per request (escalated on empty max_tokens replies)
    thinking=None,  # Claude thinking config, e.g. {'type': 'disabled'} or {'type': 'enabled', 'budget_tokens': 4000}
):
    if msg_history is None:
        msg_history = []

    if 'claude' in model:
        # Claude models
        new_msg_history = chat_with_agent_claude(msg, model=model, msg_history=msg_history, logging=logging,
                                                 max_tokens=max_tokens, thinking=thinking)
        conv_msg_history = convert_msg_history(new_msg_history, model=model)
        logging(conv_msg_history)
        if convert:
            new_msg_history = conv_msg_history
        new_msg_history = msg_history + new_msg_history

    elif model.startswith('o3-'):
        # OpenAI models
        new_msg_history = chat_with_agent_openai(msg, model=model, msg_history=msg_history, logging=logging)
        # Current version does not support cross-model conversion
        # new_msg_history = convert_msg_history(new_msg_history, model=model)
        new_msg_history = msg_history + new_msg_history

    else:
        # Models without in-built tool calling
        new_msg_history = chat_with_agent_manualtools(msg, model=model, msg_history=msg_history, logging=logging)
        conv_msg_history = convert_msg_history(new_msg_history, model=model)
        if convert:
            new_msg_history = conv_msg_history

    if raise_on_empty and not _history_has_nonempty_reply(new_msg_history):
        raise EmptyResponseError(f"Empty or missing assistant reply from model {model}", msg_history=new_msg_history)

    return new_msg_history


if __name__ == "__main__":
    # Test the tool calling functionality
    msg = "hello!"
    chat_with_agent(msg)
