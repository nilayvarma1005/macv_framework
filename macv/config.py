import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Securely fetch API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not OPENAI_API_KEY or not TAVILY_API_KEY:
    raise ValueError("API keys for OpenAI and Tavily must be set in the .env file.")

# Model configurations
GENERATOR_MODEL = "gpt-4-turbo"
FAST_MODEL = "gpt-3.5-turbo"
AGENT_MODEL = "gpt-4-turbo"

# Dataset configurations
DATASETS = {
    "squad": {"path": "squad", "split": "validation", "question_col": "question", "answer_col": "answers", "domain": "general"},
    "sciq": {"path": "sciq", "split": "test", "question_col": "question", "answer_col": "correct_answer", "domain": "science"},
    "finqa": {"path": "dreamerdeo/finqa", "split": "validation", "question_col": "question", "answer_col": "answer", "domain": "finance"}
}

# Evaluation settings
NUM_SAMPLES_PER_DATASET = 10  # Adjust for full evaluation
RESULTS_FILE = "data/msv_evaluation_results.csv"