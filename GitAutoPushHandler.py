# Version 03

import os
import time
import subprocess
import csv
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

BASE_REPO_DIR = os.path.expanduser("~/auto_git_repos")


class GitAutoPushHandler(FileSystemEventHandler):
    def __init__(self, local_path, repo_path):
        self.local_path = local_path
        self.repo_path = repo_path
        self.last_commit_time = 0

    def sync_files(self):
        for root, dirs, files in os.walk(self.local_path):
            rel_path = os.path.relpath(root, self.local_path)
            target_dir = os.path.join(self.repo_path, rel_path)

            os.makedirs(target_dir, exist_ok=True)

            for file in files:
                src = os.path.join(root, file)
                dst = os.path.join(target_dir, file)

                if not os.path.exists(dst) or os.path.getmtime(src) != os.path.getmtime(dst):
                    shutil.copy2(src, dst)

    def has_changes(self):
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        return result.stdout.strip() != ""

    def git_push(self):
        subprocess.run(["git", "add", "."], cwd=self.repo_path)

        commit = subprocess.run(
            ["git", "commit", "-m", f"Auto update {time.strftime('%Y-%m-%d %H:%M:%S')}"],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        print(commit.stdout, commit.stderr)

        push = subprocess.run(
            ["git", "push"],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        print(push.stdout, push.stderr)

    def on_any_event(self, event):
        if event.is_directory:
            return

        if time.time() - self.last_commit_time < 3:
            return

        print(f"🔄 Change detected: {event.src_path}")

        try:
            self.sync_files()

            if self.has_changes():
                print("📦 Changes found, pushing...")
                self.git_push()
                print("✅ Done")
            else:
                print("ℹ️ No changes to commit")

            self.last_commit_time = time.time()

        except Exception as e:
            print("❌ Error:", e)


def load_config(csv_file):
    configs = []
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            configs.append((row['local_path'], row['repo_url'], row['repo_name']))
    return configs


def ensure_repo(repo_url, repo_name):
    repo_path = os.path.join(BASE_REPO_DIR, repo_name)

    if not os.path.exists(repo_path):
        print(f"⬇️ Cloning {repo_name}...")
        subprocess.run(["git", "clone", repo_url, repo_path])
    else:
        print(f"✔ Repo exists: {repo_name}")

    return repo_path


def main():
    os.makedirs(BASE_REPO_DIR, exist_ok=True)

    observer = Observer()
    configs = load_config("repos.csv")

    for local_path, repo_url, repo_name in configs:
        if not os.path.exists(local_path):
            print(f"⚠️ Missing: {local_path}")
            continue

        repo_path = ensure_repo(repo_url, repo_name)

        handler = GitAutoPushHandler(local_path, repo_path)
        observer.schedule(handler, path=local_path, recursive=True)

        print(f"👀 Watching {local_path} → {repo_name}")

    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()

# Version 02

# import os
# import time
# import subprocess
# import csv
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler

# # 📁 Base directory where all repos will be cloned
# BASE_REPO_DIR = os.path.expanduser("~/auto_git_repos")


# class GitAutoPushHandler(FileSystemEventHandler):
#     def __init__(self, repo_path):
#         self.repo_path = repo_path
#         self.last_commit_time = 0

#     def on_any_event(self, event):
#         if time.time() - self.last_commit_time < 5:
#             return

#         print(f"🔄 Change detected in {self.repo_path}")

#         try:
#             subprocess.run(["git", "add", "."], cwd=self.repo_path)
#             subprocess.run(
#                 ["git", "commit", "-m", f"Auto update {time.strftime('%Y-%m-%d %H:%M:%S')}"],
#                 cwd=self.repo_path
#             )
#             subprocess.run(["git", "push"], cwd=self.repo_path)

#             print("✅ Changes pushed!")
#             self.last_commit_time = time.time()

#         except Exception as e:
#             print("❌ Error:", e)


# def load_config(csv_file):
#     configs = []
#     with open(csv_file, newline='') as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             configs.append((row['local_path'], row['repo_url'], row['repo_name']))
#     return configs


# def ensure_repo_cloned(repo_url, repo_name):
#     repo_path = os.path.join(BASE_REPO_DIR, repo_name)

#     if not os.path.exists(repo_path):
#         print(f"⬇️ Cloning {repo_name}...")
#         subprocess.run(["git", "clone", repo_url, repo_path])
#     else:
#         print(f"✔ Repo exists: {repo_name}")

#     return repo_path


# def sync_files(local_path, repo_path):
#     # Copy files from local_path → repo_path
#     for root, dirs, files in os.walk(local_path):
#         rel_path = os.path.relpath(root, local_path)
#         target_dir = os.path.join(repo_path, rel_path)

#         os.makedirs(target_dir, exist_ok=True)

#         for file in files:
#             src_file = os.path.join(root, file)
#             dest_file = os.path.join(target_dir, file)

#             try:
#                 with open(src_file, "rb") as fsrc:
#                     with open(dest_file, "wb") as fdst:
#                         fdst.write(fsrc.read())
#             except Exception as e:
#                 print(f"❌ File copy error: {e}")


# def main():
#     os.makedirs(BASE_REPO_DIR, exist_ok=True)

#     observer = Observer()
#     configs = load_config("repos.csv")

#     for local_path, repo_url, repo_name in configs:
#         if not os.path.exists(local_path):
#             print(f"⚠️ Missing local path: {local_path}")
#             continue

#         repo_path = ensure_repo_cloned(repo_url, repo_name)

#         # Initial sync
#         sync_files(local_path, repo_path)

#         handler = GitAutoPushHandler(repo_path)
#         observer.schedule(handler, path=local_path, recursive=True)

#         print(f"👀 Watching: {local_path} → {repo_name}")

#     observer.start()

#     try:
#         while True:
#             time.sleep(10)
#     except KeyboardInterrupt:
#         observer.stop()

#     observer.join()


# if __name__ == "__main__":
#     main()

# Version 01

# import os
# import time
# import subprocess
# import csv
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler


# class GitAutoPushHandler(FileSystemEventHandler):
#     def __init__(self, repo_path):
#         self.repo_path = repo_path
#         self.last_commit_time = 0

#     def on_any_event(self, event):
#         # Avoid too frequent commits
#         if time.time() - self.last_commit_time < 5:
#             return

#         print(f"🔄 Change detected in {self.repo_path}")

#         try:
#             subprocess.run(["git", "add", "."], cwd=self.repo_path)
#             subprocess.run(
#                 ["git", "commit", "-m", "Auto commit"],
#                 cwd=self.repo_path
#             )
#             subprocess.run(["git", "push"], cwd=self.repo_path)

#             print("✅ Changes pushed successfully!")
#             self.last_commit_time = time.time()

#         except Exception as e:
#             print("❌ Error:", e)


# def load_config(csv_file):
#     configs = []
#     with open(csv_file, newline='') as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             configs.append((row['local_path'], row['repo_path']))
#     return configs


# def main():
#     observer = Observer()
#     configs = load_config("repos.csv")

#     for local_path, repo_path in configs:
#         if not os.path.exists(local_path):
#             print(f"⚠️ Skipping missing path: {local_path}")
#             continue

#         event_handler = GitAutoPushHandler(repo_path)
#         observer.schedule(event_handler, path=local_path, recursive=True)

#         print(f"👀 Watching: {local_path} → {repo_path}")

#     observer.start()

#     try:
#         while True:
#             time.sleep(10)
#     except KeyboardInterrupt:
#         observer.stop()

#     observer.join()


# if __name__ == "__main__":
#     main()



