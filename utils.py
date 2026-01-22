import os
import re
import stat

def format_plan(plan, file_objects):
    id_to_name = {f["id"]: f["name"] for f in file_objects}
    folder_map = {}

    for fid, folder in plan["assignments"].items():
        fid = int(fid)
        folder_map.setdefault(folder, []).append(id_to_name[fid])

    lines = []
    for folder, files in folder_map.items():
        lines.append(f"📂 {folder}")
        for name in files:
            lines.append(f"   - {name}")
        lines.append("")

    return "\n".join(lines)



def get_unique_path(path):
    """
    If file exists, append (1), (2), etc.
    """
    if not os.path.exists(path):
        return path

    base, ext = os.path.splitext(path)
    counter = 1

    while True:
        new_path = f"{base} ({counter}){ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1

#Generating possible errors that the LLM created in the returned json so we can parse it back and have it regenerate properly
def validate_plan(plan, file_objects, existing_folders):
    errors = []

    # Basic json structure check
    if not isinstance(plan, dict):
        return ["Response is not a JSON object."]

    if "assignments" not in plan:
        return ["Missing 'assignments' key in response."]

    assignments = plan["assignments"]

    if not isinstance(assignments, dict):
        return ["'assignments' must be an object mapping file IDs to folder names."]


    valid_ids = {str(f["id"]) for f in file_objects}
    assigned_ids = set()

    # Validate each assignment
    for fid, folder in assignments.items():

        # ID validity
        if fid not in valid_ids:
            errors.append(f"Invalid or unknown file ID: {fid}")
            continue

        if fid in assigned_ids:
            errors.append(f"Duplicate assignment for file ID: {fid}")
        assigned_ids.add(fid)

        # Folder name sanity
        if not isinstance(folder, str) or not folder.strip():
            errors.append(f"Invalid folder name for file ID {fid}")


        # Prevent recreating base folder
        if folder in existing_folders:
            continue  # allowed, just informational

    # If the LLM missed a file id in its response
    missing = valid_ids - assigned_ids
    if missing:
        errors.append(f"Missing file IDs in plan: {', '.join(missing)}")

    return errors

def is_hidden(filepath):
    try:
        return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
    except:
        return False

