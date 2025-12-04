from typing import List
from pydantic import BaseModel, Field
from agno.agent import Agent
 
from agno.models.google import Gemini
import os

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
# 1. Define the Structure of the Plan
class Step(BaseModel):
    step_number: int
    instruction: str = Field(..., description="Detailed instruction for the worker agent")
    expected_output: str = Field(..., description="What the result should look like")

class Plan(BaseModel):
    goal: str
    steps: List[Step]

# 2. Create the Planner Agent
planner = Agent(
    model=Gemini(id="gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY")),  # Or a reasoning model like o1/Claude 3.5 Sonnet
    description="You are a senior project manager. Break down complex tasks into small, actionable steps.",
    output_schema=Plan, # <--- This forces the agent to output the Plan object above
)

# Example Usage
task = "Research the current state of Quantum Computing and write a short blog post about it."
plan_response = planner.run(task)
plan = plan_response.content # This is now a python object with a .steps list



# 3. Create the Worker Agent
worker = Agent(
    model=Gemini(id="gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY")),
    description="You are a skilled researcher and writer. Execute instructions precisely.",
    instructions=["Always check the context of previous steps before starting new ones."],
    markdown=True
)

print(f"Goal: {plan.goal}\n")

# 4. The Execution Loop
context = "" # We will build a context string to keep track of progress

for step in plan.steps:
    print(f"--- Executing Step {step.step_number}: {step.instruction} ---")
    
    # Create a prompt that includes the current step AND the context of what has been done
    step_prompt = (
        f"CURRENT TASK: {step.instruction}\n"
        f"EXPECTED OUTPUT: {step.expected_output}\n\n"
        f"PREVIOUS WORK CONTEXT:\n{context}"
    )
    
    # Run the worker
    response = worker.run(step_prompt)
    
    # Update context with the result so the next step knows what happened
    context += f"\n[Step {step.step_number} Result]: {response.content}\n"
    print(f"Done.\n")

# 5. Final Output Generation (Optional)
final_response = worker.run(f"Using the following work history, assemble the final request:\n{context}")
print(final_response.content)


 
