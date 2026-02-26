import re
import random
import sys
from textwrap import fill

VOWEL_SOUND_EXCEPTIONS_AN = {"honest", "honor", "hour", "heir", "herb"}
VOWEL_SOUND_EXCEPTIONS_A = {"university", "unicorn", "european", "one", "use", "user", "ubiquitous"}

IRREGULAR_PAST = {
    "go": "went", "run": "ran", "eat": "ate", "see": "saw", "come": "came",
    "buy": "bought", "bring": "brought", "catch": "caught", "teach": "taught",
    "think": "thought", "make": "made", "do": "did", "have": "had", "be": "was"
}

IRREGULAR_PLURALS = {
    "child": "children", "man": "men", "woman": "women", "mouse": "mice",
    "goose": "geese", "tooth": "teeth", "foot": "feet", "person": "people"
}

WORD_BANKS = {
    "name": ["Aarav", "Isha", "Rahul", "Sara", "Kabir", "Maya", "Neel", "Anaya"],
    "place": ["Mumbai", "Delhi", "Goa", "Bengaluru", "Hyderabad", "Kolkata", "Chennai", "Pune"],
    "adjective": ["wobbly", "sparkly", "mysterious", "grumpy", "zesty", "soggy", "brave", "noisy"],
    "noun": ["robot", "ladder", "mango", "backpack", "spaceship", "bicycle", "pillow", "notebook"],
    "plural_noun": ["mangoes", "pencils", "dragons", "balloons", "cookies", "puppies", "gadgets", "candies"],
    "verb": ["dance", "jump", "whisper", "sprint", "gobble", "juggle", "code", "scribble"],
    "verb_past": ["danced", "jumped", "whispered", "sprinted", "gobbled",
                  "juggled", "coded", "scribbled", "went", "ran", "ate", "saw", "came"],
    "verb_ing": ["dancing", "jumping", "whispering", "sprinting", "gobbling",
                 "juggling", "coding", "scribbling"],
    "number": ["3", "7", "9", "13", "42", "108"],
    "animal": ["tiger", "elephant", "pigeon", "panda", "koala", "dolphin", "cat", "dog"],
    "emotion": ["joy", "panic", "excitement", "curiosity", "confusion", "delight"],
    "villain_name": ["Dr. Nebula", "The Monsoon Marauder", "Glitch King", "Shadow Chef"],
}


def start_with_vowel_sound(word: str) -> bool:
    w = word.lower()
    if w in VOWEL_SOUND_EXCEPTIONS_A:
        return False
    if w in VOWEL_SOUND_EXCEPTIONS_AN:
        return True
    if re.match(r"^[aeiou]", w):
        return True
    if re.match(r"^[AEFHILMNORSX]\.?[A-Z]\.?[A-Z]?$", word):
        return True
    if w.startswith("one"):
        return False
    return False


def auto_article_fix(text: str) -> str:
    def repl(match):
        article = match.group(1)
        nxt = match.group(2)
        should_be_an = start_with_vowel_sound(nxt)
        return ("an " if should_be_an else "a ") + nxt

    text = re.sub(r"\b(a|an)\s+([A-Za-z][\w'-]*)", repl, text)
    return text


def is_number(s: str) -> bool:
    return bool(re.fullmatch(r"-?\d+(\.\d+)?", s.strip()))


def is_ing(s: str) -> bool:
    return s.lower().endswith("ing")


def is_past_tense(s: str) -> bool:
    w = s.lower()
    return w in IRREGULAR_PAST.values() or w.endswith("ed")


def is_plural(s: str) -> bool:
    w = s.lower()
    if w in IRREGULAR_PLURALS.values():
        return True
    return w.endswith("s") or w.endswith("es")


TYPE_VALIDATORS = {
    "number": is_number,
    "verb_ing": is_ing,
    "verb_past": is_past_tense,
    "plural_noun": is_plural,
}


def validate_input(kind: str, value: str) -> bool:
    fn = TYPE_VALIDATORS.get(kind)
    return True if fn is None else fn(value)


def prompt_for(kind: str, label: str, example: str = "") -> str:
    while True:
        value = input(f"{label} ({kind}{' e.g. ' + example if example else ''}): ").strip()
        if value == "":
            print("  → Please enter something.")
            continue
        if validate_input(kind, value):
            return value
        print("  → That doesn't look right for", kind, "- try again.")


def random_word(kind: str) -> str:
    bank = WORD_BANKS.get(kind) or WORD_BANKS.get("noun", [])
    return random.choice(bank) if bank else "thing"


# ---------- Templates ----------

TEMPLATES = [
    {
        "id": "space-caper",
        "title": "Space Caper",
        "story": (
            "Captain {name} grabbed {number} {plural_noun} and {verb_past} onto the "
            "{adjective} starship from {place} to escape {villain_name}. "
            "With a {adjective} {noun} in hand, the crew yelled in {emotion}!"
        ),
        "placeholders": [
            {"key": "name", "label": "A person’s name", "type": "name", "example": "Aarav"},
            {"key": "number", "label": "A number", "type": "number", "example": "7"},
            {"key": "plural_noun", "label": "A plural noun", "type": "plural_noun", "example": "cookies"},
            {"key": "verb_past", "label": "A past-tense verb", "type": "verb_past", "example": "sprinted"},
            {"key": "adjective", "label": "An adjective", "type": "adjective", "example": "wobbly"},
            {"key": "place", "label": "A place", "type": "place", "example": "Goa"},
            {"key": "villain_name", "label": "A villain’s name", "type": "villain_name", "example": "Dr. Nebula"},
            {"key": "noun", "label": "A noun", "type": "noun", "example": "backpack"},
            {"key": "emotion", "label": "An emotion", "type": "emotion", "example": "delight"},
        ],
    },
    {
        "id": "school-day",
        "title": "A Very Normal School Day",
        "story": (
            "Today, I took a {adjective} {noun} to school. "
            "My teacher {verb_past} and the class started {verb_ing}. "
            "At lunch, we traded {plural_noun} with a {adjective} {animal}."
        ),
        "placeholders": [
            {"key": "adjective", "label": "An adjective", "type": "adjective", "example": "grumpy"},
            {"key": "noun", "label": "A noun", "type": "noun", "example": "robot"},
            {"key": "verb_past", "label": "A past-tense verb", "type": "verb_past", "example": "laughed"},
            {"key": "verb_ing", "label": "A verb ending in ing", "type": "verb_ing", "example": "dancing"},
            {"key": "plural_noun", "label": "A plural noun", "type": "plural_noun", "example": "pencils"},
            {"key": "adjective", "label": "Another adjective", "type": "adjective", "example": "soggy"},
            {"key": "animal", "label": "An animal", "type": "animal", "example": "panda"},
        ],
    },
    {
        "id": "mystery",
        "title": "Monsoon Mystery",
        "story": (
            "On a {adjective} evening in {place}, Detective {name} discovered a "
            "{adjective} {noun}. The clue? {number} tiny {plural_noun} "
            "that had {verb_past} away."
        ),
        "placeholders": [
            {"key": "adjective", "label": "An adjective", "type": "adjective", "example": "mysterious"},
            {"key": "place", "label": "A place", "type": "place", "example": "Mumbai"},
            {"key": "name", "label": "A person’s name", "type": "name", "example": "Isha"},
            {"key": "adjective", "label": "Another adjective", "type": "adjective", "example": "noisy"},
            {"key": "noun", "label": "A noun", "type": "noun", "example": "ladder"},
            {"key": "number", "label": "A number", "type": "number", "example": "42"},
            {"key": "plural_noun", "label": "A plural noun", "type": "plural_noun", "example": "balloons"},
            {"key": "verb_past", "label": "A past-tense verb", "type": "verb_past", "example": "vanished"},
        ],
    },
]


PLACEHOLDER_PATTERN = re.compile(r"\{([a-zA-Z_]+)\}")


def list_templates():
    print("\nAvailable templates:")
    for i, t in enumerate(TEMPLATES, 1):
        print(f"  {i}. {t['title']}  (id: {t['id']})")
    print()


def pick_template():
    list_templates()
    while True:
        choice = input("Pick a template by number (or type id): ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(TEMPLATES):
                return TEMPLATES[idx]
        for t in TEMPLATES:
            if t["id"] == choice:
                return t
        print("  → Invalid selection, try again.")


def collect_inputs(tmpl, auto_random=False):
    keys_in_story = set(PLACEHOLDER_PATTERN.findall(tmpl["story"]))
    ordered = []
    seen = set()

    for ph in tmpl["placeholders"]:
        k = ph["key"]
        if k in keys_in_story and k not in seen:
            ordered.append(ph)
            seen.add(k)

    answers = {}

    if auto_random:
        for ph in ordered:
            answers[ph["key"]] = random_word(ph["type"])
        return answers

    print("\nFill the blanks:")
    for ph in ordered:
        answers[ph["key"]] = prompt_for(ph["type"], ph["label"], ph.get("example", ""))

    return answers


def fill_story(story: str, answers: dict) -> str:
    def repl(match):
        key = match.group(1)
        return str(answers.get(key, f"<{key}>"))

    filled = PLACEHOLDER_PATTERN.sub(repl, story)
    filled = auto_article_fix(filled)
    return filled


def wrap(text: str, width: int = 88) -> str:
    return fill(text, width=width)


def save_story(text: str):
    fname = "mad_lib_story.txt"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print(f"\nSaved to {fname}\n")


def play_once():
    tmpl = pick_template()
    print(f"\nYou chose: {tmpl['title']}\n")

    use_random = input("Auto-fill with random words? (y/N): ").strip().lower().startswith("y")
    answers = collect_inputs(tmpl, auto_random=use_random)

    story = fill_story(tmpl["story"], answers)
    print("\n— Your Story —\n")
    print(wrap(story))
    print("\n— End —\n")

    if input("Save to file? (y/N): ").strip().lower().startswith("y"):
        save_story(story)


def main():
    print("=== Mad Libs Generator ===")
    while True:
        play_once()
        again = input("Play again? (Y/n): ").strip().lower()
        if again == "n":
            print("Bye!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")
        sys.exit(0)
