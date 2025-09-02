# py-aishell-engine
An interactive Python shell enhanced with a custom command engine. Supports natural language-style inputs, extended commands, and improved user experience beyond the standard Python REPL. Designed for experimentation, scripting, and extensible command handling.


🖥️ Natural Language Terminal (NL-Terminal)
📌 Overview

The Natural Language Terminal (NL-Terminal) is a next-generation command-line interface that allows users to interact with their system using natural language instead of rigid shell syntax.
It is designed to:

Provide powerful system control (like a traditional terminal).

Add safety nets to prevent accidental destructive actions.

Ensure command clarity before execution, making it beginner-friendly yet efficient for advanced users.

✨ Core Features
🔹 Command Execution

Run system commands (ls, mkdir, rm, echo on Linux/macOS; dir, copy, del on Windows).

Execute custom scripts (Python, Shell, Batch, etc.).

Interpret natural language queries, e.g.:

"show me all files in this folder" → ls

"create a folder called test" → mkdir test

"delete the log file" → rm log.txt (with confirmation prompt).

🔹 File & Directory Management

Navigate (cd, pwd).

List contents (ls, dir).

Create/move/delete files and folders (mkdir, rm, mv, cp).

Safety Net: Any destructive or critical operations (delete, move, overwrite) will:

Ask for explicit confirmation.

Show exact paths and targets before execution.

Block wildcard deletions (like rm -rf *) unless explicitly confirmed.

🔹 Process Management

Start processes (Python, Node.js, etc.).

Kill or stop processes (with confirmation).

List running processes.

Safety Net: Prevents killing critical system processes without a strong override.

🔹 Text & File Operations

Read/write files (cat, nano, echo > file.txt).

Search text (grep, find).

Safety Net: When writing/modifying files, system will confirm target file path and ask for overwrite permission.

🔹 System Utilities

View system info (top, df, free, systeminfo).

Networking commands (ping, curl, wget).

Disk usage, memory, CPU, and uptime reports.

🔹 Scripting Support

Run Python, JavaScript, or Shell scripts directly inside terminal.

Define custom macros/shortcuts for repetitive tasks.

🛡️ Safety Nets

Delete / Move / Overwrite Confirmation

"delete report.docx" → “Are you sure you want to delete /home/user/report.docx? (y/n)”

Protected Commands

Prevents accidental use of dangerous commands (rm -rf /, format C:).

Preview Before Execution

Every natural language request is translated into the exact shell command and shown to the user:

"create a folder called test" → mkdir test

User approves before execution.

Scoped Permissions

Terminal runs in a sandboxed environment (optional mode) to prevent uncontrolled access to the entire system.

🧭 Command Clarity

Natural Language → Explicit Shell Command

The terminal always translates natural requests into exact shell commands before execution.

Interactive Disambiguation

"move file" → “Which file do you want to move?”

"create file" → “What should the file be named, and where should it be stored?”

Context-Aware Prompts

Keeps track of current directory and clarifies vague requests.

"open the log" → “Found multiple log files: log1.txt, log2.txt. Which one?”