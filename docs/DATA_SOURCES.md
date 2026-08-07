# 数据来源与口径

## 2024-25 最终积分榜

- 范围：2024-25 英超 20 支球队、38 轮最终排名。
- 快照日期：2025-05-25。
- 字段：排名、场次、胜、平、负、进球、失球、净胜球、积分。
- 来源：[Premier League official table](https://www.premierleague.com/en/tables/premier-league/2024-25/all-matchweeks)。
- 数据性质：静态历史快照，不是当前赛季实时积分榜。

后端会在 `/api/standings` 响应中返回来源名称、来源 URL、快照日期和是否完整，前端同时展示这些边界。

## 球队与球场

- 球队范围与赛季保持一致，共 20 支。
- 球场名称和所在城市按 2024-25 赛季口径整理。
- 经纬度用于地图定位，是地理参考值，不用于测绘或精确导航。
- 地图瓦片和地理署名遵循 [OpenStreetMap Copyright and License](https://www.openstreetmap.org/copyright)。

## 球员与分析指标

- 当前仅包含 12 名球员样例，用于验证数据库关系、每 90 分钟换算、证据排序和 Agent 回答链路。
- 样例球员数据会以 `source_kind = sample` 标记。
- 页面不会把这些样例描述为当前实时阵容或官方实时统计。
- 球员中心默认只纳入赛季出场不少于 450 分钟的样例，并可切换为 1800 或 2700 分钟门槛。
- 雷达百分位优先在同位置合格样例中计算；同位置少于 3 人时回退到全部合格样例，并在 API 与页面中明示比较范围。
- 每 90 分钟指标与百分位口径详见 [`PLAYER_LAB.md`](PLAYER_LAB.md)。

## 历史比赛事件

- 当前比赛快照：2003/2004 Premier League，Arsenal 4–2 Liverpool，2004-04-09。
- 来源：[StatsBomb Open Data](https://github.com/hudl/open-data)，Match ID `3749448`。
- 范围：28 次 `Shot` 事件，包括时间、球员、球队、结果、位置、xG、身体部位与进攻方式。
- 坐标：从 StatsBomb `120 × 80` 线性归一化到数据库的 `0–100 × 0–100`。
- 许可：使用和再发布前阅读上游 [`LICENSE.pdf`](https://github.com/hudl/open-data/blob/master/LICENSE.pdf)，页面与 API 保留 StatsBomb 署名。
- 详细清洗步骤、公式和边界见 [`MATCH_LAB.md`](MATCH_LAB.md)。

这场历史比赛不会与 2024-25 球员样例合并计算，也不代表当前球队状态。

## 更新原则

1. 历史快照保持赛季和日期不变，不静默替换为当前赛季数据。
2. 引入新赛季时使用新的赛季标识，并保留来源 URL 与更新时间。
3. 导入真实比赛事件或球员统计前，先记录许可、字段口径和清洗步骤。
4. 无法确认来源或更新时间的数据不进入正式分析结论。
5. 事件数据只提交经过字段筛选的可复现快照，不把大体积原始文件直接纳入仓库。
