# Enigma-Simulator

A historically accurate Enigma machine simulator written in Python. Supports both 3- and 4-rotor machines including the Enigma I, Enigma M3, and Enigma M4 'Shark'.

Features a cryptanalysis tool which leverages fitness functions to decrypt Enigma-encrypted messages using only ciphertext.

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
enigma = Enigma(rotors=['IV', 'V', 'III'], reflector_name='UKW_B', rotor_positions=[18, 5, 21], ring_settings=[2, 14, 19], plugboard_connections=['BQ', 'CR', 'DI', 'EJ', 'KW', 'MT', 'OS', 'PX', 'UZ', 'GH'])
transformed = enigma.transform_string('Sometimes it is the people no one can imagine anything of who do the things no one can imagine')
print(transformed)
# USZOLSBLVCGLFQDDMYIRIRJGVVNNJTERXAUYPPEAHNLWLGWMKUIZHFCQVTBNOAKUHQRBBUNWFHCG
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

For a 3-rotor Enigma machine with 8 rotors to choose from, there are over forty-five septillion possible configurations. This includes variations in rotor choices, orders, positions, ring settings, reflectors, and plugboard settings. Even with modern computers, brute-forcing all these combinations is infeasible. However, we can significantly reduce the complexity of cracking the code using fitness functions.

Fitness functions evaluate how "English-like" a piece of text is. We use N-grams, which provide statistics based on the probability of sequences of characters like `IONAL`, `OUGHT`, and `OWEVE`. This method exploits one of Enigma's weaknesses: messages decrypted with partially correct settings will show fragments of readable text, which improves the overall fitness score. This technique is most effective with messages longer than 200 characters.

### Cracking

This ciphertext-only attack involves determining rotor order and initial positions, finding ring settings, and deducing plugboard settings.

For example, let's take a 584-character message encrypted with unknown settings on an Enigma M3:

```
OZLUDYAKMGMXVFVARPMJIKVWPMBVWMOIDHYPLAYUWGBZFAFAFUQFZQISLEZMYPVBRDDLAGIHIFUJDFADORQOOMIZPYXDCBPWDSSNUSYZTJEWZPWFBWBMIEQXRFASZLOPPZRJKJSPPSTXKPUWYSKNMZZLHJDXJMMMDFODIHUBVCXMNICNYQBNQODFQLOGPZYXRJMTLMRKQAUQJPADHDZPFIKTQBFXAYMVSZPKXIQLOQCVRPKOBZSXIUBAAJBRSNAFDMLLBVSYXISFXQZKQJRIQHOSHVYJXIFUZRMXWJVWHCCYHCXYGRKMKBPWRDBXXRGABQBZRJDVHFPJZUSEBHWAEOGEUQFZEEBDCWNDHIAQDMHKPRVYHQGRDYQIOEOLUBGBSNXWPZCHLDZQBWBEWOCQDBAFGUVHNGCIKXEIZGIZHPJFCTMNNNAUXEVWTWACHOLOLSLTMDRZJZEVKKSSGUUTHVXXODSKTFGRUEIIXVWQYUIPIDBFPGLBYXZTCOQBCAHJYNSGDYLREYBRAKXGKQKWJEKWGAPTHGOMXJDSQKYHMFGOLXBSKVLGNZOAXGVTGXUIVFTGKPJU
```

#### 1. Determine Rotor Order and Rotor Positions

First, we decrypt the ciphertext using all rotor combinations and orders, and all possible rotor positions, assuming the ring settings are `1, 1, 1`. We store the top N (`1000` by default) decryptions and their scores for the next step.

```
GDFOWZVAIYNSDXYMHUCDWZUGSKDXTXWOIZEUFIGWECTEWRZEDTUYQRSTOOWPTMNMQGJJWJYKMWCPHJOKPQLFNUVGGBQVAVAOZTJSWTEUMCOKVKJEHUGZFNKNBBRAFKWNLSNAQSQBWOLMSNJQLIQXQFNUNYBLNSKUGHAJELTAQLQQYENLZOZOYNQYHNRONAIVUZQVSUEDZEMFWCHXWHTXJJWCMNYONQVCNDZDZDFGJTKQDWBDSROSMSUSKNJPTAKEIQXMAEHQKJAKSXMOANICTFEZZNFCSXIXKONKOXWBTMJVNSOPLWIDHCZPMUSTYDRRYPLGVYICUUBWEYFRHROPNBESIXRABBAGWEXLQYWWJCJQYCNDPSRMJPWBHVXVTXYTBXSRZQLSEJNGZLXNILRFAEHESOQRETQZGCYDKZKTXRKAYPVELTJNZHNQJZTOUKNUWVNDUQYQUPCXSPOUWYAMVXERPXEVPMVKYLULQYYWDTUOUBXRQDMYJAMXVKHSMQXOLGXXHDPSTUZQWEABRRLAVHLRPCXCBZHEFVMUHYUXXLBAMFOYTWKJGWNIQNXEZENJWOOHHDWP

Score: -5851.911352643304
Rotors: II, V, III
Rotor positions: 22, 7, 23
Ring settings: 1, 1, 1
```

**Note:** At this stage, the highest ranking candidate isn't always the best. The one shown above is the 810<sup>th</sup> highest. The top candidate had a fitness of `-5686.731256460109` with rotors `II, V, I` and rotor positions `3, 6, 6`.

#### 2. Find Ring Settings

Next, using the top N rotor and position combinations, we test all possible ring settings for the middle and rightmost rotors (keeping the leftmost rotor at `1`). As each ring is moved, we adjust the corresponding rotor position accordingly. The best candidate is stored for the next step.

```
TLMKPKCBVKCKUHSXHWVHETAQSVJOTCCNMFCHGBESBHQNKEKSPSHEYTDLCGINRITPZEATVIVIKMSKALMWGFFUDNGKAVHEVIWISMFCHINHELDUHIILCBCDEAINAZEKNVNIGEPBVAWFMEPSOFSAKWHABECJSKALCBSPKXRILBEJBENKWMFBUSTKAEGIRDBDSLUVKHIGPVPMVSDEISOYDTEWBULOATXECEFZINGOAVHJQNTBXMPBCINEFNVKZIAAFWGSKLNYCLNDLYETFMIFINTHKRMHEDFWEDUEMTNBTUQFDIVISDIAAMXUZAVXMOXFPGVNZCYNABUIIVNVHFVVPSHPFLINGFPDVHHFNQREWVMVHEQZNQTIKNCLNMFCNICGSSHUNOIEVXQPQKUGJFNNKZVFVPIKICPBSUWKEISUCHFSFGFLBPPPKBOLUVTOCZZOFEDCHDYQSVFFDKAUMDEMPVIYPPUCQFDYBENVVIKNIQEFBBWEPGUYODBOSYINNAPRIVGFQKYZAFNVFDWBTCKSCBIREBTCELVAIVSNDAQYXYWESKEUSNSEQCRITERKUNLBDIGUWRXROWDS

Score: -5641.195462427708
Rotors: II, V, III
Rotor positions: 22, 7, 23
Ring settings: 1, 4, 24
```

#### 3. Find Plugboard Settings

We first record the score of the best candidate without a plugboard. Then, we try all 2-letter pairs in the first position, fixing the highest scoring pair if it improves the score. These letters are then removed from the list, and the process repeats up to a maximum number of pairs (default is `10`).

```
JBROPOSETOCONSIDERTHEQUESTPHNCANMACHINESTHINKTHISSHTYVDBEGINWITHDEFINITIONSOFDTRMEANINGOFTHETERMSMACHINHRBDTHINKTHEDEFINITIONSMIGEJLEFRAMEDSOASTOREFLECTSOFBCLSPOSSIBLETHENORMALUSEOFSGPWORDSBUTTHISATTITUDEISDYDVEROUSIFTHEMEANINGOFTHEWNVUSMACHINEANDTHINKARETOBEENJNDBYEXAMININGHOWTHEYAREDWEMONLYUSEDITISDIFFICULTTDPKCAPETHECONCLUSIONTHATTHSSGANINGANDTHEANSWERTOTHEQENOTIONCANMACHINESTHINKISTXQPSOUGHTINASTATISTICALSUROLISUCHASAGALLUPPOLLBUTTHIPVKABSURDINSTEADOFATTEMPTIXPSUCHADEFINITIONISHALLREPGOLKDBCSYIPNDPXIGGAQOYZFAMEADDSCLOSELYRELATEDTOITANDFQYXPRESSEDINRELATIVELYUNAXDIGUOUSWORDS

Score: -3437.8872646650743
Rotors: II, V, III
Rotor positions: 22, 7, 23
Ring settings: 1, 4, 24
Plugboard: AF, KO, TV, BL, RW
```

This is our final decrypted message. While not perfect, it is mostly readable and recognisable as the opening paragraph from Alan Turing's seminal [Computing Machinery and Intelligence](https://doi.org/10.1093/mind/LIX.236.433) paper.

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
