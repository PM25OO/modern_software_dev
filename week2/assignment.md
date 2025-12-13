# 第 2 周 – 待办事项提取器

本周，我们将扩展一个最小化的 FastAPI + SQLite 应用程序，该程序将自由格式的笔记转换为枚举的待办事项。

***我们建议在开始之前阅读整个文档。***

提示：要预览此 markdown 文件
- 在 Mac 上，按 `Command (⌘) + Shift + V`
- 在 Windows/Linux 上，按 `Ctrl + Shift + V`


## 入门指南

### Cursor 设置
按照以下说明设置 Cursor 并打开你的项目：
1. 兑换你的免费一年 Cursor Pro：https://cursor.com/students
2. 下载 Cursor：https://cursor.com/download
3. 要启用 Cursor 命令行工具，请打开 Cursor 并按 `Command (⌘) + Shift+ P`（Mac 用户）或 `Ctrl + Shift + P`（非 Mac 用户）打开命令面板。输入：`Shell Command: Install 'cursor' command`。选择它并按 Enter。
4. 打开一个新的终端窗口，导航到你的项目根目录，然后运行：`cursor .`

### 当前应用程序
以下是如何开始运行当前的入门应用程序：
1. 激活你的 conda 环境。
```
conda activate cs146s 
```
2. 从项目根目录运行服务器：
```
poetry run uvicorn week2.app.main:app --reload
```
3. 打开 Web 浏览器并导航到 http://127.0.0.1:8000/。
4. 熟悉应用程序的当前状态。确保你可以成功输入笔记并生成提取的待办事项清单。

## 练习
对于每个练习，使用 Cursor 帮助你对当前的待办事项提取器应用程序实施指定的改进。

在完成作业的过程中，使用 `writeup.md` 记录你的进度。请务必包含你使用的提示词，以及你或 Cursor 所做的任何更改。我们将根据 write-up 的内容进行评分。请在代码中包含注释以记录你的更改。

### TODO 1: 搭建新功能

分析 `week2/app/services/extract.py` 中现有的 `extract_action_items()` 函数，该函数目前使用预定义的启发式方法提取待办事项。

你的任务是实现一个 **LLM 驱动** 的替代方案 `extract_action_items_llm()`，利用 Ollama 通过大型语言模型执行待办事项提取。

一些提示：
- 要生成结构化输出（即字符串的 JSON 数组），请参阅此文档：https://ollama.com/blog/structured-outputs
- 要浏览可用的 Ollama 模型，请参阅此文档：https://ollama.com/library。请注意，较大的模型将占用更多资源，因此请从小模型开始。要拉取并运行模型：`ollama run {MODEL_NAME}`

### TODO 2: 添加单元测试

在 `week2/tests/test_extract.py` 中为 `extract_action_items_llm()` 编写单元测试，涵盖多种输入（例如，项目符号列表、关键字前缀行、空输入）。

### TODO 3: 重构现有代码以提高清晰度

对后端代码进行重构，特别关注定义良好的 API 契约/模式、数据库层清理、应用程序生命周期/配置、错误处理。

### TODO 4: 使用 Agentic 模式自动化小任务

1. 将 LLM 驱动的提取集成为一个新的端点。更新前端以包含一个“Extract LLM”按钮，点击该按钮时，通过新端点触发提取过程。

2. 公开最后一个端点以检索所有笔记。更新前端以包含一个“List Notes”按钮，点击该按钮时，获取并显示它们。

### TODO 5: 从代码库生成 README

***学习目标：***
*学生学习 AI 如何内省代码库并自动生成文档，展示 Cursor 解析代码上下文并将其转换为人类可读形式的能力。*

使用 Cursor 分析当前代码库并生成结构良好的 `README.md` 文件。README 应至少包括：
- 项目简要概述
- 如何设置和运行项目
- API 端点和功能
- 运行测试套件的说明

## 交付成果
按照提供的说明填写 `week2/writeup.md`。确保你的所有更改都记录在代码库中。

## 评分标准 (总分 100 分)
- 第 1-5 部分每部分 20 分（生成的代码 10 分，每个提示词 10 分）。