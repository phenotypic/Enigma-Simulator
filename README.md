# Enigma-Simulator

A historically acurate Enigma machine simulator written in Python. Supports both 3- and 4-rotor machines e.g. the Enigma I, Enigma M3, and Enigma M4 "Shark".

Heavily inspired by [Mike Pound](https://github.com/mikepound)'s [enigma](https://github.com/mikepound/enigma) project.

Under development:

- Command line interface
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

Run the script:
```
python3 enigma.py
```

Integrate the simulator:
```python
from enigma import Enigma

# Initialise the Enigma machine with specific settings
enigma = Enigma(rotors=['I', 'II', 'III'], reflector_name='UKW_B', rotor_positions=[1, 1, 1], ring_settings=[1, 1, 1], plugboard_connections='AB CD EF')

# Encrypt/decrypt a message
output = enigma.encrypt_string('HELLO WORLD')
print(output)
```

## Enigma overview

### Components

| Component | Options | Function |
| --- | --- | --- |
| Rotors | `I`, `II`, `III`, `IV`, `V`, `VI`, `VII`, `VIII`, `Beta`, and `Gamma` | Each rotor has a unique wiring that scrambles the input letter. Rotors can be set to different starting positions and rotate during operation to change the wiring path with each key press |
| Reflector | `UKW_A`, `UKW_B`, `UKW_C` (for 3-rotor setups); `UKW_B_THIN`, `UKW_C_THIN` (for 4-rotor setups) | Reflects the signal back through the rotors, ensuring encryption and decryption are reversible with the same settings |
| Plugboard | Up to 10 letter pairs | Allows pairs of letters to be swapped before and after rotor encryption, adding another layer of complexity |

**Note:** Enigma machines of the German Wehrmacht (Heer and Luftwaffe) were supplied with rotors `I`-`V`, while the German Navy (Kriegsmarine) were supplied with rotors `I`-`VIII`.

### Signal path

When a key is pressed on the Enigma machine, the electrical signal follows this path:

```
Keyboard  -> Plugboard -> Rightmost Rotor -> Middle Rotor(s) -> Leftmost Rotor -> Reflector
                                                                                      |
Lampboard <- Plugboard <- Rightmost Rotor <- Middle Rotor(s) <- Leftmost Rotor <- Reflector
```

**Note:** The rotors rotate before the signal passes through them. When a rotor reaches its notch position, it causes the next rotor to the left to rotate as well.

## Historical accuracy

By default, the script allows for a wide range of component configurations, including those that may not be historically accurate (e.g. reuse of the same rotor type). To ensure compliance with the configurations used by the German Kriegsmarine, initialise the simulator with the `historic=True` argument:

| Rule Category | 3-Rotor Setup | 4-Rotor Setup |
| --- | --- | --- |
| **Rotor Count** | Exactly 3 rotors | Exactly 4 rotors |
| **Rotor Types** | Rotors `I`-`VIII` are allowed in any order | Leftmost rotor must be Beta or Gamma, others can be `I`-`VIII` |
| **Rotor Reuse** | Not allowed | Not allowed |
| **Reflector Types** | `UKW_A`, `UKW_B`, `UKW_C` | `UKW_B_THIN`, `UKW_C_THIN` |
| **Mandatory Rotors** | At least one of `VI`, `VII`, `VIII` must be included | At least one of `VI`, `VII`, `VIII` must be included |
| **Plugboard Connections** | Up to 10 connections | Up to 10 connections |


