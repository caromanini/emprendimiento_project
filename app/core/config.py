import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY= os.getenv("SECRET_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# False only when explicitly set to "false"; defaults to True so production is safe by default.
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "true").lower() != "false"
