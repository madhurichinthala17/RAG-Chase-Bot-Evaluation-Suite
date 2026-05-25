import os
from deepeval import login
from dotenv import load_dotenv

def run_login():
    load_dotenv()

    CONFIDENT_API_KEY = os.getenv("CONFIDENT_API_KEY")

    login(CONFIDENT_API_KEY)
