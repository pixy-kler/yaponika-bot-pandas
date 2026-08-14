# 🇯🇵 Japanese Student CRM Bot (Telegram)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.x-green)](https://docs.aiogram.dev/)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-yellow)](https://pandas.pydata.org/)
[![Hexagonal](https://img.shields.io/badge/Architecture-Hexagonal-purple)](https://en.wikipedia.org/wiki/Hexagonal_architecture)

A **production-ready Telegram bot** for a Japanese language school. It automates student registrations, collects CRM data, and provides real-time analytics — all powered by Python, Pandas, and a clean Hexagonal Architecture.

---

##Architecture

This project follows the **Hexagonal Architecture (Ports & Adapters)** pattern to ensure maintainability and testability:

- **Core (Domain):** Pure Python logic for FSM (Finite State Machine) and data validation.
- **Data Layer (Port):** Pandas + CSV file storage for CRM data (`students_jp.csv`). 
- **Adapter (Inbound Port):** Telegram Bot via `aiogram` — handles user input and commands.

> *Why this architecture? It allows you to swap Telegram for WhatsApp, MAX, or Slack by changing only the adapter — without touching the core business logic or database.*

---

## Features

-  **Multi-step registration form** using Aiogram FSM.
-  **Real-time analytics dashboard** (`/stats`) — total students, active rates, conversion metrics.
-  **Follow-up task list** (`/todo`) — instantly shows who needs a call.
-  **Birthday tracking** (great for customer retention and marketing).
-  **Automatic CSV data storage** (can be easily imported into Excel or Jupyter for deeper analysis).

---

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Language** | Python 3.10+ |
| **Framework** | Aiogram 3.x |
| **Data Processing** | Pandas, CSV |
| **Architecture** | Hexagonal / Adapter Pattern |
| **Security** | `python-dotenv` for token management |

---

## How to run this bot locally

### Prerequisites
- Python 3.10 or higher installed.
- Telegram Bot Token from [@BotFather](https://t.me/botfather).

### 1. Clone the repository
```bash
git clone https://github.com/your-username/japanese-student-crm-bot.git
cd japanese-student-crm-bot
