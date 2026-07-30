# v0.4.0 Hybrid Agent：Windows 启动与验证

本文以 PowerShell 为例。命令前的“运行目录”很重要；如果目录不对，命令即使没有拼错也会失败。

## 1. 最终目录结构

以下是当前阶段与第一版目标结构。带“后续”字样的页面会在后续阶段创建。

```text
pl-geo-analytics/
├── frontend/
│   ├── app/
│   │   ├── clubs/[clubId]/page.tsx          # 后续
│   │   ├── standings/page.tsx               # 后续
│   │   ├── players/[playerId]/page.tsx      # 后续
│   │   ├── players/page.tsx                 # 后续
│   │   ├── compare/page.tsx                 # 后续
│   │   ├── matches/[matchId]/page.tsx       # 后续
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── agent/                           # 足球分析 Agent
│   │   ├── data/                            # 阶段 2 数据展示
│   │   ├── charts/                          # 后续
│   │   ├── clubs/                           # 后续
│   │   ├── layout/                          # 后续
│   │   ├── map/                             # 后续
│   │   ├── matches/                         # 后续
│   │   ├── players/                         # 后续
│   │   ├── system/
│   │   └── ui/                              # 后续
│   ├── services/
│   ├── types/
│   ├── public/
│   ├── .env.example
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── api/routes/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   ├── tests/
│   ├── migrations/
│   ├── alembic.ini
│   ├── .env.example
│   ├── pyproject.toml
│   └── requirements.txt
├── data/
│   ├── raw/
│   ├── processed/
│   ├── geo/
│   └── sample/
├── notebooks/
├── scripts/
├── docs/
├── .editorconfig
├── .env.example
├── .gitignore
├── README.md
└── PROJECT_PLAN.md
```

## 2. 前端、后端和数据库的关系

1. 用户打开 Next.js 前端。
2. 前端通过 `NEXT_PUBLIC_API_BASE_URL` 请求 FastAPI 的 `/api/*`。
3. FastAPI 校验请求，调用数据处理服务或数据库。
4. 数据库只接受后端连接，不直接暴露给浏览器。
5. FastAPI 以统一 JSON 返回结果，前端再绘制表格、地图或图表。

数据库密码绝不能放进 `NEXT_PUBLIC_*` 变量，因为这类变量会出现在浏览器代码中。

## 3. 需要提前安装的软件

### 当前阶段必装

| 软件 | 建议版本 | 用途 |
| --- | --- | --- |
| VS Code | 最新稳定版 | 编写和调试代码 |
| Git | 最新稳定版 | 分支、提交和 GitHub |
| Node.js | 22 LTS | Next.js 前端 |
| Python | 3.12.x | FastAPI 后端 |
| Microsoft Edge / Chrome | 最新稳定版 | 浏览器调试 |

VS Code 建议扩展：

- Python
- Pylance
- ESLint
- Tailwind CSS IntelliSense
- GitLens（可选）

### 后续再安装也可以

- PostgreSQL（正式数据库）
- DBeaver 或 pgAdmin（二选一即可）
- Postman（Swagger 已能测试 API，所以不是必需）

当前已使用 SQLite，因此不需要单独安装数据库软件。

安装后在 PowerShell 验证：

```powershell
git --version
node --version
npm --version
py -3.12 --version
```

## 4. Windows 创建命令

如果从完全空白的电脑手动创建，推荐把项目放在不含中文和空格的路径，例如 `D:\Code`。

### 4.1 创建根目录并初始化 Git

运行目录：`D:\Code`

```powershell
mkdir pl-geo-analytics
cd pl-geo-analytics
git init
git branch -M main
```

### 4.2 初始化前端

运行目录：`D:\Code\pl-geo-analytics`

```powershell
npx create-next-app@latest frontend --ts --tailwind --eslint --app --use-npm --import-alias "@/*" --no-src-dir --yes
```

完成后：

```powershell
cd frontend
Copy-Item .env.example .env.local
npm run dev
```

如果你使用本仓库已有代码，不需要再次运行 `create-next-app`，只运行 `npm ci`。

### 4.3 初始化后端虚拟环境

运行目录：`D:\Code\pl-geo-analytics`

```powershell
cd backend
py -3.12 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

看到命令行开头出现 `(.venv)`，说明虚拟环境已激活。

首次初始化数据库（可选，正常启动后端也会自动完成）：

```powershell
python -m app.database.init_db
```

启动后端：

```powershell
uvicorn app.main:app --reload --port 8000
```

不要关闭这个 PowerShell 窗口。

### 4.4 启动前端

另开一个 PowerShell。

运行目录：`D:\Code\pl-geo-analytics\frontend`

```powershell
npm ci
npm run dev
```

## 5. 命令与运行目录速查

| 命令 | 运行目录 |
| --- | --- |
| `git init` | `pl-geo-analytics/` |
| `git status` | `pl-geo-analytics/` |
| `npm ci` | `pl-geo-analytics/frontend/` |
| `npm run dev` | `pl-geo-analytics/frontend/` |
| `npm run lint` | `pl-geo-analytics/frontend/` |
| `npm run build` | `pl-geo-analytics/frontend/` |
| `.\.venv\Scripts\Activate.ps1` | `pl-geo-analytics/backend/` |
| `pip install -r requirements.txt` | `pl-geo-analytics/backend/`，且已激活虚拟环境 |
| `uvicorn app.main:app --reload --port 8000` | `pl-geo-analytics/backend/` |
| `python -m app.database.init_db` | `pl-geo-analytics/backend/` |
| `alembic upgrade head` | `pl-geo-analytics/backend/` |
| `pytest` | `pl-geo-analytics/backend/` |

## 6. 初始化完成后的验证

### 后端

打开 <http://127.0.0.1:8000/api/health>，应看到：

```json
{
  "success": true,
  "message": "Premier League Insight Agent API is running",
  "data": {
    "service": "Premier League Insight Agent API",
    "status": "healthy",
    "environment": "development",
    "version": "0.4.0"
  }
}
```

打开 <http://127.0.0.1:8000/docs>，应看到 FastAPI 自动生成的 Swagger 页面，以及：

- `GET /api/health`
- `GET /api/clubs`
- `GET /api/clubs/{slug}`
- `GET /api/standings`
- `GET /api/agent/players`
- `GET /api/agent/capabilities`
- `POST /api/agent/analyze`

在 `backend/` 运行：

```powershell
pytest
```

应显示 14 个测试通过。

### 前端

打开 <http://localhost:3000>，应满足：

- 页面显示 `Premier League Insight Agent`。
- 显示“v0.4.0 · Qwen-ready Hybrid Agent”。
- 后端运行时显示“后端连接正常”。
- 显示 2024-25 完整 20 支球队、球场信息和最终积分榜历史快照。
- 可以选择萨卡与帕尔默并运行高位逼抢分析。
- 分析结果显示 5 步执行轨迹、指标百分位、证据和结论边界。
- 未配置千问时显示 `LOCAL SAFE MODE`，分析仍可正常运行。
- 配置千问后显示模型名称和 `QWEN ENHANCED`。
- 点击球队卡片时，球场坐标和积分榜高亮同步变化。
- 停止后端并刷新页面时显示“暂未连接后端”，页面本身不崩溃。
- 阶段 2 区域显示友好错误提示，并可点击“重新连接”。
- 手机宽度下页面不出现明显横向溢出。

在 `frontend/` 运行：

```powershell
npm run lint
npm run build
```

两个命令都应以退出码 0 结束。

### Git

在项目根目录运行：

```powershell
git status
git check-ignore frontend\.env.local
git check-ignore backend\.env
```

后两条命令应输出对应文件路径，表示真实环境变量不会被提交。

## 7. v0.4.0 主要新增文件

### 前端

- `frontend/components/data/stage-two-data.tsx`
- `frontend/components/agent/analysis-agent.tsx`
- `frontend/services/api.ts`
- `frontend/types/api.ts`
- `frontend/app/page.tsx`
- `frontend/app/globals.css`

### 后端

- `backend/app/models/` 中 6 个关系模型
- `backend/app/database/session.py`
- `backend/app/database/seed.py`
- `backend/app/database/init_db.py`
- `backend/app/api/routes/clubs.py`
- `backend/app/api/routes/standings.py`
- `backend/app/api/routes/agent.py`
- `backend/app/services/analysis_agent.py`
- `backend/app/services/qwen_service.py`
- `backend/app/schemas/agent.py`
- `backend/app/schemas/club.py`
- `backend/app/schemas/standing.py`
- `backend/migrations/`
- `backend/tests/test_data_api.py`
- `backend/tests/test_agent_api.py`
- `backend/tests/test_qwen_service.py`
- `docs/QWEN_INTEGRATION.md`

数据库文件 `backend/pl_geo_analytics.db` 是本地生成文件，已被 `.gitignore`
排除，不应上传 GitHub。样例数据由幂等初始化脚本写入，说明见
`data/SAMPLE_DATA.md`。

## 8. Git 分支建议

对个人项目，不建议永久保留很多已经合并的分支。清晰度主要来自提交记录、Pull Request 和版本标签。

推荐：

```text
main                         始终可运行
chore/stage-01-init          已完成的初始化工作
feat/stage-02-data-api       数据库、测试数据和基础 API
feat/stage-03-agent-mvp      足球分析 Agent MVP
feat/stage-04-qwen-integration 千问增强回答与安全回退
feat/stage-05-england-map    英格兰交互地图
feat/stage-06-full-league    完整 20 队和最终积分榜
feat/stage-07-player-stats   球员数据
feat/stage-08-radar          雷达图
feat/stage-09-match-analysis 示例比赛
chore/stage-10-polish        测试、文档和适配
```

如果 Agent MVP 已在 `main`，千问接入阶段的操作：

```powershell
git switch -c feat/stage-04-qwen-integration
git add .
git status
git commit -m "feat: add grounded Qwen response layer"
git switch main
git merge --no-ff feat/stage-04-qwen-integration
git tag v0.4.0
```

如果当前修改已经直接发生在 `main`，也可以直接提交，不需要为了形式重新复制分支。

## 9. Qwen 接入提交信息

推荐唯一主提交：

```text
feat: add grounded Qwen response layer
```

如果希望拆成两个更清楚的提交：

```text
feat: add Qwen configuration and grounded response service
feat: show hybrid Agent mode and safe fallback status
```

提交前一定先运行前端构建、后端测试和 `git status`，确认没有 `.env`、数据库文件或 `node_modules`。
