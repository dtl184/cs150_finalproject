# Genetically accurate bird music :)

## Tufts CS 150C: Algorithmic Music Composition Final Project

Due: April 22, 2025 at 11:59pm

Proposal: https://docs.google.com/document/d/1E78gNTqBVlBRK5jRlSwThFs37D9OIHajKfOeUwf537M/edit?tab=t.0

Presentation: https://docs.google.com/presentation/d/1raqYYnjn2aE6XLF5ZMPDHYSACdZqW_BcYB1d3-ZRO3k/edit?usp=sharing

Prof. Richard Townsend

Group members: Alberto Naveira (anavei01), Daniel Little (dlittl02), Emily Ertle (eertle01)
*submission done by this group member

## How to run code

Before you can run the code, you will need to make sure you have installed the proper libraries. To do this, run this command in your terminal: `pip install -r requirements.txt`. Below is a summary of how to run the program and the optional command line arguments which can be used to customize it:

**mapping.py [-h] [-rs RANDOM_SEED] [-k KEY] [-f FILENAME] [-m] [-s] [-t]**

| arg                                        | description                                                                                   |
| ------------------------------------------ | --------------------------------------------------------------------------------------------- |
| -h, --help                                 | Show this help message and exit.                                                              |
| -rs RANDOM_SEED, --random_seed RANDOM_SEED | Random seed to use. '-1' for no seed.<br />Default is 42.                                     |
| -k KEY, --key KEY                          | Key to generate the song in. Only accepts<br />flats (ex: 'Eb'), no sharps. Default is 'C'.   |
| -f FILENAME, --filename FILENAME           | Filename of .txt file where DNA is stored<br />(including extension). Default is 'SLIT1.txt' |
| -m, --midi                                 | Shows score in midi format (flag argument).                                                   |
| -s, --sheet_music                          | Shows score as sheet music (flag argument).                                                   |
| -t, --text                                 | Shows score as text (flag argument).                                                          |

All arguments in brackets are optional for running the script. The composition will only show in one of the three output types (midi, sheet music, or text). The default is midi if no argument is provided. For example, if you were to wanted to run the code with random seed *1* in the key of *Db* and use DNA stored in the file *DNA.txt*, then display the result as sheet music, you would enter the command: `mapping.py -rs 1 -k Db -f DNA.txt -s`.

## Overview

<Paragraph giving a high-level summary of your overall compositional approach

## Other insights

<(Optional) any additional interesting details you’d like to share about your approach or how you implemented it.>
