import os
import json
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from DB.description_model.models import Base, Video, Video_Snapshot

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    pool_size=5,
    max_overflow=10
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

async def execute_sql_query(sql_query: str):
    if (sql_query == "None" or "SELECT" not in sql_query):
        return "Не корректный запрос" 
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text(sql_query))
            
            if sql_query.strip().upper().startswith('SELECT'):
                row = result.fetchone()
                return row[0] if row and len(row) > 0 else None
            else:
                await connection.commit()
                return result.rowcount if hasattr(result, 'rowcount') else None
                
    except SQLAlchemyError as e:
        print(f"Ошибка выполнения SQL запроса: {e}")
        raise

async def add_json():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    with open('videos.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    async with async_session_maker() as session:
        try:
            for video_data in data['videos']:
                video = Video(
                    id=video_data['id'],
                    creator_id=video_data['creator_id'],
                    video_created_at=video_data['video_created_at'],
                    views_count=video_data['views_count'],
                    likes_count=video_data['likes_count'],
                    comments_count=video_data['comments_count'],
                    reports_count=video_data['reports_count'],
                    created_at=video_data['created_at'],
                    updated_at=video_data['updated_at']
                )
                
                session.add(video)
                
                for snapshot_data in video_data['snapshots']:
                    snapshot = Video_Snapshot(
                        id=snapshot_data['id'],
                        video_id=snapshot_data['video_id'],
                        views_count=snapshot_data['views_count'],
                        likes_count=snapshot_data['likes_count'],
                        comments_count=snapshot_data['comments_count'],
                        reports_count=snapshot_data['reports_count'],
                        delta_views_count=snapshot_data['delta_views_count'],
                        delta_likes_count=snapshot_data['delta_likes_count'],
                        delta_comments_count=snapshot_data['delta_comments_count'],
                        delta_reports_count=snapshot_data['delta_reports_count'],
                        created_at=snapshot_data['created_at'],
                        updated_at=snapshot_data['updated_at']
                    )
                    session.add(snapshot)
            
            await session.commit()
            print("Данные успешно добавлены в БД")
            
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при добавлении данных: {e}")
            raise


'''
async def main():

    await add_json()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
'''