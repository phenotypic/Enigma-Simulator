class Plugboard:
    def __init__(self, connections):
        self.wiring = list(range(26))
        
        if connections is not None:
            pairings = [pair for pair in connections.split() if pair.isalpha() and len(pair) == 2]

            if len(pairings) > 10:
                raise ValueError('Plugboard can only have 10 connections')

            for pair in pairings:
                c1, c2 = ord(pair[0]) - 65, ord(pair[1]) - 65

                if self.wiring[c1] != c1 or self.wiring[c2] != c2:
                    raise Exception('Letters can only be plugged once')

                self.wiring[c1], self.wiring[c2] = c2, c1

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
        self.forward_wiring = [ord(char) - 65 for char in encoding]
        self.backward_wiring = [self.forward_wiring.index(i) for i in range(26)]
        self.notch_position = notch
        self.rotor_position = rotor_position - 1
        self.ring_setting = ring_setting - 1

    def encipher(self, k, pos, ring, mapping):
        shift = pos - ring
        return (mapping[(k + shift + 26) % 26] - shift + 26) % 26

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
    def __init__(self, rotors, reflector_name, rotor_positions, ring_settings, plugboard_connections, historic=False):
        rotors = [rotor.upper() for rotor in rotors]
        self.check_setup(rotors, reflector_name, rotor_positions, ring_settings, historic)
        self.reflector = Reflector(reflector_name.upper())
        self.rotors = [Rotor(rotor, position, setting) for rotor, position, setting in zip(rotors, rotor_positions, ring_settings)]
        self.plugboard = Plugboard(plugboard_connections.upper() if plugboard_connections else None)

    def rotate(self):
        # Esnure only the rightmost three rotors rotate
        rotatable_rotors = self.rotors[-3:]

        if rotatable_rotors[1].is_at_notch():
            rotatable_rotors[0].turnover()
            rotatable_rotors[1].turnover()
        elif rotatable_rotors[2].is_at_notch():
            rotatable_rotors[1].turnover()
        rotatable_rotors[2].turnover()

    def encrypt(self, c):
        self.rotate()

        c = self.plugboard.substitute(c)

        # Go through rotors right to left
        for rotor in reversed(self.rotors):
            c = rotor.forward(c)

        c = self.reflector.reflect(c)

        # Go through rotors left to right
        for rotor in self.rotors:
            c = rotor.backward(c)

        c = self.plugboard.substitute(c)

        return c

    def encrypt_char(self, char):
        return chr(self.encrypt(ord(char.upper()) - 65) + 65)

    def encrypt_string(self, input_string):
        return ''.join(self.encrypt_char(char) for char in input_string if char.isalpha())
    
    def check_setup(self, rotors, reflector_name, rotor_positions, ring_settings, historic):
        # Ensure length of rotors, rotor positions, and ring settings are equal
        if len(rotors) != len(rotor_positions) or len(rotors) != len(ring_settings):
            raise ValueError('Number of rotors, rotor positions, and ring settings must be equal')
        
        # Ensure number of rotors is 3 or 4
        if len(rotors) not in [3, 4]:
            raise ValueError('Number of rotors must be 3 or 4')
        
        # Validate rotor positions and ring settings
        if not all(1 <= pos <= 26 for pos in rotor_positions):
            raise ValueError("All rotor positions must be between 1 and 26.")
        
        if not all(1 <= setting <= 26 for setting in ring_settings):
            raise ValueError("All ring settings must be between 1 and 26.")
        
        if historic:
            # Check for duplicate rotors
            if len(rotors) != len(set(rotors)):
                raise ValueError('Each rotor type can only be used once.')

            # Check for correct reflector usage
            if len(rotors) == 3 and reflector_name not in {'UKW_A', 'UKW_B', 'UKW_C'}:
                raise ValueError('Invalid reflector for 3-rotor setup')
            elif reflector_name not in {'UKW_B_THIN', 'UKW_C_THIN'}:
                raise ValueError('Invalid reflector for 4-rotor setup')
        
            # Check for correct Beta/Gamma rotor usage
            if len(rotors) == 4:
                if rotors[0] not in ['BETA', 'GAMMA']:
                    raise ValueError('First rotor in a 4-rotor setup must be Beta or Gamma')
            else:
                if 'BETA' in rotors or 'GAMMA' in rotors:
                    raise ValueError('Beta and Gamma rotors are only allowed in 4-rotor setups')


# Example usage
enigma = Enigma(['I', 'II', 'III'], 'UKW_B', [1, 2, 3], [1, 2, 3], 'AB CD EF')
encrypted = enigma.encrypt_string('HELLO WORLD')
print(encrypted)

