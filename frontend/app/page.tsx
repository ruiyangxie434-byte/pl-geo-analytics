import Link from "next/link";

import { AnalysisAgent } from "../components/agent/analysis-agent";
import { StageTwoData } from "../components/data/stage-two-data";
import { EnglandClubMap } from "../components/map/england-club-map";
import { BackendStatus } from "../components/system/backend-status";

const futureModules = [
  {
    phase: "v0.9 已上线",
    title: "Agent 分析笔记本",
    description: "分析记录、上下文追问、历史恢复与打印版球探报告已经打通。",
  },
  {
    phase: "阶段 8",
    title: "作品展示完善",
    description: "补齐关键页面截图、接口清单、部署说明和移动端细节。",
  },
  {
    phase: "v1.0 目标",
    title: "在线演示发布",
    description: "完成安全部署、最终回归测试和首个可公开访问版本。",
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
            v0.9.0 · Agent Notebook
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
              查询球员数据、换算每90分钟指标，并用真实比赛事件还原射门与进球过程。
            </p>
            <div className="hero-actions">
              <a className="primary-button" href="#club-map">
                探索英格兰球场
              </a>
              <Link className="secondary-button" href="/players">
                打开球员实验室
              </Link>
              <Link className="secondary-button" href="/matches">
                打开比赛实验室
              </Link>
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
            <p>地图、球员、比赛与可追问 Agent 报告链路已经打通，下一步面向 v1.0 完善发布质量。</p>
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
