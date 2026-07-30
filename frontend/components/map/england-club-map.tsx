"use client";

import dynamic from "next/dynamic";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import type { CSSProperties } from "react";

import { getClubs } from "../../services/api";
import type { ClubListData, ClubSummary } from "../../types/api";

type MapDataState = "loading" | "success" | "error";

const LeafletClubMap = dynamic(
  () =>
    import("./leaflet-club-map").then((module) => module.LeafletClubMap),
  {
    ssr: false,
    loading: () => (
      <div className="map-canvas-loading" aria-live="polite">
        <span className="loading-ring" aria-hidden="true" />
        <p>正在载入英格兰地图…</p>
      </div>
    ),
  },
);

function getClubInitials(name: string) {
  return name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 3)
    .toUpperCase();
}

function SelectedClubCard({ club }: { club: ClubSummary }) {
  return (
    <article
      className="map-selected-card"
      style={
        {
          "--club-color": club.primary_color,
        } as CSSProperties
      }
    >
      <div className="selected-club-heading">
        <span className="selected-club-monogram" aria-hidden="true">
          {getClubInitials(club.short_name)}
        </span>
        <div>
          <small>SELECTED CLUB</small>
          <h3>{club.name}</h3>
        </div>
      </div>

      <dl className="selected-club-facts">
        <div>
          <dt>主场</dt>
          <dd>{club.stadium.name}</dd>
        </div>
        <div>
          <dt>城市</dt>
          <dd>{club.city}</dd>
        </div>
        <div>
          <dt>建队</dt>
          <dd>{club.founded_year ?? "未知"}</dd>
        </div>
      </dl>

      <Link className="map-detail-link" href={`/clubs/${club.slug}`}>
        查看球队资料
        <span aria-hidden="true">↗</span>
      </Link>
    </article>
  );
}

export function EnglandClubMap() {
  const [state, setState] = useState<MapDataState>("loading");
  const [clubs, setClubs] = useState<ClubListData | null>(null);
  const [selectedSlug, setSelectedSlug] = useState<string | null>(null);
  const [clubQuery, setClubQuery] = useState("");
  const [requestId, setRequestId] = useState(0);

  useEffect(() => {
    const controller = new AbortController();

    async function loadClubs() {
      setState("loading");

      try {
        const response = await getClubs(controller.signal);
        if (!response.data || response.data.items.length === 0) {
          throw new Error("球队坐标为空");
        }

        setClubs(response.data);
        setSelectedSlug(
          (current) => current ?? response.data?.items[0]?.slug ?? null,
        );
        setState("success");
      } catch {
        if (!controller.signal.aborted) {
          setState("error");
        }
      }
    }

    void loadClubs();
    return () => controller.abort();
  }, [requestId]);

  const selectedClub = useMemo(
    () =>
      clubs?.items.find((club) => club.slug === selectedSlug) ??
      clubs?.items[0] ??
      null,
    [clubs, selectedSlug],
  );

  const cityTotal = useMemo(
    () => new Set(clubs?.items.map((club) => club.city) ?? []).size,
    [clubs],
  );

  const filteredClubs = useMemo(() => {
    const query = clubQuery.trim().toLocaleLowerCase();
    if (!query) {
      return clubs?.items ?? [];
    }

    return (
      clubs?.items.filter((club) =>
        [club.name, club.short_name, club.city, club.stadium.name].some(
          (value) => value.toLocaleLowerCase().includes(query),
        ),
      ) ?? []
    );
  }, [clubQuery, clubs]);

  return (
    <section
      className="map-section"
      id="club-map"
      aria-labelledby="club-map-title"
    >
      <div className="section-heading map-heading">
        <div>
          <p className="eyebrow">20-CLUB STADIUM EXPLORER</p>
          <h2 id="club-map-title">一张地图探索完整联赛</h2>
        </div>
        <p>
          2024-25 赛季 20 支球队全部接入。点击标记或搜索球队，即可定位城市并进入资料页。
        </p>
      </div>

      {state === "loading" && (
        <div className="map-state-card" aria-live="polite">
          <span className="loading-ring" aria-hidden="true" />
          <div>
            <strong>正在读取球场坐标</strong>
            <p>连接球队 API，并准备地图标记。</p>
          </div>
        </div>
      )}

      {state === "error" && (
        <div className="map-state-card map-state-error" role="alert">
          <div>
            <span>MAP DATA OFFLINE</span>
            <strong>暂时没有读到球队坐标</strong>
            <p>请确认 FastAPI 后端仍在运行，然后重新连接。</p>
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

      {state === "success" && clubs && selectedClub && (
        <>
          <div className="map-metrics" aria-label="球场探索数据概况">
            <div>
              <span>CLUBS</span>
              <strong>{clubs.total}</strong>
              <small>支赛季球队</small>
            </div>
            <div>
              <span>CITIES</span>
              <strong>{cityTotal}</strong>
              <small>座主场城市</small>
            </div>
            <div>
              <span>SEASON</span>
              <strong>{clubs.season}</strong>
              <small>历史赛季快照</small>
            </div>
          </div>

          <div className="map-explorer">
            <div className="map-canvas-shell">
              <div className="map-toolbar">
                <div>
                  <span className="map-live-dot" aria-hidden="true" />
                  <strong>ENGLAND · 2024/25 CLUB GROUNDS</strong>
                </div>
                <small>滚轮缩放已关闭 · 使用 +/- 控制</small>
              </div>

              <div
                className="map-canvas"
                aria-label="英格兰 2024-25 赛季 20 支球队球场交互地图"
              >
                <LeafletClubMap
                  clubs={clubs.items}
                  selectedSlug={selectedClub.slug}
                  onSelectClub={setSelectedSlug}
                />
              </div>

              <div className="map-legend">
                <span>
                  <i aria-hidden="true" />
                  球场标记
                </span>
                <small>地图 © OpenStreetMap contributors</small>
              </div>
            </div>

            <aside className="map-sidebar" aria-label="地图球队列表">
              <SelectedClubCard club={selectedClub} />

              <div className="map-club-list">
                <div className="map-list-heading">
                  <strong>球队坐标</strong>
                  <span>
                    {filteredClubs.length.toString().padStart(2, "0")} /{" "}
                    {clubs.total.toString().padStart(2, "0")}
                  </span>
                </div>

                <div className="map-club-search">
                  <span aria-hidden="true">⌕</span>
                  <input
                    aria-label="在地图列表中搜索球队、城市或球场"
                    onChange={(event) => setClubQuery(event.target.value)}
                    placeholder="搜索球队、城市或球场"
                    type="search"
                    value={clubQuery}
                  />
                </div>

                {filteredClubs.map((club) => (
                  <button
                    className="map-club-button"
                    data-selected={club.slug === selectedClub.slug}
                    key={club.slug}
                    type="button"
                    onClick={() => setSelectedSlug(club.slug)}
                    aria-pressed={club.slug === selectedClub.slug}
                    style={
                      {
                        "--club-color": club.primary_color,
                      } as CSSProperties
                    }
                  >
                    <span className="map-club-index">
                      {(
                        clubs.items.findIndex(
                          (item) => item.slug === club.slug,
                        ) + 1
                      )
                        .toString()
                        .padStart(2, "0")}
                    </span>
                    <span>
                      <strong>{club.short_name}</strong>
                      <small>
                        {club.city} · {club.stadium.name}
                      </small>
                    </span>
                    <i aria-hidden="true" />
                  </button>
                ))}

                {filteredClubs.length === 0 && (
                  <div className="map-club-search-empty">
                    没有匹配的球队，试试搜索城市或球场名。
                  </div>
                )}
              </div>
            </aside>
          </div>

          <p className="map-sample-notice">
            <span aria-hidden="true">i</span>
            <span>
              {clubs.sample_notice}{" "}
              <a href={clubs.source_url} rel="noreferrer" target="_blank">
                查看 {clubs.source_name} ↗
              </a>
            </span>
          </p>
        </>
      )}
    </section>
  );
}
