# Claude Code 配置

个人 Claude Code 配置仓库，包含子 Agent、斜杠命令、技能、编码规则和自动化 Hook。

## 目录结构

```
~/.claude/
├── CLAUDE.md              # 全局行为规则
├── CONTRIBUTING.md         # 贡献指南
├── agents/                 # 55 个子 Agent
├── commands/               # 76 个斜杠命令
├── contexts/               # 上下文预设（开发、研究、审查）
├── hooks/                  # Hook 配置（hooks.json）
├── output-styles/          # 回复风格预设
├── plans/                  # 执行计划
├── plugins/                # 插件配置与市场缓存
├── rules/                  # 按语言分类的编码规则（14 种语言）
├── schemas/                # 配置校验用 JSON Schema
├── scripts/                # 工具脚本（CI、Hook、公共库）
├── skills/                 # 50+ 技能
└── webnovel-writer/        # 网文写作工作区配置
```

## 核心组件

### 子 Agent（55 个）

按任务类型划分的专用子 Agent：

| 分类 | Agent |
|------|-------|
| 架构设计 | `architect`、`code-architect`、`a11y-architect`、`planner`、`dev-planner` |
| 代码审查 | `code-reviewer`、`python-reviewer`、`typescript-reviewer`、`java-reviewer`、`go-reviewer`、`rust-reviewer`、`kotlin-reviewer`、`cpp-reviewer`、`csharp-reviewer`、`dart-reviewer`、`flutter-reviewer`、`database-reviewer`、`healthcare-reviewer`、`security-reviewer` |
| 构建排错 | `build-error-resolver`、`cpp-build-resolver`、`go-build-resolver`、`java-build-resolver`、`kotlin-build-resolver`、`pytorch-build-resolver`、`rust-build-resolver`、`dart-build-resolver` |
| 开发重构 | `frontend-developer`、`code-simplifier`、`refactor-cleaner`、`performance-optimizer` |
| 测试 | `e2e-runner`、`tdd-guide`、`pr-test-analyzer` |
| 分析 | `bug-analyzer`、`comment-analyzer`、`conversation-analyzer`、`code-explorer`、`silent-failure-hunter`、`type-design-analyzer` |
| 文档 | `doc-updater`、`docs-lookup` |
| 运维 | `loop-operator`、`chief-of-staff`、`opensource-forker`、`opensource-packager`、`opensource-sanitizer` |
| AI/生成 | `gan-evaluator`、`gan-generator`、`gan-planner`、`story-generator`、`ui-sketcher` |
| 其他 | `seo-specialist`、`harness-optimizer` |

### 斜杠命令（76 个）

通过 `/命令名` 调用：

- **Git**：`commit`、`review-pr`、`prp-commit`、`prp-pr`、`prp-plan`、`prp-implement`、`prp-prd`
- **构建**：`build-fix`、`cpp-build`、`go-build`、`java-build`、`kotlin-build`、`rust-build`、`gradle-build`、`flutter-build`、`gan-build`
- **测试**：`cpp-test`、`go-test`、`kotlin-test`、`rust-test`、`flutter-test`、`tdd`、`e2e`、`test-coverage`、`generate-tests`
- **审查**：`code-review`、`cpp-review`、`go-review`、`kotlin-review`、`python-review`、`rust-review`、`flutter-review`
- **工作流**：`feature-dev`、`plan`、`verify`、`quality-gate`、`checkpoint`、`evolve`、`promote`、`orchestrate`
- **会话**：`save-session`、`resume-session`、`sessions`、`loop-start`、`loop-status`
- **技能**：`skill-create`、`skill-health`、`hookify`、`hookify-list`、`hookify-configure`、`hookify-help`
- **学习**：`learn`、`learn-eval`、`instinct-export`、`instinct-import`、`instinct-status`
- **多 Agent**：`multi-plan`、`multi-frontend`、`multi-backend`、`multi-execute`、`multi-workflow`
- **工具**：`aside`、`auto-update`、`model-route`、`pm2`、`projects`、`prune`、`setup-pm`、`update-codemaps`、`update-docs`、`jira`、`santa-loop`、`eval`

### 编码规则（14 种语言）

`rules/` 目录下按语言组织的编码标准：

`cpp`、`csharp`、`dart`、`golang`、`java`、`kotlin`、`perl`、`php`、`python`、`rust`、`swift`、`typescript`、`web`

每个语言目录包含：
- `coding-style.md` — 命名、格式化规范
- `hooks.md` — 前置/后置动作 Hook
- `patterns.md` — 设计模式与惯用法
- `security.md` — 安全最佳实践
- `testing.md` — 测试策略

根级规则：`agents.md`、`code-review.md`、`coding-style.md`、`development-workflow.md`、`git-workflow.md`、`hooks.md`、`patterns.md`、`performance.md`、`security.md`、`testing.md`

### 技能（50+）

包含领域知识与自动化能力的技能模块：

- **后端**：`backend-patterns`、`django-patterns`、`django-security`、`django-tdd`、`django-verification`、`springboot-patterns`、`springboot-security`、`springboot-tdd`、`springboot-verification`、`postgres-patterns`、`clickhouse-io`、`jpa-patterns`、`java-coding-standards`
- **前端**：`frontend-patterns`、`frontend-design`、`coding-standards`
- **语言**：`golang-patterns`、`golang-testing`、`python-patterns`、`python-testing`
- **文档处理**：`docx`、`pdf`、`pptx`、`xlsx`、`markitdown`
- **安全**：`security-review`
- **测试**：`tdd-workflow`、`e2e-testing`、`verification-loop`、`eval-harness`
- **DevOps**：`deployment-patterns`、`docker-patterns`、`database-migrations`
- **创意**：`algorithmic-art`、`canvas-design`、`theme-factory`、`slack-gif-creator`、`web-artifacts-builder`
- **写作**：`chinese-novelist-skill`、`jacky-writing`、`fireowl-novel`、`internal-comms`、`doc-coauthoring`、`brand-guidelines`
- **Obsidian**：`obsidian-cli`、`obsidian-markdown`、`obsidian-bases`、`json-canvas`
- **学习**：`continuous-learning`、`continuous-learning-v2`、`iterative-retrieval`
- **视频**：`remotion`、`video-copy-analyzer`、`subtitle-downloader`
- **元工具**：`skill-creator`、`mcp-builder`、`webapp-testing`
- **其他**：`defuddle`、`project-guidelines-example`、`strategic-compact`

### Hook 自动化

在 `hooks/hooks.json` 中配置的自动化 Hook：

- **PreToolUse**：阻止在 tmux 外启动开发服务器、tmux 使用提醒、git push 前审查、阻止随意创建 `.md` 文件、建议手动压缩上下文
- **PostToolUse**：PR URL 记录、构建分析、Prettier 自动格式化、TypeScript 类型检查、console.log 警告
- **SessionStart**：加载上次上下文、检测包管理器
- **SessionEnd**：持久化会话状态、评估会话可提取的模式
- **PreCompact**：压缩上下文前保存状态
- **Stop**：检查修改文件中的 console.log

### 脚本

`scripts/` 目录下的工具脚本：

- `ci/` — Agent、命令、Hook、规则、技能的校验脚本
- `hooks/` — 运行时 Hook 脚本（会话管理、console.log 检查、压缩建议）
- `lib/` — 公共工具库（包管理器、会话管理、会话别名、通用工具）

### 其他

- `contexts/` — 上下文预设：`dev`（开发）、`research`（研究）、`review`（审查）
- `output-styles/` — 回复风格预设：`coding-vibes`、`structural-thinking`
- `schemas/` — `hooks`、`package-manager`、`plugin` 的 JSON Schema
- `plugins/` — 插件注册表与市场缓存

## 安装

1. 克隆到 `~/.claude/`：
   ```bash
   git clone https://github.com/YOUR_USERNAME/claude-config.git ~/.claude
   ```

2. 创建 `settings.json`（手动配置或参考示例）：
   ```json
   {
     "env": {
       "ANTHROPIC_AUTH_TOKEN": "在此填入你的 Token",
       "ANTHROPIC_BASE_URL": "在此填入你的 API 地址"
     },
     "model": "sonnet",
     "effortLevel": "high"
   }
   ```

3. 安装插件依赖（如需要）：
   ```bash
   cd ~/.claude/plugins/marketplaces/claude-hud && npm install
   ```

## 安全提示

- `settings.json` 包含 API Token — **绝对不要提交**
- `mcp-configs/mcp-servers.json` 可能包含 API Key — **绝对不要提交**
- `sessions/`、`session-data/`、`debug/`、`metrics/` 为本地运行时数据 — 已通过 `.gitignore` 排除
