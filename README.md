# AI-Agent

An AI setup agent that executes 5 task types:

1. Click + install software (example: Docker Desktop)
2. CLI software installation (example: Git)
3. CLI setup task (example: Node.js + npm validation)
4. Copy required files to execution directory
5. System configuration setup (example: machine environment variable)

## Project Structure

```text
AI-Agent/
├─ main.py
├─ requirements.txt
├─ README.md
├─ config/
│  └─ software_manifest.json
├─ agents/
│  ├─ __init__.py
│  └─ orchestrator.py
├─ tasks/
│  ├─ __init__.py
│  ├─ command_runner.py
│  ├─ handlers.py
│  ├─ models.py
│  └─ parser.py
├─ utils/
│  ├─ __init__.py
│  ├─ display.py
│  └─ logger.py
├─ execution_files/
│  └─ template.env
├─ runtime/
└─ setup-agent/
   └─ logs/
      └─ setup-agent.log (auto-created)
```

## Step-by-Step Run (Windows / PowerShell)

1) Open PowerShell in this project folder:

```powershell
cd C:\Users\Admin\Desktop\AI-Agent
```

2) Optional: create virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

3) Dry-run first (safe mode):

```powershell
python main.py
```

4) Execute real install/setup commands:

```powershell
python main.py --execute
```

## Customization for your 5 Software

Edit only `config/software_manifest.json`:

- Add or replace `commands` for each task
- Use `click_install` for GUI installer flow
- Use `cli_install` or `cli_setup` for terminal commands
- Use `copy_files` with `source` and `destination`
- Use `system_config` for machine configuration commands
