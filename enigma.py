class Plugboard:
    def __init__(self, connections):
        self.wiring = list(range(26))
        
        if connections is not None:
            pairings = [pair for pair in connections.split() if pair.isalpha() and len(pair) == 2]
            plugged_characters = set()

            for pair in pairings:
                c1, c2 = ord(pair[0].upper()) - 65, ord(pair[1].upper()) - 65

                # If a character is already plugged, ignore the rest of the pairings
                if c1 in plugged_characters or c2 in plugged_characters:
                    break

                plugged_characters.add(c1)
                plugged_characters.add(c2)
                self.wiring[c1], self.wiring[c2] = c2, c1

    def forward(self, c):
        return self.wiring[c]


class Reflector:
    reflector_encodings = {
            'UKW_B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
            'UKW_C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL'
        }
    
    def __init__(self, name):
        encoding = self.reflector_encodings.get(name, 'ZYXWVUTSRQPONMLKJIHGFEDCBA')
        self.forward_wiring = [ord(char) - 65 for char in encoding]
    
    def forward(self, c):
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
            'VIII': ('FKQHTLXOCBJSPDZRAMEWNIUYGV', [12, 25])
        }
    
    def __init__(self, name, rotor_position, ring_setting):
        encoding, notch = self.rotor_encodings.get(name, ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 0))
        self.name = name
        self.forward_wiring = [ord(char) - 65 for char in encoding]
        self.backward_wiring = self.inverse_wiring(self.forward_wiring)
        self.rotor_position = rotor_position - 1
        self.notch_position = notch
        self.ring_setting = ring_setting - 1

    @staticmethod
    def inverse_wiring(wiring):
        inverse = [0] * len(wiring)
        for i, forward in enumerate(wiring):
            inverse[forward] = i
        return inverse

    @staticmethod
    def encipher(k, pos, ring, mapping):
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
    def __init__(self, rotors, reflector_name, rotor_positions, ring_settings, plugboard_connections=None):
        self.left_rotor = Rotor(rotors[0], rotor_positions[0], ring_settings[0])
        self.middle_rotor = Rotor(rotors[1], rotor_positions[1], ring_settings[1])
        self.right_rotor = Rotor(rotors[2], rotor_positions[2], ring_settings[2])
        self.reflector = Reflector(reflector_name)
        self.plugboard = Plugboard(plugboard_connections)

    def rotate(self):
        if self.middle_rotor.is_at_notch():
            self.middle_rotor.turnover()
            self.left_rotor.turnover()
        elif self.right_rotor.is_at_notch():
            self.middle_rotor.turnover()
        self.right_rotor.turnover()

    def encrypt(self, c):
        self.rotate()

        c = self.plugboard.forward(c)

        c = self.right_rotor.forward(c)
        c = self.middle_rotor.forward(c)
        c = self.left_rotor.forward(c)

        c = self.reflector.forward(c)

        c = self.left_rotor.backward(c)
        c = self.middle_rotor.backward(c)
        c = self.right_rotor.backward(c)

        c = self.plugboard.forward(c)

        return c

    def encrypt_char(self, char):
        return chr(self.encrypt(ord(char.upper()) - 65) + 65)

    def encrypt_string(self, input_string):
        return ''.join(self.encrypt_char(char) for char in input_string if char.isalpha())


# Example usage
enigma = Enigma(['I', 'II', 'VIII'], 'UKW_B', [1, 2, 3], [1, 2, 3], 'AB CD EF')
encrypted = enigma.encrypt_string('HELLO WORLD')
print(encrypted)
