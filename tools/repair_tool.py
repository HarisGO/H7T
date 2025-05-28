# tools/repair_tool.py
import os
import subprocess

CORE_UTILS = """# core/utils.py
ENCRYPTION_KEY = "98706547"

def list_tools(tool_folder="tools"):
    import os
    return [f[:-3] for f in os.listdir(tool_folder) if f.endswith(".py") and f != "__init__.py"]
"""

MAIN_PY = '''# main.py
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
    print("\\nAvailable Tools:")
    for i, tool in enumerate(tools, 1):
        print(f" [{i}] {tool}")
    print(" [0] Exit")

    choice = input("\\nSelect tool number: ")
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
    input("\\nPress Enter to return to menu...")

if __name__ == "__main__":
    while True:
        clear()
        banner()
        main_menu()
'''

def main():
    print("[*] Starting H7T Repair Process...\n")

    # Folders
    os.makedirs("core", exist_ok=True)
    os.makedirs("tools", exist_ok=True)

    # Repair core/utils.py
    if not os.path.exists("core/utils.py"):
        with open("core/utils.py", "w") as f:
            f.write(CORE_UTILS)
        print("[+] Restored core/utils.py")

    # Repair main.py
    if not os.path.exists("main.py"):
        with open("main.py", "w") as f:
            f.write(MAIN_PY)
        print("[+] Restored main.py")

    # Reinstall dependencies
    deps = ["psutil", "requests", "beautifulsoup4", "pillow"]
    for lib in deps:
        try:
            __import__(lib if lib != "beautifulsoup4" else "bs4")
        except ImportError:
            print(f"[-] Missing {lib}, installing...")
            subprocess.run(["pip", "install", lib])

    print("\n[✓] H7T is repaired and ready!")