import ast
import json
import re
import anthropic
import backoff
import openai
import copy

from llm import create_client, get_response_from_llm
from prompts.tooluse_prompt import get_tooluse_prompt
from tools import load_all_tools

CLAUDE_MODEL = 'claude-3-5-sonnet-20241022'
OPENAI_MODEL = 'claude-3-5-sonnet-20241022'

# Output-token ladder for empty turns caused by max_tokens exhaustion (thinking consumed the budget).
# Capped at what the API allows for the model.
MAX_TOKENS_CAP = 64000
TOKEN_LADDER = [16384, 32000, 64000]

def safe_extract_text(response):
    """
    Return the text of a response (str, Claude message, or OpenAI response) without raising.
    Returns '' when there is no text.
    """
    try:
        if response is None:
            return ''
        if isinstance(response, str):
            return response
        content = getattr(response, 'content', None)
        if isinstance(content, list):
            parts = [getattr(b, 'text', None) or (b.get('text') if isinstance(b, dict) else None) for b in content]
            return '\n'.join(p for p in parts if p)
        output_text = getattr(response, 'output_text', None)
        if isinstance(output_text, str):
            return output_text
        return ''
    except Exception:
        return ''

def describe_response(response):
    """
    One-line diagnostic for a response: stop_reason, block types and usage. Never raises.
    """
    try:
        stop_reason = getattr(response, 'stop_reason', None)
        content = getattr(response, 'content', None)
        if isinstance(content, list):
            block_types = [str(getattr(b, 'type', None) or (b.get('type') if isinstance(b, dict) else type(b).__name__)) for b in content]
        elif content is None:
            block_types = None
        else:
            block_types = type(content).__name__
        usage = getattr(response, 'usage', None)
        return f"stop_reason={stop_reason} block_types={block_types} usage={usage}"
    except Exception as e:
        return f"describe_response failed: {e!r}"

def process_tool_call(tools_dict, tool_name, tool_input):
    try:
        if tool_name in tools_dict:
            return tools_dict[tool_name]['function'](**tool_input)
        else:
            return f"Error: Tool '{tool_name}' not found"
    except TypeError as e:
        # Bad arguments (unknown or missing parameters): show the schema so the model can retry correctly.
        schema = None
        if tool_name in tools_dict:
            schema = tools_dict[tool_name]['info'].get('input_schema')
        return (
            f"Error: invalid arguments for tool '{tool_name}': {str(e)}. "
            f"Expected input_schema: {json.dumps(schema)}"
        )
    except Exception as e:
        return f"Error executing tool '{tool_name}': {str(e)}"

@backoff.on_exception(
    backoff.expo,
    (openai.RateLimitError, openai.APITimeoutError, anthropic.RateLimitError, anthropic.APIStatusError),
    max_time=600,
    max_value=60,
)
def get_response_withtools(
    client, model, messages, tools, tool_choice,
    logging=None, max_retry=3, temperature=None, max_tokens=None, thinking=None,
):
    try:
        if 'claude' in model:
            kwargs = {}
            if temperature is not None:
                kwargs['temperature'] = temperature
            if thinking is not None:
                kwargs['thinking'] = thinking
            response = client.messages.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens or 16384,
                tool_choice=tool_choice,
                tools=tools,
                **kwargs,
            )
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
        logging(f"Error in get_response_withtools: {str(e)}")
        if max_retry > 0:
            return get_response_withtools(client, model, messages, tools, tool_choice, logging, max_retry - 1,
                                          temperature=temperature, max_tokens=max_tokens, thinking=thinking)

        # Hitting the context window limit
        if 'Input is too long for requested model' in str(e):
            pass

        raise  # Re-raise the exception after logging

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

def chat_with_agent_manualtools(msg, model, msg_history=None, logging=print, temperature=None, max_tokens=None):
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
            **_sampling_kwargs(temperature, max_tokens),
        )
        logging(f"Output: {response}")

        # Tool use, with bounded recovery from empty turns
        for attempt in range(3):
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
                    **_sampling_kwargs(temperature, max_tokens),
                )
                logging(f"Output: {response}")

                # Check for next tool use
                tool_use = check_for_tool_use(response, model=client_model)

            if not _is_empty_response(response, model=client_model):
                break

            logging(f"Empty turn diagnostic: {describe_response(response)}")
            logging(f"Dropping empty assistant turn (attempt {attempt + 1}/3); nudging the model.")
            if attempt >= len(EMPTY_NUDGES):
                logging("Empty turn persisted after all nudges; giving up so the caller can restart.")
                # Drop the empty turn so it is not stored in the history.
                if len(new_msg_history) >= 2 and new_msg_history[-1].get('role') == 'assistant':
                    new_msg_history = new_msg_history[:-1]
                break

            # Remove the empty assistant turn and the user message before it; resend that user
            # message merged with the nudge so roles keep alternating.
            base_history = new_msg_history
            prev_text = ''
            if len(new_msg_history) >= 2 and new_msg_history[-1].get('role') == 'assistant' \
                    and new_msg_history[-2].get('role') == 'user':
                base_history = new_msg_history[:-2]
                prev = new_msg_history[-2].get('content')
                if isinstance(prev, str):
                    prev_text = prev
                elif isinstance(prev, list):
                    prev_text = '\n'.join(b.get('text', '') for b in prev if isinstance(b, dict) and b.get('text'))

            # Claude: the empty turn may have stopped at max_tokens (thinking used the whole budget).
            # Re-issue the same user turn with the next token-ladder rung before nudging. get_response_from_llm
            # does not expose stop_reason, so this is attempted for Claude models only.
            if 'claude' in client_model and prev_text:
                recovered_text = None
                last_rung = len(TOKEN_LADDER) - 1
                failed_max = max_tokens or 4096  # the limit get_response_from_llm used for this turn
                for rung, max_tok in enumerate(TOKEN_LADDER):
                    if max_tok > MAX_TOKENS_CAP or max_tok <= failed_max:
                        continue
                    logging(f"max_tokens recovery (manual): rung {rung + 1}/{len(TOKEN_LADDER)} max_tokens={max_tok}")
                    try:
                        cand_text, cand_hist = get_response_from_llm(
                            msg=prev_text,
                            client=client,
                            model=client_model,
                            system_message=system_message,
                            print_debug=False,
                            msg_history=base_history,
                            temperature=temperature if temperature is not None else 0.7,
                            max_tokens=max_tok,
                        )
                    except Exception as e:
                        logging(f"max_tokens recovery (manual) rung {rung + 1} failed: {e!r}")
                        continue
                    if isinstance(cand_text, str) and cand_text.strip():
                        logging(f"max_tokens recovery (manual) succeeded on rung {rung + 1}.")
                        recovered_text = (cand_text, cand_hist)
                        break
                    logging(f"max_tokens recovery (manual) rung {rung + 1} still empty.")
                if recovered_text is not None:
                    response, new_msg_history = recovered_text
                    logging(f"Output: {response}")
                    continue

            resend = f"{prev_text}\n\n{EMPTY_NUDGES[attempt]}" if prev_text else EMPTY_NUDGES[attempt]
            response, new_msg_history = get_response_from_llm(
                msg=resend,
                client=client,
                model=client_model,
                system_message=system_message,
                print_debug=False,
                msg_history=base_history,
                **_sampling_kwargs(temperature, max_tokens),
            )
            logging(f"Output: {response}")

    except Exception as e:
        logging(f'chat_with_agent error: {e!r}')

    return new_msg_history

def _sampling_kwargs(temperature=None, max_tokens=None):
    kwargs = {}
    if temperature is not None:
        kwargs['temperature'] = temperature
    if max_tokens is not None:
        kwargs['max_tokens'] = max_tokens
    return kwargs

EMPTY_NUDGES = [
    (
        "Continue: think briefly (under 500 words), then call a tool now to implement the solution."
    ),
    (
        "Continue: think briefly (under 500 words), then call a tool now to implement the solution. "
        "Use exactly this format:\n"
        "<tool_use>\n{'tool_name': 'editor', 'tool_input': {'command': 'create', "
        "'path': '<path of the target source file>', 'file_text': '<complete file contents>'}}\n</tool_use>"
    ),
]


def _is_max_tokens_stop(response):
    return getattr(response, 'stop_reason', None) == 'max_tokens'


def _recover_max_tokens(client, model, messages, tools, tool_choice, logging, temperature=None, failed_max=None):
    """
    For an empty response that stopped at max_tokens, re-issue the SAME messages with the next rung
    of TOKEN_LADDER above `failed_max` (the limit that produced the empty turn); the last rung also
    disables thinking. Returns the first non-empty response, or None if the ladder is exhausted.
    """
    last = len(TOKEN_LADDER) - 1
    rungs = [(i, m) for i, m in enumerate(TOKEN_LADDER)
             if m <= MAX_TOKENS_CAP and (failed_max is None or m > failed_max)]
    for rung, max_tok in rungs:
        thinking = {'type': 'disabled'} if rung == last else None
        logging(f"max_tokens recovery: rung {rung + 1}/{len(TOKEN_LADDER)} max_tokens={max_tok} "
                f"thinking={'disabled' if thinking else 'default'}")
        try:
            candidate = get_response_withtools(
                client=client, model=model, messages=messages, tool_choice=tool_choice, tools=tools,
                logging=logging, temperature=temperature, max_tokens=max_tok, thinking=thinking,
            )
        except Exception as e:
            logging(f"max_tokens recovery rung {rung + 1} failed: {e!r}")
            continue
        if not _is_empty_response(candidate, model=model):
            logging(f"max_tokens recovery succeeded on rung {rung + 1} (max_tokens={max_tok}).")
            return candidate
        logging(f"max_tokens recovery rung {rung + 1} still empty: {describe_response(candidate)}")
        if not _is_max_tokens_stop(candidate):
            break
    return None


def _is_empty_response(response, model=''):
    """
    True when the response has no non-whitespace text and no tool call.
    """
    if isinstance(response, str):
        has_text = bool(response.strip())
    elif 'claude' in model:
        has_text = any(
            getattr(block, 'type', None) == 'text' and (getattr(block, 'text', '') or '').strip()
            for block in (getattr(response, 'content', None) or [])
        )
    else:
        has_text = bool((getattr(response, 'output_text', '') or '').strip())
    has_tool = check_for_tool_use(response, model=model) is not None
    return (not has_text) and (not has_tool)


def _append_nudge(msg_history, text):
    """
    Add a nudge without stacking consecutive user messages: merge it into the last
    message if that is a user message (tool_result or text), otherwise append a new user message.
    """
    if msg_history and msg_history[-1].get("role") == "user":
        last = msg_history[-1]
        content = last.get("content")
        if isinstance(content, str):
            last["content"] = content + "\n\n" + text
        elif isinstance(content, list):
            content.append({"type": "text", "text": text})
        else:
            last["content"] = [{"type": "text", "text": text}]
    else:
        msg_history.append({"role": "user", "content": [{"type": "text", "text": text}]})
    return msg_history


def chat_with_agent_claude(
        msg,
        model='bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0',
        msg_history=None,
        logging=print,
        temperature=None,
        max_tokens=None,
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
    sampling = _sampling_kwargs(temperature, max_tokens)

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
            tool_choice={"type": "auto"},
            tools=tools,
            logging=logging,
            **sampling,
        )

        final_response = None
        gave_up = False
        # Bounded: up to 3 attempts to recover from empty responses (no text and no tool call).
        for attempt in range(3):
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
                response = get_response_withtools(
                    client=client,
                    model=client_model,
                    messages=msg_history + new_msg_history,
                    tool_choice={"type": "auto"},
                    tools=tools,
                    logging=logging,
                    **sampling,
                )

                # Check for next tool use
                tool_use = check_for_tool_use(response, model=client_model)

            # Get final response
            final_response = next((block.text for block in response.content if hasattr(block, "text")), None)
            if not _is_empty_response(response, model=client_model):
                break
            logging(f"Empty turn diagnostic: {describe_response(response)}; safe text={safe_extract_text(response)!r}")

            # Empty turn caused by max_tokens exhaustion: re-issue the SAME messages with a larger budget
            # before resorting to a textual nudge.
            if _is_max_tokens_stop(response):
                recovered = _recover_max_tokens(
                    client, client_model, msg_history + new_msg_history, tools,
                    {"type": "auto"}, logging, temperature=sampling.get('temperature'),
                    failed_max=sampling.get('max_tokens') or 16384,
                )
                if recovered is not None:
                    response = recovered
                    continue  # re-evaluate the recovered response (tool use or text)

            # Empty turn: drop it (never stored in history) and nudge with an escalating message.
            logging(f"Dropping empty assistant turn (attempt {attempt + 1}/3); nudging the model.")
            final_response = None
            if attempt >= len(EMPTY_NUDGES):
                logging("Empty turn persisted after all nudges; giving up so the caller can restart.")
                gave_up = True
                break
            _append_nudge(new_msg_history, EMPTY_NUDGES[attempt])
            response = get_response_withtools(
                client=client,
                model=client_model,
                messages=msg_history + new_msg_history,
                tool_choice={"type": "auto"},
                tools=tools,
                logging=logging,
                **sampling,
            )
        if final_response is not None and not gave_up:
            new_msg_history.append({
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": final_response,
                    }
                ],
            })

    except Exception as e:
        logging(f'chat_with_agent error: {e!r}')

    return new_msg_history

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

        # Get final response
        new_msg_history.append(response)

    except Exception:
        pass

    return new_msg_history

def chat_with_agent(
    msg,
    model=CLAUDE_MODEL,
    msg_history=None,
    logging=print,
    convert=False,  # Convert the message history to a generic format, so that msg_history can be used across models
    temperature=None,
    max_tokens=None,
):
    if msg_history is None:
        msg_history = []

    if 'claude' in model:
        # Claude models
        new_msg_history = chat_with_agent_claude(msg, model=model, msg_history=msg_history, logging=logging,
                                                 temperature=temperature, max_tokens=max_tokens)
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
        new_msg_history = chat_with_agent_manualtools(msg, model=model, msg_history=msg_history, logging=logging,
                                                      temperature=temperature, max_tokens=max_tokens)
        conv_msg_history = convert_msg_history(new_msg_history, model=model)
        if convert:
            new_msg_history = conv_msg_history

    return new_msg_history


if __name__ == "__main__":
    # Test the tool calling functionality
    msg = "hello!"
    chat_with_agent(msg)
