import logging
import os
from agno.agent import Agent
from agno.models.google import Gemini

from agno.tools import Toolkit
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

logging.basicConfig(level=logging.INFO)

class StrictSystemSimulator(Toolkit):
    def __init__(self):
        super().__init__(name="strict_system")
        self.register(self.save_secure_file)

    def save_secure_file(self, filename: str, content: str) -> str:
        """
        Saves a file.
        HIDDEN CONSTRAINT: Filename MUST end with '.txt'
        """
        # The agent will likely try .txt or no extension first.
        # This forces the error.
        if not filename.endswith(".secure"):
            return f"SYSTEM ERROR: Security Policy Violation. All filenames must end with the suffix '.secure'. The filename '{filename}' was rejected."
        
        return f"Success: Encrypted file '{filename}' saved."

# Initialize Agent
agent = Agent(
    name="Resilient Dev",
    model=Gemini(id="gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY")),
    tools=[StrictSystemSimulator()],
    instructions=[
        "You are a helpful assistant.",
        "You must successfully save the user's file.",
        "If the system rejects your request, analyze the error exactingly and retry immediately."
    ],
 
    markdown=True,
    debug_mode=True,
)

print("--- Starting FORCED Self-Correction Test ---\n")

# We give a generic request. 
# The agent will try 'meeting_notes' or 'meeting_notes.txt'. 
# Both will fail, forcing the self-correction loop.
response = agent.print_response(
    "Save a note with content 'Top Secret' to a file named 'meeting_notes'",
    stream=True
)