# Simple Todo

A modern todo application with natural language task input and smart notification system.

## Features

- **Natural Language Task Input**: Simply type your task with time information (e.g., "Submit report by 5pm tomorrow")
- **Smart Time Extraction**: Uses OpenAI API to extract task content and due time from natural language
- **Notification System**: Receive reminders at strategic intervals before tasks are due
- **Clean UI**: Modern interface with two main panes - Add Task and Task List

## Technology Stack

- **Frontend**: React with Shadcn UI components
- **Backend**: FastAPI (Python)
- **Database**: SQLite
- **Notifications**: Apprise library (supports multiple notification channels)

## Installation

### Prerequisites

- Python 3.8+
- Node.js 14+
- OpenAI API key

### Backend Setup

```bash
# Navigate to backend directory
cd todo/backend

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Edit the .env file with your OpenAI API key and notification settings