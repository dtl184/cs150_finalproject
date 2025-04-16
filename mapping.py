#!/usr/bin/env python3
# Purpose: This code takes a piece of genetic code (a DNA sequence) and performs transcription and translation on it. Then, using a mapping of each of the 21 amino acids to roman numeral chords based on the chemical properties of these amino acids, we generated a chord sequence. We used this chord sequence to shape a melody generated from the original DNA sequence. Rhythms for the melody were generated randomly.
# 
# Author(s): Emily Ertle, Alberto Naveira, and Dan Little
# Date: 3/16/24
import argparse
from music21 import *
import numpy as np
import os
import random
from typing import Optional

# acknowledgment: The translation dictionary below was generated using ChatGPT
# Dictionary for performing biological 'translation' of RNA codons into amino acids (standard one-letter abbreviations)
TRANSLATION = {
    # Phenylalanine
    'uuu': ['F'], 'uuc': ['F'],
    # Leucine
    'uua': ['L'], 'uug': ['L'],
    'cuu': ['L'], 'cuc': ['L'], 'cua': ['L'], 'cug': ['L'],
    # Isoleucine
    'auu': ['I'], 'auc': ['I'], 'aua': ['I'],
    # Methionine (Start)
    'aug': ['M'],
    # Valine
    'guu': ['V'], 'guc': ['V'], 'gua': ['V'], 'gug': ['V'],
    # Serine
    'ucu': ['S'], 'ucc': ['S'], 'uca': ['S'], 'ucg': ['S'],
    'agu': ['S'], 'agc': ['S'],
    # Proline
    'ccu': ['P'], 'ccc': ['P'], 'cca': ['P'], 'ccg': ['P'],
    # Threonine
    'acu': ['T'], 'acc': ['T'], 'aca': ['T'], 'acg': ['T'],
    # Alanine
    'gcu': ['A'], 'gcc': ['A'], 'gca': ['A'], 'gcg': ['A'],
    # Tyrosine
    'uau': ['Y'], 'uac': ['Y'],
    # Stop codons
    'uaa': ['Stop'], 'uag': ['Stop'], 'uga': ['Stop'],
    # Histidine
    'cau': ['H'], 'cac': ['H'],
    # Glutamine
    'caa': ['Q'], 'cag': ['Q'],
    # Asparagine
    'aau': ['N'], 'aac': ['N'],
    # Lysine
    'aaa': ['K'], 'aag': ['K'],
    # Aspartic Acid
    'gau': ['D'], 'gac': ['D'],
    # Glutamic Acid
    'gaa': ['E'], 'gag': ['E'],
    # Cysteine
    'ugu': ['C'], 'ugc': ['C'],
    # Tryptophan
    'ugg': ['W'],
    # Arginine
    'cgu': ['R'], 'cgc': ['R'], 'cga': ['R'], 'cgg': ['R'],
    'aga': ['R'], 'agg': ['R'],
    # Glycine
    'ggu': ['G'], 'ggc': ['G'], 'gga': ['G'], 'ggg': ['G']
}

# Dictionary mapping from single-letter amino acid shorthands to roman numeral chords
AMINO_ACID_TO_CHORD = {
    # Nonpolar (Hydrophobic) – Major chords
    'M': ['I'],
    'A': ['IV'],
    'V': ['V'],
    'L': ['Imaj7'],
    'I': ['IVmaj7'],
    'G': ['I[add6]'],
    'F': ['V[add6]'],
    'W': ['I[add9]'],
    'P': ['IV[add9]'],

    # Polar Uncharged – Minor chords
    'S': ['ii'],
    'T': ['iii'],
    'N': ['vi'],
    'Q': ['ii7'],
    'C': ['iii7'],
    'Y': ['vi7'],
    
    # Acidic – Diminished chords
    'D': ['vii°'],
    'E': ['vii°7'],

    # Basic – Dominant chords
    'K': ['V7'],
    'R': ['V7/iii'],
    'H': ['V7#5'],
    
    'Stop': ['Rest']
}
    
# Dictionary mapping nucleotides to chord tone indices
NUCLEOTIDE_TO_INDEX = {
    'a': [0],
    'c': [1],
    't': [2],
    'g': [3],
}


def get_mapping_output(mapping: dict, input: str, stream: Optional[stream.Part]=None, k: Optional[key.Key]=None, key_list: Optional[list]=None):
    """Converts mapping input to output. If stream is given, adds output to the stream. If key_list is given, builds a list of the key centers in the stream.

    Args:
        input (str): The nonterminal to expand.
        stream (Optional[stream.Part], optional): The stream.Part object to add to. Defaults to None.
        k (Optional[key.Key], optional): The primary song key. Defaults to None.
        key_list (Optional[list], optional): A list of key centers in the song. Defaults to None.
    """
    possible = mapping[input]
    choice = possible[random.randint(0, len(possible) - 1)]
    if stream is None:
        return choice
    else:
        # Add the chord of length 4 (in quarter notes) to stream
        stream.append(chord.Chord(roman.RomanNumeral(choice, k), quarterLength = 4.0))
        # Add the main key to the key list for the bar 
        if key_list is not None:
            key_list.append(k)


def main():
    # Build argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-rs', '--random_seed', type=int, help="Random seed to use. '-1' for no seed. Default is 42.")
    parser.add_argument('-k', '--key', type=str, help="Key to generate the song in. Only accepts flats (ex: 'Eb'), no sharps. Default is 'C'.")
    parser.add_argument('-f', '--filename', type=str, help="Filename of .txt file where DNA is stored (including extension). Default is 'SLIT1.txt'")
    parser.add_argument('-m', '--midi', help='Shows score in midi format (flag argument).', action='store_true')
    parser.add_argument('-s', '--sheet_music', help='Shows score as sheet music (flag argument).', action='store_true')
    parser.add_argument('-t', '--text', help='Shows score as text (flag argument).', action='store_true')
    
    # Parse arguments, set up program
    args = parser.parse_args()
    # Random Seed
    if args.random_seed:
        if args.random_seed == -1:
            print('Generating a random piece of music.')
        else:
            print(f'Seed set to {args.random_seed}')
    else:
        random.seed = 42
        print(f'Seed set to default: 42')
    
    # Key
    k = key.Key('C')
    key_set_flag = False
    if args.key:
        for letter in ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']:
            if args.key == letter:
                k = key.Key(letter)
                print(f'Key set to {letter}')
                key_set_flag = True
        if not key_set_flag:
            print(f'Key provided is invalid. Key set to default: C')
    
    # Filename
    if args.filename:
        if args.filename[-4:] == '.txt' and os.path.isfile(args.filename):
            filename = args.filename
            print(f'Filename set to: {filename}')
        else:
            print(f'Filename provided is invalid. Filename set to default: SLIT1.txt')
            filename = 'SLIT1.txt'
    else:
        filename = 'SLIT1.txt'
        print(f'Filename set to default: SLIT1.txt')
        
    if args.midi:
        output_type = 'midi'
    elif args.sheet_music:
        output_type = ''
    elif args.text:
        output_type = 'text'
    else:
        output_type = 'midi'
    
    # Set up the score
    score = stream.Score()
    chords = stream.Part()
    chords.append(clef.BassClef())
    melody = stream.Part()
    melody.append(clef.TrebleClef())

    # Add time signature and key information to the score
    time_signature = meter.TimeSignature('4/4')
    chords.append(time_signature)
    melody.append(time_signature)
    chords.append(k)
    melody.append(k)

    nucleotides = ''
    # Get DNA from .txt file
    with open(filename) as f_in:
        for line in f_in:
            nucleotides += line.strip()
    
    # Add chords to the first part object
    key_list = []
    curr_codon = ''
    for n in nucleotides:
        # Transcription
        if n.lower() == 't':
            n = 'u'
        curr_codon += n.lower()
        # If codon is size 3, translate into amino acid
        if len(curr_codon) % 3 == 0:
            # Translation
            amino_acid = get_mapping_output(TRANSLATION, curr_codon.lower())
            get_mapping_output(AMINO_ACID_TO_CHORD, amino_acid, chords, k, key_list)
            get_mapping_output(AMINO_ACID_TO_CHORD, 'R', chords, k, key_list)
            curr_codon = ''

    # Calculate the time in quarter notes occupied by the chords
    chord_length = 0
    for chord in chords.notes:
        chord_length += chord.duration.quarterLength
        
    chords = chords.transpose(-12)

    flag = False
    current_chord_idx = 0
    melody_length = 0
    measure_pos = 0
    
    # Add a melody based on the DNA sequence and shaped by the protein-based chord sequence.
    while not flag:
        # Continue while the melody is not longer than the chords
        if melody_length >= chord_length:
            flag = True
            break
        # Iterate through the pitches in the DNA
        for n in nucleotides:
            # Figure out chord tone using nucleotide
            i = get_mapping_output(NUCLEOTIDE_TO_INDEX, n.lower())
            # Get current chord
            curr_chord = chords.notes[current_chord_idx]
            
            # TODO: Replace this part with the generative model
            # Pick a note length randomly
            quarter_length = random.choices([0.25, 0.5, 1], weights=[.1, .5, .4])[0]
            
            # Add note to the melody
            melody.append(note.Note(curr_chord.pitches[i % len(curr_chord.notes)], quarterLength=quarter_length).transpose(12))
            
            # Calculate location in the score and measure
            measure_pos += quarter_length
            melody_length += quarter_length
            if melody_length >= chord_length:
                flag = True
                break
            if measure_pos >= 4:
                current_chord_idx += 1
                measure_pos -= 4

    # Insert everything into the score object
    score.insert(0, melody)
    score.insert(0, chords)
    score.insert(0, metadata.Metadata())
    score.metadata.title = 'Bird Song'
    score.metadata.composer = 'Emily Ertle, Alberto Naveira, Dan Little'
    

    # Play midi, output sheet music, or print the contents of the stream
    if output_type == '':
        score.show()
    else:    
        score.show(output_type)

if __name__ == "__main__":
    main()