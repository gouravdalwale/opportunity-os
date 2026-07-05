import asyncio
import json
import sys
from utils.gemini import ask_opportunity_gemini, ask_opportunity_gemini_with_tools
from utils.skill_loader import load_skill
from mcp_server.client import MCPClient


async def async_find_opportunities(profile: str) -> str:
    """
    Asynchronously coordinates the opportunity discovery process:
    1. Loads the opportunity agent's skill guidelines.
    2. Spawns the MCP server subprocess and connects to it over stdio.
    3. Retrieves search tools registered on the server.
    4. Passes the profile analysis and tool schemas to the Groq/Gemini client.
    5. Executes any tool calls requested by the model and feeds results back.
    6. Returns the final curated recommendation list.
    """
    skill = load_skill("skills/opportunity/SKILL.md")

    # Base prompt to explain context and define the task
    prompt = f"""
{skill}

----------------------------------------
PROFILE ANALYSIS
----------------------------------------

{profile}

----------------------------------------
TASK
----------------------------------------

Recommend the best career opportunities according to your skill definition.
You have tools available to search the opportunity database. Use them to get real results.
"""

    print("🚀 Opportunity Agent connecting to MCP Server...", file=sys.stderr)
    try:
        async with MCPClient() as client:
            # Discover tools from MCP server
            mcp_tools = await client.get_available_tools()
            print(f"DEBUG: MCP tools found: {[t.name for t in mcp_tools]}", file=sys.stderr)
            
            # Map tools to OpenAI/Groq function calling format
            openai_tools = []
            for tool in mcp_tools:
                openai_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                })
            
            # Call the LLM with the list of tools
            print("DEBUG: Sending initial prompt and tool definitions to LLM...", file=sys.stderr)
            message = ask_opportunity_gemini_with_tools(prompt, tools=openai_tools)
            
            # Check if the LLM wants to call any tools
            if hasattr(message, "tool_calls") and message.tool_calls:
                print(f"DEBUG: LLM requested {len(message.tool_calls)} tool calls.", file=sys.stderr)
                tool_results_summary = []
                
                # Execute each tool call requested by the LLM
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    print(f"DEBUG: Executing tool '{tool_name}' with args {tool_args}...", file=sys.stderr)
                    tool_result = await client.call_tool(tool_name, tool_args)
                    
                    # Store tool execution result
                    tool_results_summary.append(
                        f"### Results from Tool '{tool_name}' (Args: {tool_args}):\n{tool_result}"
                    )
                
                # Feed the real data back to the LLM for final generation
                final_prompt = f"""
{skill}

----------------------------------------
PROFILE ANALYSIS
----------------------------------------

{profile}

----------------------------------------
REAL OPPORTUNITIES RETRIEVED VIA MCP TOOLS
----------------------------------------

The opportunity-search tools successfully returned the following data from the database:

{"\n\n".join(tool_results_summary)}

----------------------------------------
TASK
----------------------------------------

Recommend the best career opportunities according to your skill definition.
You MUST prioritize and incorporate the real opportunities listed in the 'REAL OPPORTUNITIES RETRIEVED VIA MCP TOOLS' section above.
Provide your recommendations exactly in the required layout format.
"""
                print("DEBUG: Sending tool results to LLM for final recommendations...", file=sys.stderr)
                return ask_opportunity_gemini(final_prompt)
            else:
                # Fallback to direct output if model decides no tool calls are needed
                print("DEBUG: LLM returned direct response without tool calls.", file=sys.stderr)
                if hasattr(message, "content") and message.content:
                    return message.content
                return str(message)
                
    except Exception as e:
        # Fallback to standard execution without tools to ensure robustness
        print(f"⚠️ Warning: MCP Integration encountered an error: {str(e)}", file=sys.stderr)
        print("Falling back to standard career recommendation without tools...", file=sys.stderr)
        return ask_opportunity_gemini(prompt)


def find_opportunities(profile: str) -> str:
    """
    Synchronous entrypoint for the Opportunity Agent.
    Coordinates with the async MCP server and client using asyncio.run.
    """
    return asyncio.run(async_find_opportunities(profile))