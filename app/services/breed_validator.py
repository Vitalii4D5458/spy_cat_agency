import httpx

async def validate_breed(breed: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.thecatapi.com/v1/breeds/search?q={breed}")
            if response.status_code == 200:
                breeds = response.json()
                return len(breeds) > 0
    except Exception:
        pass
    return False
