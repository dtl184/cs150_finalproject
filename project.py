import argparse
from music21 import *
import os
import random
from mapping import *
from rhythm import generate_bird_rhythm

def main():
    # Build argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-rs', '--random_seed', type=int, help='random seed to use')
    parser.add_argument('-k', '--key', type=str, help='key to generate the song in')
    parser.add_argument('-f', '--filename', type=str, help='filename of .txt file where DNA is stored')
    parser.add_argument('-m', '--midi', help='shows score in midi format', action='store_true')
    parser.add_argument('-s', '--sheet_music', help='shows score as sheet music', action='store_true')
    parser.add_argument('-t', '--text', help='shows score as text', action='store_true')
    parser.add_argument('-p', '--population_size', type=int, default=20, help='population size for genetic algorithm')
    parser.add_argument('-g', '--generations', type=int, default=50, help='number of generations for genetic algorithm')
    parser.add_argument('-mr', '--mutation_rate', type=float, default=0.01, help='mutation rate for genetic algorithm')
    parser.add_argument('-cr', '--crossover_rate', type=float, default=0.7, help='crossover rate for genetic algorithm')
    
    # Parse arguments, set up program
    args = parser.parse_args()
    # Random Seed
    if args.random_seed:
        if args.random_seed == -1:
            print('Generating a random piece of music.')
        else:
            random.seed = args.random_seed
            rs = args.random_seed
            print(f'Seed set to {args.random_seed}')
    else:
        random.seed = 42
        rs = 42
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
    
    
    chordList = set()
    for _,cL in AMINO_ACID_TO_CHORD.items():
        chordList.add(cL[0])
        
    chordTypes = {
        'tonic': [
            'vi', 'vi7', 'iii', 'iii7', 'I[add6]', 'I', 'I[add9]', 'Imaj7'
        ],
        'subdominant': [
            'ii7', 'IV[add9]', 'IV', 'IVmaj7', 'ii'
        ],
        'dominant': [
            'V7#5', 'V7', 'vii°', 'V', 'vii°7', 'V7/iii', 'V[add6]'
        ],
        'Rest': ['Rest']
    }
    
    rewardMap = {
        ('tonic', 'tonic'): 1,
        ('tonic', 'subdominant'): 6,
        ('tonic', 'dominant'): 3,
        ('subdominant', 'tonic'): 2,
        ('subdominant', 'subdominant'): 4,
        ('subdominant', 'dominant'): 4,
        ('dominant', 'tonic'): 8,
        ('dominant', 'subdominant'): 0,
        ('dominant', 'dominant'): 2
    }
    
    # DNA bases
    BASES = ['a', 't', 'g', 'c']

    # Genetic Algorithm Hyperparameters
    POPULATION_SIZE = args.population_size
    GENERATIONS = args.generations
    MUTATION_RATE = args.mutation_rate
    CROSSOVER_RATE = args.crossover_rate

    chord2Function = {}
    for fun, cL in chordTypes.items():
        for c in cL:
            chord2Function[c] = fun
            
    originalSeq = ''
    with open(filename) as f_in:
            for line in f_in:
                originalSeq += line.strip()

    def create_music(DNASeq, k = key.Key('C'), rs = 42):
        ## Commenting out irrelevant argparse stuff
        random.seed = rs
        # k = key.Key('C')
        
        # Set up the score
        # score = stream.Score()
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
        
        ##### GET NUCLEOTIDES FROM INPUT
        for char in DNASeq:
            nucleotides += char
        
        
        # Add chords to the first part object
        key_list = []
        curr_codon = ''
        roman_chords = []
        for n in nucleotides:
            # Transcription
            if n.lower() == 't':
                n = 'u'
            curr_codon += n.lower()
            # If codon is size 3, translate into amino acid
            if len(curr_codon) % 3 == 0:
                # Translation
                amino_acid = get_mapping_output(TRANSLATION, curr_codon.lower())
                curr_chord = get_mapping_output(AMINO_ACID_TO_CHORD, amino_acid, chords, k, key_list)
                roman_chords.append(curr_chord)
                # get_mapping_output(AMINO_ACID_TO_CHORD, 'R', chords, k, key_list)
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
        rhythm_idx = 0
        
        rhythmList = generate_bird_rhythm(chord_length)
        rhythmList = [r for r in rhythmList if r > 0]
        
        if sum(rhythmList) < chord_length:
            rhythmList.append(chord_length - sum(rhythmList))
        
        # Add a melody based on the DNA sequence and shaped by the protein-based chord sequence.
        while not flag:
            # Continue while the melody is not longer than the chords
            if melody_length >= (chord_length-1e-4):
                flag = True
                break
            # Iterate through the pitches in the DNA
            for n in nucleotides:
                # print(current_chord_idx, melody_length, measure_pos, rhythm_idx, rhythmList[rhythm_idx])
                # Figure out chord tone using nucleotide
                i = get_mapping_output(NUCLEOTIDE_TO_INDEX, n.lower())
                # Get current chord
                curr_chord = chords.notes[current_chord_idx]
                
                # TODO: Replace this part with the generative model
                # Pick a note length randomly
                quarter_length = rhythmList[rhythm_idx] # random.choices([0.25, 0.5, 1], weights=[.1, .5, .4])[0]
                
                # Add note to the melody
                melody.append(note.Note(curr_chord.pitches[i % len(curr_chord.notes)], quarterLength=quarter_length).transpose(12))
                
                # Calculate location in the score and measure
                measure_pos += quarter_length
                melody_length += quarter_length
                rhythm_idx += 1
                if melody_length >= (chord_length-1e-4):
                    flag = True
                    break
                if measure_pos >= 4:
                    current_chord_idx += 1
                    measure_pos -= 4
        
        return melody, roman_chords

    def reward(melody, chords, k):
        count = 0
        # melody smoothness evaluation
        pastNote = None
        for n in melody:
            if not isinstance(n, note.Note): continue
            if pastNote is None: pastNote = n.pitch.midi
            else:
                count += 2 * (1 / (1 + abs(n.pitch.midi - pastNote)))
                if n.pitch.midi == pastNote: count -= 2
                pastNote = n.pitch.midi
        
        if n.pitch.midi in [i+k.pitches[0].midi for i in [0,4,7,12]]: count += 20
        
        # chord progression evaluation
        pastChord = None
        for c in chords:
            if pastChord is None and c != 'Rest': pastChord = c
            else:
                if 'Rest' == c: continue
                count += rewardMap[(chord2Function[pastChord], chord2Function[c])]
                pastChord = c
        if chord2Function[c] == 'tonic': count += 20
        
        
        return count

    # Helper: mutate a DNA string
    def mutate(dna):
        dna = list(dna)
        for i in range(len(dna)):
            if random.random() < MUTATION_RATE:
                dna[i] = random.choice(BASES)
        return ''.join(dna)

    # Helper: crossover two parents
    def crossover(parent1, parent2):
        if random.random() > CROSSOVER_RATE:
            return parent1, parent2
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2

    # Helper: evaluate fitness
    def fitness(dna, k, rs):
        melody, chords = create_music(dna, k, rs)
        return reward(melody, chords, k)

    # Genetic Algorithm
    def evolve_music(initial_dna, generations=GENERATIONS, k = key.Key('C'), rs = 42):
        # Initial population
        population = [mutate(initial_dna) for _ in range(POPULATION_SIZE)]
        population[0] = initial_dna  # include the original sequence
        best_scores = []
        for gen in range(generations):
            scored = [(dna, fitness(dna, k, rs)) for dna in population]
            scored.sort(key=lambda x: x[1], reverse=True)  # highest reward first

            print(f"Generation {gen+1}: Best score = {scored[0][1]}")
            
            best_scores.append(scored[0][1])
            # Elitism: keep top 2
            new_population = [scored[0][0], scored[1][0]]

            # Create next generation
            while len(new_population) < POPULATION_SIZE:
                parent1, parent2 = random.choices(scored[:10], k=2)  # select from top 10
                child1, child2 = crossover(parent1[0], parent2[0])
                new_population.extend([mutate(child1), mutate(child2)])

            population = new_population[:POPULATION_SIZE]  # trim if overfilled

        # Return the best DNA and its melody/chords
        best_dna = max(population, key=lambda dna: fitness(dna, k, rs))  # Use lambda to pass additional parameters
        melody, chords = create_music(best_dna, k=k, rs=rs)
        return best_dna, melody, chords, best_scores


    best_dna, melody, roman_chords, best_scores = evolve_music(originalSeq, k=k, rs=rs)

    #k = key.Key('C')
    score = stream.Score()
    chords = stream.Part()
    chords.append(clef.BassClef())
    time_signature = meter.TimeSignature('4/4')
    chords.append(time_signature)
    chords.append(k)

    for c in roman_chords:
        if c == 'Rest': chords.append(note.Rest(length= 4.0))
        else:
            chords.append(chord.Chord(roman.RomanNumeral(c, k), quarterLength = 4.0))

    chords = chords.transpose(-12)

    score.insert(0, melody)
    score.insert(0, chords)
    score.insert(0, metadata.Metadata())
    score.metadata.title = 'Genetically accurate bird music :)'
    score.metadata.composer = 'Emily Ertle, Alberto Naveira, Dan Little'

    # Play midi, output sheet music, or print the contents of the stream
    if output_type == '':
        score.show()
    else:    
        score.show(output_type)
    
    
if __name__ == "__main__":
    main()

