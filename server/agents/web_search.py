import asyncio
from typing import Any, Dict, List

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from server.config import BRIGHTDATA_API_KEY
from server.llm import llm

client: MultiServerMCPClient | None = None
agent = None
_init_lock = asyncio.Lock()
_initialised = False

async def _init():
    global client, agent, _initialised
    if _initialised: 
        return
    if not BRIGHTDATA_API_KEY:
        raise RuntimeError('BRIGHTDATA_API_KEY missing in environment')
    
    client = MultiServerMCPClient(
        {
            'web-search': {
                'url': f'https://mcp.brightdata.com/mcp?token={BRIGHTDATA_API_KEY}',
                'transport': 'streamable_http'
            }
        }
    )

    tools = await client.get_tools()
    agent = create_react_agent(model=llm, tools=tools)
    _initialised = True

async def ensure_initialised():
    if _initialised:
        return
    async with _init_lock:
        if not _initialised:
            await _init()

async def prompt(
    prompt: str, 
    history: List[Dict[str, Any]] | None = None
):
    await ensure_initialised()

    msgs: List[Dict[str, Any]] = []
    if history:
        msgs.extend(history)

    msgs.append({"role": "user", "content": prompt})

    response = await agent.ainvoke({ 'messages': msgs })

    return response