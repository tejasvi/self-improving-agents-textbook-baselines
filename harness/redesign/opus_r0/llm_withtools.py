import ast
import json
import re
import traceback
import anthropic
import backoff
import openai
import copy

from llm import create_client, get_response_from_llm
from prompts.tooluse_prompt import get_tooluse_prompt
from tools import load_all_tools

CLAUDE_MODEL = 'claude-3-5-sonnet-20241022'
OPENAI_MODEL = 'claude-3-5-sonnet-20241022'

MAX_OUTPUT_TOKENS_TOOLS = 8192
MAX_TOOL_ITERATIONS = 90
KEEP_FULL_TOOL_RESULTS = 8
OLD_TOOL_RESULT_CHARS = 1500


def process_tool_call(tools_dict, tool_name, tool_input):
    try:
        if tool_name in tools_dict:
            if not isinstance(tool_input, dict):
                return f"Error: tool input for '{tool_name}' must be an object"
            result = tools_dict[tool_name]['function'](**tool_input)
            return str(result) if result is not None else ""
        else:
            return f"Error: Tool '{tool_name}' not found"
    except Exception as e:
        return f"Error executing tool '{tool_name}': {str(e)}"


def _is_fatal_error(e):
    return isinstance(e, (anthropic.BadRequestError, openai.BadRequestError))


@backoff.on_exception(
    backoff.expo,
    (openai.RateLimitError, openai.APITimeoutError, anthropic.RateLimitError, anthropic.APIStatusError),
    max_time=600,
    max_value=60,
    giveup=_is_fatal_error,
)
def get_response_withtools(
    client, model, messages, tools, tool_choice,
    logging=None, max_retry=3
):
    try:
        if 'claude' in model:
            response = client.messages.create(
                model=model,
                messages=messages,
                max_tokens=MAX_OUTPUT_TOKENS_TOOLS,
                tool_choice=tool_choice,
                tools=tools,
            )
        elif model.startswith('o3-'):
            response = client.responses.create(
                model=model,
                input=messages,
                tool_choice=tool_choice,
                tools=tools,
                parallel_tool_calls=False
            )
        else:
            raise ValueError(f"Unsupported model: {model}")
        return response
    except Exception as e:
        if logging:
            logging(f"Error in get_response_withtools: {str(e)}")
        if max_retry > 0 and not _is_fatal_error(e):
            return get_response_withtools(client, model, messages, tools, tool_choice, logging, max_retry - 1)
        raise


def check_for_tool_use(response, model=''):
    """
    Checks if the response contains a tool call.
    """
    if 'claude' in model:
        if response.stop_reason == "tool_use":
            tool_use_block = next((block for block in response.content if block.type == "tool_use"), None)
            if tool_use_block is not None:
                return {
                    'tool_id': tool_use_block.id,
                    'tool_name': tool_use_block.name,
                    'tool_input': tool_use_block.input,
                }

    elif model.startswith('o3-'):
        tool_call = None
        for item in response.output:
            if item.type == "function_call":
                tool_call = item
                break

        if tool_call:
            return {
                'tool_id': tool_call.call_id,
                'tool_name': tool_call.name,
                'tool_input': json.loads(tool_call.arguments),
            }

    else:
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

    return None


def convert_tool_info(tool_info, model=None):
    """
    Converts tool_info from Claude format to the given model's format.
    """
    if 'claude' in model:
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

        if isinstance(content_blocks, str):
            new_content.append({"type": "text", "text": content_blocks})
        else:
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
    if msg_history is None:
        msg_history = []
    system_message = f'You are a coding agent.\n\n{get_tooluse_prompt()}'
    new_msg_history = msg_history

    try:
        all_tools = load_all_tools(logging=logging)
        tools_dict = {tool['info']['name']: tool for tool in all_tools}

        client, client_model = create_client(model)

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

        tool_use = check_for_tool_use(response, model=client_model)
        for _ in range(MAX_TOOL_ITERATIONS):
            if not tool_use:
                break
            tool_name = tool_use['tool_name']
            tool_input = tool_use['tool_input']
            tool_result = process_tool_call(tools_dict, tool_name, tool_input)

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
            tool_use = check_for_tool_use(response, model=client_model)

    except Exception:
        logging(f"Error in chat_with_agent_manualtools:\n{traceback.format_exc()}")

    return new_msg_history


def _claude_block_to_dict(block):
    """Convert an anthropic content block into a plain dict that is safe to resend."""
    btype = getattr(block, 'type', None) if not isinstance(block, dict) else block.get('type')
    if btype == 'text':
        text = getattr(block, 'text', None) if not isinstance(block, dict) else block.get('text')
        if not text or not text.strip():
            return None
        return {"type": "text", "text": text}
    if btype == 'tool_use':
        if isinstance(block, dict):
            return {"type": "tool_use", "id": block.get('id'), "name": block.get('name'), "input": block.get('input') or {}}
        return {"type": "tool_use", "id": block.id, "name": block.name, "input": block.input or {}}
    return None


def _compact_old_tool_results(tool_result_blocks):
    """Shorten older tool results to keep the context small."""
    if len(tool_result_blocks) <= KEEP_FULL_TOOL_RESULTS:
        return
    for blk in tool_result_blocks[:-KEEP_FULL_TOOL_RESULTS]:
        content = blk.get('content')
        if isinstance(content, str) and len(content) > OLD_TOOL_RESULT_CHARS:
            half = OLD_TOOL_RESULT_CHARS // 2
            blk['content'] = content[:half] + "\n...[old output truncated]...\n" + content[-half:]


def chat_with_agent_claude(
        msg,
        model='bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0',
        msg_history=None,
        logging=print,
    ):
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
    tool_result_blocks = []

    try:
        client, client_model = create_client(model)

        all_tools = load_all_tools(logging=logging)
        tools_dict = {tool['info']['name']: tool for tool in all_tools}
        tools = [convert_tool_info(tool['info'], model=client_model) for tool in all_tools]

        finished = False
        for iteration in range(MAX_TOOL_ITERATIONS):
            _compact_old_tool_results(tool_result_blocks)
            response = get_response_withtools(
                client=client,
                model=client_model,
                messages=msg_history + new_msg_history,
                tool_choice={"type": "auto"},
                tools=tools,
                logging=logging,
            )
            blocks = [b for b in (_claude_block_to_dict(x) for x in response.content) if b is not None]
            text_blocks = [b for b in blocks if b['type'] == 'text']
            tool_blocks = [b for b in blocks if b['type'] == 'tool_use']
            for tb in text_blocks:
                logging(f"Assistant: {tb['text']}")

            if response.stop_reason == "max_tokens":
                # Partial tool calls are unusable: drop them and ask the model to continue.
                logging("Response truncated at max_tokens; asking the model to continue.")
                kept = text_blocks if text_blocks else [{"type": "text", "text": "(response truncated)"}]
                new_msg_history.append({"role": "assistant", "content": kept})
                new_msg_history.append({
                    "role": "user",
                    "content": [{
                        "type": "text",
                        "text": (
                            "Your previous response was cut off because it exceeded the output length limit, "
                            "and any partial tool call in it was DISCARDED (nothing was executed or written). "
                            "Continue the task. Keep your prose short, and keep each tool call reasonably small: "
                            "write files with a single concise tool call, and use the editor's `str_replace` "
                            "command for incremental changes instead of rewriting large files."
                        ),
                    }],
                })
                continue

            if tool_blocks:
                new_msg_history.append({"role": "assistant", "content": blocks})
                results = []
                for tb in tool_blocks:
                    logging(f"Tool Used: {tb['name']}\nTool Input: {tb['input']}")
                    result = process_tool_call(tools_dict, tb['name'], tb['input'])
                    if not result or not str(result).strip():
                        result = "(no output)"
                    logging(f"Tool Result: {result[:5000]}")
                    rb = {
                        "type": "tool_result",
                        "tool_use_id": tb['id'],
                        "content": result,
                    }
                    tool_result_blocks.append(rb)
                    results.append(rb)
                new_msg_history.append({"role": "user", "content": results})
                continue

            # Final answer (no tool use)
            final_blocks = text_blocks if text_blocks else [{"type": "text", "text": "(no response)"}]
            new_msg_history.append({"role": "assistant", "content": final_blocks})
            finished = True
            break

        if not finished:
            logging("Reached maximum number of tool iterations.")
            if new_msg_history and new_msg_history[-1]['role'] == 'user':
                new_msg_history.append({
                    "role": "assistant",
                    "content": [{"type": "text", "text": "(stopped: iteration limit reached)"}],
                })

    except Exception:
        logging(f"Error in chat_with_agent_claude:\n{traceback.format_exc()}")

    return new_msg_history


def chat_with_agent_openai(
        msg,
        model='o3-mini-2025-01-31',
        msg_history=None,
        logging=print,
    ):
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
        client, client_model = create_client(model)

        all_tools = load_all_tools(logging=logging)
        tools_dict = {tool['info']['name']: tool for tool in all_tools}
        tools = [convert_tool_info(tool['info'], model=client_model) for tool in all_tools]

        response = get_response_withtools(
            client=client,
            model=client_model,
            messages=msg_history + new_msg_history,
            tool_choice="auto",
            tools=tools,
            logging=logging,
        )
        logging(f"\n{separator} Agent Response {separator}\n{response}")

        tool_use = check_for_tool_use(response, model=client_model)
        for _ in range(MAX_TOOL_ITERATIONS):
            if not tool_use:
                break
            tool_name = tool_use['tool_name']
            tool_input = tool_use['tool_input']
            tool_result = process_tool_call(tools_dict, tool_name, tool_input)

            logging(f"Tool Used: {tool_name}")
            logging(f"Tool Input: {tool_input}")
            logging(f"Tool Result: {tool_result}")

            tool_call = None
            for item in response.output:
                if item.type == "function_call":
                    tool_call = item
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
            tool_use = check_for_tool_use(response, model=client_model)
            logging(f"Tool Response: {response}")

        new_msg_history.append(response)

    except Exception:
        logging(f"Error in chat_with_agent_openai:\n{traceback.format_exc()}")

    return new_msg_history


def chat_with_agent(
    msg,
    model=CLAUDE_MODEL,
    msg_history=None,
    logging=print,
    convert=False,
):
    if msg_history is None:
        msg_history = []

    if 'claude' in model:
        new_msg_history = chat_with_agent_claude(msg, model=model, msg_history=msg_history, logging=logging)
        conv_msg_history = convert_msg_history(new_msg_history, model=model)
        logging(conv_msg_history)
        if convert:
            new_msg_history = conv_msg_history
        new_msg_history = msg_history + new_msg_history

    elif model.startswith('o3-'):
        new_msg_history = chat_with_agent_openai(msg, model=model, msg_history=msg_history, logging=logging)
        new_msg_history = msg_history + new_msg_history

    else:
        new_msg_history = chat_with_agent_manualtools(msg, model=model, msg_history=msg_history, logging=logging)
        conv_msg_history = convert_msg_history(new_msg_history, model=model)
        if convert:
            new_msg_history = conv_msg_history

    return new_msg_history


if __name__ == "__main__":
    msg = "hello!"
    chat_with_agent(msg)
