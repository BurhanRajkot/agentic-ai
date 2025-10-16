import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.delete_file import schema_delete_file
from call_functions import call_function

# ✅ Memory integration
from memory import init_db, save_message, load_messages


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    system_prompt = """
    You are a helpful AI coding agent.
    When a user asks a question or makes a request, make a function call plan.
    You can perform operations like listing files, reading/writing files, and executing Python files.
    All paths you provide should be relative to the working directory.
    """

    if len(sys.argv) < 2:
        print("Bro, I need a prompt!")
        sys.exit(1)

    prompt = sys.argv[1]
    verbose_flag = len(sys.argv) == 3 and sys.argv[2] == "--verbose"

    # Initialize DB and load messages
    init_db()
    messages = load_messages()

    # Add current user input
    user_message = types.Content(role="user", parts=[types.Part(text=prompt)])
    messages.append(user_message)
    save_message("user", prompt)

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

    generate_content(client, messages, config, verbose_flag)


def generate_content(client, messages, config, verbose):
    MAX_ITERATIONS = 25

    for iteration in range(MAX_ITERATIONS):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=messages,
                config=config
            )

            if verbose:
                print(f"\n--- Iteration {iteration + 1} ---")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            if not response.function_calls:
                print("Final response:")
                print(response.text)
                save_message("assistant", response.text)
                break

            for candidate in response.candidates:
                messages.append(candidate.content)
                save_message("assistant", candidate.content.parts[0].text)

            function_responses = []
            for function_call_part in response.function_calls:
                result = call_function(function_call_part, verbose)
                function_responses.append(result.parts[0])
                save_message("tool", result.parts[0].text if hasattr(result.parts[0], "text") else str(result.parts[0]))

            messages.append(types.Content(role="tool", parts=function_responses))

        except Exception as e:
            print(f"Error during generation: {e}")
            break
    else:
        print(f"\nReached maximum iterations ({MAX_ITERATIONS}). Agent may not have completed its task.")


if __name__ == "__main__":
    main()
