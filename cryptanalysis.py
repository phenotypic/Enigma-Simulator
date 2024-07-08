from enigma import Enigma
from progressbar import progressbar
from string import ascii_uppercase
import itertools, heapq

# Function to find the best rotors and rotor positions
def find_rotors_and_positions(ciphertext, scorer, top_n, available_rotors, reflector):
    top_rotor_configs = []
    heapq.heapify(top_rotor_configs)
    
    # Generate all permutations of rotors and combinations of rotor positions
    rotor_permutations = list(itertools.permutations(available_rotors, 3))
    rotor_position_combinations = list(itertools.product(range(1, 27), repeat=3))
    
    # Iterate through each combination of rotors and rotor positions
    for rotors in progressbar(rotor_permutations):
        for position in rotor_position_combinations:
            # Initialise the Enigma machine with the current settings and decrypt the ciphertext
            e = Enigma(rotors, reflector, position, [1, 1, 1], [])
            decrypted = e.transform_string(ciphertext)
            # Score the decrypted text
            score = scorer.score(decrypted)
            # Maintain a heap of the top N scores and corresponding settings
            if len(top_rotor_configs) < top_n:
                heapq.heappush(top_rotor_configs, (score, (rotors, position)))
            else:
                heapq.heappushpop(top_rotor_configs, (score, (rotors, position)))

    return top_rotor_configs

# Function to find the best ring settings given a list of base configurations
def find_ring_settings(ciphertext, scorer, top_rotor_configs, reflector):
    best_score = float('-inf')
    best_settings = {}

    # Iterate over each base configuration
    for rotor_config in progressbar(top_rotor_configs):
        rotors, initial_rotor_positions = rotor_config[1]
        
        # Iterate through possible ring settings for the second and third rotors
        for ring2 in range(1, 27):
            for ring3 in range(1, 27):
                ring_settings = [1, ring2, ring3]
                # Adjust the rotor position based on the ring settings
                adjusted_rotor_positions = [
                    initial_rotor_positions[0],
                    (initial_rotor_positions[1] + ring2 - 2) % 26 + 1,
                    (initial_rotor_positions[2] + ring3 - 2) % 26 + 1,
                ]
                # Initialise the Enigma machine with the current settings and decrypt the ciphertext
                e = Enigma(rotors, reflector, adjusted_rotor_positions, ring_settings, [])
                decrypted = e.transform_string(ciphertext)
                # Score the decrypted text
                score = scorer.score(decrypted)
                # Update the best settings if the current score is higher
                if score > best_score:
                    best_score = score
                    best_settings = {
                        'rotors': rotors,
                        'rotor_positions': adjusted_rotor_positions,
                        'ring_settings': ring_settings,
                        'score': score
                    }

    return best_settings

# Function to find the best plugboard settings
def find_plugboard(ciphertext, scorer, best_settings, max_pairs, reflector):
    alphabet = list(ascii_uppercase)
    best_settings['plugboard'] = []

    # Iterate to find the best plugboard pairs
    for _ in range(max_pairs):
        top_score = float('-inf')
        top_pair = None
        
        # Test each combination of remaining letters
        for letter_pair in itertools.combinations(alphabet, 2):
            test_plugboard = best_settings['plugboard'] + [''.join(letter_pair)]
            # Initialise the Enigma machine with the current settings and decrypt the ciphertext
            e = Enigma(best_settings['rotors'], reflector, best_settings['rotor_positions'], best_settings['ring_settings'], test_plugboard)
            decrypted = e.transform_string(ciphertext)
            # Score the decrypted text
            score = scorer.score(decrypted)
            # Update the top score and pair if the current score is higher
            if score > top_score:
                top_score = score
                top_pair = letter_pair

        # If a top pair is found, update the best settings and remove the letters from the alphabet
        if top_pair and top_score > best_settings['score']:
            best_settings['score'] = top_score
            best_settings['plugboard'].append(''.join(top_pair))
            alphabet.remove(top_pair[0])
            alphabet.remove(top_pair[1])
        else:
            break

    return best_settings
