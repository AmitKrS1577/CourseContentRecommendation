# NextStep AI

NextStep AI is a personalized course-path recommender that helps learners decide what to study next. A learner describes a goal, chooses a target knowledge level, and can optionally list completed modules. The app uses that information to generate distinct, ordered learning paths with course titles, descriptions, links, and a short explanation of how each path supports the goal.

## How it works

1. The React frontend sends the learner's goal, target level, and completed modules to the recommendation API.
2. The FastAPI backend passes the learner profile to a Pydantic AI agent.
3. The agent can search the web for open courses, check the local course catalog, and account for completed modules when considering prerequisites.
4. The backend returns the resulting paths to the frontend, where learners can compare them and open course details.

The agent is prompted to return three different paths and assign them High, Mid, and Low scores. A final rule-based step enforces those score labels by output position: the first path is High, the second Mid, and the third Low. This is a presentation/ranking rule, not a separately calculated measure of course quality.

## Technology

- **Frontend:** React, TypeScript, and Vite
- **Backend:** Python and FastAPI
- **Recommendation agent:** Pydantic AI, configured to use Gemini by default
- **Course discovery:** DuckDuckGo web search and a ChromaDB-backed local catalog

## Project layout

- `frontend/` — learner form, recommendation results, and course detail interface
- `backend/app/api/` — recommendation API endpoint
- `backend/app/service/` — AI agent, course discovery tools, and ranking logic
- `backend/app/repository/` — local course catalog access
- `backend/chroma_db/` — generated local vector-store data
- `ranking_logic_documentation.md` — additional detail on the recommendation and ranking flow

## API

The frontend calls `POST /api/recommend` on the local backend. The request includes `user_id`, `stated_goal`, `expected_level`, and an optional `completed_modules` value. The response contains a list of paths, each with a name, score, rationale, and ordered course details.

Configure provider credentials and other local settings through environment variables in a local `.env` file. Do not commit credentials or other secrets to source control.
