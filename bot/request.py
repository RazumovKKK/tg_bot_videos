import aiohttp

class Get_Requests:

    @staticmethod
    async def make_request(url1: str):
        url = "http://localhost:8000/sql/" + url1
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    print(f"Ошибка: {response.status}")
                    return None