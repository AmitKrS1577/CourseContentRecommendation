# Recommendation Ranking Logic Documentation

## Overview
The NextStep AI Recommender system uses a hybrid approach to ranking educational learning paths. It combines the power of a live internet-searching AI agent (powered by Pydantic-AI and Gemini) with a post-processing **rule-based ranking layer**.

## How the Ranking Works

### 1. Data Retrieval and Filtering (The Tools)
The AI agent is equipped with several tools to gather data before ranking:
- **`search_open_courses`**: Scrapes the live web (via DuckDuckGo) to pull in highly-rated free courses matching the learner's query.
- **`retrieve_course_catalog`**: Performs a semantic search against the ChromaDB vector database to pull local courses.
- **`check_prerequisites`**: Evaluates a candidate course's required modules against the user's `completed_modules` list. If the course demands a prerequisite that the user hasn't explicitly completed, the tool flags it so the AI can discard it.

### 2. LLM-Based Generation
Once the agent gathers candidate courses from its tools, it evaluates them against the learner's **Stated Goal**.
The agent is explicitly instructed to construct exactly 3 distinct learning paths (e.g., "The Practical Path", "The Theory-First Path") and rank them natively as 'High', 'Mid', and 'Low' based on its semantic understanding of the goal.

### 3. Final Rule-Based Scoring Layer
Before the paths are returned to the user, they pass through a strict Python function `apply_rule_based_ranking()`.
This layer acts as a safeguard and an override to the AI's intuition:
- **Rule:** The system enforces a strict tier hierarchy based on the agent's output sequence. The 1st generated path is mathematically forced to "High", the 2nd to "Mid", and the 3rd to "Low".
- If the AI hallucinated the scores (e.g., scoring all of them as "High"), the rule-based layer intercepts and overwrites the scores to adhere to the strict tiering, prepending `(Rule-Based Override)` to the rationale.

This satisfies both the need for semantic, human-like AI generation and strict, verifiable algorithmic rule-based evaluation.
