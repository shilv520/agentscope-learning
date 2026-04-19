# -*- coding: utf-8 -*-
"""
阶段1：实践练习 - 创建不同角色的 Agent

练习目标：
1. 修改 sys_prompt 创建不同角色
2. 添加自定义工具
3. 观察 Agent 的行为变化

练习任务：
- 任务1：创建一个"翻译助手" Agent
- 任务2：创建一个"代码助手" Agent
- 任务3：添加一个自定义工具
"""

import asyncio
import os
from typing import Annotated

from agentscope.agent import ReActAgent, UserAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.model import DashScopeChatModel
from agentscope.tool import Toolkit, tool_function, execute_python_code, execute_shell_command


# ========== 自定义工具示例 ==========
@tool_function
def get_current_time() -> Annotated[str, "返回当前时间"]:
    """获取当前日期和时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool_function
def calculate(expression: Annotated[str, "数学表达式，如 '2+3*4'"]) -> str:
    """计算数学表达式"""
    try:
        result = eval(expression)
        return f"计算结果: {expression} = {result}"
    except Exception as e:
        return f"计算错误: {e}"


# ========== 不同角色的 Agent ==========
def create_translator_agent() -> ReActAgent:
    """创建翻译助手 Agent"""
    toolkit = Toolkit()
    toolkit.register_tool_function(get_current_time)

    return ReActAgent(
        name="Translator",
        sys_prompt="""你是一个专业的翻译助手。
- 可以翻译中文、英文、日文、韩文等语言
- 翻译时保持原文的风格和语气
- 专业术语要准确翻译
- 请用中文回复用户""",
        model=DashScopeChatModel(
            api_key=os.environ.get("DASHSCOPE_API_KEY"),
            model_name="qwen-max",
            stream=True,
        ),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),
    )


def create_code_assistant_agent() -> ReActAgent:
    """创建代码助手 Agent"""
    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(execute_shell_command)
    toolkit.register_tool_function(get_current_time)

    return ReActAgent(
        name="CodeHelper",
        sys_prompt="""你是一个专业的编程助手。
- 可以编写、解释、调试 Python 代码
- 提供代码优化建议
- 解释编程概念和最佳实践
- 使用 execute_python_code 工具运行代码验证
- 请用中文回复""",
        model=DashScopeChatModel(
            api_key=os.environ.get("DASHSCOPE_API_KEY"),
            model_name="qwen-max",
            stream=True,
        ),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),
    )


def create_general_assistant_agent() -> ReActAgent:
    """创建通用助手 Agent（带更多工具）"""
    toolkit = Toolkit()
    toolkit.register_tool_function(get_current_time)
    toolkit.register_tool_function(calculate)
    toolkit.register_tool_function(execute_python_code)

    return ReActAgent(
        name="Assistant",
        sys_prompt="""你是一个全能助手，可以：
- 回答各种问题
- 进行数学计算
- 编写和运行代码
- 提供时间信息
请用中文回复，尽可能帮助用户完成任务。""",
        model=DashScopeChatModel(
            api_key=os.environ.get("DASHSCOPE_API_KEY"),
            model_name="qwen-max",
            stream=True,
        ),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),
    )


async def run_agent(agent: ReActAgent) -> None:
    """运行指定的 Agent"""
    user = UserAgent(name="User")

    print(f"\n{'='*50}")
    print(f"Agent: {agent.name}")
    print(f"{'='*50}")
    print("输入 'exit' 退出，输入 'switch' 切换 Agent")

    msg = None
    while True:
        msg = await user(msg)
        content = msg.get_text_content()

        if content == "exit":
            break
        if content == "switch":
            return

        msg = await agent(msg)


async def main() -> None:
    """主函数：选择并运行不同的 Agent"""

    # 创建不同的 Agent
    agents = {
        "1": create_translator_agent(),
        "2": create_code_assistant_agent(),
        "3": create_general_assistant_agent(),
    }

    print("\n选择要运行的 Agent：")
    print("1. 翻译助手 (Translator)")
    print("2. 代码助手 (CodeHelper)")
    print("3. 通用助手 (Assistant)")

    while True:
        choice = await asyncio.to_thread(input, "\n请输入选择 (1/2/3) 或 'exit' 退出: ")
        choice = choice.strip()

        if choice == "exit":
            break
        if choice in agents:
            await run_agent(agents[choice])
        else:
            print("无效选择，请输入 1、2 或 3")


if __name__ == "__main__":
    if not os.environ.get("DASHSCOPE_API_KEY"):
        print("请设置环境变量 DASHSCOPE_API_KEY")
        exit(1)

    asyncio.run(main())