
# Investigation and improvement of the optimisation function for the generation of a sowing map in equidistant sowing

## Untersuchung und Verbesserung der Optimierungsfunktion für die Generierung einer Aussaatkarte in der Gleichstandssaat

The purpose of this project is to simulate seed sowing on a plot, enabling drone operation, and to calculate the most optimized sowing methods.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Contact](#contact)

## Introduction

This is a project designed to simulate equilateral triangle sowing in a plot. 
It serves as a bachelor's thesis and is part of the "Spot farming – an alternative for future plant production" project. 
The project enables the division and sowing of plots to accommodate the characteristics of drone sowing. 
It can also identify the most optimized sowing methods for reference.

## Installation

Ensure that Python and Git are installed.
A virtual environment is a recommended option, but it is not mandatory.
```bash
# Clone the repository
git clone https://github.com/CarrQuin/Sowing-planning.git

# Navigate to the project directory
cd Sowing-planning

# Create and activate a virtual environment
python -m venv venv

source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install the dependencies
pip install -r requirements.txt.
```

## Usage 

As a user, you only need to use the file "Aussaatplanung_script.py". In the variable section, 
you can input the variables you want to control and specify the file type for saving.  
You can also choose to enable optimization mode, which may take more time.

You can also run it once with the default variables to see the actual effect.
Click "Run Python File" on the right side of the title bar to run the current file.

## Contact

If you encounter any problems while using it, feel free to contact me.

 * Email: k.qian@tu-braunschweig.de