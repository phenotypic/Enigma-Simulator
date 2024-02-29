# Enigma-Simulator

A historically accurate Enigma machine simulator written in Python. Supports both 3- and 4-rotor machines including the Enigma I, Enigma M3, and Enigma M4 "Shark".

Inspired by [Mike Pound](https://github.com/mikepound)'s [enigma](https://github.com/mikepound/enigma) project.

**Under development:**

- Attack scripts: bombe, fitness functions, machine learning

## Usage

Clone the repository:
```
git clone https://github.com/phenotypic/Enigma-Simulator.git
```

Change to the project directory:
```
cd Enigma-Simulator
```

Import the simulator:
```python
from enigma import Enigma
```

3-rotor enigma:
```python
enigma = Enigma(rotors=['IV', 'VII', 'III'], reflector_name='UKW_B', rotor_positions=[18, 5, 21], ring_settings=[2, 14, 19], plugboard_connections='bq cr di ej kw mt os px uz gh')
transformed = enigma.transform_string('Sometimes it is the people no one can imagine anything of who do the things no one can imagine')
print(transformed)
# KLFNHABWWYLCJIFRDGPFSPDETDNAKRNDSZJGXKDVFKCRZYEGXSXQAJOQQOTXHONGIURHBKPYIACN
```

4-rotor enigma:
```python
enigma = Enigma(rotors=['GAMMA', 'VI', 'VIII', 'IV'], reflector_name='UKW_C_THIN', rotor_positions=[19, 6, 25, 3], ring_settings=[8, 2, 12, 20], plugboard_connections='bq cr di ej kw mt os px uz gh')
transformed = enigma.transform_string('Sometimes it is the people no one can imagine anything of who do the things no one can imagine')
print(transformed)
# NSORZZEIBALCKRRAXBDRPLAGYGFJNFKGTBLBIUUFAKZJQWXMAVJMFBXHEXXZKKHDLCMRBDEXJDVJ
```

**Notes:** The Enigma machine's symmetric design allows for both encryption and decryption using the `transform_string` method. Rotor positions and ring settings can be passed as numbers (1-26) or letters (A-Z).

## Enigma overview

When a key is pressed on a physical Enigma machine, the electrical signal follows this path:

```
Keyboard  -> Plugboard -> Rightmost Rotor -> Middle Rotor(s) -> Leftmost Rotor -> Reflector
                                                                                      |
Lampboard <- Plugboard <- Rightmost Rotor <- Middle Rotor(s) <- Leftmost Rotor <- Reflector
```

**Note:** Rotors rotate before the signal passes through them. When a rotor reaches its notch position, it causes the next rotor to rotate as well.

### Components

| Component | Options | Function |
| --- | --- | --- |
| Rotors | `I`, `II`, `III`, `IV`, `V`, `VI`, `VII`, `VIII`, `Beta`, and `Gamma` | Each rotor has a unique wiring that scrambles the input letter. Rotors can be set to different starting positions and rotate during operation to change the wiring path with each key press |
| Reflector | `UKW_A`, `UKW_B`, `UKW_C` (for 3-rotor setups); `UKW_B_THIN`, `UKW_C_THIN` (for 4-rotor setups) | Reflects the signal back through the rotors, ensuring encryption and decryption are reversible with the same settings |
| Plugboard | Up to 10 letter pairs | Allows pairs of letters to be swapped before and after rotor encryption, adding another layer of complexity |

**Note:** Enigma machines of the German Wehrmacht (Heer and Luftwaffe) were supplied with rotors `I`-`V`, while the German Navy (Kriegsmarine) were supplied with rotors `I`-`VIII`.

## Historical accuracy

By default, the script allows for a wide range of component configurations, including those that may not be historically accurate (e.g. reuse of the same rotor type). Follow these rules to ensure compliance with German Kriegsmarine configurations:

| | 3-Rotor Setup | 4-Rotor Setup |
| --- | --- | --- |
| **Rotor Count** | Exactly 3 rotors | Exactly 4 rotors |
| **Rotor Types** | Rotors `I`-`VIII` are allowed in any order | Leftmost rotor must be `Beta` or `Gamma`, others can be `I`-`VIII` |
| **Rotor Reuse** | Not allowed | Not allowed |
| **Reflector Types** | `UKW_A`, `UKW_B`, `UKW_C` | `UKW_B_THIN`, `UKW_C_THIN` |
| **Mandatory Rotors** | At least one of `VI`, `VII`, `VIII` must be included | At least one of `VI`, `VII`, `VIII` must be included |
| **Plugboard Connections** | Up to 10 letter pairs | Up to 10 letter pairs |
