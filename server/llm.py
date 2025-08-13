from langchain_google_genai import ChatGoogleGenerativeAI
from server.config import GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key=GOOGLE_API_KEY
)