MY_REACT_PROMPT = """你是一个具备推理和行动能力的AI助手。你可以通过思考分析问题，然后调用合适的工具来获取信息，最终给出准确的答案。

## 可用工具
{tools}

## 工作流程
请严格按照以下格式进行回应，每次只能执行一个步骤：

Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一：
- `{{tool_name}}[{{tool_input}}]` - 调用指定工具
- `Finish[最终答案]` - 当你有足够信息给出最终答案时

## 重要提醒
1. 每次回应必须包含Thought和Action两部分
2. 工具调用的格式必须严格遵循：工具名[参数]
3. 只有当你确信有足够信息回答问题时，才使用Finish
4. 如果工具返回的信息不够，继续使用其他工具或相同工具的不同参数

## 当前任务
**Question:** {question}

## 执行历史
{history}

现在开始你的推理和行动：
"""

import re
from typing import Optional, List, Tuple
from hello_agents import ReActAgent, HelloAgentsLLM, Config, Message, ToolRegistry


class MyReActAgent(ReActAgent):
    """
    重写的ReAct Agent - 推理与行动结合的智能体
    """

    def __init__(
            self,
            name: str,
            llm: HelloAgentsLLM,
            tool_registry: ToolRegistry,
            system_prompt: Optional[str] = None,
            config: Optional[Config] = None,
            max_steps: int = 5,
            custom_prompt: Optional[str] = None
    ):
        """
        初始化 MyReActAgent

        参数:
            name: Agent 的名称
            llm: HelloAgentsLLM 的实例，负责与大语言模型通信
            tool_registry: ToolRegistry 的实例，用于管理和执行 Agent 可用的工具
            system_prompt: 系统提示词，用于设定 Agent 的角色和行为准则
            config: 配置对象，用于传递框架级的设置
            max_steps: ReAct 循环的最大执行步数，防止无限循环
            custom_prompt: 自定义的提示词模板，用于替换默认的 ReAct 提示词
        """
        super().__init__(name, llm, system_prompt, config)
        self.tool_registry = tool_registry
        self.max_steps = max_steps
        self.current_history: List[str] = []
        self.prompt_template = custom_prompt if custom_prompt else MY_REACT_PROMPT
        print(f"✅ {name} 初始化完成，最大步数: {max_steps}")

    def run(self, input_text: str, **kwargs) -> str:
        """运行ReAct Agent"""
        self.current_history = []
        current_step = 0

        print(f"\n🤖 {self.name} 开始处理问题: {input_text}")

        while current_step < self.max_steps:
            current_step += 1
            print(f"\n--- 第 {current_step} 步 ---")

            # 1. 构建提示词
            tools_desc = self.tool_registry.get_tools_description()
            history_str = "\n".join(self.current_history)
            prompt = self.prompt_template.format(
                tools=tools_desc,
                question=input_text,
                history=history_str
            )

            """
            构建发送给 LLM 的消息列表， messages 示例:
            [{'content': '你是一个具备推理和行动能力的 AI 助手...

            ## 可用工具
            - calculate: 执行数学计算，支持基本的四则运算
            - search: 搜索互联网信息

            ## 工作流程
            请严格按照以下格式进行回应...

            ## 当前任务
            **Question:** 请帮我计算：(25 + 15) * 3 - 8 的结果是多少？

            ## 执行历史


            现在开始你的推理和行动：
            ', 'role': 'user'}]
            """
            messages = [{"role": "user", "content": prompt}]

            # 2. 调用LLM
            """
            response_text 示例：
            Thought: 这是一个简单的数学计算问题，需要计算 (25 + 15) * 3 - 8 的结果。我可以使用calculate工具来进行这个数学计算。根据运算优先级，先计算括号内的加法，再乘法，最后减法。
            Action: calculate[(25 + 15) * 3 - 8]
            """
            response_text = self.llm.invoke(messages, **kwargs)

            # 3. 解析输出
            thought, action = self._parse_output(response_text)

            # 4. 检查完成条件
            if action and action.startswith("Finish"):
                # 如 action: Finish[112]
                final_answer = self._parse_action_input(action)
                self.add_message(Message(input_text, "user"))
                self.add_message(Message(final_answer, "assistant"))
                return final_answer

            # 5. 执行工具调用
            if action:
                # tool_name: calculate  tool_input: (25 + 15) * 3 - 8
                tool_name, tool_input = self._parse_action(action)
                # observation: 112
                observation = self.tool_registry.execute_tool(tool_name, tool_input)
                self.current_history.append(f"Action: {action}")
                # 添加到历史记录,current_history:['Action: calculate[(25 + 15) * 3 - 8]', 'Observation: 112']
                self.current_history.append(f"Observation: {observation}")

        # 达到最大步数
        final_answer = "抱歉，我无法在限定步数内完成这个任务。"
        self.add_message(Message(input_text, "user"))
        self.add_message(Message(final_answer, "assistant"))
        return final_answer
