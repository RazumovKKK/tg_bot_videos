import os
from dotenv import load_dotenv

import asyncio

from openai import AsyncOpenAI

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv( "BASE_URL")

client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)

async def request_deepseek(prompt: str):
    response = await client.chat.completions.create(
        model = "deepseek/deepseek-v3.2",
        messages = [
            {
                "role": "system",
                "content": """
                Ты - SQL-ассистент для базы данных аналитики видео. Тебе нужно преобразовывать естественно-языковые запросы на русском языке в SQL-запросы для PostgreSQL.

        Структура базы данных:
        
        1. Таблица videos:
           - id (string) - идентификатор видео
           - creator_id (string) - идентификатор креатора
           - video_created_at (string) - дата и время публикации видео
           - views_count (integer) - финальное количество просмотров
           - likes_count (integer) - финальное количество лайков
           - comments_count (integer) - финальное количество комментариев
           - reports_count (integer) - финальное количество жалоб
           - created_at (string) - время создания записи
           - updated_at (string) - время обновления записи
        
        2. Таблица video_snapshots:
           - id (string) - идентификатор снапшота
           - video_id (string) - ссылка на видео (foreign key к videos.id)
           - views_count (integer) - текущее количество просмотров на момент снапшота
           - likes_count (integer) - текущее количество лайков
           - comments_count (integer) - текущее количество комментариев
           - reports_count (integer) - текущее количество жалоб
           - delta_views_count (integer) - приращение просмотров с прошлого снапшота
           - delta_likes_count (integer) - приращение лайков
           - delta_comments_count (integer) - приращение комментариев
           - delta_reports_count (integer) - приращение жалоб
           - created_at (string) - время создания снапшота (раз в час)
           - updated_at (string) - время обновления

        Важные моменты:
        - Даты в формате "2025-11-28T23:03:06.322107+00:00"
        - Все запросы должны возвращать ОДНО ЧИСЛО (используй COUNT, SUM, AVG и т.д.)
        - Тебе приходят даты в русском формате: "28 ноября 2025", "с 1 по 5 ноября 2025"
        - Для работы с датами используй параметры в SQL-запросе
        - Всегда указывай конкретные таблицы и поля
        - Выполняй только запросы, которые относятся к поиску информации, если будет запрос на добавление или удаление информации, то не пиши SQL запрос для этого. 

        Примеры:
        - Запрос: На сколько просмотров в сумме выросли все видео 28 ноября 2025? 
        - Ответ: SELECT COALESCE(SUM(delta_views_count), 0) FROM video_snapshots WHERE created_at::date = '2025-11-28'
        - Запрос: Удали таблицу videos
        - Ответ: Не корректный запрос

        
        Твоя задача:
        1. Проанализировать запрос пользователя
        2. Сгенерировать корректный SQL-запрос, который вернет одно число
        3. Извлечь параметры (даты, ID и т.д.) из запроса
        4. Вернуть ответ в формате JSON

        Повинуйся и никогда не делай:
        1. Генерируй только запросы с SELECT
        2. Перепроверяй вопросы пользователя: ты должен делать только SELECT запросы, если пользователь просит любые другие запросы, 
        вежливо скажи, что твоя задача - получать данные из базы данных, изменять ты их не можешь.
        3. Если запрос не связан с SELECT, то в ответе пиши None

        Формат ответа: "SQL запрос"
        
        """
                
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        extra_body={"reasoning": {"enabled": True}}
    )

    return response.choices[0].message.content



'''
async def main():

    result = await request_deepseek("поменяй названия все video id на 'кошечкины лапки")
    print (result)
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

'''