import Link from "next/link";

import { AnalysisAgent } from "../components/agent/analysis-agent";
import { StageTwoData } from "../components/data/stage-two-data";
import { EnglandClubMap } from "../components/map/england-club-map";
import { BackendStatus } from "../components/system/backend-status";

const futureModules = [
  {
    phase: "阶段 6",
    title: "球员雷达图",
    description: "按位置计算同位置百分位，更直观地比较球员能力结构。",
  },
  {
    phase: "阶段 7",
    title: "比赛空间分析",
    description: "用来源明确的事件数据展示射门位置、时间线与比赛走势。",
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
          <Link className="brand" href="/" aria-label="英超智析 Agent 首页">
            <span className="brand-mark" aria-hidden="true">
              AI
            </span>
            <span>
              <strong>英超智析 Agent</strong>
              <small>Premier League Insight Agent</small>
            </span>
          </Link>
          <span className="phase-badge">
            v0.5.0 · Stadium Explorer
          </span>
        </header>

        <section className="hero" aria-labelledby="hero-title">
          <div className="hero-copy">
            <p className="eyebrow">
              Premier League · Geography · Data · Agent
            </p>
            <h1 id="hero-title">
              先从主场出发，
              <span>再让数据回答。</span>
            </h1>
            <p className="hero-description">
              在英格兰地图上探索球队与球场，再让英超智析 Agent
              自动查询球员数据、换算每90分钟指标，并基于可追溯证据组织回答。
            </p>
            <div className="hero-actions">
              <a className="primary-button" href="#club-map">
                探索英格兰球场
              </a>
              <a className="secondary-button" href="#analysis-agent">
                体验分析 Agent
              </a>
            </div>
          </div>

          <BackendStatus />
        </section>

        <EnglandClubMap />

        <AnalysisAgent />

        <StageTwoData />

        <section className="module-section" id="roadmap" aria-labelledby="roadmap-title">
          <div className="section-heading">
            <div>
              <p className="eyebrow">BUILD ROADMAP</p>
              <h2 id="roadmap-title">接下来做什么</h2>
            </div>
            <p>地图探索路径已经打通，下一步继续补齐可视化与真实比赛数据。</p>
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
