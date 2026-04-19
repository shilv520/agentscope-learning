# -*- coding: utf-8 -*-
"""
阶段1补充：通用 Agent 示例（使用 OpenAI 兼容接口）

本文件展示如何使用通用 OpenAI 接口创建 Agent，
兼容：OpenAI、DeepSeek、通义千问、本地模型等。

关键点：
- 使用 OpenAIChatModel 替代 DashScopeChatModel
- 使用 OpenAIChatFormatter 替代 DashScopeChatFormatter
- 可配置自定义 base_url 连接任何兼容服务
"""

import asyncio
import os

from agentscope.agent import ReActAgent
from agentscope.formatter import OpenAIChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.model import OpenAIChatModel
from agentscope.message import Msg
from agentscope.tool import Toolkit, execute_python_code


async def test_openai_agent() -> None:
    """使用 OpenAI 官方 API"""

    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)

    agent = ReActAgent(
        name="OpenAIBot",
        sys_prompt="你是一个智能助手。请用中文简洁回复。",
        model=OpenAIChatModel(
            api_key=os.environ.get("OPENAI_API_KEY"),
            model_name="gpt-4o",  # 或 gpt-3.5-turbo
            stream=True,
        ),
        formatter=OpenAIChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),
    )

    test_msg = Msg(
        name="user",
        content="你好，请计算 100 + 200",
        role="user",
    )

    print("=" * 50)
    print("OpenAI Agent（官方 API）")
    print("=" * 50)

    response = await agent(test_msg)
    print("完成")


async def test_deepseek_agent() -> None:
    """使用 DeepSeek API（OpenAI 兼容）"""

    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)

    agent = ReActAgent(
        name="DeepSeekBot",
        sys_prompt="你是一个智能助手。请用中文简洁回复。",
        model=OpenAIChatModel(
            api_key=os.environ.get("DEEPSEEK_API_KEY"),
            model_name="deepseek-chat",
            base_url="https://api.deepseek.com/v1",  # DeepSeek 的端点
            stream=True,
        ),
        formatter=OpenAIChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),
    )

    test_msg = Msg(
        name="user",
        content="你好，请计算 50 * 3",
        role="user",
    )

    print("=" * 50)
    print("DeepSeek Agent（OpenAI 兼容接口）")
    print("=" * 50)

    response = await agent(test_msg)
    print("完成")


async def test_qwen_openai_agent() -> None:
    """使用通义千问 OpenAI 兼容接口"""

    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)

    agent = ReActAgent(
        name="QwenBot",
        sys_prompt="你是一个智能助手。请用中文简洁回复。",
        model=OpenAIChatModel(
            api_key=os.environ.get("DASHSCOPE_API_KEY"),
            model_name="qwen-plus",  # qwen-max, qwen-plus, qwen-turbo
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            stream=True,
        ),
        formatter=OpenAIChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),
    )

    test_msg = Msg(
        name="user",
        content="你好，请计算 123 + 456",
        role="user",
    )

    print("=" * 50)
    print("通义千问 Agent（OpenAI 兼容模式）")
    print("=" * 50)
    print(f"问题: {test_msg.content}")
    print("-" * 50)

    response = await agent(test_msg)

    for block in response.content:
        if hasattr(block, "text"):
            print(block.text)

    print("\n[SUCCESS] Agent 运行成功！")


async def test_local_model_agent() -> None:
    """使用本地模型（如 Ollama、vLLM）"""

    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)

    # 假设你本地运行了 Ollama（默认端口 11434）
    agent = ReActAgent(
        name="LocalBot",
        sys_prompt="你是一个智能助手。",
        model=OpenAIChatModel(
            api_key="not-needed",  # 本地模型通常不需要 API key
            model_name="llama3",  # Ollama 中的模型名
            base_url="http://localhost:11434/v1",  # Ollama OpenAI 兼容端点
            stream=True,
        ),
        formatter=OpenAIChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),
    )

    test_msg = Msg(
        name="user",
        content="你好",
        role="user",
    )

    print("=" * 50)
    print("本地模型 Agent（Ollama）")
    print("=" * 50)

    # 注意：本地模型可能不支持工具调用
    response = await agent(test_msg)
    print("完成")


async def main() -> None:
    """演示多种模型后端"""

    print("\nAgentScope 支持多种模型后端")
    print("=" * 50)
    print("1. OpenAI 官方 API")
    print("2. DeepSeek（OpenAI 兼容）")
    print("3. 通义千问 OpenAI 兼容模式")
    print("4. 本地模型（Ollama/vLLM）")
    print("=" * 50)

    # 使用通义千问 OpenAI 兼容模式演示（因为你已有 DashScope API Key）
    if os.environ.get("DASHSCOPE_API_KEY"):
        await test_qwen_openai_agent()
    else:
        print("请设置 DASHSCOPE_API_KEY 或 OPENAI_API_KEY")


if __name__ == "__main__":
    asyncio.run(main())