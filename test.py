from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
def main():
    working_directory = "calculator"
    #print(write_file("calculator", "notes.txt", "this is my first note"))
    
    # Test 2: File in nested directory structure
    #print(write_file("calculator", "data/results/output.txt", "calculation results go here"))
    
    # Test 3: Security test - trying to write outside working directory
    #print(write_file("calculator", "../secrets.txt", "this should be blocked"))
    
    #print(write_file(working_directory, "lorem.txt", "wait, this isn't lorem ipsum u dumb ass mother fucking son of a bitch go and fuck your self u asshole"))
    
    print(run_python_file(working_directory, "main.py" , ["3 + 6"]))
    #print(run_python_file("working_directory", "test.py"))

main()