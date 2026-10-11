"""API Router for recommendations."""

import logging

from fastapi import APIRouter

from app.core.exceptions import CourseRecommendationError
from app.repository.course_repository import course_repository
from app.schemas.course import (FrontendCourseItem, FrontendRecommendation, LearnerProfile,
                                RecommendationRequest, RecommendationResponse)
from app.service.recommendation_service import recommendation_service

router = APIRouter(prefix="/api", tags=["Recommendations"])
logger = logging.getLogger(__name__)


@router.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """Generates course recommendations based on the user's profile."""

    logger.info("Received recommendation request", extra={"user_id": request.user_id})

    profile = LearnerProfile(
        user_id=request.user_id,
        stated_goal=request.stated_goal,
        expected_level=request.expected_level,
        completed_modules=getattr(request, 'completed_modules', "")
    )

    try:
        recommendations = await recommendation_service.generate_recommendations(profile)

        frontend_recs = []
        for rec in recommendations:
            frontend_courses = [
                FrontendCourseItem(
                    course_title=c.course_title,
                    url=c.url,
                    description=c.description
                )
                for c in rec.courses
            ]
            
            frontend_recs.append(
                FrontendRecommendation(
                    path_name=rec.path_name,
                    score=rec.score,
                    rationale=rec.rationale,
                    courses=frontend_courses,
                )
            )

        logger.info(
            "Successfully generated recommendations",
            extra={"count": len(frontend_recs)},
        )
        return RecommendationResponse(recommendations=frontend_recs)

    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        raise CourseRecommendationError(str(e))
