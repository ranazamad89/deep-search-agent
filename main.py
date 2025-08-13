

import os
import asyncio
from dotenv import load_dotenv
from typing import List, Dict, Any
from tavily import AsyncTavilyClient
from openai import AsyncOpenAI
from agents import Agent, Runner, function_tool, ModelSettings, OpenAIChatCompletionsModel, RunContextWrapper, set_tracing_disabled
from dataclasses import dataclass
import datetime
load_dotenv()
set_tracing_disabled(disabled=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")   # Get API keys from environment variables.
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not gemini_api_key or not tavily_api_key:        # Check to make sure the required API keys are available.
    raise ValueError("Please ensure GEMINI_API_KEY and TAVILY_API_KEY are set in your .env file.")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"       # Configure the base URL for the Gemini API.

# Initialize the AsyncOpenAI-compatible client for Gemini.
external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url=BASE_URL)

# Initialize the Tavily client for web searches.
tavily_client = AsyncTavilyClient(api_key=tavily_api_key)

# Initialize the chat model using the Gemini client.
model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash", 
    openai_client=external_client
)
# --- Data Models and Tools ---
@dataclass
class UserContext:
    """A data class to hold user-specific context."""
    username: str
    email: str | None = None

@function_tool()
async def get_user_info(local_context: RunContextWrapper[UserContext]) -> str:
    """
    Retrieves the username and email from the user's context. This is an example tool
    that the agent can use to get information about the current user.
    """
    user_info = f"User Information:\nUsername: {local_context.context.username}"
    if local_context.context.email:
        user_info += f"\nEmail: {local_context.context.email}"
    return user_info

@function_tool
async def tavily_web_search(local_context: RunContextWrapper[UserContext], query: str, max_results: int = 5) -> str:
    """
    Performs a web search using the Tavily API and returns the results.
    Args:
        query: The search query string.
        max_results: The maximum number of search results to return.
    Returns:
        A formatted string of the search results with their titles, URLs, and snippets.
    """
    response = await tavily_client.search(query=query, max_results=max_results)
    
    formatted_results = []
    if response and response.get('results'):
        for result in response['results']:
            formatted_results.append(
                f"Title: {result['title']}\nURL: {result['url']}\nContent: {result['content']}"
            )
    else:
        return "No search results found."

    return "\n\n".join(formatted_results)

# --- Main Application Logic ---

async def print_streamed_output(text: str):
    """
    Simulates streaming by printing a string character by character with a delay.
    This provides a visual effect of a real-time response.
    """
    for char in text:
        print(char, end='', flush=True)
        await asyncio.sleep(0.01)
    print() # Print a newline at the end

async def main():
    """
    The main asynchronous function to run the deep search agent.
    This function handles the user input loop and agent execution.
    """
    print("\n🔎 DEEP SEARCH AGENT")
    print("-" * 30)
    print("A research agent that uses Tavily for multi-step web searches.")
    print("Note: Output is now 'streamed' for a better user experience!")

    # Instructions for the agent, defining its persona and task.
    agent_instructions = """You are a meticulous research assistant specializing in performing deep, multi-step searches. Your task is to:
1.  **Analyze the User's Request**: Break down the user's question into 2-3 specific, actionable sub-questions or search queries.
2.  **Execute Searches**: For each sub-question, use the `tavily_web_search` tool.
3.  **Synthesize Findings**: Combine the information from all your search results to provide a comprehensive, well-structured, and accurate answer.
4.  **Cite Sources**: Mention the URLs or sources you used to build your final answer, checking for the most relevant and reliable information.
5.  **Avoid Single-Query Answers**: Do not answer the question with only one search result. You must perform multiple searches to demonstrate a deep understanding of the topic.
"""
    
    # Create the agent instance with its instructions, model settings, and tools.
    deep_search_agent = Agent(
        name="Deep Search Agent",
        instructions=agent_instructions,
        model_settings=ModelSettings(temperature=0.3, max_tokens=5000),
        model=model,
        tools=[tavily_web_search]  # Use only the functional Tavily tool.
    )

    # Example user context data.
    user_context_data = UserContext(username="TestUser", email="test@example.com")
    
    is_running = True
    while is_running:
        # Prompt for user input.
        user_question = input("Write a question for the Deep Search Agent (or 'exit' to stop): ")
        
        if user_question.lower() == 'exit':
            is_running = False
            print("Exiting the Deep Search Agent. Goodbye!")
            continue

        print("🔎 Searching for answers... Please wait.", flush=True)

        # Run the agent with the user's question and the context data.
        # This is an asynchronous operation, so we await the result.
        result_deep_search = await Runner.run(
            starting_agent=deep_search_agent,
            input=user_question,
            context=user_context_data,
        )
        
        print("\n" + "="*50)
        print("Agent's final output:\n")
        # Use the new streaming function to print the result.
        await print_streamed_output(result_deep_search.final_output)
        print("="*50)

# Entry point for the script.
if __name__ == "__main__":
    asyncio.run(main())




