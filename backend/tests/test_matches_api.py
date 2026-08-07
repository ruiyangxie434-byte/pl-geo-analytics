from fastapi.testclient import TestClient


def test_match_list_returns_attributed_historical_snapshot(
    api_client: TestClient,
) -> None:
    response = api_client.get("/api/matches")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total"] == 1
    assert data["source_name"] == "StatsBomb Open Data"
    assert "2003-04" in data["sample_notice"]

    match = data["items"][0]
    assert match["source_match_id"] == "3749448"
    assert match["season"] == "2003-04"
    assert match["matchweek"] == 31
    assert match["home_team"]["slug"] == "arsenal"
    assert match["home_team"]["score"] == 4
    assert match["home_team"]["shots"] == 15
    assert match["home_team"]["total_xg"] == 2.006
    assert match["away_team"]["slug"] == "liverpool"
    assert match["away_team"]["score"] == 2
    assert match["away_team"]["shots"] == 13
    assert match["away_team"]["total_xg"] == 1.941
    assert match["shot_count"] == 28
    assert match["goal_count"] == 6
    assert match["total_xg"] == 3.947


def test_match_detail_returns_normalized_shots_and_goal_timeline(
    api_client: TestClient,
) -> None:
    response = api_client.get("/api/matches/3749448")

    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data["shots"]) == 28
    assert sum(shot["is_goal"] for shot in data["shots"]) == 6
    assert all(0 <= shot["x"] <= 100 for shot in data["shots"])
    assert all(0 <= shot["y"] <= 100 for shot in data["shots"])
    assert all(0 <= shot["xg"] <= 1 for shot in data["shots"])
    assert "120×80" in data["coordinate_note"]

    henry_goals = [
        shot["minute"]
        for shot in data["shots"]
        if shot["player_name"] == "Thierry Henry" and shot["is_goal"]
    ]
    assert henry_goals == [30, 49, 76]


def test_unknown_match_uses_unified_error(api_client: TestClient) -> None:
    response = api_client.get("/api/matches/not-a-match")

    assert response.status_code == 404
    assert response.json()["message"] == "未找到该比赛快照"
