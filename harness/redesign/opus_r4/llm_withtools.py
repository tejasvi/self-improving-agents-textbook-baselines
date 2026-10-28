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

CLAUDE_MAX_TOKENS = 8192
MAX_TOOL_RESULT_CHARS = 12000
MAX_AGENT_TURNS = 90


def truncate_middle(text, max_chars=MAX_TOOL_RESULT_CHARS):
    if text is None:
        return ""
    text = str(text)
    if len(text) <= max_chars:
        return text
    half = max_chars // 2
    return text[:half] + f"\n... [output truncated: {len(text) - max_chars} characters omitted] ...\n" + text[-half:]


def process_tool_call(tools_dict, tool_name, tool_input):
    try:
        if tool_name in tools_dict:
            return tools_dict[tool_name]['function'](**tool_input)
        else:
            return f"Error: Tool '{tool_name}' not found"
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
    logging=None, max_retry=3
):
    try:
        if 'claude' in model:
            response = client.messages.create(
                model=model,
                messages=messages,
                max_tokens=CLAUDE_MAX_TOKENS,
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
        if 'too long' in str(e).lower() or 'prompt is too long' in str(e).lower():
            raise
        if max_retry > 0:
            return get_response_withtools(client, model, messages, tools, tool_choice, logging, max_retry - 1)
        raise

def check_for_tool_use(response, model=''):
    """
    Checks if the response contains a tool call.
    """
    if 'claude' in model:
        if response.stop_reason == "tool_use":
            tool_use_block = next(block for block in response.content if block.type == "tool_use")
            return {
                'tool_id': tool_use_block.id,
                'tool_name': tool_use_block.name,
                'tool_input': tool_use_block.input,
            }

    elif model.startswith('o3-'):
        tool_call = None
        for tc in response.output:
            if tc.type == "function_call":
                tool_call = tc
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
        for _ in range(MAX_AGENT_TURNS):
            if not tool_use:
                break
            tool_name = tool_use['tool_name']
            tool_input = tool_use['tool_input']
            tool_result = truncate_middle(process_tool_call(tools_dict, tool_name, tool_input))

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

    except Exception as e:
        logging(f"Error in chat_with_agent_manualtools: {e}")

    return new_msg_history


def _block_to_dict(block):
    btype = getattr(block, 'type', None)
    if btype == 'text':
        return {"type": "text", "text": block.text}
    if btype == 'tool_use':
        return {"type": "tool_use", "id": block.id, "name": block.name, "input": block.input}
    return None


TRUNCATION_NOTICE = (
    "Your previous response was cut off because it exceeded the maximum output length, "
    "so any tool call in it was NOT executed. Continue the task. Keep reasoning concise. "
    "If you were writing a large file, write it in smaller steps (e.g. create the file with the first part, "
    "then append further parts using bash with a heredoc: cat >> file << 'EOF' ... EOF), "
    "or write a more compact version."
)


def chat_with_agent_claude(
        msg,
        model='bedrock/us.anthropic.claude-3-5-sonnet-20241022-v2:0',
        msg_history=None,
        logging=print,
        max_turns=MAX_AGENT_TURNS,
    ):
    if msg_history is None:
        msg_history = []
    new_msg_history = [
        {
            "role": "user",
            "content": [{"type": "text", "text": msg}],
        }
    ]

    try:
        client, client_model = create_client(model)

        all_tools = load_all_tools(logging=logging)
        tools_dict = {tool['info']['name']: tool for tool in all_tools}
        tools = [convert_tool_info(tool['info'], model=client_model) for tool in all_tools]

        finished = False
        for turn in range(max_turns):
            response = get_response_withtools(
                client=client,
                model=client_model,
                messages=msg_history + new_msg_history,
                tool_choice={"type": "auto"},
                tools=tools,
                logging=logging,
            )
            blocks = response.content or []
            stop_reason = response.stop_reason

            text_blocks = [{"type": "text", "text": b.text} for b in blocks
                           if getattr(b, 'type', None) == 'text' and b.text and b.text.strip()]
            for tb in text_blocks:
                logging(f"[turn {turn}] Assistant: {tb['text']}")
            tool_uses = [b for b in blocks if getattr(b, 'type', None) == 'tool_use']

            if stop_reason == 'max_tokens':
                logging(f"[turn {turn}] Response truncated (max_tokens).")
                kept = text_blocks if text_blocks else [{"type": "text", "text": "(response truncated)"}]
                new_msg_history.append({"role": "assistant", "content": kept})
                new_msg_history.append({
                    "role": "user",
                    "content": [{"type": "text", "text": TRUNCATION_NOTICE}],
                })
                continue

            if tool_uses:
                assistant_content = [d for d in (_block_to_dict(b) for b in blocks) if d is not None]
                assistant_content = [d for d in assistant_content
                                     if not (d["type"] == "text" and not d["text"].strip())]
                new_msg_history.append({"role": "assistant", "content": assistant_content})
                results = []
                for tu in tool_uses:
                    tool_input = tu.input if isinstance(tu.input, dict) else {}
                    logging(f"[turn {turn}] Tool call: {tu.name} {tool_input}")
                    result = process_tool_call(tools_dict, tu.name, tool_input)
                    result = truncate_middle(result)
                    if not result.strip():
                        result = "(no output)"
                    logging(f"[turn {turn}] Tool result: {result}")
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": tu.id,
                        "content": result,
                    })
                new_msg_history.append({"role": "user", "content": results})
                continue

            # Final response (no tool use)
            final_response = "\n".join(tb["text"] for tb in text_blocks)
            new_msg_history.append({
                "role": "assistant",
                "content": [{"type": "text", "text": final_response}],
            })
            finished = True
            break

        if not finished:
            logging("Agent reached the maximum number of turns.")

    except Exception as e:
        logging(f"Error in chat_with_agent_claude: {e}")

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
        for _ in range(MAX_AGENT_TURNS):
            if not tool_use:
                break
            tool_name = tool_use['tool_name']
            tool_input = tool_use['tool_input']
            tool_result = truncate_middle(process_tool_call(tools_dict, tool_name, tool_input))

            logging(f"Tool Used: {tool_name}")
            logging(f"Tool Input: {tool_input}")
            logging(f"Tool Result: {tool_result}")

            tool_call = None
            for tc in response.output:
                if tc.type == "function_call":
                    tool_call = tc
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

    except Exception as e:
        logging(f"Error in chat_with_agent_openai: {e}")

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
