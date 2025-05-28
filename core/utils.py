ENCRYPTION_KEY = "98706547"

def list_tools(tool_folder="tools"):
    import os
    return [f[:-3] for f in os.listdir(tool_folder) if f.endswith(".py") and f != "__init__.py"]