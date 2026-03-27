from hello_agents import SimpleAgent, HelloAgentsLLM
from hello_agents.tools.builtin.protocol_tools import MCPTool

import os
# os.environ['WEATHER_API_KEY'] = '8a2c90191e1af94411b704f4f7b32009'

agent = SimpleAgent(name="天气助手", llm=HelloAgentsLLM(base_url="https://api.chatanywhere.tech/v1"))

# 使用 npx 运行 Open-Meteo 免费天气 MCP服务器（无需 API key）
print("------- 启动免费天气 MCP服务器 -------")
print("使用 Open-Meteo API（免费，无需 API key）\n")

weather_tool = MCPTool(
    server_command=["npx", "-y", "@gbrigandi/mcp-server-openmeteo"],
    name="weather",
    auto_expand=True
)

# 打印可用工具信息
expanded_tools = weather_tool.get_expanded_tools()
print(f"展开的工具数量：{len(expanded_tools)}")
for tool in expanded_tools:
    print(f"工具名：{tool.name}")
print("-------\n")

agent.add_tool(weather_tool)

# 测试天气查询
response = agent.run("北京今天天气怎么样？")
print(response)
