import os
from agno.agent import Agent
 
from agno.models.google import Gemini
from agno.tools.hackernews import HackerNewsTools
from agno.tools.duckduckgo import DuckDuckGoTools

from dotenv import load_dotenv  
load_dotenv()  # Load environment variables from .env file

from agno.db.sqlite import SqliteDb
# from agno.db.in_memory import InMemoryDb

# Setup the SQLite database
db = SqliteDb(db_file="tmp/data.db")

agent = Agent(
    model=Gemini(id="gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY")),
    db = db,
    tools=[ DuckDuckGoTools()],
    instructions="Write a report on the topic. Output only the report.", 
    
    markdown=True,
    debug_mode=True,
    read_chat_history= True,
    add_history_to_context=True,

    num_history_runs = 3
)
agent.print_response("Trending startups and products.", stream=True)

agent.print_response("Summarize these in one paragraph.")