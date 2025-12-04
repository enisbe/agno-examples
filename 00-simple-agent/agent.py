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
    instructions="Write a report on the topic. Output only the report.",
    markdown=True,
)
agent.print_response("Trending startups and products.")