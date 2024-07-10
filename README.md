# Enigma-Simulator

A historically accurate Enigma machine simulator written in Python. Supports both 3- and 4-rotor machines including the Enigma I, Enigma M3, and Enigma M4 'Shark'.

Includes a cryptanalysis tool capable of breaking Enigma-encrypted messages using only ciphertext.

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

The `main.py` script provides an interface for both the Enigma machine simulator and the cryptanalysis tool.

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

For a 3-rotor machine with 8 rotors to choose from, there are more than forty-five septillion possible configurations of rotors, rotor orders, rotor positions, ring settings, reflectors, and plugboards. Even with modern computers, this is too many to bruteforce. However, we can use fitness functions to significantly reduce the overall complexity of the cracking process. 

Fitness functions measure how 'English-like' a piece of text is. Here, we use N-grams which return a statistic based on the probability of constituent sequences of characters, e.g. `IONAL`, `OUGHT`, and `OWEVE`. This exploits one of Enigma's key weaknesses: messages decrypted with partially correct settings will have islands of plaintext that are reflected in overall fitness. This works best against messages with >200 characters.

### Cracking

```
OZLUDYAKMGMXVFVARPMJIKVWPMBVWMOIDHYPLAYUWGBZFAFAFUQFZQISLEZMYPVBRDDLAGIHIFUJDFADORQOOMIZPYXDCBPWDSSNUSYZTJEWZPWFBWBMIEQXRFASZLOPPZRJKJSPPSTXKPUWYSKNMZZLHJDXJMMMDFODIHUBVCXMNICNYQBNQODFQLOGPZYXRJMTLMRKQAUQJPADHDZPFIKTQBFXAYMVSZPKXIQLOQCVRPKOBZSXIUBAAJBRSNAFDMLLBVSYXISFXQZKQJRIQHOSHVYJXIFUZRMXWJVWHCCYHCXYGRKMKBPWRDBXXRGABQBZRJDVHFPJZUSEBHWAEOGEUQFZEEBDCWNDHIAQDMHKPRVYHQGRDYQIOEOLUBGBSNXWPZCHLDZQBWBEWOCQDBAFGUVHNGCIKXEIZGIZHPJFCTMNNNAUXEVWTWACHOLOLSLTMDRZJZEVKKSSGUUTHVXXODSKTFGRUEIIXVWQYUIPIDBFPGLBYXZTCOQBCAHJYNSGDYLREYBRAKXGKQKWJEKWGAPTHGOMXJDSQKYHMFGOLXBSKVLGNZOAXGVTGXUIVFTGKPJU

Score: -6246.36679772713
```

#### 1. Determine Rotor Order and Rotor Positions

First, we decipher the ciphertext with each rotor combination and rotor order for all possible combinations of rotor positions, assuming the ring settings are `1, 1, 1`. The top N (`1000` by default) decryptions are stored alongside their score for the next step.

```
GDFOWZVAIYNSDXYMHUCDWZUGSKDXTXWOIZEUFIGWECTEWRZEDTUYQRSTOOWPTMNMQGJJWJYKMWCPHJOKPQLFNUVGGBQVAVAOZTJSWTEUMCOKVKJEHUGZFNKNBBRAFKWNLSNAQSQBWOLMSNJQLIQXQFNUNYBLNSKUGHAJELTAQLQQYENLZOZOYNQYHNRONAIVUZQVSUEDZEMFWCHXWHTXJJWCMNYONQVCNDZDZDFGJTKQDWBDSROSMSUSKNJPTAKEIQXMAEHQKJAKSXMOANICTFEZZNFCSXIXKONKOXWBTMJVNSOPLWIDHCZPMUSTYDRRYPLGVYICUUBWEYFRHROPNBESIXRABBAGWEXLQYWWJCJQYCNDPSRMJPWBHVXVTXYTBXSRZQLSEJNGZLXNILRFAEHESOQRETQZGCYDKZKTXRKAYPVELTJNZHNQJZTOUKNUWVNDUQYQUPCXSPOUWYAMVXERPXEVPMVKYLULQYYWDTUOUBXRQDMYJAMXVKHSMQXOLGXXHDPSTUZQWEABRRLAVHLRPCXCBZHEFVMUHYUXXLBAMFOYTWKJGWNIQNXEZENJWOOHHDWP

Score: -5851.911352643304
Rotors: II, V, III
Rotor positions: 22, 7, 23
Ring settings: 1, 1, 1
```

#### 2. Find Ring Settings

Using the top N best rotor and rotor positions, we try all possible combinations of ring settings on the middle and rightmost rotor (keeping the leftmost rotor set to `1`). The rotors must stay registered with the recovered indicator setting, so as each ring is moved, the trial rotor position for that rotor is moved in the same direction. We store the highest ranking candidate for the next step.

```
TLMKPKCBVKCKUHSXHWVHETAQSVJOTCCNMFCHGBESBHQNKEKSPSHEYTDLCGINRITPZEATVIVIKMSKALMWGFFUDNGKAVHEVIWISMFCHINHELDUHIILCBCDEAINAZEKNVNIGEPBVAWFMEPSOFSAKWHABECJSKALCBSPKXRILBEJBENKWMFBUSTKAEGIRDBDSLUVKHIGPVPMVSDEISOYDTEWBULOATXECEFZINGOAVHJQNTBXMPBCINEFNVKZIAAFWGSKLNYCLNDLYETFMIFINTHKRMHEDFWEDUEMTNBTUQFDIVISDIAAMXUZAVXMOXFPGVNZCYNABUIIVNVHFVVPSHPFLINGFPDVHHFNQREWVMVHEQZNQTIKNCLNMFCNICGSSHUNOIEVXQPQKUGJFNNKZVFVPIKICPBSUWKEISUCHFSFGFLBPPPKBOLUVTOCZZOFEDCHDYQSVFFDKAUMDEMPVIYPPUCQFDYBENVVIKNIQEFBBWEPGUYODBOSYINNAPRIVGFQKYZAFNVFDWBTCKSCBIREBTCELVAIVSNDAQYXYWESKEUSNSEQCRITERKUNLBDIGUWRXROWDS

Score: -5641.195462427708
Rotors: II, V, III
Rotor positions: 22, 7, 23
Ring settings: 1, 4, 24
```

#### 3. Find Plugboard Settings

First, we store the score of the best candidate with no plugboard. Then we try all 2-letter pairs in the first position and fix the highest scoring pair if it scores higher than with no plugboard. Those letters are removed from the alphabet list and the process is repeated up to a maximum number of pairs (default is `10`).

```
JBROPOSETOCONSIDERTHEQUESTPHNCANMACHINESTHINKTHISSHTYVDBEGINWITHDEFINITIONSOFDTRMEANINGOFTHETERMSMACHINHRBDTHINKTHEDEFINITIONSMIGEJLEFRAMEDSOASTOREFLECTSOFBCLSPOSSIBLETHENORMALUSEOFSGPWORDSBUTTHISATTITUDEISDYDVEROUSIFTHEMEANINGOFTHEWNVUSMACHINEANDTHINKARETOBEENJNDBYEXAMININGHOWTHEYAREDWEMONLYUSEDITISDIFFICULTTDPKCAPETHECONCLUSIONTHATTHSSGANINGANDTHEANSWERTOTHEQENOTIONCANMACHINESTHINKISTXQPSOUGHTINASTATISTICALSUROLISUCHASAGALLUPPOLLBUTTHIPVKABSURDINSTEADOFATTEMPTIXPSUCHADEFINITIONISHALLREPGOLKDBCSYIPNDPXIGGAQOYZFAMEADDSCLOSELYRELATEDTOITANDFQYXPRESSEDINRELATIVELYUNAXDIGUOUSWORDS

Score: -3437.8872646650743
Rotors: II, V, III
Rotor positions: 22, 7, 23
Ring settings: 1, 4, 24
Plugboard: AF, KO, TV, BL, RW
```

### Settings

| Setting | Description |
| --- | --- |
| Rotors | Crack enigma with rotors `I`-`V` or `I`-`VIII` |
| Reflector | Choose reflector `UKW_A`, `UKW_B`, or `UKW_C` |
| Top N | The number of top rotor and rotor position combinations considered for finding the best ring settings (default is `1000`) |
| Max Pairs | The maximum number of plugboard pairs considered during cracking (default is `10`) |

## Resources

- Mike Pound's [enigma](https://github.com/mikepound/enigma)
- Practical Cryptography's [Cryptanalysis of Enigma](http://www.practicalcryptography.com/cryptanalysis/breaking-machine-ciphers/cryptanalysis-enigma/)
- Jim Gillogly's [Ciphertext only Cryptanalysis of the Enigma](http://web.archive.org/web/20060720040135/http://members.fortunecity.com/jpeschel/gillog1.htm)
- Heidi Williams's [Applying Statistical Language Recognition Techniques in the Ciphertext only Cryptanalysis of Enigma](http://www.tandfonline.com/doi/abs/10.1080/0161-110091888745)
