# A2A Friend Scheduling Demo

This document describes a multi-agent application demonstrating how to orchestrate conversations between different agents to schedule a meeting between friends using Google's A2A (Agent-to-Agent) protocol.

This application includes four agents:

- **Host Agent**: Orchestrates the scheduling task.
- **Chamara Agent**: Represents Chamara’s calendar and availability preferences.
- **Ravindu Agent**: Represents Kavindu’s calendar and availability preferences.
- **Lakmina Agent**: Represents Lakmina’s calendar and availability preferences.

---

## 🛠️ Setup and Deployment

### ✅ Prerequisites

Before running the application, ensure you have:

1. **[uv](https://docs.astral.sh/uv/getting-started/installation/)** – Python package manager used in this project.
2. **Python 3.13** – Required to run the A2A SDK.
3. **.env File**

Create a `.env` file in the root of the `a2a_friend_scheduling` directory with your Google API key:
```env
GOOGLE_API_KEY="your_api_key_here"
```

---

## 🚀 Running the Agents

Each agent must be run in a separate terminal.

> The first time you run each agent, `uv` will create a virtual environment and install dependencies.

### Terminal 1: Run Chamara Agent
```bash
cd chamara_agent_crewai
uv venv
source .venv/bin/activate
uv run --active .
```

### Terminal 2: Run Kavindu Agent
```bash
cd ravindu_agent_langgraph
uv venv
source .venv/bin/activate
uv run --active app/__main__.py
```

### Terminal 3: Run Lakmina Agent
```bash
cd lakmina_agent_adk
uv venv
source .venv/bin/activate
uv run --active .
```

### Terminal 4: Run Host Agent
```bash
cd host_agent_adk
uv venv
source .venv/bin/activate
uv run --active adk web
```

---

## 💬 Interacting with the Host Agent

Once all agents are running, the Host Agent will coordinate the scheduling process by:

1. **Initiating Requests**  
   Frame scheduling questions like:  
   `"Are you available for a hangout between 2024-08-01 and 2024-08-03?"`

2. **Official Agent References**  
   Make sure to pass the official agent names (`Chamara_Agent`, `Kavindu_Agent`, `Lakmina_Agent`) when sending availability queries.

3. **Analyzing Responses**  
   The Host Agent will compare all responses and identify common available time slots.

4. **Check Room Availability**  
   Before confirming, it uses the `list_court_availabilities` tool to ensure the meeting location is also available.

5. **Propose & Confirm**  
   Suggests room-available time slots to the user and confirms the preferred time.

6. **Book the Room**  
   Uses `book_meeting` (or similar) to finalize the booking using the `start_time` and `end_time`.

7. **Final Confirmation**  
   Relays booking details (including Booking ID) to the user.  
   *No manual permissions or assumptions are made – all actions depend on defined tools and agent responses.*

---

## ✅ Behavior Guidelines

- **Clear Communication**: Use simple, readable formats (e.g., bullet points).
- **Strict Tool Usage**: All decisions/actions must be based on tools, not assumptions.
- **Agent Identity**: Each friend is represented by their respective agent:
  - `Chamara_Agent`
  - `Ravindu_Agent`
  - `Lakmina_Agent`
- **System Date**:  
  `Today's Date (YYYY-MM-DD):` `{{ dynamically insert date }}`  
- **Available Agents Block**:
  ```xml
  <Available Friend Agents>
    Chamara_Agent
    Kavindu_Agent
    Lakmina_Agent
  </Available Friend Agents>
  ```

---

## 📚 References

- [Google A2A SDK GitHub](https://github.com/google/a2a-python)  
- [Google A2A Codelab](https://codelabs.developers.google.com/intro-a2a-purchasing-concierge#1)