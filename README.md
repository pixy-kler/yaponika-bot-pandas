# Japanese School CRM Bot (Hexagonal Architecture)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.x-green)](https://docs.aiogram.dev/)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-yellow)](https://pandas.pydata.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Hexagonal-purple)](https://en.wikipedia.org/wiki/Hexagonal_architecture)

A **dual-bot CRM system** for a Japanese language school, built with **Hexagonal Architecture (Ports & Adapters)**.

**One shared core (Pandas + FSM) — Two independent adapters (Teacher Bot & Student Bot).**

---

## System Architecture

This project follows the **Hexagonal Architecture (Ports & Adapters)** pattern:

- **Core (Domain):** `core.py` — Shared business logic (FSM, Data Validation).
- **Data Layer (Port):** Pandas + CSV (`students_jp.csv`) for CRM storage.
- **Adapters (Inbound Ports):** Two independent Telegram bots:
  - `bot_teacher.py` — For the teacher to manually register students.
  - `bot_student.py` — For students to submit their own applications.

> *Why Hexagonal? It allows adding new interfaces (WhatsApp, VK, web forms) without changing the core logic or database structure.*

---

## Features

- **Multi-step registration forms** (FSM) for both teachers and students.
- **Unified data storage** — all applications go into a single `students_jp.csv`.
- **Real-time analytics** (`/stats`) & **follow-up lists** (`/todo`).
- **Birthday tracking** for student retention.
- **Separation of concerns** — Teacher and Student bots run independently but share the same data.

---

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Language** | Python 3.10+ |
| **Bot Framework** | Aiogram 3.x |
| **Data Processing** | Pandas, CSV |
| **Architecture** | Hexagonal / Adapter Pattern |
| **Security** | `python-dotenv` for token management |

---

## How to run this project locally

### Prerequisites
- Python 3.10+
- Telegram Bot Token from [@BotFather](https://t.me/botfather).

### 1. Clone the repository

git clone https://github.com/pixy-kler/yaponika-bot-pandas.git
cd yaponika-bot-pandas

### 2. Set up environment variables

Create a .env file in the root directory and add:

TELEGRAM_TOKEN=your_actual_token_here

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run the bots

You need two separate terminal windows to run both bots:

**Terminal 1 (Teacher Bot):**

python bot_teacher.py

**Terminal 2 (Student Bot):**

python bot_student.py

---

## **Telegram Commands**

### Teacher Bot (bot_teacher.py)
| Command | Description |
| :--- | :--- |
| `/start` | Show welcome message |
| `/new` | Manually register a new student (7-step form) |
| `/stats` | View CRM analytics (total, active, conversion %) |
| `/todo` | View all new students waiting for a follow-up call |
| `/clear` | Cancel current registration |

### Student Bot (`bot_student.py`)
| Command | Description |
| :--- | :--- |
| `/start` | Show welcome message with bot features |
| `/reg` | Submit your own application (7-step registration form) |
| `/clear` | Cancel current registration |

---

### Data Structure (`students_jp.csv`)

| Column | Description |
| :--- | :--- |
| `timestamp` | Registration date & time |
| `tg_username` | Student's Telegram username |
| `name` | Full name |
| `birthday` | Date of birth (DD.MM.YYYY) |
| `phone` | Contact phone number |
| `level` | Japanese level (N5, N4, etc.) |
| `goal` | Learning goal (Work, Internship, Hobby) |
| `preferred_time` | Preferred lesson time |
| `status` | CRM status (e.g., "New (Need Call)") |
| `notes` | Additional notes |
| `source_bot` | Source of application (`TEACHER_BOT` or `STUDENT_BOT`) |

---

## Future Enhancements (Roadmap)

    -   Web Dashboard using Streamlit for visual analytics.
    -    Automated birthday greetings via Telegram.
    - Google Calendar integration for lesson scheduling.

---

## Contributing

Contributions are welcome! Feel free to fork the project, make changes, and submit a Pull Request.

---

## Contact

Author: pixy-kler
Project Type: Data Engineering / Automation / Async API / Hexagonal Architecture

---

If you found this project useful, give it a star on GitHub!