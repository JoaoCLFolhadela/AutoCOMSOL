# AutoCOMSOL - GUI for Automating COMSOL Simulations

## Introduction
AutoCOMSOL is a Python-based software with a graphical user interface (GUI), developed during a master's thesis, designed to automate and streamline numerical simulations in COMSOL. Developed using the CustomTkinter framework, the GUI facilitates a user-friendly and interactive approach to managing complex simulations. This project contains scripts and supporting files that work in harmony to realize this application. The task at hand was to automatize the process of solving 512 different simulations. Each one simulates heat being applied to each position on a thermoelectric material to explore its viability as an E-Tattoo. The final work is with this extracted data to develop a Machine Learning (ML) model that predicts where is heat being applied.

## Installation & Usage
CustomTkinter and pandas must be installed (use pip install customtkinter; pandas) and COMSOL version 5.6. This script only works for the used COMSOL model but serves as an example to other simulations that might require such dynamic control.

## Working Principle
The goal was to have every combination possible of positions being heated, where heat is applied for 8 seconds and the voltage produced via the Seebeck Effect is measured. In total, there are 9 positions so every combination possible for these 9 positions is to have first only one point at a time active: 9 different simulations, then two points at a time: 36 different simulations, the three points at a time, and so on summing 512 simulations in total. The software developed allows one to choose any number of points to be active, the set of combinations is computed and simulates all those simulations. If we want to start from a random combination (due to system shutdown, for instance) the software allows for by using "points to skip". It also predicts how long will take for the total set of combinations to simulate.


## File Structure
- AutoCOMSOL.py: This is the main script that houses the GUI application, implementing various methods to manage and visualize simulations dynamically.
- no_combinations.py: A supplementary script that is integrated within the main script to assist in tracking the combinations of simulations to be performed.
- automate_etattoo.mph: A COMSOL model file that is utilized by the GUI for conducting numerical simulations. It is where the materials, parameters and studies to perform are defined.
- BG.png: The background image of the E-tattoo
- IFIMUP.png: Research institute's logo


For more info contact up201709374@fc.up.pt


