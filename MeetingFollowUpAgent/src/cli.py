import json
import os
from typing import List
from src.models import MeetingSummary, ActionItem
from src.config import Config

class CLI:
    def __init__(self):
        pass

    def display_summary(self, summary: MeetingSummary):
        print("\n" + "="*50)
        print("MEETING SUMMARY")
        print("="*50)
        print(summary.summary)
        
        print("\n--- TOPICS ---")
        for t in summary.topics:
            print(f"- {t}")
            
        print("\n--- DECISIONS ---")
        for d in summary.decisions:
            status = "Confirmed" if d.is_confirmed else "Proposed"
            print(f"[{status}] {d.description}")
            print(f"  (Supporting: '{d.supporting_text}')")
            
        print("\n--- OPEN QUESTIONS ---")
        for q in summary.open_questions:
            print(f"- {q}")
            
        print("\n--- RISKS AND CONCERNS ---")
        for r in summary.risks_and_concerns:
            print(f"- {r}")
            
        print("\n--- MISSING/UNCLEAR INFORMATION ---")
        for m in summary.missing_or_unclear_information:
            print(f"- {m}")
            
        print("\n" + "="*50)

    def review_actions(self, actions: List[ActionItem]) -> List[dict]:
        print("\n--- ACTION REVIEW ---")
        if not actions:
            print("No actions found.")
            return []

        approved_actions = []
        for i, action in enumerate(actions, 1):
            status = "Confirmed" if action.is_confirmed else "Proposed"
            print(f"\nAction #{i}: [{status}]")
            print(f"Description: {action.description}")
            print(f"Owner: {action.owner or 'Unassigned'}")
            print(f"Deadline: {action.deadline or 'None'}")
            print(f"Supporting Text: '{action.supporting_text}'")
            
            while True:
                choice = input("Approve (a), Reject (r), Modify (m)? [a/r/m]: ").strip().lower()
                if choice == 'a':
                    approved_actions.append(action.model_dump())
                    print("Action approved.")
                    break
                elif choice == 'r':
                    print("Action rejected.")
                    break
                elif choice == 'm':
                    desc = input(f"Description [{action.description}]: ").strip() or action.description
                    owner = input(f"Owner [{action.owner or ''}]: ").strip() or action.owner
                    deadline = input(f"Deadline [{action.deadline or ''}]: ").strip() or action.deadline
                    
                    modified_action = action.model_copy(update={
                        "description": desc,
                        "owner": owner if owner else None,
                        "deadline": deadline if deadline else None,
                        "is_confirmed": True # Modifying implicitly confirms it
                    })
                    approved_actions.append(modified_action.model_dump())
                    print("Action modified and approved.")
                    break
                else:
                    print("Invalid choice. Please enter a, r, or m.")
                    
        return approved_actions

    def save_actions(self, actions: List[dict]):
        if not actions:
            print("\nNo actions to save.")
            return
            
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        
        # Load existing actions if file exists
        existing_actions = []
        if os.path.exists(Config.OUTPUT_FILE):
            with open(Config.OUTPUT_FILE, 'r', encoding='utf-8') as f:
                try:
                    existing_actions = json.load(f)
                except json.JSONDecodeError:
                    existing_actions = []
                    
        existing_actions.extend(actions)
        
        with open(Config.OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(existing_actions, f, indent=2)
            
        print(f"\nSaved {len(actions)} approved actions to {Config.OUTPUT_FILE}")
