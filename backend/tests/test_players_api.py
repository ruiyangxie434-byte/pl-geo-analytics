from fastapi.testclient import TestClient


def test_player_lab_returns_per90_metrics_and_sample_metadata(
    api_client: TestClient,
) -> None:
    response = api_client.get("/api/players")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["season"] == "2024-25"
    assert data["minimum_minutes"] == 450
    assert data["pool_total"] == 12
    assert data["total"] == 12
    assert data["items"][0]["slug"] == "mohamed-salah"
    assert data["items"][0]["per90"]["goals_per90"] == 0.77
    profile = data["items"][0]["percentiles"]
    assert profile["scope"] == "position_sample"
    assert profile["peer_count"] == 6
    assert profile["metrics"]["goals_per90"] == 100
    assert profile["metrics"]["assists_per90"] == 100
    assert all(
        0 <= value <= 100
        for value in profile["metrics"].values()
    )
    assert "12 名" in data["sample_notice"]
    assert "同位置" in data["percentile_notice"]


def test_player_lab_filters_position_club_query_and_minutes(
    api_client: TestClient,
) -> None:
    midfielders = api_client.get(
        "/api/players?position=MID&minimum_minutes=2700"
    )
    assert midfielders.status_code == 200
    midfielder_data = midfielders.json()["data"]
    assert midfielder_data["pool_total"] == 10
    assert midfielder_data["total"] == 4
    assert {
        item["slug"]
        for item in midfielder_data["items"]
    } == {
        "bruno-guimaraes",
        "declan-rice",
        "moises-caicedo",
        "youri-tielemans",
    }

    club = api_client.get("/api/players?club_slug=arsenal")
    assert club.status_code == 200
    assert {
        item["slug"] for item in club.json()["data"]["items"]
    } == {"bukayo-saka", "declan-rice"}

    query = api_client.get("/api/players?query=egypt")
    assert query.status_code == 200
    assert [
        item["slug"] for item in query.json()["data"]["items"]
    ] == ["mohamed-salah"]


def test_player_lab_supports_sorting_and_pagination(
    api_client: TestClient,
) -> None:
    response = api_client.get(
        "/api/players?sort_by=tackles_per90&order=desc&limit=3&offset=0"
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total"] == 12
    assert len(data["items"]) == 3
    values = [item["per90"]["tackles_per90"] for item in data["items"]]
    assert values == sorted(values, reverse=True)


def test_player_detail_exposes_totals_and_position_fallback(
    api_client: TestClient,
) -> None:
    response = api_client.get("/api/players/virgil-van-dijk")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["full_name"] == "Virgil van Dijk"
    assert data["club"]["slug"] == "liverpool"
    assert data["totals"]["minutes"] == 3330
    assert data["per90"]["interceptions_per90"] == 1.08
    assert data["percentiles"]["scope"] == "all_sample_players"
    assert data["percentiles"]["peer_count"] == 12


def test_player_api_validates_filters_and_unknown_player(
    api_client: TestClient,
) -> None:
    invalid_position = api_client.get("/api/players?position=STRIKER")
    assert invalid_position.status_code == 422
    assert invalid_position.json()["success"] is False

    invalid_minutes = api_client.get("/api/players?minimum_minutes=-1")
    assert invalid_minutes.status_code == 422

    missing = api_client.get("/api/players/not-a-player")
    assert missing.status_code == 404
    assert missing.json()["message"] == "未找到该球员或赛季数据"
