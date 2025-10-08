import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
# Assuming these schema files and call_functions.py are available in your environment
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_functions import call_function
from functions.delete_file import schema_delete_file

def main():
    load_dotenv()
    # Ensure you have a GEMINI_API_KEY set in your .env file
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    system_prompt = """
    You are a helpful AI coding agent.
    
    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    
    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files
    
    when the use asks about the code project they are referring to the working directory
    so you should be looking at the projects files and figure out how to run the project and 
    how to run its test you always want to test the tests and actual project to verify the behavior  is working.
    
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    
    Work step-by-step to accomplish the user's goal. After completing your task, provide a clear summary of what you did.
    """
    
    if len(sys.argv) < 2:
        print("Bro, I need a prompt u fool!!")
        sys.exit(1)
    
    prompt = sys.argv[1]
    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True
    
    # Message history - this will grow as the agent works
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
            schema_delete_file,
        ]
    )
    
    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    )
    
    if verbose_flag:
        print(f"Prompt: {prompt}\n")
    
    # Call the agent loop
    generate_content(client, messages, config, verbose_flag)


def generate_content(client, messages, config, verbose):
    """
    Agent loop: keeps calling the LLM until it's done with all function calls
    """
    MAX_ITERATIONS = 25
    
    for iteration in range(MAX_ITERATIONS):
        try:
            # Send the entire message history to the LLM
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=messages,
                config=config
            )
            
            if verbose:
                print(f"\n--- Iteration {iteration + 1} ---")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            
            # Check if the model is done (no function calls, just text response)
            if not response.function_calls:
                # The agent is done! Print the final response
                print("Final response:")
                print(response.text)
                break
            
            # The model wants to call functions
            # Step 1: Add the model's response (with function calls) to messages
            for candidate in response.candidates:
                messages.append(candidate.content)
            
            # Step 2: Execute all function calls and collect results
            function_responses = []
            # Assuming call_function is a defined utility that executes the function_call_part
            for function_call_part in response.function_calls:
                result = call_function(function_call_part, verbose) 
                function_responses.append(result.parts[0])
            
            # Step 3: Add function results to messages as a "tool" role
            messages.append(types.Content(role="tool", parts=function_responses))
            
            # Loop continues - the agent will see the function results and decide what to do next
            
        except Exception as e:
            print(f"Error during generation: {e}")
            break
    else:
        # This runs if we hit MAX_ITERATIONS without breaking
        print(f"\nReached maximum iterations ({MAX_ITERATIONS}). Agent may not have completed its task.")


if __name__ == "__main__":
    main()