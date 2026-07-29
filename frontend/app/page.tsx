import Link from "next/link";

import { AnalysisAgent } from "../components/agent/analysis-agent";
import { StageTwoData } from "../components/data/stage-two-data";
import { BackendStatus } from "../components/system/backend-status";

const futureModules = [
  {
    phase: "阶段 3B",
    title: "英格兰地图",
    description: "从球场地理位置进入每一支英超球队的故事。",
  },
  {
    phase: "竞赛冲刺 3",
    title: "真实工具调用",
    description: "让千问自主选择球员查询、指标计算和对比工具。",
  },
  {
    phase: "竞赛冲刺 4",
    title: "记忆与报告",
    description: "保存战术偏好、支持连续追问，并导出球探分析报告。",
  },
];

export default function Home() {
  return (
    <main>
      <div className="page-shell">
        <header className="site-header">
          <Link className="brand" href="/" aria-label="Premier League Insight Agent 首页">
            <span className="brand-mark" aria-hidden="true">
              PL
            </span>
            <span>
              <strong>Premier League Insight Agent</strong>
              <small>英超地理探索与球员数据分析平台</small>
            </span>
          </Link>
          <span className="phase-badge">
            v0.4.0 · Qwen-ready Hybrid Agent
          </span>
        </header>

        <section className="hero" aria-labelledby="hero-title">
          <div className="hero-copy">
            <p className="eyebrow">Premier League · Geography · Data</p>
            <h1 id="hero-title">
              把足球问题交给
              <span>会调用数据的 Agent。</span>
            </h1>
            <p className="hero-description">
              PitchMind 会理解分析目标，自动查询球员数据、换算每90分钟指标、
              比较样例百分位，并让千问基于可追溯证据组织回答。
            </p>
            <div className="hero-actions">
              <a className="primary-button" href="#analysis-agent">
                体验分析 Agent
              </a>
              <a className="secondary-button" href="#data-preview">
                查看数据底座
              </a>
            </div>
          </div>

          <BackendStatus />
        </section>

        <AnalysisAgent />

        <StageTwoData />

        <section className="module-section" id="roadmap" aria-labelledby="roadmap-title">
          <div className="section-heading">
            <div>
              <p className="eyebrow">BUILD ROADMAP</p>
              <h2 id="roadmap-title">接下来做什么</h2>
            </div>
            <p>优先完成参赛所需的 Agent 闭环，再继续推进地图与完整数据。</p>
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
