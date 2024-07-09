# Enigma-Simulator

A historically accurate Enigma machine simulator written in Python. Supports both 3- and 4-rotor machines including the Enigma I, Enigma M3, and Enigma M4 'Shark'.

Includes a cryptanalysis tool capable of breaking Enigma-encrypted messages using only ciphertext.

Inspired by [Mike Pound](https://github.com/mikepound)'s [enigma](https://github.com/mikepound/enigma) project.

## Usage

Clone the repository:
```
git clone https://github.com/phenotypic/Enigma-Simulator.git
```

Change to the project directory:
```
cd Enigma-Simulator
```

Install dependencies:
```
pip3 install -r requirements.txt
```

Run the main script:
```
python3 main.py
```

The `main.py` script provides an interface for both the Enigma machine simulator and the cryptanalysis tool. When you run `main.py`, you can choose to either simulate an Enigma machine or perform cryptanalysis on an Enigma-encrypted message.

#### Enigma Machine Simulator

For the Enigma machine simulator, you can customise:
- Rotors
- Rotor positions
- Ring settings
- Reflector
- Plugboard connections

#### Cryptanalysis Tool

For the cryptanalysis tool, you can customise:
- Rotors (cracking Enigma with rotors I-V or I-VIII; 4-rotor Enigma machines are not supported yet)
- Reflector
- Top N (the number of top rotor and rotor position combinations considered for finding the best ring settings; default is 1000)
- Max Pairs (the maximum number of plugboard pairs considered during cracking; default is 10)

### Importing the Simulator

If you prefer to import and use the Enigma machine simulator directly in your own Python environment:

```python
from enigma import Enigma
```

3-rotor enigma:
```python
enigma = Enigma(rotors=['IV', 'VII', 'III'], reflector_name='UKW_B', rotor_positions=[18, 5, 21], ring_settings=[2, 14, 19], plugboard_connections=['BQ', 'CR', 'DI', 'EJ', 'KW', 'MT', 'OS', 'PX', 'UZ', 'GH'])
transformed = enigma.transform_string('Sometimes it is the people no one can imagine anything of who do the things no one can imagine')
print(transformed)
# KLFNHABWWYLCJIFRDGPFSPDETDNAKRNDSZJGXKDVFKCRZYEGXSXQAJOQQOTXHONGIURHBKPYIACN
```

4-rotor enigma:
```python
enigma = Enigma(rotors=['GAMMA', 'VI', 'VIII', 'IV'], reflector_name='UKW_C_THIN', rotor_positions=[19, 6, 25, 3], ring_settings=[8, 2, 12, 20], plugboard_connections=['BQ', 'CR', 'DI', 'EJ', 'KW', 'MT', 'OS', 'PX', 'UZ', 'GH'])
transformed = enigma.transform_string('Sometimes it is the people no one can imagine anything of who do the things no one can imagine')
print(transformed)
# NSORZZEIBALCKRRAXBDRPLAGYGFJNFKGTBLBIUUFAKZJQWXMAVJMFBXHEXXZKKHDLCMRBDEXJDVJ
```

**Notes:** The Enigma machine's symmetric design allows for both encryption and decryption using the `transform_string` method. Rotor positions and ring settings can be passed as numbers (1-26) or letters (A-Z).

## Enigma Machine

When a key is pressed on a physical Enigma machine, the electrical signal follows this path:

```
Keyboard  → Plugboard → Rightmost Rotor → Middle Rotor(s) → Leftmost Rotor
                                                                   ↓
                                                               Reflector
                                                                   ↓
Lampboard ← Plugboard ← Rightmost Rotor ← Middle Rotor(s) ← Leftmost Rotor
```

**Note:** Rotors rotate before the signal passes through them. When a rotor reaches its notch position, it causes the next rotor to rotate as well.

### Components

| Component | Options | Function |
| --- | --- | --- |
| Rotors | `I`, `II`, `III`, `IV`, `V`, `VI`, `VII`, `VIII`, `Beta`, and `Gamma` | Each rotor has a unique wiring that scrambles the input letter. Rotors can be set to different starting positions and rotate during operation to change the wiring path with each key press |
| Reflector | `UKW_A`, `UKW_B`, `UKW_C` (for 3-rotor setups); `UKW_B_THIN`, `UKW_C_THIN` (for 4-rotor setups) | Reflects the signal back through the rotors, ensuring encryption and decryption are reversible with the same settings |
| Plugboard | Up to 10 letter pairs | Allows pairs of letters to be swapped before and after rotor encryption, adding another layer of complexity |

**Note:** Enigma machines of the German Wehrmacht (Heer and Luftwaffe) were supplied with rotors `I`-`V`, while the German Navy (Kriegsmarine) were supplied with rotors `I`-`VIII`.

### Historical accuracy

By default, the script allows for a wide range of component configurations, including those that may not be historically accurate (e.g. reuse of the same rotor type). Follow these rules to ensure compliance with German Kriegsmarine configurations:

| | 3-Rotor Setup | 4-Rotor Setup |
| --- | --- | --- |
| **Rotor Count** | Exactly 3 rotors | Exactly 4 rotors |
| **Rotor Types** | Rotors `I`-`VIII` are allowed in any order | Leftmost rotor must be `Beta` or `Gamma`, others can be `I`-`VIII` |
| **Rotor Reuse** | Not allowed | Not allowed |
| **Reflector Types** | `UKW_A`, `UKW_B`, `UKW_C` | `UKW_B_THIN`, `UKW_C_THIN` |
| **Mandatory Rotors** | At least one of `VI`, `VII`, `VIII` must be included | At least one of `VI`, `VII`, `VIII` must be included |
| **Plugboard Connections** | Up to 10 letter pairs | Up to 10 letter pairs |

## Cryptanalysis

- **Scoring**: Uses quadgrams for scoring; a fitness function determines how 'English-like' the decryption is. Only English is implemented currently, but other languages can be added by generating new quadgram files.
- **Target Length**: Designed to decrypt messages of length 200-250 characters using only the ciphertext.
- **Complexity Reduction**: The process exploits the fact that the rotor order and indicator settings can be determined independent of the plugboard and ring settings, significantly reducing overall complexity.

### Steps

#### 1. Determine Rotor Order and Indicator Settings:

- Try deciphering the ciphertext with each rotor combination and rotor order for all possible combinations of indicator settings, assuming the ring settings are 'AAA'.
- Store the top N (1000 by default) decryptions for the next step.

#### 2. Find Ring Settings:

- Using the best rotor and indicator settings from the previous step, try each possible ring setting on the fast rotor first.
- The rotors must stay registered with the recovered indicator setting, so as each ring is moved, the trial indicator setting for that rotor is moved in the same direction.
- Use quadgram statistics to rank the candidates.

#### 3. Find Plugboard Settings:

- First, store the score with no plugboard.
- Try all 2-letter pairs in the first position and fix the highest scoring pair if it scores higher than with no plugboard.
- Remove those letters from the alphabet list and repeat for up to the maximum number of pairs (default is 10).

By following these steps, the script efficiently reduces the problem space and attempts to crack the Enigma-encrypted message.
