import argparse
import sys
from src.agent import MeetingAgent
from src.cli import CLI

def main():
    parser = argparse.ArgumentParser(description="Meeting Follow-up Agent")
    parser.add_argument("input_file", help="Path to the meeting notes file (txt or md)")
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            notes = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.")
        sys.exit(1)

    print("Analyzing meeting notes... Please wait.")
    
    try:
        agent = MeetingAgent()
        summary = agent.process_notes(notes)
    except Exception as e:
        print(f"Error during AI processing: {e}")
        sys.exit(1)

    cli = CLI()
    cli.display_summary(summary)
    
    approved_actions = cli.review_actions(summary.actions)
    cli.save_actions(approved_actions)

if __name__ == "__main__":
    main()
