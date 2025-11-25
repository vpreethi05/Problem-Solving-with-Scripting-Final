Problem Solving with Scripting — Final Project

OsloMet — Master in Data Science

This repository contains the final submission for the course Problem Solving with Scripting.
The project is divided into two independent Python packages:

Task 1: Smart Courier Routing
A modular routing system that loads delivery data, validates rows, computes distances, and produces an optimised route using Greedy or Pareto-weighted selection.

Task 2: Conway’s Game of Life
A simulation engine implementing classical Life rules (Conway, HighLife, SuperLife) and a custom ChaosLife rule using decorators for metaprogramming.


## 📁 Repository Structure

```text
Problem-Solving-with-Scripting-Final/
│
├── Smart_Courier_Routing/
│   ├── cli/
│   │   └── menu.py
│   ├── core/
│   │   ├── reader.py
│   │   ├── validator.py
│   │   ├── haversine.py
│   │   ├── transport.py
│   │   ├── optimizer.py
│   │   └── metrics_writer.py
│   ├── utils/
│   │   ├── decorators.py
│   │   ├── logger.py
│   │   └── plotter.py
│   ├── data/
│   │   └── sample.csv
│   ├── output/               # Auto-generated during execution
│   ├── tests/
│   │   ├── test_basic.py
│   │   └── conftest.py
│   └── main.ipynb            #  Jupyter demo
│
├── ConwayGameOfLife/
│   ├── gameoflife/
│   │   ├── gol.py
│   │   ├── patterns.py
│   │   ├── rules.py
│   │   ├── rulesmanager.py
│   │   ├── test.py
│   │   └── save.py
│   ├── outputs/              # Auto-generated grid states
│   │ 
│   │   
│   ├── pattern.txt
│   └── main.py
│
├── requirements.txt
├── README.md
└── .gitignore



# 🔧 **Installation Instructions**

You need **Python 3.10 or newer**.

---

## **1 — Clone the repository**

```bash
git clone https://github.com/vpreethi05/Problem-Solving-with-Scripting-Final
cd Problem-Solving-with-Scripting-Final


# 2 — **Create a virtual environment**

**Windows (PowerShell):**

python -m venv venv
venv\Scripts\activate


**Mac/Linux:**

python3 -m venv venv
source venv/bin/activate

3 — Install project dependencies
pip install -r requirements.txt

▶️ How to Run Task 1 (Smart Courier Routing)

Navigate to the Task 1 directory:

cd Smart_Courier_Routing
python -m cli.menu


The CLI will ask for:

Path to CSV file

Depot location (latitude, longitude)

Transport mode (car, bicycle, walking)

Objective (fastest / lowest_cost / lowest_co2 / pareto)

Task 1 Outputs (saved in Smart_Courier_Routing/output/)

route.csv

metrics.csv

rejected.csv

route_plot.png

run.log

▶️ How to Run Task 2 (Conway’s Game of Life)

Navigate to the Task 2 folder:

cd ConwayGameOfLife
python main.py


The program will prompt for:

Grid dimensions

Rule set (conway / highlife / superlife / chaoslife)

Number of generations

Task 2 Outputs (saved in ConwayGameOfLife/outputs/)

Each generation’s grid state is saved as a text file.

🧪 Running Tests

To run all tests in the repository:

pytest


Or run per task:

cd Smart_Courier_Routing
pytest

cd ConwayGameOfLife
pytest

📦 Dependencies

All dependencies are listed in:

requirements.txt


Install using:

pip install -r requirements.txt

🤖 AI Usage Disclosure

AI assistance (ChatGPT / OpenAI) was used only to refine academic wording, improve explanations, and help with LaTeX and documentation formatting.

All algorithms, logic, implementation, and testing were developed by the author.
