import asyncio
import random

from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from google.adk.runners import InMemoryRunner
from google.genai import types

from ai_agent.prompt import INSTRUCTIONS


APP_NAME="chatssd"
USER_ID=f"user-{random.randint(10, 1000)}"

chat_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="Tells the current time in a specified city.",
    instruction=INSTRUCTIONS,
    tools=[google_search],
)

runner = InMemoryRunner(
    agent=chat_agent,
    app_name=APP_NAME,
)

def create_session():
    session = asyncio.run(runner.session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID
    ))
    return session

def run_root_agent(session_id: str, new_message: str):
    content = types.Content(
        role='user', parts=[types.Part.from_text(text=new_message)]
    )
    result = ""
    for event in runner.run(
        user_id=USER_ID,
        session_id=session_id,
        new_message=content,
    ):
        if event.content.parts and event.content.parts[0].text:
            print(f'** {event.author}: {event.content.parts[0].text}')
            result += f'** {event.author}: {event.content.parts[0].text}'
    return result
