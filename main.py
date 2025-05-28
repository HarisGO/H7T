# main.py
import os
import importlib
from core.utils import list_tools

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(r"""
 _   _  _______ _____   _____ 
| | | |/ /_   _|_   _| |__  / 
| |_| ' /  | |   | |     / /  
|  _  <   | |   | |    / /_  
|_| |_|\_\ |_|   |_|   /____| 

H7T - Modular Hacker Toolkit
""")

def main_menu():
    tools = list_tools()
    print("\nAvailable Tools:")
    for i, tool in enumerate(tools, 1):
        print(f" [{i}] {tool}")
    print(" [0] Exit")

    choice = input("\nSelect tool number: ")
    if choice == "0":
        exit()

    try:
        selected_tool = tools[int(choice) - 1]
        run_tool(selected_tool)
    except (IndexError, ValueError):
        print("Invalid selection.")
        input("Press Enter to continue...")

def run_tool(tool_name):
    try:
        module = importlib.import_module(f"tools.{tool_name}")
        if hasattr(module, "main"):
            module.main()
        else:
            print("This tool has no main() function.")
    except Exception as e:
        print(f"Failed to run tool: {e}")
    input("\nPress Enter to return to menu...")

if __name__ == "__main__":
    while True:
        clear()
        banner()
        main_menu()