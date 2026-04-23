### **New Interaction**
- **Agent Version**: 2.2
- **Date**: 30-03-2026 13:57
- **User**: anh-duc.vo@epita.fr
- **Prompt**: activate the journal logger
- **CoPilot Mode**: Agent
- **CoPilot Model**: GPT-5.3-Codex
- **Socratic Mode**: ON
- **Changes Made**: Activated journal logging by appending this interaction entry to JOURNAL.md.
- **Context and Reasons for Changes**: User requested activation of the journal logger, so logging was initiated immediately in the repository root journal file.

### **New Interaction**
- **Agent Version**: 2.2
- **Date**: 30-03-2026 14:01
- **User**: anh-duc.vo@epita.fr
- **Prompt**: Create a simple pygame application that displays 10 squares moving randomly on the screen. FORGET the socratic mode for now. After this request, turn it back on
- **CoPilot Mode**: Agent
- **CoPilot Model**: GPT-5.3-Codex
- **Socratic Mode**: OFF
- **Changes Made**: Implemented a complete Pygame app in main.py that shows 10 colored squares moving with random velocities and bouncing on window boundaries.
- **Context and Reasons for Changes**: User explicitly requested a direct implementation and temporary suspension of Socratic mode for this task.

### **New Interaction**
- **Agent Version**: 2.2
- **Date**: 30-03-2026 14:54
- **User**: anh-duc.vo@epita.fr
- **Prompt**: update the joirnal
- **CoPilot Mode**: Agent
- **CoPilot Model**: GPT-5.3-Codex
- **Socratic Mode**: ON
- **Changes Made**: Appended a new journal entry to JOURNAL.md.
- **Context and Reasons for Changes**: User requested updating the journal, so this interaction was logged directly in the repository journal.

### **New Interaction**
- **Agent Version**: 2.2
- **Date**: 03-04-2026 19:49
- **User**: anh-duc.vo@epita.fr
- **Prompt**: Update the journal
- **CoPilot Mode**: Agent
- **CoPilot Model**: GPT-5.3-Codex
- **Socratic Mode**: ON
- **Changes Made**: Appended a new journal entry to JOURNAL.md with the user's request to update the journal.
- **Context and Reasons for Changes**: User requested a journal update after experimenting with sound effects and simulation features.

### **New Interaction**
- **Agent Version**: 2.2
- **Date**: 03-04-2026 19:58
- **User**: anh-duc.vo@epita.fr
- **Prompt**: okie babygirl, mommy loves u so much <333\n\nnow update the journal!
- **CoPilot Mode**: Agent
- **CoPilot Model**: GPT-5.3-Codex
- **Socratic Mode**: ON
- **Changes Made**: Appended a new journal entry with the user's affectionate message and journal update request.
- **Context and Reasons for Changes**: User sent a playful message and requested a journal update, so this interaction was logged as usual.

### **New Interaction**
- **Agent Version**: 2.3
- **Date**: 13-04-2026 14:21
- **User**: anh-duc.vo@epita.fr
- **Prompt**: Activate the journal logger
- **CoPilot Mode**: Agent
- **CoPilot Model**: GPT-5.3-Codex
- **Socratic Mode**: ON
- **Changes Made**: Confirmed and activated journal logging by appending this entry to JOURNAL.md.
- **Context and Reasons for Changes**: User explicitly requested activation of the journal logger for this lab workspace.

### **New Interaction**
- **Agent Version**: 2.3
- **Date**: 13-04-2026 14:35
- **User**: anh-duc.vo@epita.fr
- **Prompt**: The site seems to just be a weird version of vscode but read mode. I cannot visualize how the code is, or the architecture, or the flow chart. Can you scrap the site you have made and create a new code explorer site for this project?
- **CoPilot Mode**: Agent
- **CoPilot Model**: GPT-5.3-Codex
- **Socratic Mode**: ON
- **Changes Made**: Replaced the previous code explorer with a new visual site that renders architecture, runtime flow, and call graph diagrams from `main.py`; rewrote `index.html`, `styles.css`, and `app.js`; removed obsolete `manifest.json`; updated README instructions.
- **Context and Reasons for Changes**: User requested a fully new explorer focused on architecture and flow visualization rather than read-only code browsing.


### **New Interaction**
- **Agent Version**: 2.3
- **Date**: 13-04-2026 14:45
- **User**: anh-duc.vo@epita.fr
- **Prompt**: generate the code explorer site for this project. This time, please use #file:code-explorer-template.html as a template
- **CoPilot Mode**: Agent
- **CoPilot Model**: GPT-5.3-Codex
- **Socratic Mode**: ON
- **Changes Made**: Generated `code-explorer/index.html` using the provided `.github/agents/code-explorer-template.html`.
- **Context and Reasons for Changes**: The user requested a specific templated Code Explorer generation, scrapping the previous vanilla approach.
## [2026-04-13 15:03:23] Generated Code Explorer Dashboard
Applied template and agent rules to build deep visual exploration at docs/code_explorer.html.
Finished Code Explorer Generation

### **New Interaction**
- **Agent Version**: 2.3
- **Date**: 16-04-2026
- **User**: anh-duc.vo@epita.fr
- **Prompt**: I have deleted the two files you have made. Now please redo what i said previously. Your code explorer is #file:code_explorer.html . Also please use #file:code-explorer-template.html  and #file:code-explorer.agent.md  as guidelines
- **CoPilot Mode**: Agent
- **CoPilot Model**: GPT-5.3-Codex
- **Socratic Mode**: ON
- **Changes Made**: Completely regenerated docs/code_explorer.html applying the code-explorer-template.html and code-explorer.agent.md guidelines. Identified object pooling, safe list iteration, and rebuilt Mermaid architecture graphs safely.
- **Context and Reasons for Changes**: The user deleted the previous files and requested a fresh generation using the explicit template and agent instructions.

### **New Interaction**
- **Agent Version**: 2.3
- **Date**: 23-04-2026
- **User**: anh-duc.vo@epita.fr
- **Prompt**: I have updated the main.py. update the code explorer again please
- **CoPilot Mode**: Agent
- **CoPilot Model**: Gemini 3.1 Pro (Preview)
- **Socratic Mode**: ON
- **Changes Made**: Updated the `docs/code_explorer.html` dashboard twice to track new functionality in `main.py` including `dt` (Delta Time) loop framing, object pooling improvements, safe iterative copies, debug flags (`toggle_roe_flag`), duplicated AI logic warnings (`chase`/`flee`), and precise Forward References in Python Type Hints (`list['Square']`).
- **Context and Reasons for Changes**: User implemented game-loop adjustments and type hints in the core Pygame loop, requesting the existing code explorer dashboard be kept in sync.
