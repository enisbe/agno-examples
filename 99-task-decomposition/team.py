from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
# 1. Define Specialized Agents (The "Workers")
# These agents are focused on executing specific types of tasks.

researcher = Agent(
    name="Researcher",
    role="Web Researcher",
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    instructions="Find accurate and up-to-date information. Always cite your sources.",
    debug_mode=True,
)

writer = Agent(
    name="Writer",
    role="Technical Writer",
    model=OpenAIChat(id="gpt-4o"),
    instructions="Write clear, concise technical content in markdown format.",
)

reviewer = Agent(
    name="Reviewer",
    role="Quality Assurance",
    model=OpenAIChat(id="gpt-4o"),
    instructions="Review content for accuracy and clarity. Suggest specific improvements.",
)

# 2. Define the Team (The "Manager")
# The Team coordinates the agents by delegating tasks to them.

agent_team = Team(
    name="Content Production Team",
    members=[researcher, writer, reviewer],  # The workers available
    model=OpenAIChat(id="gpt-4o"),          # The brain of the manager
    instructions=[
        "You are a project manager. Your goal is to coordinate a team to complete user requests.",
        "Follow this process:",
        "1. Break the user request into a clear list of steps.",
        "2. Delegate each step to the appropriate agent (Researcher, Writer, or Reviewer).",
        "3. Review the output of each step before moving to the next.",
        "4. Consolidate the final result."
    ],
    debug_mode=True,  # Lets you see the delegation happening
    markdown=True,
)

# 3. Run the Team
# The team will now auto-generate the plan and execute it step-by-step.
agent_team.print_response(
    "Research the latest features of Python 3.13 and write a blog post about them.", 
    stream=True
)