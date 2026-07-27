"use client";

import { useEffect, useMemo, useState } from "react";
import type { CSSProperties, FormEvent } from "react";

import { getAgentPlayers, runAgentAnalysis } from "../../services/api";
import type {
  AgentAnalysisData,
  AgentFocus,
  AgentPlayerOption,
} from "../../types/api";

const FOCUS_OPTIONS: {
  value: AgentFocus;
  label: string;
  description: string;
}[] = [
  {
    value: "balanced",
    label: "综合",
    description: "攻防指标均衡",
  },
  {
    value: "scoring",
    label: "终结",
    description: "进球、xG与射门",
  },
  {
    value: "creativity",
    label: "创造",
    description: "助攻与关键传球",
  },
  {
    value: "pressing",
    label: "逼抢",
    description: "抢断与拦截优先",
  },
];

export function AnalysisAgent() {
  const [players, setPlayers] = useState<AgentPlayerOption[]>([]);
  const [firstSlug, setFirstSlug] = useState("bukayo-saka");
  const [secondSlug, setSecondSlug] = useState("cole-palmer");
  const [focus, setFocus] = useState<AgentFocus>("pressing");
  const [question, setQuestion] = useState(
    "萨卡和帕尔默，谁更适合高位逼抢体系？请给出数据依据。",
  );
  const [isLoadingPlayers, setIsLoadingPlayers] = useState(true);
  const [isRunning, setIsRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AgentAnalysisData | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    async function loadPlayers() {
      try {
        const response = await getAgentPlayers("2024-25", controller.signal);
        if (!response.data) {
          throw new Error("接口未返回球员数据");
        }
        setPlayers(response.data.items);
      } catch {
        if (!controller.signal.aborted) {
          setError("没有读取到可分析球员，请确认后端仍在运行。");
        }
      } finally {
        if (!controller.signal.aborted) {
          setIsLoadingPlayers(false);
        }
      }
    }

    void loadPlayers();
    return () => controller.abort();
  }, []);

  const playerMap = useMemo(
    () => new Map(players.map((player) => [player.slug, player])),
    [players],
  );

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (firstSlug === secondSlug) {
      setError("请选择两名不同的球员。");
      return;
    }

    setError(null);
    setIsRunning(true);
    try {
      const response = await runAgentAnalysis({
        question,
        player_slugs: [firstSlug, secondSlug],
        season: "2024-25",
        focus,
      });
      if (!response.data) {
        throw new Error("Agent 没有返回分析结果");
      }
      setResult(response.data);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Agent 暂时无法完成分析，请稍后重试。",
      );
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <section className="agent-section" id="analysis-agent" aria-labelledby="agent-title">
      <div className="section-heading agent-heading">
        <div>
          <p className="eyebrow">PITCHMIND · AGENT MVP</p>
          <h2 id="agent-title">足球分析与球探决策 Agent</h2>
        </div>
        <p>
          不是普通聊天框。Agent 会拆解任务、调用数据库工具、统一指标口径，
          再用可追溯证据生成建议。
        </p>
      </div>

      <div className="agent-workspace">
        <form className="agent-console" onSubmit={handleSubmit}>
          <div className="console-header">
            <div>
              <span className="live-dot" aria-hidden="true" />
              <strong>新建分析任务</strong>
            </div>
            <span>LOCAL RULE AGENT · v0.3</span>
          </div>

          <div className="console-body">
            <div className="field-group">
              <div className="field-label">
                <label htmlFor="first-player">选择分析对象</label>
                <span>2 PLAYERS</span>
              </div>
              <div className="player-select-grid">
                <div className="select-shell">
                  <small>球员 A</small>
                  <select
                    id="first-player"
                    value={firstSlug}
                    onChange={(event) => setFirstSlug(event.target.value)}
                    disabled={isLoadingPlayers || isRunning}
                  >
                    {players.map((player) => (
                      <option value={player.slug} key={player.slug}>
                        {player.full_name} · {player.club_name}
                      </option>
                    ))}
                  </select>
                </div>
                <span className="versus-mark" aria-hidden="true">
                  VS
                </span>
                <div className="select-shell">
                  <small>球员 B</small>
                  <select
                    id="second-player"
                    value={secondSlug}
                    onChange={(event) => setSecondSlug(event.target.value)}
                    disabled={isLoadingPlayers || isRunning}
                  >
                    {players.map((player) => (
                      <option value={player.slug} key={player.slug}>
                        {player.full_name} · {player.club_name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            <fieldset className="field-group focus-fieldset">
              <legend>分析重点</legend>
              <div className="focus-grid">
                {FOCUS_OPTIONS.map((option) => (
                  <label
                    className="focus-option"
                    data-selected={focus === option.value}
                    key={option.value}
                  >
                    <input
                      type="radio"
                      name="focus"
                      value={option.value}
                      checked={focus === option.value}
                      onChange={() => setFocus(option.value)}
                      disabled={isRunning}
                    />
                    <strong>{option.label}</strong>
                    <small>{option.description}</small>
                  </label>
                ))}
              </div>
            </fieldset>

            <div className="field-group">
              <div className="field-label">
                <label htmlFor="agent-question">任务描述</label>
                <span>{question.length}/500</span>
              </div>
              <textarea
                id="agent-question"
                value={question}
                maxLength={500}
                rows={4}
                onChange={(event) => setQuestion(event.target.value)}
                disabled={isRunning}
              />
            </div>

            {error && (
              <p className="agent-error" role="alert">
                {error}
              </p>
            )}

            <button
              className="agent-run-button"
              type="submit"
              disabled={isLoadingPlayers || isRunning || question.length < 6}
            >
              {isRunning ? (
                <>
                  <span className="loading-ring" aria-hidden="true" />
                  Agent 正在调用分析工具
                </>
              ) : (
                <>
                  <span aria-hidden="true">▶</span>
                  启动 Agent 分析
                </>
              )}
            </button>
            <p className="console-notice">
              本阶段使用可解释的本地规则引擎，无需外部 API 密钥；所有结论均来自
              样例数据库。
            </p>
          </div>
        </form>

        <div className="agent-output" aria-live="polite">
          {!result && (
            <div className="agent-empty">
              <div className="agent-orbit" aria-hidden="true">
                <span>PM</span>
              </div>
              <p className="eyebrow">WAITING FOR TASK</p>
              <h3>把一个足球问题交给 Agent</h3>
              <p>
                运行后，这里会展示任务规划、工具调用、对比指标、证据链和最终建议。
              </p>
              <ol>
                <li>理解分析意图</li>
                <li>读取数据库记录</li>
                <li>计算每90分钟指标</li>
                <li>输出有依据的决策</li>
              </ol>
            </div>
          )}

          {result && (
            <div className="agent-result">
              <div className="result-topbar">
                <span>
                  <i aria-hidden="true" />
                  TASK COMPLETED
                </span>
                <code>{result.run_id}</code>
              </div>

              <article className="recommendation-card">
                <span>AGENT RECOMMENDATION</span>
                <h3>{result.recommendation.headline}</h3>
                <p>{result.recommendation.summary}</p>
                <div className="score-row">
                  {result.players.map((player) => (
                    <div key={player.slug}>
                      <span
                        className="player-color"
                        style={
                          {
                            "--result-player-color": player.club_color,
                          } as CSSProperties
                        }
                      />
                      <div>
                        <small>{player.full_name}</small>
                        <strong>
                          {result.recommendation.scores[player.slug]}
                        </strong>
                      </div>
                    </div>
                  ))}
                  <div className="confidence-chip">
                    <small>置信度</small>
                    <strong>
                      {Math.round(result.recommendation.confidence * 100)}%
                    </strong>
                  </div>
                </div>
              </article>

              <div className="result-block">
                <div className="result-block-title">
                  <span>01</span>
                  <h4>Agent 执行轨迹</h4>
                </div>
                <div className="agent-trace">
                  {result.steps.map((step) => (
                    <div className="trace-step" key={step.index}>
                      <span>{step.index}</span>
                      <div>
                        <strong>{step.title}</strong>
                        <code>{step.tool}</code>
                        <p>{step.detail}</p>
                      </div>
                      <i aria-label="已完成">✓</i>
                    </div>
                  ))}
                </div>
              </div>

              <div className="result-block">
                <div className="result-block-title">
                  <span>02</span>
                  <h4>{result.focus_label}指标</h4>
                </div>
                <div className="metric-grid">
                  {result.metrics.map((metric) => (
                    <article className="metric-card" key={metric.key}>
                      <div>
                        <strong>{metric.label}</strong>
                        <small>权重 {Math.round(metric.weight * 100)}%</small>
                      </div>
                      {metric.values.map((value) => {
                        const player = playerMap.get(value.player_slug);
                        return (
                          <div className="metric-player" key={value.player_slug}>
                            <span>{player?.full_name ?? value.player_slug}</span>
                            <strong>{value.value.toFixed(2)}</strong>
                            <div
                              className="metric-bar"
                              title={`样例百分位 ${value.percentile}`}
                            >
                              <i
                                style={{
                                  width: `${value.percentile}%`,
                                  background:
                                    player?.club_color ?? "var(--accent)",
                                }}
                              />
                            </div>
                            <small>P{value.percentile}</small>
                          </div>
                        );
                      })}
                    </article>
                  ))}
                </div>
              </div>

              <div className="result-block">
                <div className="result-block-title">
                  <span>03</span>
                  <h4>关键证据</h4>
                </div>
                <div className="evidence-list">
                  {result.evidence.map((item) => (
                    <article key={item.title}>
                      <strong>{item.title}</strong>
                      <p>{item.detail}</p>
                    </article>
                  ))}
                </div>
              </div>

              <div className="limitations">
                <strong>结论边界</strong>
                <ul>
                  {result.limitations.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
                <p>{result.sample_notice}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
