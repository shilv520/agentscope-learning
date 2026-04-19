# -*- coding: utf-8 -*-
"""
阶段1：Hello AgentScope - 第一个 Agent 示例

学习目标：
1. 理解 ReActAgent 的创建流程
2. 掌握核心组件：Model, Agent, Memory, Tool, Formatter
3. 了解异步编程模式

运行方式：
1. 设置环境变量：export DASHSCOPE_API_KEY=your_key
2. 运行：python 01_hello_agentscope.py
"""

import asyncio
import os

from agentscope.agent import ReActAgent, UserAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.model import DashScopeChatModel
from agentscope.tool import (
    Toolkit,
    execute_shell_command,
    execute_python_code,
    view_text_file,
)


async def main() -> None:
    """运行第一个 ReAct Agent"""

    # ========== 1. 创建工具集 (Toolkit) ==========
    # Toolkit 是工具的容器，Agent 可以调用这些工具
    toolkit = Toolkit()

    # 注册内置工具函数
    toolkit.register_tool_function(execute_shell_command)  # 执行 shell 命令
    toolkit.register_tool_function(execute_python_code)     # 执行 Python 代码
    toolkit.register_tool_function(view_text_file)          # 查看文本文件

    # ========== 2. 创建 Agent ==========
    # ReActAgent 是核心 Agent 类型，采用 ReAct（Reasoning + Acting）模式
    agent = ReActAgent(
        name="Friday",  # Agent 名称
        sys_prompt="你是一个名为 Friday 的智能助手，可以帮助用户完成各种任务。请用中文回复。",  # 系统提示词
        model=DashScopeChatModel(
            api_key="sk-3b0dd0f9d0f241bfb14656c1197bd4c1",
            model_name="qwen-max",  # 使用 qwen-max 模型
            enable_thinking=False,  # 是否启用思考模式
            stream=True,  # 流式输出
        ),
        formatter=DashScopeChatFormatter(),  # Prompt 格式化器
        toolkit=toolkit,  # 工具集
        memory=InMemoryMemory(),  # 内存（存储对话历史）
    )

    # ========== 3. 创建用户 Agent ==========
    # UserAgent 用于接收用户输入
    user = UserAgent(name="User")

    # ========== 4. 运行对话循环 ==========
    msg = None
    while True:
        # 用户输入
        msg = await user(msg)
        if msg.get_text_content() == "exit":
            break
        # Agent 处理并回复
        msg = await agent(msg)


if __name__ == "__main__":

    # 运行异步主函数
    asyncio.run(main())
