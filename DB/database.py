import os
import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from DB.description_model.models import Base, Video, Video_Snapshot

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

session_local = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

def execute_sql_query(sql_query: str):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            
            row = result.fetchone()
            
            if row and len(row) > 0:
                return row[0]
            else:
                return None
                
    except Exception as e:
        raise

def add_json():
    Base.metadata.create_all(bind=engine)

    with open('videos.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    with Session(engine) as session:
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
        
        try:
            session.commit()
        except Exception as e:
            session.rollback()
