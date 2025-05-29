# tools/local_web_server.py

import http.server
import socketserver
import os
import threading
import socket # For checking if port is in use

# Define a custom handler to serve files from the specified directory
class CustomHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

def is_port_in_use(port):
    """Checks if a given port is currently in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def serve_directory(directory_path, port):
    """Starts the HTTP server in a new thread."""
    try:
        os.chdir(directory_path) # Change current working directory for the server
        
        # Configure the handler with the specified directory
        handler = lambda *args, **kwargs: CustomHTTPHandler(*args, directory=directory_path, **kwargs)
        httpd = socketserver.TCPServer(("", port), handler)
        
        print(f"Serving files from directory: {os.path.abspath(directory_path)}")
        print(f"Server started at http://localhost:{port}/")
        print("\nPress Ctrl+C in this terminal to stop the server.")
        
        httpd.serve_forever() # This will block until Ctrl+C

    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Error: Port {port} is already in use. Please choose a different port.")
        else:
            print(f"An OS error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while starting the server: {e}")
    finally:
        # Ensure we change back to the original directory (or a safe one)
        # This is tricky because os.chdir is global. For H7T, it's simpler
        # to just note that the script changes directory.
        pass # The H7T runner will likely re-initialize for next tool

def main():
    """
    Starts a local web server to serve static files from a specified directory.
    """
    print("--- Local Web Server ---")
    print("This tool will serve files from a chosen directory on a local port.")

    while True:
        server_dir = input("Enter the path to the directory to serve (e.g., './my_website_folder'): ").strip()
        if not server_dir:
            print("Directory path cannot be empty.")
            continue
        if not os.path.isdir(server_dir):
            print(f"Error: '{server_dir}' is not a valid directory.")
            continue
        break

    default_port = 8000
    while True:
        try:
            port_input = input(f"Enter the port number (default: {default_port}): ").strip()
            port = int(port_input) if port_input else default_port
            if not 1024 <= port <= 65535:
                print("Port number must be between 1024 and 65535 (inclusive).")
            elif is_port_in_use(port):
                print(f"Port {port} is already in use. Please choose a different port.")
            else:
                break
        except ValueError:
            print("Invalid port number. Please enter a number.")
        except Exception as e:
            print(f"An error occurred while checking port: {e}")

    # Start the server. We don't need threading here as H7T tools block
    # and the user expects the server to run until explicitly stopped (Ctrl+C).
    serve_directory(server_dir, port)

    print("\nServer stopped.") # This will only print after httpd.serve_forever() exits (e.g., by Ctrl+C)

# Do NOT call main() here. H7T does that automatically.
