"use client";

import L from "leaflet";
import Link from "next/link";
import { useEffect, useMemo, useRef } from "react";
import {
  MapContainer,
  Marker,
  Popup,
  TileLayer,
  Tooltip,
  ZoomControl,
  useMap,
} from "react-leaflet";
import type { LatLngBoundsExpression } from "leaflet";

import type { ClubSummary } from "../../types/api";

interface LeafletClubMapProps {
  clubs: ClubSummary[];
  selectedSlug: string;
  onSelectClub: (slug: string) => void;
}

function getClubInitials(name: string) {
  return name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 3)
    .toUpperCase()
    .replace(/[^A-Z0-9]/g, "");
}

function getSafeColor(color: string) {
  return /^#[0-9a-f]{6}$/i.test(color) ? color : "#48e5a4";
}

function ClubMapMarker({
  club,
  isSelected,
  onSelectClub,
}: {
  club: ClubSummary;
  isSelected: boolean;
  onSelectClub: (slug: string) => void;
}) {
  const icon = useMemo(
    () =>
      L.divIcon({
        className: "club-map-marker-wrapper",
        html: `<span class="club-map-marker${isSelected ? " is-selected" : ""}" style="--marker-color:${getSafeColor(club.primary_color)}"><b>${getClubInitials(club.short_name)}</b></span>`,
        iconAnchor: [22, 22],
        iconSize: [44, 44],
        popupAnchor: [0, -20],
        tooltipAnchor: [0, -18],
      }),
    [club.primary_color, club.short_name, isSelected],
  );

  return (
    <Marker
      eventHandlers={{
        click: () => onSelectClub(club.slug),
      }}
      icon={icon}
      position={[club.stadium.latitude, club.stadium.longitude]}
      zIndexOffset={isSelected ? 1000 : 0}
    >
      <Tooltip direction="top" opacity={1}>
        <span className="club-map-tooltip">
          <strong>{club.short_name}</strong>
          <small>
            {club.city} · {club.stadium.name}
          </small>
        </span>
      </Tooltip>
      <Popup>
        <div className="club-map-popup">
          <span>{club.city}</span>
          <strong>{club.name}</strong>
          <small>{club.stadium.name}</small>
          <Link href={`/clubs/${club.slug}`}>查看球队资料 →</Link>
        </div>
      </Popup>
    </Marker>
  );
}

function MapLifecycle({
  selectedClub,
}: {
  selectedClub: ClubSummary | null;
}) {
  const map = useMap();
  const previousSlug = useRef(selectedClub?.slug ?? null);

  useEffect(() => {
    const timer = window.setTimeout(() => map.invalidateSize(), 80);
    return () => window.clearTimeout(timer);
  }, [map]);

  useEffect(() => {
    if (!selectedClub) {
      return;
    }

    if (previousSlug.current === selectedClub.slug) {
      return;
    }

    previousSlug.current = selectedClub.slug;
    const prefersReducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;

    map.flyTo(
      [selectedClub.stadium.latitude, selectedClub.stadium.longitude],
      8,
      {
        animate: !prefersReducedMotion,
        duration: prefersReducedMotion ? 0 : 0.9,
      },
    );
  }, [map, selectedClub]);

  return null;
}

export function LeafletClubMap({
  clubs,
  selectedSlug,
  onSelectClub,
}: LeafletClubMapProps) {
  const selectedClub =
    clubs.find((club) => club.slug === selectedSlug) ?? clubs[0] ?? null;

  const stadiumBounds = useMemo(
    () =>
      clubs.map(
        (club) =>
          [club.stadium.latitude, club.stadium.longitude] as [number, number],
      ) as LatLngBoundsExpression,
    [clubs],
  );

  return (
    <MapContainer
      bounds={stadiumBounds}
      boundsOptions={{ padding: [44, 44] }}
      className="leaflet-club-map"
      maxZoom={14}
      minZoom={5}
      scrollWheelZoom={false}
      zoomControl={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url={
          process.env.NEXT_PUBLIC_MAP_TILE_URL ??
          "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        }
      />
      <ZoomControl position="topright" />
      <MapLifecycle selectedClub={selectedClub} />

      {clubs.map((club) => (
        <ClubMapMarker
          club={club}
          isSelected={club.slug === selectedSlug}
          key={club.slug}
          onSelectClub={onSelectClub}
        />
      ))}
    </MapContainer>
  );
}
