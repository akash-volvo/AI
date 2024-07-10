# Automated XPath Correction

This document includes instructions for installing the necessary packages, setting up Python, and running the provided script.

## Prerequisites

- Python 3.x
- Word2Vec Pre-Trained Model

## Installation Instructions

### Step 1: Install Python

If you don't have Python installed, follow these steps:

1. Download Python from the [official website](https://www.python.org/downloads/).
2. Run the installer and follow the installation instructions.
3. Ensure that Python is added to your system PATH.

### Step 2: Copy Word2Vec Model

Copy the .bin file into the `Algorithm` folder


### Step 3: Clone the Repository
```bash
git clone https://github.com/akash-volvo/AI.git
```


### Step 4: Install the required packages
```bash
pip install -r requirements.txt
```


### Step 5: Run the algorithm to find similarity/ Run the algorithm to suggest weights
```bash
python3 index.py
python3 algorithm.py
```
