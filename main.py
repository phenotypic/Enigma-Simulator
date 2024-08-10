from pyfiglet import Figlet
from prettytable import PrettyTable
from ngram_score import ngram_score
import enigma, cryptanalysis, os, re

# Available rotors and reflectors for the Enigma machine
available_rotors = list(enigma.Rotor.rotor_encodings.keys())
available_reflectors = list(enigma.Reflector.reflector_encodings.keys())

def modify_array(user_config, option):
    option = list(user_config.keys())[int(option) - 1]
    input_str = input(f'\nEnter {option.lower()}: ').replace("'", '')
    if ',' in input_str or ' ' in input_str:
        input_str = re.split(r',\s*|\s+', input_str.strip())
    
    if option == 'Rotors':
        user_config[option] = [available_rotors[int(elem) - 1] if elem.isdigit() else elem.upper() for elem in input_str][:4]
    else:
        user_config[option] = [int(elem) if elem.isdigit() else elem.upper() for elem in input_str][:13]
        if option != 'Plugboard Connections':
            user_config[option] = user_config[option][:4]

def display_settings_table(user_config):
    table = PrettyTable(['Option', 'Setting', 'Value'])
    for i, (key, value) in enumerate((user_config.items())):
        if isinstance(value, list):
            display_value = ', '.join(map(str, value))
        else:
            display_value = str(value)
        table.add_row([i + 1, key, display_value])
    print(table)
    while True:
        chosen_setting = input('\nSelect option to modify: ')
        if chosen_setting.isdigit() and 1 <= int(chosen_setting) <= len(user_config):
            return chosen_setting
        else:
            print(f'Invalid option, please select a number between 1 and {len(user_config)}')


def select_reflector(user_config, three_rotors=False):
    # Use a different name for the local variable to avoid shadowing
    local_reflectors = available_reflectors[:3] if three_rotors else available_reflectors

    # Display the available reflectors
    reflector_table = PrettyTable(['Number', 'Reflector'])
    for i, reflector in enumerate(local_reflectors):
        reflector_table.add_row([i + 1, reflector])
    print(reflector_table)

    # Select the reflector (either by number or by name)
    reflector_choice = input('\nSelect reflector: ')
    if reflector_choice.isdigit():
        user_config['Reflector'] = local_reflectors[int(reflector_choice) - 1]
    else:
        user_config['Reflector'] = reflector_choice.replace(' ', '_').upper()

def clear_display():
    os.system('clear' if os.name != 'nt' else 'cls')

def get_enigma_settings():
    # Default settings for the Enigma machine
    user_config = {
        'Rotors': ['VI', 'I', 'III'],
        'Rotor Positions': [1, 17, 12],
        'Ring Settings': [5, 13, 24],
        'Reflector': 'UKW_B',
        'Plugboard Connections': ['BQ', 'CR', 'DI', 'EJ', 'KW', 'MT', 'OS', 'PX', 'UZ', 'GH']
    }

    while True:
        # Display the settings table and prompt the user to select an option
        clear_display()
        chosen_setting = display_settings_table(user_config)

        # If the user presses Return, check if the settings are valid and return the settings
        if not chosen_setting:
            if len(user_config['Rotors']) == len(user_config['Rotor Positions']) == len(user_config['Ring Settings']):
                return user_config
            else:
                input('\nNumber of rotors, rotor positions, and ring settings must match! ')
                continue

        # Handle the selected option
        if chosen_setting == '1':
            print('\nAvailable rotors:', ', '.join(available_rotors))
        if chosen_setting == '4':
            select_reflector(user_config, False)
            continue

        modify_array(user_config, chosen_setting)

def use_enigma(user_config, plaintext):
    # Create an Enigma machine with the user's settings and encrypt the plaintext
    e = enigma.Enigma(
        user_config['Rotors'], user_config['Reflector'], 
        user_config['Rotor Positions'], user_config['Ring Settings'], 
        user_config['Plugboard Connections']
    )
    encrypted = e.transform_string(plaintext)
    print('\nTransformed message:', encrypted)

def get_crack_settings():
    # Default settings for the cryptanalysis tool
    user_config = {
        'N-Gram File': 'english_quintgrams.txt',
        'Rotors': available_rotors[:5],
        'Reflector': 'UKW_B',
        'Top N': 1000,
        'Max Pairs': 10
    }

    while True:
        clear_display()
        chosen_setting = display_settings_table(user_config)

        # If the user presses Return, return the settings
        if not chosen_setting:
            return user_config

        # Handle the selected option
        if chosen_setting == '1':
            file_list = os.listdir('frequencies')
            file_table = PrettyTable(['Option', 'File'])
            for i, file_name in enumerate(file_list):
                file_table.add_row([i + 1, file_name])
            print(file_table)
    
            user_config['N-Gram File'] = file_list[int(input('\nSelect file: ')) - 1]
        elif chosen_setting == '2':
            rotor_table = PrettyTable(['Option', 'Number of Rotors', 'Rotors'])
            rotor_table.add_row([1, 5, ', '.join(available_rotors[:5])])
            rotor_table.add_row([2, 8, ', '.join(available_rotors[:8])])
            print(rotor_table)

            user_input = input('\nSelect number of rotors: ')
            # Mapping user input to rotor counts
            rotor_count = {'1': 5, '2': 8, '5': 5, '8': 8, '3': 3}.get(user_input)
            user_config['Rotors'] = available_rotors[:8][:rotor_count]
        elif chosen_setting == '3':
            select_reflector(user_config, True)
        elif chosen_setting == '4':
            user_config['Top N'] = int(input('\nEnter top N: '))
        elif chosen_setting == '5':
            user_config['Max Pairs'] = int(input('\nEnter max pairs: '))

def crack_enigma(user_config, ciphertext):
    scorer = ngram_score(f'frequencies/{user_config["N-Gram File"]}')
    print('\nSearching for the best rotors and rotor positions...')
    top_rotor_configs = cryptanalysis.find_rotors_and_positions(
        ciphertext, scorer, user_config['Top N'], user_config['Rotors'], user_config['Reflector']
    )

    print('\nSearching for the best ring settings...')
    best_settings = cryptanalysis.find_ring_settings(
        ciphertext, scorer, top_rotor_configs, user_config['Reflector']
    )

    print('\nSearching for the best plugboard settings...')
    best_settings = cryptanalysis.find_plugboard(
        ciphertext, scorer, best_settings, user_config['Max Pairs'], user_config['Reflector']
    )

    print('\nRotors:', best_settings['rotors'])
    print('Rotor positions:', best_settings['rotor_positions'])
    print('Ring settings:', best_settings['ring_settings'])
    print('Plugboard settings:', best_settings['plugboard'])

    e = enigma.Enigma(
        best_settings['rotors'], user_config['Reflector'], 
        best_settings['rotor_positions'], best_settings['ring_settings'], 
        best_settings['plugboard']
    )
    best_settings['decrypted'] = e.transform_string(ciphertext)
    print('\nDecrypted message:', best_settings['decrypted'])

if __name__ == "__main__":
    f = Figlet(font='big')
    print('\n' + f.renderText('Enigma'))

    operation_mode = PrettyTable(['Option', 'Stage'])
    operation_mode.add_row([1, 'Enigma Machine'])
    operation_mode.add_row([2, 'Cryptanalysis'])
    print(operation_mode)

    chosen_operation = input('\nSelect option: ')
    if chosen_operation == '1':
        user_config = get_enigma_settings()
        while True:
            plaintext = input('\nEnter message to encrypt: ')
            if not plaintext:
                break
    
            use_enigma(user_config, plaintext)
    elif chosen_operation == '2':
        user_config = get_crack_settings()
        ciphertext = input('\nEnter message to decrypt: ')
        crack_enigma(user_config, ciphertext)
    else:
        print('Invalid option selected')
