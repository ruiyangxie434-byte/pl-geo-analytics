"use client";

import type { KeyboardEvent } from "react";

import type { MatchShotData } from "../../types/api";

interface ShotMapProps {
  shots: MatchShotData[];
  selectedShotId: string | null;
  onSelect: (shot: MatchShotData) => void;
}

const viewBoxWidth = 720;
const viewBoxHeight = 430;
const pitch = { x: 28, y: 28, width: 664, height: 356 };

function shotPosition(shot: MatchShotData) {
  const attackingHalfX = Math.max(50, Math.min(100, shot.x));
  return {
    x: pitch.x + ((attackingHalfX - 50) / 50) * pitch.width,
    y: pitch.y + (shot.y / 100) * pitch.height,
  };
}

function shotRadius(xg: number) {
  return 7 + Math.sqrt(Math.max(0, xg)) * 19;
}

function accessibleShotLabel(shot: MatchShotData) {
  return `${shot.minute + 1}分钟，${shot.player_name ?? "未知球员"}，${shot.outcome}，xG ${shot.xg.toFixed(3)}`;
}

export function ShotMap({ shots, selectedShotId, onSelect }: ShotMapProps) {
  function handleKeyDown(
    event: KeyboardEvent<SVGGElement>,
    shot: MatchShotData,
  ) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      onSelect(shot);
    }
  }

  return (
    <div className="shot-map-wrap">
      <svg
        className="shot-map"
        viewBox={`0 0 ${viewBoxWidth} ${viewBoxHeight}`}
        role="img"
        aria-label="归一化进攻半场射门位置图"
      >
        <defs>
          <linearGradient id="pitch-gradient" x1="0" x2="1">
            <stop offset="0" stopColor="#0f2b23" />
            <stop offset="1" stopColor="#12372b" />
          </linearGradient>
          <filter id="shot-glow" x="-70%" y="-70%" width="240%" height="240%">
            <feGaussianBlur stdDeviation="5" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        <rect
          className="shot-pitch-fill"
          x={pitch.x}
          y={pitch.y}
          width={pitch.width}
          height={pitch.height}
          rx="18"
        />
        <g className="shot-pitch-lines" aria-hidden="true">
          <rect
            x={pitch.x}
            y={pitch.y}
            width={pitch.width}
            height={pitch.height}
            rx="18"
          />
          <line
            x1={pitch.x}
            y1={pitch.y}
            x2={pitch.x}
            y2={pitch.y + pitch.height}
          />
          <path
            d={`M ${pitch.x + pitch.width * 0.7} ${pitch.y + pitch.height * 0.18} H ${pitch.x + pitch.width} V ${pitch.y + pitch.height * 0.82} H ${pitch.x + pitch.width * 0.7}`}
          />
          <path
            d={`M ${pitch.x + pitch.width * 0.9} ${pitch.y + pitch.height * 0.36} H ${pitch.x + pitch.width} V ${pitch.y + pitch.height * 0.64} H ${pitch.x + pitch.width * 0.9}`}
          />
          <path
            d={`M ${pitch.x + pitch.width * 0.7} ${pitch.y + pitch.height * 0.33} A ${pitch.height * 0.17} ${pitch.height * 0.17} 0 0 0 ${pitch.x + pitch.width * 0.7} ${pitch.y + pitch.height * 0.67}`}
          />
          <circle
            cx={pitch.x + pitch.width * 0.82}
            cy={pitch.y + pitch.height / 2}
            r="3.5"
          />
          <line
            x1={pitch.x + pitch.width}
            y1={pitch.y + pitch.height * 0.44}
            x2={pitch.x + pitch.width + 15}
            y2={pitch.y + pitch.height * 0.44}
          />
          <line
            x1={pitch.x + pitch.width + 15}
            y1={pitch.y + pitch.height * 0.44}
            x2={pitch.x + pitch.width + 15}
            y2={pitch.y + pitch.height * 0.56}
          />
          <line
            x1={pitch.x + pitch.width + 15}
            y1={pitch.y + pitch.height * 0.56}
            x2={pitch.x + pitch.width}
            y2={pitch.y + pitch.height * 0.56}
          />
        </g>
        <text className="shot-map-direction" x="42" y="414">
          中线方向
        </text>
        <text className="shot-map-direction" x="618" y="414">
          进攻方向 →
        </text>

        {shots.map((shot) => {
          const position = shotPosition(shot);
          const selected = shot.source_event_id === selectedShotId;
          return (
            <g
              className="shot-point"
              data-goal={shot.is_goal}
              data-selected={selected}
              key={shot.source_event_id}
              role="button"
              tabIndex={0}
              aria-label={accessibleShotLabel(shot)}
              onClick={() => onSelect(shot)}
              onKeyDown={(event) => handleKeyDown(event, shot)}
            >
              <title>{accessibleShotLabel(shot)}</title>
              <circle
                cx={position.x}
                cy={position.y}
                r={shotRadius(shot.xg)}
                fill={shot.is_goal ? shot.team_color : "rgba(7, 17, 15, 0.76)"}
                stroke={shot.team_color}
                strokeWidth={selected ? 5 : shot.is_goal ? 3.5 : 2.5}
                filter={selected ? "url(#shot-glow)" : undefined}
              />
              {shot.is_goal && (
                <path
                  d={`M ${position.x - 5} ${position.y} H ${position.x + 5} M ${position.x} ${position.y - 5} V ${position.y + 5}`}
                  stroke="#ffffff"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  aria-hidden="true"
                />
              )}
            </g>
          );
        })}
      </svg>

      <div className="shot-map-legend" aria-label="射门图图例">
        <span><i className="legend-shot" />普通射门</span>
        <span><i className="legend-goal">+</i>进球</span>
        <small>圆点越大，xG 越高</small>
      </div>
    </div>
  );
}
