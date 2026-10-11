from typing import List, Optional

from pydantic import BaseModel, Field


class Course(BaseModel):
    """Represents a single course in the content catalog."""

    id: str = Field(..., description="Unique identifier for the course")
    title: str = Field(..., description="The title of the course")
    description: str = Field(
        ..., description="Detailed description of what the course covers"
    )
    prerequisites: List[str] = Field(
        default_factory=list,
        description="List of course IDs that must be completed before taking this course",
    )


class LearnerProfile(BaseModel):
    """Represents a learner's current state and goals."""

    user_id: str = Field(..., description="Unique identifier for the learner")
    stated_goal: str = Field(
        ..., description="What the user wants to achieve (e.g., 'Learn data science')"
    )
    expected_level: str = Field(
        ..., description="The user's target knowledge level (e.g., beginner, intermediate, advanced)"
    )
    completed_modules: Optional[str] = Field(default="", description="Comma separated list of completed modules")


class CourseItem(BaseModel):
    """Represents a single course within a learning path."""
    
    course_title: str = Field(..., description="The real title of the open source course")
    url: str = Field(..., description="The live URL link to the course")
    description: str = Field(..., description="A short description of what this specific course covers")


class Recommendation(BaseModel):
    """Represents a full learning path recommendation."""

    path_name: str = Field(..., description="A catchy name for this path (e.g., 'The Fast Track', 'The Theoretical Route')")
    score: str = Field(..., description="A recommendation level: 'High', 'Mid', or 'Low'")
    rationale: str = Field(
        ..., description="A clear explanation of why this entire path fits their goal"
    )
    courses: List[CourseItem] = Field(
        ..., description="A sequence of courses from beginner up to the expected level"
    )


class FrontendCourseItem(BaseModel):
    course_title: str
    url: str
    description: str


class FrontendRecommendation(BaseModel):
    """Frontend projection of a recommendation path."""

    path_name: str
    score: str
    rationale: str
    courses: List[FrontendCourseItem]


class RecommendationRequest(BaseModel):
    """Payload sent from the frontend to request recommendations."""

    user_id: str
    stated_goal: str
    expected_level: str
    completed_modules: Optional[str] = Field(default="", description="Comma separated list of completed modules")


class RecommendationResponse(BaseModel):
    """Response returned to the frontend containing mapped recommendations."""

    recommendations: List[FrontendRecommendation]
