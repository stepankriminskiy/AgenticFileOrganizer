# Agentic File Organizer

AI-powered file organizer.

Uses agentic architecture to self feed and correct issues.

The system is self-correcting, validates its own output, and adapts to user preferences over time.

Remembers user's preferences + history.

## Description

Agentic File Organizer is a Python-based file organization tool that uses a self-correcting looping agentic llm architecture.

Instead of relying on hardcoded rules or file extensions alone, the organizer takes the user's written input and it's own reasoning to create folders and move files.

The system is designed to be self-correcting. If the LLM produces invalid output (missing files, duplicate assignments, invalid folder names, etc.), the error is detected, fed back into the model, and a corrected plan is generated. This loop continues until a valid and safe result is produced.

Files are tracked using internal IDs rather than filenames to prevent mismatches or accidental overwrites. The organizer also prefers existing folders when possible and avoids creating unnecessary or redundant directories.

Over time, the system can adapt to user preferences by favoring previously used folder structures and organization patterns, allowing it to behave more consistently across runs.


## Getting Started

### Prerequisites
#### OpenAi Api Key:
##### Windows
```
setx OPENAI_API_KEY "your_api_key_here"
```

##### Mac / Linux
```
export OPENAI_API_KEY="your_api_key_here"
```

### Installing + Running
```
git clone https://github.com/stepankriminskiy/AgenticFileOrganizer.git
```

#### Option 1 - Running Executable:
* Simply just run the AgenticFileOrganizer.exe 

#### Option 2 - Running through python:
* Install Dependencies
```
pip install -r requirements.txt
```
* Run program
```
python main.py
```
   

## Usage
### Step 1: Start With a Disorganized Folder
#### This is an example of an unorganized directory before running the tool.
<img width="400" alt="image" src="https://github.com/user-attachments/assets/043b8708-da2d-4087-b26b-98fbdbb8285b" /> <img width="400" alt="image" src="https://github.com/user-attachments/assets/6c680225-4f34-4497-87da-c2420c8f0517" />

### Step 2: Provide Optional Guidance
#### You can give the agent direction on how you'd like files grouped or handled.
<img width="494" height="374" alt="image" src="https://github.com/user-attachments/assets/ad70553e-b868-4898-9331-0dfe9c96a3bb" />

### Step 3: Generate the Organization Plan
#### The agent analyzes the directory and generates a proposed plan.
<img width="291" height="128" alt="image" src="https://github.com/user-attachments/assets/93a10452-2de5-4c9a-9de5-5d16c8eaa109" /><img width="1150" height="1208" alt="image" src="https://github.com/user-attachments/assets/1a7af787-447a-4b50-a872-209d8d82ac23" />

### Step 4: Review and Refine the Plan
#### I chose to refine the plan with the prompt below.
<img width="494" height="372" alt="image" src="https://github.com/user-attachments/assets/83215186-68b7-49a8-843c-c3d731b500a8" />

### Step 5: Apply the Changes
#### I was satisfied with the changes and decided to move the files.
<img width="737" height="379" alt="image" src="https://github.com/user-attachments/assets/951e4f2e-102e-4088-abe7-3fdaf119fd7d" /><img width="232" height="139" alt="image" src="https://github.com/user-attachments/assets/ebc03b54-1665-4083-8835-c7060bebf1f2" />

### Step 6: Final Result
#### The directory is now cleanly organized based on intent.
<img width="962" height="444" alt="image" src="https://github.com/user-attachments/assets/afff3bdb-f1fb-43da-b20c-087523983fd0" />







