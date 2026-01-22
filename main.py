from agent import FileOrganizerAgent
from ui import *
from utils import *

# Total amount of retried before exiting if the LLM fails to generate a proper output with the data being refed
MAX_RETRIES = 3

if __name__ == "__main__":
    path = select_folder()

    if not path:
        show_info("Cancelled", "No folder selected.")
        exit()

    user_notes = ask_user_input(
        "Optional Instructions",
        "Add any instructions for organizing your files:"
    ) or ""

    agent = FileOrganizerAgent()
    files, folders = agent.scan_directory(path)

    if not files:
        show_info("Empty Folder", "No files found in this directory.")
        exit()

    # Create stable ID mapping
    file_objects = [
        {"id": i, "name": fname}
        for i, fname in enumerate(files)
    ]

    # Error counter for how many times we had to refeed the llm on bad data return
    attempts = 0
    user_errors = ""
    while True:
        plan = agent.get_plan(file_objects, folders, path, user_notes, user_errors)

        # Here we are validating if there's an errors
        errors = validate_plan(plan, file_objects, folders)
        if errors:
            attempts += 1
            if attempts > MAX_RETRIES:
                fatal_error(
                    "The AI failed to generate a valid plan after multiple attempts.\n\n"
                    "Please try again or adjust your instructions."
                )
            error_text = "\n".join(errors)
            # Add feedback to the agent
            user_errors = f"\nThe previous plan had the following errors:\n{error_text}\nPlease fix them."
            continue

        # Reset the user errors
        user_errors = ""

        plan_text = format_plan(plan, file_objects)
        choice = show_plan_and_confirm(plan_text)

        if choice == "apply":
            agent.execute(path, plan, file_objects)
            show_info("Success", "Files organized successfully.")
            break

        elif choice == "refine":
            feedback = ask_user_input(
                "Refine Plan",
                "What would you like to change?"
            )

            if not feedback:
                show_info("Cancelled", "No feedback provided.")
                break

            user_notes += f"\nUser feedback: {feedback}"

        elif choice == "cancel":
            show_info("Cancelled", "Operation cancelled.")
            break
        else:
            show_info("Cancelled", "Operation cancelled.")
            break



