import asyncio
from hello_agents.protocols import MCPClient
from openai import OpenAI
import json

client = OpenAI()


async def main():
    github_client = MCPClient([
        "npx", "-y", "@modelcontextprotocol/server-github"
    ])

    async with github_client:
        # 1 获取工具
        mcp_tools = await github_client.list_tools()

        # 转 OpenAI tools 格式
        tools = [{
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t.get("description", ""),
                "parameters": t.get("input_schema", {})
            }
        } for t in mcp_tools]

        # 2 用户输入
        messages = [
            {"role": "user", "content": "帮我找 AI agents 的 GitHub 项目"}
        ]

        # 3 第一次 LLM 调用
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        msg = resp.choices[0].message

        # 4 工具调用
        if msg.tool_calls:
            for call in msg.tool_calls:
                tool_name = call.function.name
                args = json.loads(call.function.arguments)

                result = await github_client.call_tool(tool_name, args)

                messages.append(msg)
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result)
                })

        # 5 第二次 LLM
        final = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        print(final.choices[0].message.content)


asyncio.run(main())
