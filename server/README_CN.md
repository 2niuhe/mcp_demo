# MCP 服务器示例

本目录包含使用 Python MCP SDK 实现的模型上下文协议（Model Context Protocol，MCP）服务器示例。

## 可用的 MCP 服务器

### 1. 计算器服务器 (`calculator.py`)

一个简单的计算器，提供数学运算作为 MCP 工具。

**功能：**
- 基本算术运算（加、减、乘、除）
- 高级数学函数（幂、平方根、立方根、阶乘）
- 三角函数（正弦、余弦、正切）
- 对数函数

**运行服务器：**
```bash
python calculator.py
```

### 2. 文件管理器服务器 (`file_manager.py`)

一个文件管理服务器，提供文件系统操作作为 MCP 工具。

**功能：**
- 列出目录中的文件
- 读取文件内容
- 将内容写入文件
- 创建目录
- 获取文件信息
- 搜索文件

**运行服务器：**
```bash
python file_manager.py
```

### 3. 天气服务服务器 (`weather_service.py`)

一个从 OpenWeatherMap API 获取数据的天气服务。

**功能：**
- 获取城市的当前天气
- 获取最多 5 天的天气预报
- 获取位置的空气污染数据
- 获取城市的地理编码信息

**设置：**
1. 将根目录中的 `.env.example` 复制到 `.env`
2. 在 `.env` 文件中添加您的 OpenWeatherMap API 密钥

**运行服务器：**
```bash
python weather_service.py
```

## 使用 MCP Inspector 进行测试

您可以使用 MCP Inspector 工具测试这些 MCP 服务器：

1. 安装 MCP Inspector：
   ```bash
   pip install "mcp[cli]"
   ```

2. 在一个终端中运行 MCP 服务器：
   ```bash
   python calculator.py
   ```

3. 在另一个终端中，运行 MCP Inspector：
   ```bash
   mcp inspect
   ```

4. 按照提示连接到您的 MCP 服务器并测试可用的工具。
