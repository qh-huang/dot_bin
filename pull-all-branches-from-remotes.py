#!/usr/bin/env python3
import subprocess
import sys

def main():
    # Check if at least one argument is provided
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <remote_name1> [<remote_name2> ...]")
        sys.exit(1)

    remote_names = sys.argv[1:]
    subprocess.run(["git", "config", "advice.diverging", "false"])

    for remote_name in remote_names:
        print(f"Checking out branches from remote '{remote_name}'...")
        try:
            # Fetch all branches from the remote
            subprocess.run(["git", "fetch", remote_name])

            # Get the list of remote branches
            sha_and_remote_branches = subprocess.check_output(["git", "ls-remote", "--heads", f"{remote_name}"]).decode("utf-8").splitlines()

            branch_names = []
            for sha_and_remote_branch in sha_and_remote_branches:
                parts = sha_and_remote_branch.split()
                for part in parts:
                    if part.startswith("refs/heads/"):
                        #print(part)
                        branch_name = part[11:]
                        #print(branch_name)
                        branch_names.append(branch_name)

            for branch_name in branch_names:
                try:
                    subprocess.run(["git", "checkout", "--force", "--track", f"{remote_name}/{branch_name}"])
                except subprocess.CalledProcessError as e:
                    print(f"ERROR: {e}")

                # [TODO] Pull the latest changes from the remote branch
                #subprocess.run(["git", "pull", "--ff-only", remote_name, branch_name])

            print(f"Finished checking out branches from remote '{remote_name}'.")
        except subprocess.CalledProcessError as e:
            print(f"Error checking out branches from remote '{remote_name}': {e}")
        except FileNotFoundError:
            print("Error: Git executable not found. Please ensure Git is installed.")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
