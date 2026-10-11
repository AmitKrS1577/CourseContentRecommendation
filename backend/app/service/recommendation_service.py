"""Service layer for handling recommendation business logic."""

import os
from dotenv import load_dotenv
import asyncio
from pydantic_ai import Agent, RunContext
from duckduckgo_search import DDGS
from pydantic_ai.exceptions import UnexpectedModelBehavior

from app.schemas.course import LearnerProfile, Recommendation

load_dotenv()

MODEL_NAME = os.getenv("RECOMMENDATION_MODEL", "google:gemini-flash-lite-latest")

recommendation_agent = Agent(
    model=MODEL_NAME,
    deps_type=LearnerProfile,
    output_type=list[Recommendation],
    retries=3,
    system_prompt=(
        "You are an expert educational advisor. Your task is to recommend EXACTLY 3 distinct, complete learning paths "
        "from the live internet based on the learner's goal and expected target level.\n\n"
        "Follow these exact steps:\n"
        "1. Use the 'search_open_courses' tool to search the internet for highly-rated free courses matching their goal.\n"
        "   IMPORTANT: If the user provides `completed_modules`, you MUST use the `check_prerequisites` tool to evaluate them.\n"
        "   CRITICAL: Do NOT recommend any topics, courses, or difficulty levels that the user has already listed in their `completed_modules`. Assume they have already mastered those topics and recommend the next logical step.\n"
        "   You may also use `retrieve_course_catalog` to check our internal local Vector DB.\n"
        "2. Formulate 3 distinct learning paths (e.g., 'The Practical Path', 'The Theory-First Path').\n"
        "3. For each path, generate a sequence of `courses` starting from absolute beginner up to their specific `expected_level`.\n"
        "4. For each course in the sequence, provide its real `course_title`, a short `description`, and the actual `url` to the course.\n"
        "5. You MUST rank the 3 paths. Assign the 1st path a `score` of 'High', the 2nd path a `score` of 'Mid', and the 3rd path a `score` of 'Low'.\n"
        "6. Provide a clear one-line `rationale` explaining why this complete path fits their goal."
    ),
)


@recommendation_agent.tool
def search_open_courses(ctx: RunContext[LearnerProfile], query: str) -> str:
    """Searches the live internet for free open-source courses related to the query."""
    try:
        search_query = f"{query} free open source course tutorial"
        with DDGS() as ddgs:
            results = list(ddgs.text(search_query, max_results=8))
        
        formatted = ""
        for r in results:
            formatted += f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n\n"
        return formatted
    except Exception as e:
        return f"Search failed: {str(e)}. Fall back to your internal knowledge to recommend real courses with valid URLs."


@recommendation_agent.tool
def retrieve_course_catalog(ctx: RunContext[LearnerProfile], category: str) -> str:
    """Legacy Tool: Retrieves courses from a static local catalog database."""
    from app.repository.course_repository import course_repository
    courses = course_repository.semantic_search(category, top_k=5)
    
    if not courses:
        return "No local courses found for this category."
        
    formatted = "Available Local Courses:\n"
    for c in courses:
        prereqs = ", ".join(c.prerequisites) if c.prerequisites else "None"
        formatted += f"- ID: {c.id}, Title: {c.title}, Prerequisites: {prereqs}\n"
        formatted += f"  Description: {c.description}\n\n"
    
    return formatted


@recommendation_agent.tool
def check_prerequisites(ctx: RunContext[LearnerProfile], course_id: str, required_modules: list[str]) -> bool:
    """Legacy Tool: Checks if the learner has completed the required prerequisite modules."""
    completed = ctx.deps.completed_modules.lower() if ctx.deps.completed_modules else ""
    
    # If no prerequisites are required, return True
    if not required_modules:
        return True
        
    # Check if the required modules are mentioned in the completed_modules string
    for req in required_modules:
        if req.lower() not in completed:
            return False
            
    return True


def apply_rule_based_ranking(paths: list[Recommendation], goal: str) -> list[Recommendation]:
    """Applies a simple rule-based ranking layer over the AI's output to strictly enforce High/Mid/Low."""
    # Ensure strict ranking: 1st is High, 2nd is Mid, 3rd is Low
    expected_scores = ['High', 'Mid', 'Low']
    
    for i, path in enumerate(paths):
        if i < len(expected_scores):
            # If the AI messed up the score, the rule-based layer corrects it
            if path.score != expected_scores[i]:
                path.score = expected_scores[i]
                path.rationale = "(Rule-Based Override): " + path.rationale
            
    return paths


class RecommendationService:
    """Service class encapsulating business logic for recommendations."""

    async def generate_recommendations(
        self, profile: LearnerProfile
    ) -> list[Recommendation]:
        """Generates recommendations for a given learner profile.

        Args:
            profile: The profile containing the user's goal and knowledge level.

        Returns:
            A list of exactly 3 recommended courses.
        """
        prompt = (
            f"The user's stated goal is: '{profile.stated_goal}'.\n"
            f"The user's expected target level is: '{profile.expected_level}'.\n"
            "Please use your tools to search the web, formulate exactly 3 distinct learning paths, and recommend them with scores and a full sequence of courses from beginner to the target level."
        )

        max_retries = 3
        for attempt in range(max_retries):
            try:
                result = await recommendation_agent.run(prompt, deps=profile)
                response_data = getattr(result, "data", getattr(result, "output", []))
                if not isinstance(response_data, list):
                    return []
                # Apply the rule-based ranking layer before returning
                ranked_data = apply_rule_based_ranking(response_data, profile.stated_goal)
                return ranked_data
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    if attempt < max_retries - 1:
                        await asyncio.sleep(45) # Wait 45 seconds for Free Tier quotas to reset
                        continue
                raise e
        
        return []


recommendation_service = RecommendationService()
