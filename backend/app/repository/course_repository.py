"""Course Repository Layer. Handles data retrieval and semantic searching."""

import chromadb
from chromadb.utils import embedding_functions

from app.schemas.course import Course
from app.models.course import CourseEntity
from app.core.database import SessionLocal

class CourseRepository:
    def __init__(self):
        # Initialize a Persistent ChromaDB client
        self._chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self._real_ef = embedding_functions.DefaultEmbeddingFunction()
        
        # Create a new collection (v2) so we don't conflict with the old dummy vectors
        self._collection = self._chroma_client.get_or_create_collection(
            name="course_catalog_v2",
            embedding_function=self._real_ef
        )

    def _sync_chroma(self, courses: list[Course]):
        """Helper to sync MySQL data to Chroma if the vector DB is empty."""
        if self._collection.count() == 0 and courses:
            documents = [c.description for c in courses]
            metadatas = [{"title": c.title} for c in courses]
            ids = [c.id for c in courses]
            self._collection.add(documents=documents, metadatas=metadatas, ids=ids)

    def get_all_courses(self) -> list[Course]:
        """Retrieves the full course catalog from MySQL."""
        with SessionLocal() as db:
            entities = db.query(CourseEntity).all()
            courses = [
                Course(
                    id=e.id, 
                    title=e.title, 
                    description=e.description, 
                    prerequisites=e.prerequisites
                ) for e in entities
            ]
            self._sync_chroma(courses)
            return courses

    def semantic_search(self, query: str, top_k: int = 5) -> list[Course]:
        """Retrieve courses from the catalog that semantically match the query."""
        results = self._collection.query(query_texts=[query], n_results=top_k)
        
        if not results or not results["ids"] or not results["ids"][0]:
            return []
            
        matched_ids = results["ids"][0]
        
        # Retrieve full course details from MySQL based on matched semantic IDs
        with SessionLocal() as db:
            entities = db.query(CourseEntity).filter(CourseEntity.id.in_(matched_ids)).all()
            
            # Re-map entities back into Pydantic models in the correct semantic order
            course_map = {
                e.id: Course(
                    id=e.id, 
                    title=e.title, 
                    description=e.description, 
                    prerequisites=e.prerequisites
                ) for e in entities
            }
            
            return [course_map[cid] for cid in matched_ids if cid in course_map]

course_repository = CourseRepository()
