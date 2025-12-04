from agno.agent.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb
# Setup the SQLite database
db = SqliteDb(db_file="tmp/data.db")
 
from dotenv import load_dotenv  
load_dotenv()  # Load environment variables from .env file
import os
 
agent = Agent(
    model=Gemini(id="gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY")),
    db=db,
    session_id="chat_history",
    instructions="You are a helpful assistant that can answer questions about space and oceans.",
    add_history_to_context=True,
)

agent.print_response("Tell me a new interesting fact about space")
print(agent.get_chat_history())

agent.print_response("Tell me a new interesting fact about oceans")
print(agent.get_chat_history())