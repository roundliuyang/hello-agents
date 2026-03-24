from openai import OpenAI
import json
import requests

# 步骤1：为每个LLM提供商定义函数
# OpenAI格式
openai_tools = [
    {
        "type": "function",
        "function": {
            "name": "search_github",
            "description": "搜索GitHub仓库",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"}
                },
                "required": ["query"]
            }
        }
    }
]

# Claude格式
claude_tools = [
    {
        "name": "search_github",
        "description": "搜索GitHub仓库",
        "input_schema": {  # 注意：不是parameters
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "搜索关键词"}
            },
            "required": ["query"]
        }
    }
]


def search_github(query):
    return requests.get(
        "https://api.github.com/search/repositories",
        params={"q": query}
    ).json()


client = OpenAI(
    base_url="https://api.chatanywhere.tech/v1"
)

# 第一次请求
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "找 Kafka 项目"}],
    tools=openai_tools,
    tool_choice="auto"
)

msg = resp.choices[0].message

# 调用工具
if msg.tool_calls:
    tool_call = msg.tool_calls[0]
    args = json.loads(tool_call.function.arguments)

    result = search_github(**args)

    # 第二次请求（带工具结果）
    final = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "找 Kafka 项目"},
            msg,
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            }
        ]
    )

    print(final.choices[0].message.content)
