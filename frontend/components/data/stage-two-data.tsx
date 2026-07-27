"use client";

import { useEffect, useMemo, useState } from "react";
import type { CSSProperties } from "react";

import { getClubs, getStandings } from "../../services/api";
import type { ClubListData, StandingTableData } from "../../types/api";

type DataState = "loading" | "success" | "error";

function getClubInitials(name: string) {
  return name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 3)
    .toUpperCase();
}

export function StageTwoData() {
  const [state, setState] = useState<DataState>("loading");
  const [clubs, setClubs] = useState<ClubListData | null>(null);
  const [standings, setStandings] = useState<StandingTableData | null>(null);
  const [selectedSlug, setSelectedSlug] = useState<string | null>(null);
  const [requestId, setRequestId] = useState(0);

  useEffect(() => {
    const controller = new AbortController();

    async function loadData() {
      setState("loading");

      try {
        const [clubResponse, standingResponse] = await Promise.all([
          getClubs(controller.signal),
          getStandings("2024-25", controller.signal),
        ]);

        if (!clubResponse.data || !standingResponse.data) {
          throw new Error("接口未返回数据");
        }

        setClubs(clubResponse.data);
        setStandings(standingResponse.data);
        setSelectedSlug(
          (current) =>
            current ?? standingResponse.data?.items[0]?.club.slug ?? null,
        );
        setState("success");
      } catch {
        if (!controller.signal.aborted) {
          setState("error");
        }
      }
    }

    void loadData();
    return () => controller.abort();
  }, [requestId]);

  const selectedClub = useMemo(
    () => clubs?.items.find((club) => club.slug === selectedSlug) ?? null,
    [clubs, selectedSlug],
  );

  return (
    <section
      className="data-section"
      id="data-preview"
      aria-labelledby="data-title"
    >
      <div className="section-heading data-heading">
        <div>
          <p className="eyebrow">DATABASE CONNECTED</p>
          <h2 id="data-title">阶段 2 数据层</h2>
        </div>
        <p>
          球队、球员与积分榜已经由 FastAPI 从 SQLite
          读取，前端不再硬编码业务数据。
        </p>
      </div>

      {state === "loading" && (
        <div className="data-loading" aria-live="polite">
          <span className="loading-ring" aria-hidden="true" />
          <div>
            <strong>正在读取球队数据库</strong>
            <p>同时请求球队列表和 2024-25 积分榜样例。</p>
          </div>
        </div>
      )}

      {state === "error" && (
        <div className="data-error" role="alert">
          <div>
            <span>DATA OFFLINE</span>
            <h3>暂时没有读到阶段 2 数据</h3>
            <p>请确认后端终端仍在运行，然后点击重新连接。</p>
          </div>
          <button
            className="secondary-button"
            type="button"
            onClick={() => setRequestId((value) => value + 1)}
          >
            重新连接
          </button>
        </div>
      )}

      {state === "success" && clubs && standings && (
        <>
          <div className="data-metrics" aria-label="阶段 2 数据概况">
            <div>
              <span>SCHEMA</span>
              <strong>6</strong>
              <small>张关系表</small>
            </div>
            <div>
              <span>CLUBS</span>
              <strong>{clubs.total}</strong>
              <small>支样例球队</small>
            </div>
            <div>
              <span>PLAYERS</span>
              <strong>{clubs.player_total}</strong>
              <small>名样例球员</small>
            </div>
            <div>
              <span>SEASON</span>
              <strong>{standings.season}</strong>
              <small>积分榜切片</small>
            </div>
          </div>

          <div className="data-layout">
            <article className="clubs-panel">
              <div className="panel-title">
                <div>
                  <span>01</span>
                  <h3>球场坐标样例</h3>
                </div>
                <small>选择球队查看地点</small>
              </div>

              <div className="club-list">
                {clubs.items.map((club) => (
                  <button
                    className="club-card"
                    data-selected={club.slug === selectedSlug}
                    key={club.slug}
                    onClick={() => setSelectedSlug(club.slug)}
                    style={
                      {
                        "--club-color": club.primary_color,
                      } as CSSProperties
                    }
                    type="button"
                    aria-pressed={club.slug === selectedSlug}
                  >
                    <span className="club-monogram" aria-hidden="true">
                      {getClubInitials(club.short_name)}
                    </span>
                    <span className="club-card-copy">
                      <strong>{club.short_name}</strong>
                      <small>
                        {club.city} · {club.stadium.name}
                      </small>
                    </span>
                    <span className="club-arrow" aria-hidden="true">
                      ↗
                    </span>
                  </button>
                ))}
              </div>

              {selectedClub && (
                <div className="coordinate-readout" aria-live="polite">
                  <div>
                    <span>SELECTED GROUND</span>
                    <strong>{selectedClub.stadium.name}</strong>
                    <small>
                      {selectedClub.city} · 建队于{" "}
                      {selectedClub.founded_year ?? "未知"} 年
                    </small>
                  </div>
                  <code>
                    {selectedClub.stadium.latitude.toFixed(4)},{" "}
                    {selectedClub.stadium.longitude.toFixed(4)}
                  </code>
                </div>
              )}
            </article>

            <article className="standings-panel">
              <div className="panel-title">
                <div>
                  <span>02</span>
                  <h3>{standings.season} 积分榜</h3>
                </div>
                <small>{standings.total} 队样例切片</small>
              </div>

              <div className="table-scroll">
                <table>
                  <thead>
                    <tr>
                      <th scope="col">排名</th>
                      <th scope="col">球队</th>
                      <th scope="col">赛</th>
                      <th scope="col">胜</th>
                      <th scope="col">平</th>
                      <th scope="col">负</th>
                      <th scope="col">净胜</th>
                      <th scope="col">积分</th>
                    </tr>
                  </thead>
                  <tbody>
                    {standings.items.map((item) => (
                      <tr
                        data-selected={item.club.slug === selectedSlug}
                        key={item.club.slug}
                      >
                        <td className="rank-cell">{item.position}</td>
                        <td>
                          <button
                            className="table-club-button"
                            type="button"
                            onClick={() => setSelectedSlug(item.club.slug)}
                          >
                            <span
                              aria-hidden="true"
                              style={{ background: item.club.primary_color }}
                            />
                            {item.club.short_name}
                          </button>
                        </td>
                        <td>{item.played}</td>
                        <td>{item.won}</td>
                        <td>{item.drawn}</td>
                        <td>{item.lost}</td>
                        <td>
                          {item.goal_difference > 0 ? "+" : ""}
                          {item.goal_difference}
                        </td>
                        <td className="points-cell">{item.points}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <p className="sample-notice">
                <span aria-hidden="true">i</span>
                {standings.sample_notice}
              </p>
            </article>
          </div>
        </>
      )}
    </section>
  );
}
