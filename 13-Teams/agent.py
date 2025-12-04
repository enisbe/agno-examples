import os
from agno.team import Team
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv 
load_dotenv()  # Load environment variables from .env file
from agno.models.google import Gemini
# Create specialized agents
news_agent = Agent(
    model=Gemini(id="gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY")),
    id="news-agent",
    name="News Agent",
    role="Get the latest news and provide summaries",
    tools=[DuckDuckGoTools()]
)

weather_agent = Agent(
    model=Gemini(id="gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY")),   
    id="weather-agent",
    name="Weather Agent",
    role="Get weather information and forecasts",
    tools=[DuckDuckGoTools()]
)

# Create the team
team = Team(
    name="News and Weather Team",
    members=[news_agent, weather_agent],    
    model=Gemini(id="gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY")),

    instructions="Coordinate with team members to provide comprehensive information. Delegate tasks based on the user's request."
)

team.print_response("What's the latest news and weather in Tokyo?", stream=True)