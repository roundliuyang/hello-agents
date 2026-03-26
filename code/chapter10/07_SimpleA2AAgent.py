from hello_agents.protocols.a2a.implementation import A2AServer, A2A_AVAILABLE


def create_calculator_agent():
    """创建一个计算器智能体"""
    if not A2A_AVAILABLE:
        print("❌ A2A SDK 未安装，请运行: pip install a2a-sdk")
        return None

    print("🧮 创建计算器智能体")

    # 创建 A2A 服务器
    calculator = A2AServer(
        name="calculator-agent",  # 智能体的唯一标识名称
        description="专业的数学计算智能体",  # 智能体的功能描述
        version="1.0.0",
        capabilities={  # 能力声明，告诉其他智能体它能做什么
            "math": ["addition", "subtraction", "multiplication", "division"],
            "advanced": ["power", "sqrt", "factorial"]
        }
    )

    # 工作原理：
    # 1.@calculator.skill("add") 是装饰器语法
    # 2.它把下面的 add_numbers 函数注册为智能体的一个技能
    # 3.技能的名称是 "add"
    # 4.注册后，可以通过 calculator.skills["add"] 来调用这个函数
    # 作用：
    # - 声明式注册：告诉 A2AServer，这个函数是智能体的一个技能
    # - 技能映射：将函数 add_numbers 映射到技能名 "add"
    # - 能力暴露：其他智能体可以通过 A2A 协议发现和调用这个技能
    # 注册后，智能体的 skills 字典中会包含：
    # calculator.skills = {
    #     "add": <add_numbers 函数>,
    #     "multiply": <multiply_numbers 函数>,
    #     "info": <get_info 函数>
    # }
    # 可以通过技能名调用 result = calculator.skills["add"]("计算 5 + 3")
    @calculator.skill("add")
    def add_numbers(query: str) -> str:
        """加法计算"""
        try:
            # 简单解析 "计算 5 + 3" 格式
            parts = query.replace("计算", "").replace("加", "+").replace("加上", "+")
            if "+" in parts:
                numbers = [float(x.strip()) for x in parts.split("+")]
                result = sum(numbers)
                return f"计算结果: {' + '.join(map(str, numbers))} = {result}"
            else:
                return "请使用格式: 计算 5 + 3"
        except Exception as e:
            return f"计算错误: {e}"

    @calculator.skill("multiply")
    def multiply_numbers(query: str) -> str:
        """乘法计算"""
        try:
            parts = query.replace("计算", "").replace("乘以", "*").replace("×", "*")
            if "*" in parts:
                numbers = [float(x.strip()) for x in parts.split("*")]
                result = 1
                for num in numbers:
                    result *= num
                return f"计算结果: {' × '.join(map(str, numbers))} = {result}"
            else:
                return "请使用格式: 计算 5 * 3"
        except Exception as e:
            return f"计算错误: {e}"

    @calculator.skill("info")
    def get_info(query: str) -> str:
        """获取智能体信息"""
        return f"我是 {calculator.name}，可以进行基础数学计算。支持的技能: {list(calculator.skills.keys())}"

    print(f"✅ 计算器智能体创建成功，支持技能: {list(calculator.skills.keys())}")
    return calculator


# 创建智能体
calc_agent = create_calculator_agent()
if calc_agent:
    # 测试技能
    print("\n🧪 测试智能体技能:")
    test_queries = [
        "获取信息",
        "计算 10 + 5",
        "计算 6 * 7"
    ]

    for query in test_queries:
        if "信息" in query:
            result = calc_agent.skills["info"](query)
        elif "+" in query:
            result = calc_agent.skills["add"](query)
        elif "*" in query or "×" in query:
            result = calc_agent.skills["multiply"](query)
        else:
            result = "未知查询类型"

        print(f"  📝 查询: {query}")
        print(f"  🤖 回复: {result}")
        print()
