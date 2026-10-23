"""Deterministic, plain-language explanations generated from label data (no language model).

Every factual statement is assembled from the label (key, figure, chord tones, bass, inversion) or
from the notes; the general paragraphs are fixed texts per chord family. Interpretation is
attributed to the analyst.
"""

from __future__ import annotations

from music21 import interval as m21interval
from music21 import pitch as m21pitch

from ppe.compare import CLASS_TEXT
from ppe.model import Label
from ppe.spelling import pretty

ORDINAL = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 7: "seventh"}
DEGREE_NAME = {1: "tonic", 2: "supertonic", 3: "mediant", 4: "subdominant", 5: "dominant",
               6: "submediant", 7: "leading tone"}

FAMILY = {
    "tonic": ("Home.",
              "The tonic chord is built on the first degree of the key. It is where the music feels at rest; most phrases begin or end here."),
    "tonic six-four": ("The tonic over its fifth: usually not a resting point.",
                       "A tonic triad in second inversion (with the fifth in the bass) rarely feels like home. Most often it decorates the dominant (the cadential six-four, whose sixth and fourth fall to the dominant's fifth and third), or it appears over a held or passing bass. Analysts differ in whether they label it as a tonic chord or as part of the dominant."),
    "dominant": ("Tension that wants to resolve home.",
                 "The dominant is built on the fifth degree. Its third is the leading tone, a semitone below the tonic, which pulls upward; with a seventh added, the pull becomes stronger still. Dominants usually resolve to the tonic."),
    "predominant": ("Preparation: moving away from home, toward the dominant.",
                    "Chords on the second and fourth degrees typically lead to the dominant. They create the sense of departure before the tension of the dominant arrives."),
    "submediant": ("A softer substitute for the tonic, or a step toward the predominant.",
                   "The chord on the sixth degree shares two notes with the tonic. After a dominant it can replace the expected tonic (a deceptive resolution); elsewhere it often leads on to a predominant chord."),
    "mediant": ("A chord that shares two notes with the tonic, coloured differently.",
                "The chord on the third degree is less directional than the dominant; in minor keys it is the tonic of the relative major."),
    "leading-tone": ("A dominant without its root.",
                     "Diminished chords on the seventh degree contain the leading tone and the dominant's seventh; they behave like a dominant and resolve to the tonic. The diminished seventh is the same sound as a dominant minor ninth without its root."),
    "subtonic": ("A chord on the lowered seventh degree.", "Often borrowed from the minor mode, it lacks the leading tone's pull."),
    "neapolitan": ("A dark, lowered second degree, leading to the dominant.",
                   "The Neapolitan is a major chord built on the lowered second degree (a semitone above the tonic), usually in first inversion, hence 'N⁶'. It acts as a predominant: its lowered second degree falls by step to the leading tone of the dominant, a striking, shadowed approach to the cadence."),
    "augmented sixth": ("A chromatic predominant whose outer notes spread outward to the dominant.",
                        "Augmented-sixth chords place the lowered sixth degree and the raised fourth degree an augmented sixth apart; they resolve outward by semitone to the dominant's octave. The Italian, French and German types differ in their middle notes."),
    "cadential six-four": ("The dominant arriving, decorated by notes of the tonic.",
                           "A tonic chord in second inversion over the dominant bass usually works as a decoration of the dominant: its sixth and fourth fall to the fifth and third of the dominant chord that follows."),
    "applied": ("A borrowed dominant: it points to a chord other than the tonic.",
                "An applied (secondary) chord treats another chord of the key as a temporary tonic, giving it its own dominant or leading-tone chord. 'V/V' is the dominant of the dominant. Whether such a passage is a brief tonicisation or a real modulation is often a matter of interpretation."),
    "mixture": ("A chord borrowed from the parallel mode.",
                "Modal mixture borrows chords from the parallel major or minor key (for example ♭VI or iv in a major key), darkening or brightening the colour without changing the tonic."),
    "other": ("", ""),
}

INVERSION = {
    (False, 0): "in root position (the root is in the bass)",
    (False, 1): "in first inversion (the third is in the bass)",
    (False, 2): "in second inversion (the fifth is in the bass)",
    (True, 0): "in root position (the root is in the bass)",
    (True, 1): "in first inversion (the third is in the bass)",
    (True, 2): "in second inversion (the fifth is in the bass)",
    (True, 3): "in third inversion (the seventh is in the bass)",
}


def _names(names) -> str:
    return "–".join(pretty(n) for n in names)


def degree_of(label: Label) -> tuple[int, int] | None:
    """(scale degree 1-7, alteration relative to the key's scale) of the label's root."""
    from music21 import key as m21key

    try:
        k = m21key.Key(label.key.tonic, label.key.mode)
        deg, acc = k.getScaleDegreeAndAccidentalFromPitch(m21pitch.Pitch(label.root))
        return deg, int(acc.alter) if acc is not None else 0
    except Exception:  # noqa: BLE001 - explanation must never break the UI
        return None


def degree_phrase(label: Label) -> str:
    d = degree_of(label)
    if not d:
        return ""
    deg, alter = d
    how = {-1: "lowered ", 1: "raised ", -2: "doubly lowered ", 2: "doubly raised "}.get(alter, "")
    return f" on the {how}{ORDINAL.get(deg, '')} degree"


def explain_label(label: Label, next_label: Label | None = None, analyst: str = "") -> dict:
    gist, general = FAMILY.get(label.family, FAMILY["other"])
    seventh = len(label.pcs) >= 4
    inv = INVERSION.get((seventh, label.inversion), f"with {pretty(label.bass)} in the bass")
    key = label.key.label
    quality = label.quality
    who = f"{analyst} reads" if analyst else "Read as"
    if label.applied_to:
        target = label.applied_to
        what = f"{who} {label.display} in {key}: a {quality} chord ({_names(label.pitches)}) acting as a {label.figure.split('/')[0]} of {target}"
    else:
        what = f"{who} {label.display} in {key}: a {quality} chord{degree_phrase(label)}, {_names(label.pitches)}"
    sentence = f"{what}, {inv}."
    if next_label is not None:
        sentence += f" Next: {next_label.display}" + (f" (now in {next_label.key.label})" if next_label.key != label.key else "") + "."
    return {"gist": gist, "instance": sentence, "general": general, "family": label.family}


def explain_comparison(cls: str, a: Label, b: Label, a_name: str, b_name: str) -> str:
    base = CLASS_TEXT[cls]
    if cls == "same":
        return base
    if cls == "key_frame":
        return (f"{base} {a_name} hears {a.display} in {a.key.label}; {b_name} hears {b.display} in {b.key.label}. "
                "The notes are the same; the question is which key the music is in at this moment: has it modulated, "
                "or is it only leaning toward another key (tonicisation)? That is a matter of hearing, not of fact.")
    if cls == "extension":
        extra = (b.pcs - a.pcs) or (a.pcs - b.pcs)
        names = [pretty(n) for n in (b.pitches if b.pcs > a.pcs else a.pitches)
                 if m21pitch.Pitch(n).pitchClass in extra]
        who = b_name if b.pcs > a.pcs else a_name
        return (f"{base} {who} counts {', '.join(names)} as part of the chord; the other analyst treats it as a "
                "melodic note decorating a simpler chord.")
    if cls == "inversion":
        return f"{base} {a_name}: {pretty(a.bass)}; {b_name}: {pretty(b.bass)}."
    return f"{base} {a_name}: {a.display} ({_names(a.pitches)}); {b_name}: {b.display} ({_names(b.pitches)})."


def describe_interval(low: str, high: str) -> dict:
    i = m21interval.Interval(m21pitch.Pitch(low), m21pitch.Pitch(high))
    return {"name": i.niceName, "short": i.directedSimpleName if i.semitones < 12 else i.name,
            "semitones": i.semitones}
