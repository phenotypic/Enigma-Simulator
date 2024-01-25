# Enigma-Simulator

An Enigma Machine simulator written in Python. Accurately replicates the functionality of the original World War II Enigma, including its rotors, plugboard, and reflector.

Supports both 3- and 4-rotor Enigma machines including the Enigma I, Enigma M3, and Enigma M4 "Shark". Includes optional historical accuracy checks for rotor types, order, reflector usage, and plugboard wiring.

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

Below is an overview of the inner working of a physical Enigma Machine. You can find more technical details [here](https://www.ciphermachinesandcryptology.com/en/enigmatech.htm).

### Components

#### 1. Rotors
- **Options:** `I`, `II`, `III`, `IV`, `V`, `VI`, `VII`, `VIII`, `Beta`, and `Gamma`.
- **Function:** Each rotor has a unique wiring that scrambles the input letter. Rotors can be set to different starting positions and rotate during operation to change the wiring path with each key press.

#### 2. Reflector
- **Options:** `UKW_A`, `UKW_B`, `UKW_C` (for 3-rotor setups); `UKW_B_THIN`, `UKW_C_THIN` (for 4-rotor setups).
- **Function:** Reflects the signal back through the rotors, ensuring encryption and decryption are reversible with the same settings.

#### 3. Plugboard
- **Function:** Allows pairs of letters to be swapped before and after rotor encryption, adding another layer of complexity.

### Signal path

When a key is pressed on the Enigma machine, an electrical signal follows the path summarised below:

```
Keyboard  -> Plugboard -> Rightmost Rotor -> Middle Rotor(s) -> Leftmost Rotor -> Reflector
                                                                                      |
Lampboard <- Plugboard <- Rightmost Rotor <- Middle Rotor(s) <- Leftmost Rotor <- Reflector
```

**Note:** The rotation of the rotors happens before the signal passes through them. When a rotor reaches its notch position, it causes the next rotor to the left to rotate as well.

## Historical accuracy rules

You can optionally enable historical accuracy rules used by the German Kriegsmarine by initialising the machine with the `historic=True` parameter.

| Rule Category | 3-Rotor Setup | 4-Rotor Setup |
| --- | --- | --- |
| **Rotor Count** | Exactly 3 rotors | Exactly 4 rotors |
| **Rotor Types** | Rotors `I`-`VIII` are allowed in any order | Leftmost rotor must be Beta or Gamma, others can be `I`-`VIII` |
| **Rotor Reuse** | Not allowed | Not allowed |
| **Reflector Types** | `UKW_A`, `UKW_B`, `UKW_C` | `UKW_B_THIN`, `UKW_C_THIN` |
| **Mandatory Rotors** | At least one of `VI`, `VII`, `VIII` must be included | At least one of `VI`, `VII`, `VIII` must be included |
| **Plugboard Connections** | Up to 10 connections | Up to 10 connections |


