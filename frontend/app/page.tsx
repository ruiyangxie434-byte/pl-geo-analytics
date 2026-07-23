import Link from "next/link";

import { BackendStatus } from "../components/system/backend-status";

const futureModules = [
  {
    phase: "阶段 2",
    title: "数据与数据库",
    description: "球队、球员、积分榜及比赛事件的可追溯数据层。",
  },
  {
    phase: "阶段 3",
    title: "英格兰地图",
    description: "从球场地理位置进入每一支英超球队的故事。",
  },
  {
    phase: "阶段 5–7",
    title: "足球数据分析",
    description: "每 90 分钟指标、球员雷达对比和示例比赛射门图。",
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
          <span className="phase-badge">v0.1.0 · 阶段 1</span>
        </header>

        <section className="hero" aria-labelledby="hero-title">
          <div className="hero-copy">
            <p className="eyebrow">Premier League · Geography · Data</p>
            <h1 id="hero-title">
              从英格兰地图出发，
              <span>读懂球场上的数据。</span>
            </h1>
            <p className="hero-description">
              第一阶段已建立可运行的 Next.js 与 FastAPI
              骨架。真实球队、球员和比赛数据将在后续阶段逐步接入，当前页面不使用伪造业务数据。
            </p>
            <div className="hero-actions">
              <a
                className="primary-button"
                href="http://127.0.0.1:8000/docs"
                target="_blank"
                rel="noreferrer"
              >
                打开 API 文档
              </a>
              <a className="secondary-button" href="#roadmap">
                查看下一步
              </a>
            </div>
          </div>

          <BackendStatus />
        </section>

        <section className="module-section" id="roadmap" aria-labelledby="roadmap-title">
          <div className="section-heading">
            <div>
              <p className="eyebrow">BUILD ROADMAP</p>
              <h2 id="roadmap-title">第一版核心模块</h2>
            </div>
            <p>先确保每一层可运行，再逐步增加真实数据和交互。</p>
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
