"""Script to seed the MySQL database with initial data."""

import os
from sqlalchemy import inspect
from app.core.database import engine, Base, SessionLocal
from app.models.course import CourseEntity
from app.repository.mock_data import CATALOG

def seed():
    print("Creating tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    
    with SessionLocal() as db:
        existing_ids = {c.id for c in db.query(CourseEntity.id).all()}
        
        new_courses = 0
        print("Checking for new courses to add...")
        for course in CATALOG:
            if course.id not in existing_ids:
                entity = CourseEntity(
                    id=course.id,
                    title=course.title,
                    description=course.description,
                    prerequisites=course.prerequisites
                )
                db.add(entity)
                new_courses += 1
        
        if new_courses > 0:
            db.commit()
            print(f"Successfully seeded {new_courses} new courses into MySQL!")
        else:
            print("Database is already up to date. No new courses to seed.")

if __name__ == "__main__":
    seed()
