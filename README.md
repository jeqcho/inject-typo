# TypoGen: A Rule-Based Typographical Noise Generator
*Technical Specification for Engineering Implementation*

## Overview
TypoGen is a Python package that introduces controlled, realistic typographical errors into text.  
It exposes a single primary function:

```python
generate_typos(text: str, strength: float, seed: int | None) -> str
```

The goal is to produce human-like typos based on empirically observed distributions while allowing a user to tune the *intensity* of corruption from 0.0 (no changes) to 1.0 (maximum corruption). Randomness must be **reproducible** given the same seed.

The package must follow a **rule-based typo model** incorporating realistic error types, keyboard-adjacency constraints, and stable probabilities.

## Installation

```bash
pip install git+https://github.com/jeqcho/inject-typo.git
```

## Demo

**Original text:**
> The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet and is commonly used for testing purposes.

### Fine-grained control (0.00 to 0.10)

| Strength | Output |
|----------|--------|
| 0.00 | The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet and is commonly used for testing purposes. |
| 0.01 | The quick brown foxjumps over the lazy dog. This sentence contains every letter of the alphabet and is commonly used for teating purposes. |
| 0.02 | The quick brown foxj umps over the lazy dog. This sentence contains every letter of the alphabet andqis commonly used for tetkng purposes. |
| 0.03 | Teh quickbrpwn foxj umps over the lazy dog. This sentence contains every letter of the alphabet andqis commonly used for tetkng purposes. |
| 0.04 | Thbe quickb rwn foxgjumps over the lazy dog. This sentence containse very letter of the alphabet andqis commonly used for tetkng purposes. |
| 0.05 | Thge quickvbrokwn foxj umps over the lazy dg. This sentence containsgevery letter of the aplhabet andqis commonly used for tetkng purposes. |
| 0.06 | Tye quickqbrkwn fox wjumps over the lazy dgo. This sentence containsevery letter of the aophabet andi s commonly used for tedtng pjrposes. |
| 0.07 | Tje quickkbrpwn foxqjumps over the lazy dkg. This sentence contains wevery letter of the aplhabt andgis commonly used for tetslng prposds. |
| 0.08 | Tje quickkbrpwn foxjumps over the lazy dolg.vThis sentence contains wevery letter of the aplhabt andgis commonly used for tetslng prposds. |
| 0.09 | Tbe quifkrbrkwn foxhjumps over the lazy dg. oThis sentence containsvevery letter of the alpphabte andis commonly used for tewtnig pkrpsds. |
| 0.10 | Tye quikcbriwn foxujumps oiger the lazy dkg.hThis sentence containsqevery letter of the slpphabte andis commonly used for tewtnig pkrpsds. |

### Full range (0.0 to 1.0)

| Strength | Output |
|----------|--------|
| 0.0 | The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet and is commonly used for testing purposes. |
| 0.1 | Tye quikcbriwn foxujumps oiger the lazy dkg.hThis sentence containsqevery letter of the slpphabte andis commonly used for tewtnig pkrpsds. |
| 0.2 | Teh quivk lbrinw foxpjumpls pber the lazy dpg.T tis sentendehcontainsrevery letter of the sohabedt andvis comnmonly sued fr tewtnig pkrpsds. |
| 0.3 | Tbzequikarlsn ofxjums ifer the lazy diyegRbus smetencxedcontaines vgefry lettrf pf teh qiohabft andkis fonmonlg uhse dfr tewtnig pkrpsds. |
| 0.5 | Tgsquicxkj bhropqn roxqjunls boifer thejlazy dlzgRksptsenecrdontainhsrbrryl strfe okf reh zlkohanr tandis donmjpnlg ise folr teztfnig rplds. |
| 0.7 | Fdhq ixukvgopqjvfgoixrjismpge tetiazsyvdkvkHtld hqhetfmxe rdobginwdwrykdtct  hehhwkoahvw tznd liqv oljkpnlbyyseertprtedztfnig rplds. |
| 1.0 | Rnfhqofjg epbw fxhkpmlwdovehnrdkzzskyldigbTjd ewrfenfrfwoohysbsgsifhtywtivsfhjwjzktndutnlhsfljkmhhl lydsee srltr erzylbtqluhprfsp |

---

## 1. Package Goals
1. Produce text with controlled error rates.
2. Produce errors that resemble real typographical mistakes.
3. Be deterministic when given a random seed.
4. Be installable via pip (`pip install typogen`).
5. Provide a clean, well-documented public API.

---

## 2. Typographical Error Model

### 2.1 Error Types
The following four error types must be implemented:

| Error Type      | Description                                   | Example       |
|------------------|-----------------------------------------------|---------------|
| **Substitution** | Replace char with adjacent keyboard key       | `cat` → `cat` → `dat` |
| **Deletion**     | Remove one character                          | `cat` → `ct`  |
| **Insertion**    | Insert adjacent keyboard key after char       | `cat` → `caat` |
| **Transposition**| Swap adjacent characters                      | `cat` → `cta` |

### 2.2 Default Error Type Probabilities
Follow empirical distribution (Conijn et al., 2019):

- Substitution: **0.57**
- Insertion: **0.18**
- Transposition: **0.13**
- Deletion: **0.11**

These should be constants accessible for modification by advanced users, e.g.:
```python
DEFAULT_ERROR_PROBS = {
    "substitution": 0.57,
    "insertion": 0.18,
    "transposition": 0.13,
    "deletion": 0.11,
}
```

### 2.3 Keyboard Adjacency Map
A QWERTY‐layout adjacency dictionary must be included.  
Example (partial):

```python
KEY_ADJ = {
    "a": ["q", "w", "s", "z"],
    "b": ["v", "g", "h", "n"],
    "c": ["x", "d", "f", "v"],
    ...
}
```

- Only alphabetic characters require adjacency-based behavior.
- Case sensitivity should be preserved.
- Characters missing from the map default to substitution with a random alphabetic character.

---

## 3. Typo Strength Model

### 3.1 Strength Input
`strength` is a float in **[0.0, 1.0]** and determines the probability that each *character* undergoes a typo event.

### 3.2 Conversion to Error Rate
Define:
```
error_rate = strength
```

Thus:
- `strength = 0.00` → 0% characters modified  
- `strength = 0.10` → 10% of characters modified  
- `strength = 1.00` → every character modified

### 3.3 Selection of Characters to Modify
For each character index `i` in the string:
- Generate a random float in [0,1].
- If `< error_rate`, a typo is applied.
- Only one error type is applied per selected character.

### 3.4 Seed Behavior
- If `seed` is provided, initialize RNG via `random.seed(seed)`.
- If not provided, leave RNG untouched (nondeterministic).

---

## 4. Core Function Specification

### 4.1 Function Signature
```python
def generate_typos(text: str, strength: float, seed: int | None = None) -> str:
```

### 4.2 Input Validation Rules
- `text` must be `str`.  
- `0.0 <= strength <= 1.0`, else raise `ValueError`.  
- `seed` must be `int` or `None`.  

### 4.3 Processing Steps (High-Level)
1. Initialize RNG from `seed` if provided.
2. Convert text into a mutable representation (e.g. list of characters).
3. Iterate over character positions:
   - Sample whether this character gets a typo (probability = `strength`).
   - If yes, select error type using `DEFAULT_ERROR_PROBS`.
   - Apply the transformation according to its rules.
4. Join characters back into a string.
5. Return modified string.

---

## 5. Detailed Error Rules

### 5.1 Substitution
- Look up character in adjacency map.
- If available, choose one randomly from adjacency list.
- Preserve original case.
- If no adjacency list exists, replace with random ASCII letter.

### 5.2 Deletion
- Character is removed entirely.
- Do nothing if string length < 2.

### 5.3 Insertion
- Insert one adjacent key immediately after the current position.
- If no adjacency, insert a random alphabetical char.

### 5.4 Transposition
- Swap char at index `i` with char at index `i+1`.
- If `i` is last index, skip or fallback to substitution.

---

## 6. Package Structure

```
typogen/
    __init__.py
    core.py                # main algorithm
    keyboard.py            # adjacency maps & constants
    errors.py              # error functions (substitution, deletion...)
    utils.py               # randomness helpers, validation
    tests/
        test_basic.py
        test_reproducibility.py
        test_strength_levels.py
    README.md
    pyproject.toml
```

---

## 7. Testing Requirements

### 7.1 Reproducibility Test
```
generate_typos("hello", 0.5, seed=1234)
must equal
generate_typos("hello", 0.5, seed=1234)
```

### 7.2 Strength Test
- `strength=0` → input unchanged.
- `strength=1` → every char modified (subject to boundary rules).

### 7.3 Error Distribution Test
- With large input and high strength, distribution of error types should approximate DEFAULT_ERROR_PROBS.

### 7.4 Keyboard Map Test
- Substitution should only choose adjacent keys.

---

## 8. Performance Notes
- Runtime must be linear in input length, `O(n)`.
- Memory usage minimal (mutable char list).

---

## 9. Licensing & Attribution
Include attribution in README for empirical distributions based on:

**Conijn, R., Zaanen, M., Leijten, M., & van Waes, L. (2019).  
*How to Typo? Building a Process-Based Model of Typographic Error Revisions.*  
Journal of Writing Analytics, 3.**

---

## 10. Future Extensions (Optional)
- Word-level error model.
- Language-aware misspellings (phonetic).
- Multi-keyboard support (Dvorak, mobile layouts).
- Configurable error profiles per user type.

---

## End of Document
