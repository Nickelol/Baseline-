from typing import List
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from table_post import Post
from table_feed import Feed
from schema import PostGet
from sqlalchemy import func  # Изменили импорт функции count

app = FastAPI()

def get_db():
    with SessionLocal() as db:
        return db

@app.get("/post/recommendations/", response_model=List[PostGet])
def get_post_recommendations(
    id: int = Query(None, description="ID пользователя (пока не используется)"),
    limit: int = Query(10, description="Количество рекомендуемых постов"),
    db: Session = Depends(get_db)
):
    # Получаем топ постов по количеству лайков
    recommended_posts = db.query(Post)\
        .select_from(Feed)\
        .filter(Feed.action == 'like')\
        .join(Post)\
        .group_by(Post.id)\
        .order_by(func.count(Post.id).desc())\
        .limit(limit)\
        .all()
    
    return recommended_posts
