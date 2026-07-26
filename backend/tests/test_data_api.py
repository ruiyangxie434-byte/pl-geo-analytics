from fastapi.testclient import TestClient


def test_club_list_returns_seeded_sample_slice(api_client: TestClient) -> None:
    response = api_client.get("/api/clubs")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["total"] == 5
    assert body["data"]["player_total"] == 10
    assert len(body["data"]["items"]) == 5
    assert all(
        club["source_kind"] == "sample"
        for club in body["data"]["items"]
    )
    assert {
        club["slug"]
        for club in body["data"]["items"]
    } == {
        "arsenal",
        "aston-villa",
        "liverpool",
        "manchester-city",
        "newcastle-united",
    }


def test_club_detail_includes_sample_players(api_client: TestClient) -> None:
    response = api_client.get("/api/clubs/liverpool")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "Liverpool"
    assert data["stadium"]["name"] == "Anfield"
    assert len(data["players"]) == 2
    assert {player["full_name"] for player in data["players"]} == {
        "Mohamed Salah",
        "Virgil van Dijk",
    }


def test_unknown_club_uses_unified_error(api_client: TestClient) -> None:
    response = api_client.get("/api/clubs/not-a-club")

    assert response.status_code == 404
    assert response.json() == {
        "success": False,
        "message": "未找到该球队",
        "data": None,
        "errors": None,
    }


def test_standings_are_sorted_and_marked_partial(api_client: TestClient) -> None:
    response = api_client.get("/api/standings?season=2024-25")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["season"] == "2024-25"
    assert data["total"] == 5
    assert data["is_partial"] is True
    assert [item["position"] for item in data["items"]] == [1, 2, 3, 5, 6]
    assert data["items"][0]["club"]["slug"] == "liverpool"
    assert data["items"][0]["points"] == 84


def test_standings_validate_season_format(api_client: TestClient) -> None:
    response = api_client.get("/api/standings?season=2025")

    assert response.status_code == 422
    assert response.json()["success"] is False
    assert response.json()["errors"][0]["field"] == "query.season"
