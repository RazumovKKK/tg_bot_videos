import os
from dotenv import load_dotenv

import asyncio

from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def request_deepseek(prompt: str):
    response = client.chat.completions.create(
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

        Примеры:
        - Запрос: На сколько просмотров в сумме выросли все видео 28 ноября 2025? 
        - Ответ: SELECT COALESCE(SUM(delta_views_count), 0) FROM video_snapshots WHERE created_at::date = '2025-11-28'

        
        Твоя задача:
        1. Проанализировать запрос пользователя
        2. Сгенерировать корректный SQL-запрос, который вернет одно число
        3. Извлечь параметры (даты, ID и т.д.) из запроса
        4. Вернуть ответ в формате JSON

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


#print(request_deepseek("Сколько видео у креатора с id 404eb087b02b4ae9a66ce39411cb299b вышло с 1 ноября 2025 по 5 ноября 2025 включительно?"))
