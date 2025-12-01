import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_get_live_value_bets():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/odds/live")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
    if len(data) > 0:
        bet = data[0]
        assert "match_id" in bet
        assert "edge" in bet
        assert "true_probability" in bet
        assert bet["edge"] > 0
