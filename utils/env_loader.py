from dotenv import load_dotenv
import os

def get_google_api_key():
    load_dotenv()
    return os.getenv("GOOGLE_API_KEY")
