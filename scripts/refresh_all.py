import os
import subprocess
import argparse
from dotenv import load_dotenv

load_dotenv()

def parse_args():
    parser = argparse.ArgumentParser(description="Run Contentful health checks")
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of entries to print (default: 5)"
    )
    parser.add_argument(
         "--exclude-status",
         nargs="+",
         default=[],
         help="Exclude entries with this in_operation status. No default exclusions."
    )
    return parser.parse_args()

SPACE_ID = os.environ["CONTENTFUL_SPACE_ID"]
MANAGEMENT_TOKEN = os.environ["CONTENTFUL_MANAGEMENT_ACCESS_TOKEN"]


# def run(command: list[str]) -> None:
#     print(f"Running: {' '.join(command)}")
#     subprocess.run(command, check=True)

def run(command: list[str]) -> None:
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(command)}")

def main():
    args = parse_args()

    run([
        "npx", "contentful", "space", "export",
        "--space-id", SPACE_ID,
        "--management-token", MANAGEMENT_TOKEN,
        "--environment-id", "master",
        "--export-dir", "data",
        "--content-file", "export.json"
    ])
    run(["python3", "scripts/build_broken_link_lookup.py"])

    run_check_command = ["python3", "scripts/run_check.py", "--limit", str(args.limit)]
    if args.exclude_status:
        run_check_command += ["--exclude-status"] + args.exclude_status

    run(run_check_command)

if __name__ == "__main__":
    main()