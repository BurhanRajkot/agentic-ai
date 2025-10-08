# Agentic AI

![Python](https://img.shields.io/badge/python-3.13-blue?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

**A Python-based AI agent for managing and interacting with code projects.**  

Agentic AI is a **smart AI assistant** that can perform various file operations, execute scripts, and even modify code files—all safely within a project’s working directory.

---
## I have pushed the env by error and that key has been deactivated so please add your own key and use that.

## Pushing the env was a rookie error so yes i have removed it from further commits but some damange has been done so again that KEY does not WORK.

## **Features**

| Feature | Description |
|---------|-------------|
| `get_files_info` | Lists all files and directories in the working directory, including sizes and types (file/folder). |
| `get_file_content` | Reads and returns the content of a file (limited to a maximum number of characters for safety). |
| `write_file` | Writes content to a file, automatically creating missing directories if needed. |
| `delete_file` | Deletes a specified file safely inside the working directory. |
| `run_python_file` | Executes a Python script with optional arguments and returns both stdout and stderr. |
| Extendable | Can be extended to support other languages like C# by adding new functions. |
| AI-Powered | Uses Gemini AI to decide which function to call based on your natural language instructions. |

---

## **Installation**

1. Clone the repository:

bash
git clone https://github.com/BurhanRajkot/agentic-ai.git
cd agentic-ai


2. Set up a Python virtual environment:

bash
python3 -m venv .venv
- source .venv/bin/activate   # Linux/macOS
- .venv\Scripts\activate      # Windows
pip install -r requirements.txt


3. Add your Gemini API key in a `.env` file:


GEMINI_API_KEY=your_api_key_here


---

## **Usage**

Run the AI agent with a prompt: These are to test if everything works on your computer.

bash
uv run main.py "Read the contents of calculator/main.py"
uv run main.py "Delete the file movie.html"
uv run main.py "Write 'Hello World' into newfile.txt"

Use `--verbose` to see detailed function calls and execution flow:


uv run main.py "List all files in calculator" --verbose

---

# Important INFO
- Use Models with 1,000,000 Quota or the one with unlimited one.
- No need to use high value LLMS as this program is not designed for that and that is waste of resource


## **Example Outputs**

### Reading a file:
Prompt: Read calculator/lorem.txt
Output:
"Lorem ipsum dolor sit amet, consectetur adipiscing elit..."

### Deleting a file:
Prompt: Delete movie.html
Output:
OK. `movie.html` has been removed from the working directory.


### Executing a Python script:\
Prompt: Run calculator/tests.py
STDOUT: Test results...
STDERR: 

---

## **Extending the AI**

1. Add a new Python function in the `functions/` folder.  
2. Create a corresponding **schema** so the AI knows how to call it.  
3. Update `call_functions.py` to handle the new function.  

You can add **C# support** by creating functions that:

- Read/write/delete `.cs` files.  
- Compile and run C# scripts via `subprocess`.  

---

## **Contributing**

1. Fork the repository.  
2. Create a new branch for your feature.  
3. Submit a pull request with a detailed description.  

---

## **License**

MIT License – free to use, modify, and distribute.  

---

## **Notes**

- All file operations are **restricted to the working directory** for security.  
- Files exceeding the configured `MAX_CHARS` will be **truncated** when read.  
- Python execution is **sandboxed** and time-limited to prevent infinite loops.  


