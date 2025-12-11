import asyncio
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.mcp import MCPServerStreamableHTTP
from dotenv import load_dotenv
import os
from .tools import list_files, read_file, rename_file
from pydantic import BaseModel

class Item(BaseModel):
    question: str

class DeepSeekAgent:
    def __init__(self):
        load_dotenv()
        self.model = OpenAIChatModel(
                'deepseek-chat',
                provider=OpenAIProvider(
                    base_url='https://api.deepseek.com', api_key=os.environ.get('DEEPSEEK_API_KEY')
                ),)

        self.agent = Agent(self.model, system_prompt="You are an experienced programmer.", tools=[list_files, rename_file, read_file])
    
    def run_sync(self, question: str, history: list):
        return self.agent.run_sync(question, message_history=history)
    
    async def run(self, question: str, history: list):
        return await self.agent.run(question, message_history=history)



def main():
    #agent = Agent(model, system_prompt="You are an experienced programmer.", tools=[list_files, rename_file, read_file])
    agent = DeepSeekAgent()
    history = []
    while True:
        user_input = input("Enter your command (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        response = agent.run_sync(user_input, message_history=history)
        history = list(response.all_messages())
        print(response)

async def mcp_client():
    server = MCPServerStreamableHTTP('http://localhost:8000/mcp')
    model = OpenAIChatModel(
            'deepseek-chat',
            provider=OpenAIProvider(
                base_url='https://api.deepseek.com', api_key=os.environ.get('DEEPSEEK_API_KEY')
            ),)
    agent = Agent(model, toolsets=[server], system_prompt="You are an experienced programmer.")
    async with agent:
        history = []
        while True:
            user_input = input("Enter your command (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break
            response = await agent.run(user_input, message_history=history)
            history = list(response.all_messages())
            print(response)

if __name__ == "__main__":
    #asyncio.run(mcp_client())
    main()