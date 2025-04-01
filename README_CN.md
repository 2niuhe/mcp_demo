# MCP 演示项目

本项目包含模型上下文协议（Model Context Protocol，MCP）的服务器和客户端示例实现。

## 项目结构

项目分为两个主要部分：

- **server/**：包含 MCP 服务器示例
- **client/**：包含 MCP 客户端演示实现

## MCP 服务器

`server/` 目录包含三个 MCP 服务器示例：

1. **计算器服务器**：提供数学运算功能
2. **文件管理器服务器**：提供文件系统操作
3. **天气服务服务器**：提供天气数据查询功能

详细信息请参阅 [服务器 README](server/README_CN.md)。

## MCP 客户端

`client/` 目录包含一个 MCP 客户端演示实现，它可以：

- 连接到多个 MCP 服务器
- 列出可用工具
- 执行工具
- 提供基于 LLM 的聊天界面

详细信息请参阅 [客户端 README](client/README_CN.md)。

## 设置

1. 克隆此仓库
2. 安装依赖项：
   ```bash
   pip install -r requirements.txt
   ```
3. 设置环境变量：
   ```bash
   cp .env.example .env
   # 编辑 .env 文件添加您的 API 密钥
   ```

## 快速开始

1. 启动 MCP 服务器（例如，计算器服务器）：
   ```bash
   cd server
   python calculator.py
   ```

2. 在另一个终端中，启动 MCP 客户端：
   ```bash
   cd client
   python mcp_client_demo.py
   ```

3. 在客户端中，您可以：
   - 输入 `tools` 查看可用工具
   - 输入 `execute` 执行特定工具
   - 输入 `chat` 启动聊天模式
   - 输入 `help` 查看帮助信息

## 环境变量

- `OPENWEATHER_API_KEY`：用于天气服务的 OpenWeatherMap API 密钥
- `LLM_API_KEY`：用于聊天模式的 DeepSeek API 密钥

## 许可证

本项目作为 MCP 协议的示例实现提供。
