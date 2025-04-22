import random
from music21 import converter, note, chord, stream

# bird calls from the xml file and how many measures they are
BIRD_MEASURE_MAP = [
    ("Nightingale", 1),
    ("Cuckoo", 1),
    ("Northern Lapwing", 1),
    ("Sparrow", 1),
    ("Black Bird", 4),
    ("Duck", 1),
    ("Throstle", 2),
    ("Unknown", 1),
    ("Bantam Cock", 2),
    ("Game Cock", 2),
    ("Game Cock Alt", 1),
    ("Little Bird", 2),
    ("Red Tailed Hawk", 1),
    ("Peacock", 2),
    ("Parrot", 1),
    ("Unknown 1Alt", 1),
    ("Pigeon", 1),
    ("Unknown 2Alt", 1),
    ("Owl", 2),
]

def extract_bird_rhythms(filepath, bird_measure_map):
    """
    Build a dictionary with each bird type as key and the rhythm of their call as the value
    """
    score = converter.parse(filepath)
    part = score.parts[0]
    measures = list(part.getElementsByClass(stream.Measure))

    bird_rhythms = {}
    current_measure = 0

    for bird_name, measure_count in bird_measure_map:
        rhythm_sequence = []
        for i in range(current_measure, current_measure + measure_count):
            if i < len(measures):
                for element in measures[i].notesAndRests:
                    if isinstance(element, (note.Note, note.Rest, chord.Chord)):
                        rhythm_sequence.append(float(element.quarterLength))
        bird_rhythms[bird_name] = rhythm_sequence
        current_measure += measure_count

    return bird_rhythms

def generate_random_measure():
    """
    Between bird calls create random rhythms
    """
    options = [1.0, 0.5, 0.25]
    total = 0
    measure = []
    while total < 4.0:
        dur = random.choice(options)
        if total + dur <= 4.0:
            measure.append(dur)
            total += dur
    return measure

def generate_rhythm(bird_rhythms, target_duration):
    """
    Creates a custom rhythm with bird calls and random rhythms
    """
    output_rhythm = []
    bird_names = list(bird_rhythms.keys())

    total_duration = 0
    while total_duration < target_duration:
        bird = random.choice(bird_names)
        bird_rhythm = bird_rhythms[bird]
        bird_dur = sum(bird_rhythm)

        if total_duration + bird_dur <= target_duration:
            output_rhythm.extend(bird_rhythm)
            total_duration += bird_dur
        else:
            break

        rand_measure = generate_random_measure()
        rand_dur = sum(rand_measure)

        if total_duration + rand_dur <= target_duration:
            output_rhythm.extend(rand_measure)
            total_duration += rand_dur
        else:
            break

    while sum(output_rhythm) > target_duration:
        output_rhythm.pop()

    return output_rhythm

def generate_bird_rhythm(target_duration, filepath='./Bird_Calls/score.xml'):
    """
    API call function
    """
    bird_rhythms = extract_bird_rhythms(filepath, BIRD_MEASURE_MAP)
    return generate_rhythm(bird_rhythms, target_duration=target_duration)


