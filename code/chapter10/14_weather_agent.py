"""在 Agent 中使用天气 MCP 服务器"""

import os
from dotenv import load_dotenv
from hello_agents import SimpleAgent, HelloAgentsLLM
from hello_agents.tools import MCPTool

load_dotenv()


def create_weather_assistant():
    """创建天气助手"""
    llm = HelloAgentsLLM(base_url="https://api.chatanywhere.tech/v1")

    assistant = SimpleAgent(
        name="天气助手",
        llm=llm,
        system_prompt="""你是天气助手，可以查询城市天气。
使用 get_weather 工具查询天气，支持中文城市名。
"""
    )

    # 为什么能找到 weather_tool 中的 get_weather？
    # 因为 MCPTool 在初始化时会自动：
    # 1.连接 MCP 服务器（weather_server）
    # 2.列出所有可用工具（通过 list_tools()）
    # 3.保存工具列表（self._available_tools）
    # 4.展开为独立工具（get_expanded_tools()）
    # 5.注册到 Agent（add_tool() 时自动完成）
    # 6.最终，get_weather 作为一个独立的工具被注册到 assistant 的工具注册表中，LLM 就能识别并调用它了。
    # ✅ 连接成功！
    # ✅ 工具 'mcp_get_weather' 已注册。
    # ✅ 工具 'mcp_list_supported_cities' 已注册。
    # ✅ 工具 'mcp_get_server_info' 已注册。
    # ✅ MCP工具 'mcp' 已展开为 3 个独立工具

    # 获取天气服务器脚本的路径
    server_script = os.path.join(os.path.dirname(__file__), "14_weather_mcp_server.py")
    # 创建 MCP 工具，启动天气服务器进程
    weather_tool = MCPTool(server_command=["python", server_script])
    # 将天气工具添加到助手智能体中
    assistant.add_tool(weather_tool)

    return assistant


def demo():
    """演示"""
    assistant = create_weather_assistant()

    print("\n查询北京天气：")
    response = assistant.run("北京今天天气怎么样？")
    print(f"回答: {response}\n")


def interactive():
    """交互模式"""
    assistant = create_weather_assistant()

    while True:
        user_input = input("\n你: ").strip()
        if user_input.lower() in ['quit', 'exit']:
            break
        response = assistant.run(user_input)
        print(f"助手: {response}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        interactive()
