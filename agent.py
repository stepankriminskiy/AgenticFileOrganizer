import os
import json
from openai import OpenAI
from prompts import *
from ui import show_loading, fatal_error
from utils import *


class FileOrganizerAgent:
    def __init__(self):
        self.client = OpenAI()
        self.history = []

    def scan_directory(self, path):
        files = []
        folders = []

        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            # We don't want hidden files
            if os.path.isfile(full_path) and is_hidden(full_path) is False:
                files.append(item)
            elif os.path.isdir(full_path):
                folders.append(item)

        return files, folders

    def build_prompt(self, file_objects, folders, base_path, user_instructions):
        folder_name = os.path.basename(base_path)

        return build_file_organization_prompt(file_objects, folders, folder_name, user_instructions)

    def get_plan(self, file_objects, folders, path, user_instructions, user_errors):
        loading = show_loading("Generating new plan...")

        try:
            prompt = self.build_prompt(file_objects, folders, path, user_instructions)

            if user_errors != "":
                prompt += "\n" + user_errors

            messages = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]



            messages.extend(self.history)

            messages.append({
                "role": "user",
                "content": prompt
            })


            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0,
                messages=messages
            )

            raw = response.choices[0].message.content

            try:
                plan = json.loads(raw)
            except json.JSONDecodeError:
                fatal_error(
                    "The AI returned invalid data and the operation cannot continue.\n\n"
                    "Raw response:\n" + raw
                )

            self.history.append({
                "role": "assistant",
                "content": raw
            })

            return plan
        finally:
            loading.destroy()


    # Takes the plan and the file mappings to the id's and actually moves the files
    def execute(self, base_path, plan, file_objects):
        # Build ID → filename lookup
        id_to_name = {str(f["id"]): f["name"] for f in file_objects}

        assignments = plan["assignments"]

        for file_id, folder in assignments.items():
            filename = id_to_name.get(str(file_id))

            if not filename:
                print(f"⚠️ Skipping unknown file ID: {file_id}")
                continue

            src = os.path.join(base_path, filename)
            folder_path = os.path.join(base_path, folder)
            dst = os.path.join(folder_path, filename)

            # Ensure folder exists
            os.makedirs(folder_path, exist_ok=True)

            # Skip if source missing
            if not os.path.exists(src):
                print(f"⚠️ File not found: {src}")
                continue

            # Avoid overwrite
            safe_dst = get_unique_path(dst)

            os.rename(src, safe_dst)
