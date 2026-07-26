# Scripts

可重复执行的数据下载、清洗与更新脚本放在这里。当前数据库初始化入口位于
`backend/app/database/init_db.py`，在 `backend/` 运行
`python -m app.database.init_db` 即可。后续外部数据脚本应从环境变量读取配置，并记录数据来源与更新时间。
