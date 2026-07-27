from fastapi.testclient import TestClient


def test_agent_player_options_include_new_demo_pair(
    api_client: TestClient,
) -> None:
    response = api_client.get("/api/agent/players?season=2024-25")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total"] == 12
    assert {
        item["slug"]
        for item in data["items"]
    } >= {"bukayo-saka", "cole-palmer"}


def test_agent_compares_players_with_trace_and_evidence(
    api_client: TestClient,
) -> None:
    response = api_client.post(
        "/api/agent/analyze",
        json={
            "question": "萨卡和帕尔默，谁更适合高位逼抢体系？",
            "player_slugs": ["bukayo-saka", "cole-palmer"],
            "season": "2024-25",
            "focus": "pressing",
        },
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["task_type"] == "player_comparison"
    assert data["focus"] == "pressing"
    assert len(data["players"]) == 2
    assert len(data["steps"]) == 4
    assert all(step["status"] == "completed" for step in data["steps"])
    assert {metric["key"] for metric in data["metrics"]} >= {
        "tackles_per90",
        "interceptions_per90",
    }
    assert data["recommendation"]["winner_slug"] in {
        "bukayo-saka",
        "cole-palmer",
    }
    assert len(data["evidence"]) == 3


def test_agent_can_resolve_chinese_player_names(
    api_client: TestClient,
) -> None:
    response = api_client.post(
        "/api/agent/analyze",
        json={
            "question": "比较萨卡和帕尔默的创造能力，给出选择理由",
            "season": "2024-25",
            "focus": "creativity",
        },
    )

    assert response.status_code == 200
    assert {
        item["slug"]
        for item in response.json()["data"]["players"]
    } == {"bukayo-saka", "cole-palmer"}


def test_agent_rejects_duplicate_players(api_client: TestClient) -> None:
    response = api_client.post(
        "/api/agent/analyze",
        json={
            "question": "比较两名不同球员的综合表现",
            "player_slugs": ["bukayo-saka", "bukayo-saka"],
        },
    )

    assert response.status_code == 422
    assert response.json()["success"] is False
