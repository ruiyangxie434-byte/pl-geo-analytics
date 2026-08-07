# Scripts

可重复执行的数据下载、清洗与更新脚本放在这里。当前数据库初始化入口位于
`backend/app/database/init_db.py`，在 `backend/` 运行
`python -m app.database.init_db` 即可。后续外部数据脚本应从环境变量读取配置，并记录数据来源与更新时间。

## 生成 Match Lab 快照

`build_match_snapshot.py` 读取 StatsBomb Open Data 的比赛与事件 JSON，筛选 Match ID `3749448`，验证 28 次射门，归一化坐标，并生成 API 使用的紧凑快照。

```powershell
python .\scripts\build_match_snapshot.py
```

应用启动时不会下载远程事件数据。来源、许可、字段与解释边界见 [`docs/MATCH_LAB.md`](../docs/MATCH_LAB.md)。
