import asyncio
from hello_agents.protocols import MCPClient
from openai import OpenAI
import json

client = OpenAI(
    base_url="https://api.chatanywhere.tech/v1"
)


# 连接到 MCP 服务器
async def main():
    github_client = MCPClient([
        "npx", "-y", "@modelcontextprotocol/server-github"
    ])

    async with github_client:
        # 1 获取工具
        mcp_tools = await github_client.list_tools()
        print(f"✅ GitHub MCP 服务器提供了 {len(mcp_tools)} 个工具：\n")

        for i, tool in enumerate(mcp_tools, 1):
            print(f"{i}. 工具名：{tool['name']}")
            print(f"   描述：{tool.get('description', '无描述')[:80]}...")
            print()

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


# asyncio.run(main())


# 发现可用工具
async def discover_tools():
    client = MCPClient(["npx", "-y", "@modelcontextprotocol/server-filesystem", "."])

    async with client:
        # 获取所有可用工具
        tools = await client.list_tools()

        print(f"服务器提供了 {len(tools)} 个工具：")
        for tool in tools:
            print(f"\n工具名称: {tool['name']}")
            print(f"描述: {tool.get('description', '无描述')}")

            # 打印参数信息
            if 'inputSchema' in tool:
                schema = tool['inputSchema']
                if 'properties' in schema:
                    print("参数:")
                    for param_name, param_info in schema['properties'].items():
                        param_type = param_info.get('type', 'any')
                        param_desc = param_info.get('description', '')
                        print(f"  - {param_name} ({param_type}): {param_desc}")


asyncio.run(discover_tools())
