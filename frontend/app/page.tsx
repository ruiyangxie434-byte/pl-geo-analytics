import Link from "next/link";

import { StageTwoData } from "../components/data/stage-two-data";
import { BackendStatus } from "../components/system/backend-status";

const futureModules = [
  {
    phase: "阶段 3",
    title: "英格兰地图",
    description: "从球场地理位置进入每一支英超球队的故事。",
  },
  {
    phase: "阶段 4",
    title: "球队详情",
    description: "阵容、赛季概况、近期赛果与可排序完整积分榜。",
  },
  {
    phase: "阶段 5–7",
    title: "球员与比赛分析",
    description: "每 90 分钟指标、球员雷达对比与示例比赛射门图。",
  },
];

export default function Home() {
  return (
    <main>
      <div className="page-shell">
        <header className="site-header">
          <Link className="brand" href="/" aria-label="PL Geo Analytics 首页">
            <span className="brand-mark" aria-hidden="true">
              PL
            </span>
            <span>
              <strong>PL Geo Analytics</strong>
              <small>英超地理探索与球员数据分析平台</small>
            </span>
          </Link>
          <span className="phase-badge">v0.2.0 · 阶段 2</span>
        </header>

        <section className="hero" aria-labelledby="hero-title">
          <div className="hero-copy">
            <p className="eyebrow">Premier League · Geography · Data</p>
            <h1 id="hero-title">
              从英格兰地图出发，
              <span>读懂球场上的数据。</span>
            </h1>
            <p className="hero-description">
              现在项目已经拥有可迁移的 SQLite 数据层、球队与球员模型，以及从
              FastAPI 实时读取的积分榜样例。下一步将把球场坐标放到英格兰地图上。
            </p>
            <div className="hero-actions">
              <a className="primary-button" href="#data-preview">
                查看阶段 2 数据
              </a>
              <a
                className="secondary-button"
                href="http://127.0.0.1:8000/docs"
                target="_blank"
                rel="noreferrer"
              >
                打开 API 文档
              </a>
            </div>
          </div>

          <BackendStatus />
        </section>

        <StageTwoData />

        <section className="module-section" id="roadmap" aria-labelledby="roadmap-title">
          <div className="section-heading">
            <div>
              <p className="eyebrow">BUILD ROADMAP</p>
              <h2 id="roadmap-title">接下来做什么</h2>
            </div>
            <p>阶段 2 已完成，后续界面全部复用这一套数据库与 API。</p>
          </div>

          <div className="module-grid">
            {futureModules.map((module) => (
              <article className="module-card" key={module.phase}>
                <span>{module.phase}</span>
                <h3>{module.title}</h3>
                <p>{module.description}</p>
              </article>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
