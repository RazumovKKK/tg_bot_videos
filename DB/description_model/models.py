from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped

class Base(DeclarativeBase):
    pass

class Video(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True, index=True)
    creator_id = Column(String, index=True)
    video_created_at = Column(String)
    views_count = Column(Integer)
    likes_count = Column(Integer)
    comments_count = Column(Integer)
    reports_count = Column(Integer)

    created_at = Column(String)
    updated_at = Column(String)

class Video_Snapshot(Base):
    __tablename__ = "video_snapshots"

    id = Column(String, primary_key=True, index=True)

    video_id = Column(String, ForeignKey("videos.id"), index=True)

    video = relationship("Video")

    views_count = Column(Integer)
    likes_count = Column(Integer)
    comments_count = Column(Integer)
    reports_count = Column(Integer)

    delta_views_count = Column(Integer)
    delta_likes_count = Column(Integer)
    delta_comments_count = Column(Integer)
    delta_reports_count = Column(Integer)

    
    created_at = Column(String)
    updated_at = Column(String)



