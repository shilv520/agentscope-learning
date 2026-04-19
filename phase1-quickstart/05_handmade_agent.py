# -*- coding: utf-8 -*-
"""
阶段1补充：纯手工 Agent（不依赖任何框架）

本文件展示 Agent 的核心原理，完全从零实现，
帮助你理解 Agent 是如何工作的。

核心原理：
1. Agent = LLM + Memory + Tools
2. ReAct = Reasoning（推理） + Acting（执行工具）
3. 循环：思考 → 决策 → 执行工具 → 观察 → 再思考
"""

import asyncio
import json
import os
from openai import OpenAI
from typing import Callable


# ========== 核心组件 ==========

class Memory:
    """简单的对话记忆"""

    def __init__(self):
        self.history = []

    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def get(self):
        return self.history.copy()


class Tool:
    """工具定义"""

    def __init__(self, name: str, func: Callable, description: str):
        self.name = name
        self.func = func
        self.description = description


def execute_python(code: str) -> str:
    """执行 Python 代码"""
    try:
        result = {}
        exec(code, result)
        if "result" in result:
            return str(result["result"])
        return "代码执行成功（无返回值）"
    except Exception as e:
        return f"错误: {e}"


# ========== 纯手工 ReAct Agent ==========

class HandmadeReActAgent:
    """
    从零实现的 ReAct Agent
    核心流程：Think → Act → Observe → Think...
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1",
        model: str = "qwen-plus",
        tools: list[Tool] = None,
    ):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.memory = Memory()
        self.tools = tools or []

        # 系统提示：定义 Agent 行为
        self.system_prompt = """你是一个智能助手。

你可以使用以下工具：
{tool_descriptions}

工作流程：
1. 收到问题后，先思考是否需要使用工具
2. 如果需要，输出 JSON 格式的工具调用：
   {"tool": "工具名", "input": "输入参数"}
3. 等待工具执行结果
4. 根据结果给出最终回答

如果不需要工具，直接回答即可。
"""

    def _build_tool_schema(self) -> str:
        """构建工具描述"""
        descriptions = []
        for tool in self.tools:
            descriptions.append(f"- {tool.name}: {tool.description}")
        return "\n".join(descriptions)

    async def think(self) -> str:
        """思考阶段：调用 LLM"""

        messages = [
            {"role": "system", "content": self.system_prompt.format(
                tool_descriptions=self._build_tool_schema()
            )}
        ] + self.memory.get()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return response.choices[0].message.content

    async def act(self, thought: str) -> tuple[str, str]:
        """执行阶段：解析并执行工具"""

        # 尝试解析 JSON 工具调用
        try:
            # 简单解析：查找 JSON 块
            if "{" in thought and "}" in thought:
                start = thought.index("{")
                end = thought.rindex("}") + 1
                json_str = thought[start:end]
                tool_call = json.loads(json_str)

                if "tool" in tool_call:
                    tool_name = tool_call["tool"]
                    tool_input = tool_call.get("input", "")

                    # 查找并执行工具
                    for tool in self.tools:
                        if tool.name == tool_name:
                            result = tool.func(tool_input)
                            return tool_name, result

        except (json.JSONDecodeError, ValueError):
            pass

        return None, None

    async def run(self, user_input: str) -> str:
        """完整 ReAct 循环"""

        # 1. 用户输入
        self.memory.add("user", user_input)

        max_iterations = 5
        for i in range(max_iterations):
            # 2. 思考
            thought = await self.think()
            print(f"\n[思考 {i+1}]: {thought}")

            # 3. 执行工具
            tool_name, tool_result = await self.act(thought)

            if tool_name:
                print(f"\n[执行工具]: {tool_name}")
                print(f"[工具结果]: {tool_result}")

                # 4. 观察：把结果加入记忆
                self.memory.add("assistant", thought)
                self.memory.add("system", f"工具 {tool_name} 执行结果: {tool_result}")

                # 继续思考...
                continue

            # 5. 无工具调用，输出最终答案
            self.memory.add("assistant", thought)
            return thought

        return "达到最大迭代次数"


# ========== 运行演示 ==========

async def main():
    """演示纯手工 Agent"""

    if not os.environ.get("DASHSCOPE_API_KEY"):
        print("请设置 DASHSCOPE_API_KEY")
        return

    # 定义工具
    tools = [
        Tool(
            name="execute_python",
            func=execute_python,
            description="执行 Python 代码并返回结果。输入为代码字符串。",
        )
    ]

    # 创建 Agent
    agent = HandmadeReActAgent(
        api_key=os.environ.get("DASHSCOPE_API_KEY"),
        tools=tools,
    )

    print("=" * 50)
    print("纯手工 ReAct Agent（无框架依赖）")
    print("=" * 50)
    print("\n原理：Think → Act → Observe 循环")
    print("=" * 50)

    # 测试
    user_input = "请用 Python 计算 123 + 456 的结果"
    print(f"\n[用户]: {user_input}")

    result = await agent.run(user_input)
    print(f"\n[最终回答]: {result}")

    print("\n" + "=" * 50)
    print("核心要点：")
    print("1. Agent = LLM + Memory + Tools")
    print("2. ReAct 循环：Think → Act → Observe")
    print("3. AgentScope 框架帮你封装了这些细节")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())