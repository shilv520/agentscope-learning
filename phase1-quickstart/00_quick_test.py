# -*- coding: utf-8 -*-
"""
阶段1：快速测试 - 验证 Agent 是否正常工作
"""

import asyncio
import os

from agentscope.agent import ReActAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.model import DashScopeChatModel
from agentscope.message import Msg
from agentscope.tool import Toolkit, execute_python_code


async def test_agent() -> None:
    """快速测试 Agent 是否正常工作"""

    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)

    agent = ReActAgent(
        name="Friday",
        sys_prompt="你是一个名为 Friday 的智能助手。请用中文简洁回复。",
        model=DashScopeChatModel(
            api_key=os.environ.get("DASHSCOPE_API_KEY"),
            model_name="qwen-max",
            stream=True,
        ),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),
    )

    # 发送测试消息
    test_msg = Msg(name="user", content="你好，请用 Python 计算 123 + 456 的结果。", role="user")

    print("=" * 50)
    print("测试 AgentScope ReActAgent")
    print("=" * 50)
    print(f"问题: {test_msg.content}")
    print("-" * 50)

    # 调用 Agent
    response = await agent(test_msg)

    print("-" * 50)
    print(f"\n回复内容:")
    for block in response.content:
        if hasattr(block, 'text'):
            print(block.text)
        elif isinstance(block, dict) and 'text' in block:
            print(block['text'])
        else:
            print(block)
    print("\n" + "=" * 50)
    print("[SUCCESS] Agent 运行成功！阶段1验证完成。")


if __name__ == "__main__":
    if not os.environ.get("DASHSCOPE_API_KEY"):
        print("[ERROR] 请设置环境变量 DASHSCOPE_API_KEY")
        exit(1)

    print("正在连接 DashScope API...")
    asyncio.run(test_agent())