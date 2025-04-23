# Genetically accurate bird music :)

## Tufts CS 150C: Algorithmic Music Composition Final Project

Due: April 22, 2025 at 11:59pm

Presentation: https://docs.google.com/presentation/d/1raqYYnjn2aE6XLF5ZMPDHYSACdZqW_BcYB1d3-ZRO3k/edit?usp=sharing

Prof. Richard Townsend

Group members: Alberto Naveira (anavei01), Daniel Little (dlittl02), Emily Ertle (eertle01)
*submission done by this group member

## How to run code

Before you can run the code, you will need to make sure you have installed the proper libraries. To do this, run this command in your terminal: `pip install -r requirements.txt`. Below is a summary of how to run the program and the optional command line arguments which can be used to customize it:

**project.py [-h] [-rs RANDOM_SEED] [-k KEY] [-f FILENAME] [-m] [-s] [-t]**

| arg                                        | description                                                                                   |
| ------------------------------------------ | --------------------------------------------------------------------------------------------- |
| -h, --help                                 | Show this help message and exit.                                                              |
| -rs RANDOM_SEED, --random_seed RANDOM_SEED | Random seed to use. '-1' for no seed.<br />Default is 42.                                     |
| -k KEY, --key KEY                          | Key to generate the song in. Only accepts<br />flats (ex: 'Eb'), no sharps. Default is 'C'.   |
| -f FILENAME, --filename FILENAME           | Filename of .txt file where DNA is stored<br />(including extension). Default is 'SLIT1.txt'  |
| -m, --midi                                 | Shows score in midi format (flag argument).                                                   |
| -s, --sheet_music                          | Shows score as sheet music (flag argument).                                                   |
| -t, --text                                 | Shows score as text (flag argument).                                                          |
| -p, --population_size                      | Population size for genetic algorithm.                                                        |
| -g, --generations                          | Number of generations for genetic algorithm.                                                  |
| -mr, --mutation_rate                       | Mutation rate for genetic algorithm.                                                          |
| -cr, --crossover_rate                      | Crossover rate for genetic algorithm.                                                         |

All arguments in brackets are optional for running the script. The composition will only show in one of the three output types (midi, sheet music, or text). The default is midi if no argument is provided. For example, if you were to wanted to run the code with random seed *1* in the key of *Db* and use DNA stored in the file *DNA.txt*, then display the result as sheet music, you would enter the command: `mapping.py -rs 1 -k Db -f DNA.txt -s`.

You will need the following files in your working directory to be able to run project.py:
* SLIT1.txt
* score.xml
* requirements.txt
* mapping.py
* rhythm.py

## Overview

The approach mainly revolves around making bird music. We tease that apart into: (1) genetic material extraction and optimization via GA, (2) chord and melody initialization via manual mapping and (3) rhythmic mapping of generated melody via rhythm generator to produce rhythms imitating bird calls. This approach is interesting because it incorporates a creative way to get a seed for a musical idea: biological data optimized via GA; along with an innovative approach to create rhythmic motifs that imitate bird calls. 
