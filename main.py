from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage

from dotenv import load_dotenv
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    yield

app = FastAPI(
    title='Agentic AI server testing',
    docs_url='/',
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

model = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

class PromptRequest(BaseModel):
    prompt: str

class TokenUsage(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int
class ModelResponse(BaseModel):
    content: str
    model_name: str
    token_usage: TokenUsage

@app.post('/api/generate')
async def generate(req: PromptRequest):
    prompt = str(req.prompt)

    messages = [
        SystemMessage(content='You are a helpful assistant'),
        HumanMessage(content=prompt)
    ]
    answer = await model.ainvoke(messages)

    return ModelResponse(
        content=answer.content,
        model_name=answer.response_metadata.get('model_name', 'unknown'),
        token_usage=TokenUsage(
            input_tokens=answer.usage_metadata['input_tokens'],
            output_tokens=answer.usage_metadata['output_tokens'],
            total_tokens=answer.usage_metadata['total_tokens']
        )
    )


