# Problem-Solving-with-Scripting-Final
Python scripting assignment containing Task 1 (Smart Courier Routing) and Task 2 (Conway’s Game of Life). Includes modular Python packages, documentation, tests, and instructions for running the project.


Problem Solving with Scripting — Final Project

OsloMet — Master in Data Science

This repository contains the final submission for the course Problem Solving with Scripting.
The solution is divided into two independent components:

Task 1 — Smart Courier Routing
A modular Python package that loads delivery data, validates rows, computes distances, and produces an optimized delivery route using Greedy or Pareto weighting.

Task 2 — Conway’s Game of Life
A simulation engine implementing multiple Life-like cellular automata rules, including a custom ChaosLife rule.

📁 Repository Structure
Problem-Solving-with-Scripting-Final/
│
├── Smart_Courier_Routing/
│   ├── cli/
│   ├── core/
│   ├── utils/
│   ├── data/
│   ├── output/
│   ├── tests/
│   └── main.ipynb   (optional)
│
├── ConwayGameOfLife/
│   ├── gameoflife/
│   ├── patterns/
│   ├── outputs/
│   ├── tests/
│   ├── main.py
│   └── pattern.txt
│
├── requirements.txt
├── README.md
└── .gitignore

🔧 Installation Instructions

You need Python 3.10+.

1 — Clone the repository
git clone https://github.com/vpreethi05/Problem-Solving-with-Scripting-Final
cd Problem-Solving-with-Scripting-Final

2 — Create a Python virtual environment
Windows PowerShell:
python -m venv venv
venv\Scripts\activate

Mac/Linux:
python3 -m venv venv
source venv/bin/activate

3 — Install required packages
pip install -r requirements.txt

▶️ How to Run Task 1 (Smart Courier Routing)

Navigate to the folder:

cd Smart_Courier_Routing
python -m cli.menu


The CLI will ask for:

CSV file path

Depot (latitude, longitude)

Transport mode

Objective function (fastest / lowest_cost / lowest_co2 / pareto)

Outputs saved to Smart_Courier_Routing/output/:

route.csv

metrics.csv

rejected.csv

route_plot.png

run.log

▶️ How to Run Task 2 (Conway’s Game of Life)

Navigate to:

cd ConwayGameOfLife
python main.py


You will be asked for:

Grid size

Rule set

Number of generations

Outputs saved to:

ConwayGameOfLife/outputs/

🧪 Running Tests

To run all tests:

pytest


Or run per task:

cd Smart_Courier_Routing
pytest

cd ConwayGameOfLife
pytest

📦 Dependencies

Dependencies listed in:

requirements.txt

🤖 AI Usage Disclosure

AI assistance (ChatGPT, OpenAI) was used only to improve wording, explanations, and formatting.
All algorithms, implementation, and code development were performed by the author.