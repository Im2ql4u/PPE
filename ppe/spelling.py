"""Pitch spelling helpers (music21 uses '#'/'-'; humans read '♯'/'♭')."""

from __future__ import annotations

STEP_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
ACC_TEXT = {-2: "𝄫", -1: "♭", 0: "", 1: "♯", 2: "𝄪"}


def pretty(name: str) -> str:
    """'C#' -> 'C♯', 'B-4' -> 'B♭4', 'E--' -> 'E𝄫'. Leaves octave digits in place."""
    if not name:
        return name
    step, rest = name[0], name[1:]
    acc = 0
    while rest and rest[0] in "#-":
        acc += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    return step.upper() + ACC_TEXT.get(acc, "") + rest


def m21_name(step: str, alter: int) -> str:
    return step + ("#" * alter if alter > 0 else "-" * (-alter))


def figure_display(figure: str) -> str:
    """Typeset a Roman-numeral figure: 'V65' -> 'V⁶₅', 'viio7/V' -> 'vii°⁷/V', 'bVI' -> '♭VI'."""
    sup = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    sub = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    stacked = {"65": "⁶₅", "43": "⁴₃", "42": "⁴₂", "64": "⁶₄", "53": "", "2": "⁴₂"}

    def one(part: str) -> str:
        out, i = "", 0
        # leading accidentals
        while i < len(part) and part[i] in "b#-":
            out += "♭" if part[i] in "b-" else "♯"
            i += 1
        # numeral letters (Roman numerals, N, It, Ger, Fr, Cad)
        j = i
        while j < len(part) and (part[j].isalpha() and part[j] not in "o%ø"):
            j += 1
        out += part[i:j]
        i = j
        while i < len(part) and part[i] in "o%ø+":
            out += {"o": "°", "%": "ø", "ø": "ø", "+": "+"}[part[i]]
            i += 1
        rest = part[i:]
        # figures and bracketed extensions like [b9]
        digits = ""
        while rest and rest[0].isdigit():
            digits += rest[0]
            rest = rest[1:]
        if digits:
            out += stacked.get(digits, digits.translate(sup))
        rest = rest.replace("b", "♭").replace("#", "♯")
        return out + rest

    return "/".join(one(p) for p in figure.split("/"))


def interval_name_short(semitones: int) -> str:
    names = ["P1", "m2", "M2", "m3", "M3", "P4", "TT", "P5", "m6", "M6", "m7", "M7"]
    return names[semitones % 12]
