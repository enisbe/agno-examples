import os
from agno.agent import Agent
 
from agno.models.google import Gemini
from agno.tools.hackernews import HackerNewsTools
from agno.tools.duckduckgo import DuckDuckGoTools

from dotenv import load_dotenv  
load_dotenv()  # Load environment variables from .env file

agent = Agent(
    model=Gemini(id="gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY")),
    tools=[ DuckDuckGoTools()],
    instructions="You are helpfull assistant.",
    markdown=True,
    debug_level=2,
    debug_mode=True,
    
)
agent.cli_app(stream=True)