from database import SessionLocal
from models import Topic

def seed_topics():
    db = SessionLocal()
    topics = ["Politics", "Health", "Sport", "Tech"]
    try:
        for topic_name in topics:
            existing_topic = (
                db.query(Topic)
                .filter(Topic.name == topic_name)
                .first()
            )
            if existing_topic is None:
                topic = Topic(name=topic_name)
                db.add(topic)
        db.commit()
    finally:
        db.close()
if __name__ == "__main__":
    seed_topics()

