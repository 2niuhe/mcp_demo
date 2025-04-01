# MCP 客户端演示

一个简化的 MCP 客户端实现，可连接到 MCP 服务器，列出可用工具，并通过简单的聊天界面允许执行工具。

## 功能

- 连接到配置文件中定义的多个 MCP 服务器
- 列出所有连接服务器的可用工具
- 允许您交互式地执行工具
- 提供使用 LLM 解释请求并执行工具的聊天模式

## 设置

1. 确保您已安装 Python 3.8+
2. 安装所需的依赖项：
   ```bash
   pip install -r requirements.txt
   ```
3. 将 `.env.example` 复制到 `.env` 并添加您的 API 密钥：
   ```bash
   cp .env.example .env
   # 然后在 .env 中编辑您的实际 API 密钥
   ```

## 配置

客户端使用 `servers_config.json` 文件进行配置，该文件定义了要连接的 MCP 服务器。每个服务器条目包括：

- `command`：运行服务器的命令（例如，`python`）
- `args`：传递给命令的参数（例如，`["../server/calculator.py"]`）
- `env`：为服务器设置的可选环境变量

配置示例：
```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["../server/calculator.py"],
      "env": {}
    },
    "file_manager": {
      "command": "python",
      "args": ["../server/file_manager.py"],
      "env": {}
    }
  }
}
```

## 使用方法

运行客户端：
```bash
python mcp_client_demo.py
```

### 可用命令

- `tools`：列出所有连接服务器的所有可用工具
- `execute`：交互式执行工具
- `chat`：启动与 LLM 的聊天模式（需要 API 密钥）
- `help`：显示可用命令
- `exit`/`quit`：退出程序

### 聊天模式

聊天模式使用 DeepSeek 模型解释您的请求并执行适当的工具。当 LLM 确定应该使用工具时，它将其响应格式化为包含服务器、工具和参数的 JSON 对象。然后，客户端将执行该工具并将结果发送回 LLM 以获得最终响应。

## 环境变量

- `OPENWEATHER_API_KEY`：OpenWeatherMap 服务的 API 密钥（由 weather_service MCP 服务器使用）
- `LLM_API_KEY`：DeepSeek LLM 服务的 API 密钥（由聊天模式使用）

## 添加新的 MCP 服务器

要添加新的 MCP 服务器：

1. 将服务器配置添加到 `servers_config.json`
2. 重启客户端

## 故障排除

- 如果遇到连接问题，请确保 MCP 服务器正在运行
- 如果聊天模式不工作，请检查 `.env` 文件中的 LLM API 密钥
- 对于其他问题，请检查日志中的错误消息
