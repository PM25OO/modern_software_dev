# Action Item Extractor (Week 2)

这是一个基于 FastAPI 和 SQLite 构建的待办事项提取应用程序。它可以从自由格式的笔记中提取可执行的待办事项（Action Items）。

本项目展示了如何结合传统的启发式算法和现代的大型语言模型（LLM）来处理文本数据。

## 功能特性

*   **笔记管理**：创建、查看和列出笔记。
*   **待办事项提取**：
    *   **启发式提取**：使用正则表达式和关键词匹配提取待办事项。
    *   **LLM 提取**：利用 Ollama (Llama 3.1) 智能分析文本并提取待办事项。
*   **待办事项管理**：查看提取的事项并标记完成状态。
*   **Web 界面**：提供一个简单的 HTML/JS 前端进行交互。

## 快速开始

### 前置要求

*   Python 3.10+
*   [Poetry](https://python-poetry.org/) (依赖管理)
*   [Ollama](https://ollama.com/) (用于 LLM 功能)
    *   请确保已安装并运行 Ollama，并拉取了 `llama3.1:8b` 模型：
        ```bash
        ollama pull llama3.1:8b
        ```

### 安装依赖

在项目根目录下运行：

```bash
poetry install
```

### 运行应用

启动开发服务器：

```bash
poetry run uvicorn week2.app.main:app --reload
```

服务启动后，访问 [http://127.0.0.1:8000](http://127.0.0.1:8000) 使用 Web 界面。

## API 端点

### 笔记 (Notes)

*   `GET /notes`: 获取所有笔记列表。
*   `POST /notes`: 创建新笔记。
*   `GET /notes/{note_id}`: 获取指定 ID 的笔记详情。

### 待办事项 (Action Items)

*   `GET /action-items`: 获取所有待办事项。
*   `POST /action-items/extract`: 使用启发式算法从文本中提取待办事项。
    *   参数: `{"text": "...", "save_note": true/false}`
*   `POST /action-items/extract-llm`: **(新功能)** 使用 LLM 从文本中提取待办事项。
    *   参数: `{"text": "...", "save_note": true/false}`
*   `POST /action-items/{action_item_id}/done`: 标记待办事项为完成/未完成。

## 运行测试

本项目包含单元测试，用于验证提取逻辑和 API 功能。

运行所有测试：

```bash
poetry run pytest week2/tests
```

## 项目结构

*   `app/`: 应用程序源代码
    *   `main.py`: FastAPI 应用入口和生命周期管理。
    *   `db.py`: 数据库连接和 CRUD 操作。
    *   `schemas.py`: Pydantic 数据模型。
    *   `routers/`: API 路由定义。
    *   `services/`: 业务逻辑（如提取算法）。
*   `frontend/`: 简单的静态前端文件。
*   `tests/`: 测试套件。
*   `data/`: SQLite 数据库文件存储位置。
