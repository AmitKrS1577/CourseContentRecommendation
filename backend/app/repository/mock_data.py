from app.schemas.course import Course, LearnerProfile

# 1. The Content Catalog
# We define a mini-curriculum for Data Science and Web Development to show how prerequisites work.
CATALOG = [
    # Data Science Track
    Course(
        id="py-101",
        title="Python for Beginners",
        description="Learn the fundamentals of Python programming, including variables, loops, and functions.",
        prerequisites=[],  # No prerequisites
    ),
    Course(
        id="math-101",
        title="Statistics Refresher",
        description="A quick dive into statistics, probability, and linear algebra needed for Machine Learning.",
        prerequisites=[],
    ),
    Course(
        id="ds-201",
        title="Data Analysis with Pandas",
        description="Learn how to manipulate and analyze data using the Pandas library in Python.",
        prerequisites=["py-101"],  # Requires Python
    ),
    Course(
        id="ml-301",
        title="Introduction to Machine Learning",
        description="Understand supervised and unsupervised learning algorithms using Scikit-Learn.",
        prerequisites=[
            "py-101",
            "math-101",
            "ds-201",
        ],  # Requires Python, Math, and Pandas
    ),
    Course(
        id="dl-401",
        title="Deep Learning and Neural Networks",
        description="Build neural networks from scratch and use PyTorch for advanced deep learning applications.",
        prerequisites=["ml-301"],  # Requires Introduction to Machine Learning
    ),
    # Web Development Track
    Course(
        id="web-101",
        title="HTML & CSS Basics",
        description="Learn how to structure and style basic web pages.",
        prerequisites=[],
    ),
    Course(
        id="web-201",
        title="JavaScript Fundamentals",
        description="Make your web pages interactive using vanilla JavaScript.",
        prerequisites=["web-101"],
    ),
    Course(
        id="web-301",
        title="React.js Frontend Framework",
        description="Build modern single-page applications using React.",
        prerequisites=["web-201"],
    ),
    # New Data Engineering & DB Track
    Course(
        id="db-101",
        title="Introduction to SQL",
        description="Learn to query databases, write joins, and manage relational data.",
        prerequisites=[],
    ),
    Course(
        id="db-201",
        title="Advanced Data Modeling",
        description="Design scalable schemas and learn NoSQL vs SQL trade-offs.",
        prerequisites=["db-101"],
    ),
    Course(
        id="de-301",
        title="Big Data with PySpark",
        description="Process massive datasets using Apache Spark and Python.",
        prerequisites=["py-101", "db-101"],
    ),
    Course(
        id="web-302",
        title="Backend Engineering with Node.js",
        description="Build RESTful APIs and servers using Express and Node.js.",
        prerequisites=["web-201", "db-101"],
    ),
    # DevOps & Cloud Track
    Course(
        id="ops-101",
        title="Linux and Shell Scripting",
        description="Master the terminal, bash scripting, and basic Linux administration.",
        prerequisites=[],
    ),
    Course(
        id="ops-201",
        title="Containerization with Docker",
        description="Learn how to build, run, and ship applications using Docker containers.",
        prerequisites=["ops-101"],
    ),
    Course(
        id="ops-301",
        title="Kubernetes Orchestration",
        description="Deploy, scale, and manage containerized applications with Kubernetes.",
        prerequisites=["ops-201"],
    ),
]

# 2. Simulated Learner Profiles
PROFILES = [
    # Profile 1: The Absolute Beginner
    LearnerProfile(
        user_id="user_beginner",
        stated_goal="I want to start a career in data science and learn machine learning.",
        completed_courses=[],  # Hasn't completed anything yet
    ),
    # Profile 2: The Intermediate Student
    LearnerProfile(
        user_id="user_intermediate",
        stated_goal="I want to learn machine learning algorithms.",
        completed_courses=[
            "py-101",
            "math-101",
        ],  # Has basic Python and Math, but missing Pandas
    ),
    # Profile 3: The Advanced Learner / Pivot
    LearnerProfile(
        user_id="user_advanced",
        stated_goal="I want to learn how to build neural networks.",
        completed_courses=[
            "py-101",
            "math-101",
            "ds-201",
            "ml-301",
        ],  # Ready for Deep Learning
    ),
    # Profile 4: Cross-discipline
    LearnerProfile(
        user_id="user_web",
        stated_goal="I want to build interactive frontend applications.",
        completed_courses=["web-101"],  # Ready for JavaScript
    ),
]
