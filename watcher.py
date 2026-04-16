import time
import subprocess
import os
import csv
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from colorama import Fore, Style, init
init()

print(Fore.CYAN + "🔥 Welcome to My App 🔥")
print(Fore.GREEN + "✔ Success Loaded!")
print(Fore.RED + "✖ Error Example")
print(Style.RESET_ALL)

# ===================== CONFIGURATION ====================

# The CSV file containing all the repositories to watch
CSV_FILE = 'repos.csv'

# Time (in seconds) to wait after a file event occurs 
# to ensure the file has finished writing (prevents incomplete commits).
PROCESSING_DELAY = 3 

# ===================== HANDLER CLASS ====================

class GitChangeHandler(FileSystemEventHandler):
    """
    Handles file system events for a specific repository instance 
    and triggers the Git workflow.
    """
    def __init__(self, repo_path, remote_url):
        self.repo_path = repo_path
        self.remote_url = remote_url
        print(f"\n[INIT] 🔗 Initializing Watcher for: {self.repo_path}")
        self.initialize_repo()

    def initialize_repo(self):
        """
        Ensures the directory is a valid Git repository and sets the remote origin.
        """
        if not os.path.exists(self.repo_path):
            print(f"🚨 ERROR: Directory not found: {self.repo_path}")
            return

        # 1. Check if it's a git repo
        try:
            subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], 
                           cwd=self.repo_path, check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print(f"⚠️ WARNING: {self.repo_path} is not a Git repository. Running git init...")
            try:
                subprocess.run(["git", "init"], cwd=self.repo_path, check=True)
            except subprocess.CalledProcessError:
                print(f"🚨 FATAL: Could not initialize Git repo in {self.repo_path}. Skipping.")
                return

        # 2. Set the remote origin if it doesn't exist or is incorrect
        try:
            # Check if the remote origin is already set
            remote_check = subprocess.run(["git", "remote", "get-url", "origin"], cwd=self.repo_path, capture_output=True, text=True)
            if not remote_check.stdout.strip():
                print(f"   Setting remote origin to: {self.remote_url}")
                subprocess.run(["git", "remote", "add", "origin", self.remote_url], 
                                cwd=self.repo_path, check=True)
        except Exception as e:
            print(f"   Could not set remote origin. Check URL/credentials. Error: {e}")

    def on_any_event(self, event):
        """
        Triggered whenever any event occurs.
        """
        if event.is_directory:
            return

        print(f"\n[EVENT] Detected event on {os.path.basename(event.src_path)}")
        
        # Delay to ensure file write completion
        time.sleep(PROCESSING_DELAY)
        
        self.git_commit_and_push()

    def git_commit_and_push(self):
        """Handles the git commit, add, and push cycle."""
        
        # ... (other setup code remains the same)

        try:
            print("\n⚡️ Starting Git Workflow for:", self.repo_name)
            
            # 1. Stage files
            subprocess.run(["git", "add", "."], cwd=self.repo_path, check=True)
            print("✅ Staged files successfully.")

            # 2. Commit files
            subprocess.run(["git", "commit", "-m", f"✨ Auto commit via file watcher"], 
                           cwd=self.repo_path, check=True)
            print("✅ Changes committed successfully.")

            # --- CRITICAL FIX HERE ---
            # Push the code and set the remote upstream branch.
            # Using 'master' based on your log. If your remote branch is 'main', change 'master' to 'main'.
            git_push_command = ["git", "push", "--set-upstream", "origin", "master"]
            
            print(f"   Attempting to push: {' '.join(git_push_command)}...")
            subprocess.run(git_push_command, cwd=self.repo_path, check=True)
            print("Successfully pushed changes!")

        except subprocess.CalledProcessError as e:
            print(f"🚨 Error during Git operation: {e}")
        except subprocess.CalledProcessError as e:
            # This block now catches the specific push failure
            print(f"🚨 Failed to push commits. Ensure credentials and remote are set up correctly.")
            print(f"Detailed error: {e}")
        except Exception as e:
            print(f"🚨 An unexpected error occurred: {e}")


    def git_commit_and_push_old_v1(self):
        """
        Executes the full git cycle: add, commit, and push for this specific repo.
        """
        print("------------------------------------------------------")
        print(f"⚡️ Starting Git Workflow for: {os.path.basename(self.repo_path)}...")
        
        try:
            # 1. STAGE CHANGES
            subprocess.run(["git", "add", "."], cwd=self.repo_path, check=True, capture_output=True)
            print("✅ Staged files successfully.")

            # Check if there are any changes to commit
            result = subprocess.run(["git", "status", "--porcelain"], cwd=self.repo_path, capture_output=True, text=True)
            if not result.stdout.strip():
                print("🛑 No changes detected. Skipping commit/push.")
                return

            # 2. COMMIT
            subprocess.run(["git", "commit", "-m", "✨ Auto commit via file watcher"], cwd=self.repo_path, check=True)
            print("✅ Changes committed successfully.")

            # 3. PUSH
            subprocess.run(["git", "push"], cwd=self.repo_path, check=True)
            print(f"\n🎉 Successfully PUSHED to {self.remote_url}!")

        except subprocess.CalledProcessError as e:
            print("\n\n🚨 -------------------------------------------------")
            print(f"❌ GIT ERROR occurred for {os.path.basename(self.repo_path)}!")
            print(f"   Command failed: {e.cmd}")
            print(f"   Error details: {e.stderr.decode('utf-8')}")
            print("🚨 -------------------------------------------------")
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")

# ===================== MAIN MANAGER ====================

def run_watcher_manager():
    """
    Reads the CSV and starts a separate monitoring thread for each entry.
    """
    print("==============================================================")
    print("       MULTI-REPO AUTOMATIC GIT WATCHER STARTED")
    print("==============================================================")

    try:
        with open(CSV_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            
            # Dictionary to hold the thread instances
            threads = []

            for row in reader:
                local_path = row.get('local_path', '').strip()
                repo_url = row.get('repo_url', '').strip()

                if local_path and repo_url:
                    # 1. Create the handler for this specific repo
                    handler = GitChangeHandler(local_path, repo_url)
                    
                    # 2. Start the watchdog observer
                    observer = Observer()
                    observer.schedule(handler, local_path, recursive=True)
                    
                    # 3. Start the observer in a separate thread
                    thread = threading.Thread(target=observer.start)
                    thread.daemon = True  # Allows the program to exit even if threads are running
                    thread.start()
                    threads.append(thread)
                else:
                    print(f"🛑 Skipping row due to missing data: {row}")
                    
            # Keep the main thread alive indefinitely
            print("\n\n==============================================================")
            print("✅ All monitors initialized. Waiting for file changes...")
            print("==============================================================")
            
            # Use a simple loop to keep the manager running
            while True:
                time.sleep(1)

    except FileNotFoundError:
        print(f"\nFATAL ERROR: The CSV file '{CSV_FILE}' was not found. Please create it.")
    except Exception as e:
        print(f"\nAn unexpected error occurred in the manager: {e}")

if __name__ == "__main__":
    run_watcher_manager()
