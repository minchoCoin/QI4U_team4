Optimization for evacuation route of IT building using Simulated Annealing and Quantum Annealing

For detailed information, please refer the [presentation.pdf](https://github.com/minchoCoin/QI4U_team4/blob/main/Presentation_Team4.pdf)

# React + FastAPI App

A web application built with React (Frontend) and FastAPI (Backend).

## Directory Structure

- `frontend/`: React (Vite) project
- `backend/`: FastAPI (Python) project

## Prerequisites

Ensure the following tools are installed:

- **Python** (3.9 or higher recommended)
- **Node.js** (18 or higher recommended) & **npm**

---

## Setup & Run

To run this application, you need to start the **backend** and **frontend** in separate terminal windows.

### 1. Start the Backend (FastAPI)

Open a terminal and execute the following steps:

```bash
# 1. Move to the backend directory
cd backend

# 2. Create a virtual environment (First time only)
# For Windows
python -m venv venv
# For Mac/Linux
python3 -m venv venv

# 3. Activate the virtual environment
# For Windows
venv\Scripts\activate
# For Mac/Linux
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Start the server
uvicorn main:app --reload

# 1
cd frontend 

# 2 
npm install axios

# 3 
npm run dev
