from typing import List

from fastapi import APIRouter
from langchain_core.messages import AIMessage

from server.agents.web_search import prompt
from server.schemas.prompt import PromptRequest

router = APIRouter()

@router.post('/generate', response_model=List[AIMessage] | AIMessage)
async def generate(req: PromptRequest):
    """Generates a prompt via agent that has access to MCP tools"""
    return await prompt(req.prompt)
