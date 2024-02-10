class Plugboard:
    def __init__(self, connections):
        self.wiring = list(range(26))
        
        # Set up plugboard connections
        if connections is not None:
            pairings = [pair for pair in connections.split() if pair.isalpha() and len(pair) == 2]

            if len(pairings) > 10:
                raise ValueError('Plugboard can only have 10 connections')

            for pair in pairings:
                c1, c2 = ord(pair[0]) - 65, ord(pair[1]) - 65

                if self.wiring[c1] != c1 or self.wiring[c2] != c2:
                    raise Exception('Letters can only be plugged once')

                self.wiring[c1], self.wiring[c2] = c2, c1

    # Substitute letter through the plugboard
    def substitute(self, c):
        return self.wiring[c]


class Reflector:
    reflector_encodings = {
            'UKW_A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
            'UKW_B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
            'UKW_C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
            'UKW_B_THIN': 'ENKQAUYWJICOPBLMDXZVFTHRGS',
            'UKW_C_THIN': 'RDOBJNTKVEHMLFCWZAXGYIPSUQ'
        }
    
    def __init__(self, name):
        encoding = self.reflector_encodings.get(name, 'ZYXWVUTSRQPONMLKJIHGFEDCBA')
        self.forward_wiring = [ord(char) - 65 for char in encoding]
    
    # Reflect letter through the reflector
    def reflect(self, c):
        return self.forward_wiring[c]


class Rotor:
    rotor_encodings = {
            'I': ('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 16),
            'II': ('AJDKSIRUXBLHWTMCQGZNPYFVOE', 4),
            'III': ('BDFHJLCPRTXVZNYEIWGAKMUSQO', 21),
            'IV': ('ESOVPZJAYQUIRHXLNFTGKDCMWB', 9),
            'V': ('VZBRGITYUPSDNHLXAWMJQOFECK', 25),
            'VI': ('JPGVOUMFYQBENHZRDKASXLICTW', [12, 25]),
            'VII': ('NZJHGRCXMYSWBOUFAIVLPEKQDT', [12, 25]),
            'VIII': ('FKQHTLXOCBJSPDZRAMEWNIUYGV', [12, 25]),
            'BETA': ('LEYJVCNIXWPBQMDRTAKZGFUHOS', None),
            'GAMMA': ('FSOKANUERHMBTIYCWLQPZXVGJD', None)
        }
    
    def __init__(self, name, rotor_position, ring_setting):
        encoding, notch = self.rotor_encodings.get(name, ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 0))
        self.name = name
        # Create convert forward wiring from letters to numbers
        self.forward_wiring = [ord(char) - 65 for char in encoding]
        # Create backward wiring by inverting forward wiring
        self.backward_wiring = [self.forward_wiring.index(i) for i in range(26)]
        self.notch_position = notch
        self.rotor_position = rotor_position - 1
        self.ring_setting = ring_setting - 1

    def encipher(self, c, pos, ring, mapping):
        # Adjust character by ring and position, pass through rotor wiring, then reverse adjustment
        shift = pos - ring
        return (mapping[(c + shift + 26) % 26] - shift + 26) % 26

    def forward(self, c):
        return self.encipher(c, self.rotor_position, self.ring_setting, self.forward_wiring)

    def backward(self, c):
        return self.encipher(c, self.rotor_position, self.ring_setting, self.backward_wiring)

    def is_at_notch(self):
        if isinstance(self.notch_position, list):
            return self.rotor_position in self.notch_position
        else:
            return self.rotor_position == self.notch_position

    def turnover(self):
        self.rotor_position = (self.rotor_position + 1) % 26


class Enigma:
    def __init__(self, rotors, reflector_name, rotor_positions, ring_settings, plugboard_connections):
        rotors = [rotor.upper() for rotor in rotors]
        rotor_positions = self.convert_to_numbers(rotor_positions)
        ring_settings = self.convert_to_numbers(ring_settings)
        
        self.reflector = Reflector(reflector_name.upper())
        self.rotors = [Rotor(rotor, position, setting) for rotor, position, setting in zip(rotors, rotor_positions, ring_settings)]
        self.plugboard = Plugboard(plugboard_connections.upper() if plugboard_connections else None)

    def convert_to_numbers(self, input_list):
        # Convert letters to numbers for rotor positions and ring settings if necessary
        output_list = []
        for item in input_list:
            if isinstance(item, str):
                number = ord(item.upper()) - ord('A') + 1
                output_list.append(number)
            else:
                output_list.append(item)
        return output_list

    def rotate(self):
        # Esnure only the three rightmost rotors rotate
        rotatable_rotors = self.rotors[-3:]

        # Turnover rotors if at notch position, accounting for double step
        if rotatable_rotors[1].is_at_notch():
            rotatable_rotors[0].turnover()
            rotatable_rotors[1].turnover()
        elif rotatable_rotors[2].is_at_notch():
            rotatable_rotors[1].turnover()
        rotatable_rotors[2].turnover()

    def encrypt(self, c):
        # Rotate rotors before transforming character
        self.rotate()

        # Substitute letter through plugboard
        c = self.plugboard.substitute(c)

        # Transform character through rotors right to left
        for rotor in reversed(self.rotors):
            c = rotor.forward(c)

        c = self.reflector.reflect(c)

        # Transform character through rotors left to right
        for rotor in self.rotors:
            c = rotor.backward(c)

        # Substitute letter through plugboard
        c = self.plugboard.substitute(c)

        return c

    # Transform a single character through the enigma machine
    def transform_char(self, char):
        return chr(self.encrypt(ord(char.upper()) - 65) + 65)

    # Transform a string through the enigma machine
    def transform_string(self, input_string):
        return ''.join(self.transform_char(char) for char in input_string if char.isalpha())
