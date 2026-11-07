"""
structures.py
Structural knowledge representation: Frames, one Script, Semantic Network.
"""
from knowledge_base import SYMPTOMS, MEDICATIONS, ALLERGIES

# ---------------- Frames ----------------
# slot = (slot name, type, default value, allowed values)
FRAMES = {
    "Person": {"parent": None, "slots": [
        ("name", "text", "unknown", "any"),
        ("age", "number", "0", "any")]},
    "Patient": {"parent": "Person", "slots": [
        ("symptoms", "list", "[]", ", ".join(SYMPTOMS)),
        ("allergies", "list", "[]", ", ".join(ALLERGIES)),
        ("medications", "list", "[]", ", ".join(MEDICATIONS))]},
    "Symptom": {"parent": None, "slots": [
        ("name", "text", "unknown", ", ".join(SYMPTOMS)),
        ("body_system", "text", "general", "general, respiratory, digestive, head"),
        ("severity", "text", "mild", "mild, moderate, severe")]},
    "MedicalCondition": {"parent": None, "slots": [
        ("name", "text", "unknown", "flu, common_cold, gastroenteritis, migraine, seasonal_allergy"),
        ("required_symptoms", "list", "[]", ", ".join(SYMPTOMS)),
        ("category", "text", "general", "general, respiratory, digestive")]},
    "Medication": {"parent": None, "slots": [
        ("name", "text", "unknown", ", ".join(MEDICATIONS)),
        ("drug_family", "text", "other", "penicillin, nsaid, other"),
        ("prescription_needed", "text", "no", "yes, no")]},
}


def frame_rows(frame_name):
    """Slots of a frame including slots inherited from its parent (is-a)."""
    frame = FRAMES[frame_name]
    rows = []
    if frame["parent"]:
        for row in frame_rows(frame["parent"]):
            row["inherited from"] = row["inherited from"] or frame["parent"]
            rows.append(row)
    for slot, typ, default, allowed in frame["slots"]:
        rows.append({"slot": slot, "type": typ, "default": default,
                     "allowed values": allowed, "inherited from": ""})
    return rows


# ---------------- Script ----------------
SCRIPT = {
    "name": "Medical Diagnosis Visit",
    "entry": "The patient reports at least one symptom.",
    "steps": [(1, "Patient", "Reports symptoms, allergies and medications."),
              (2, "Rule engine", "Turns the report into facts."),
              (3, "Rule engine", "Forward chaining derives possible conditions and contraindications."),
              (4, "Rule engine", "Backward chaining can prove a chosen goal."),
              (5, "Clinician", "Reviews the result (outside this system).")],
    "end": "Possible conditions and contraindications are listed, each with its rule trace.",
}

# ---------------- Semantic network ----------------
LINKS = [
    ("Patient", "is-a", "Person"),
    ("Flu", "is-a", "MedicalCondition"),
    ("CommonCold", "is-a", "MedicalCondition"),
    ("Gastroenteritis", "is-a", "MedicalCondition"),
    ("Fever", "is-a", "Symptom"),
    ("Cough", "is-a", "Symptom"),
    ("Nausea", "is-a", "Symptom"),
    ("Patient", "has-a", "Symptom"),
    ("Patient", "has-a", "Allergy"),
    ("Patient", "has-a", "Medication"),
    ("Patient", "has-a", "HumanBody"),
    ("MedicalCondition", "has-a", "Symptom"),
    ("Throat", "part-of", "RespiratorySystem"),
    ("Lungs", "part-of", "RespiratorySystem"),
    ("Stomach", "part-of", "DigestiveSystem"),
    ("RespiratorySystem", "part-of", "HumanBody"),
    ("DigestiveSystem", "part-of", "HumanBody"),
]

COLORS = {"is-a": "#4d9bff", "has-a": "#5ee0b0", "part-of": "#ffb347"}


def to_dot():
    """Graphviz text for the semantic network (dark theme colours)."""
    lines = ["digraph G {", 'bgcolor="transparent"; rankdir=LR;',
             'node [shape=box, style="rounded,filled", fillcolor="#0a1a3a", color="#4d9bff", '
             'fontcolor="white", fontname="Helvetica"];',
             'edge [fontname="Helvetica", fontsize=10];']
    for a, rel, b in LINKS:
        c = COLORS[rel]
        lines.append('"%s" -> "%s" [label="%s", color="%s", fontcolor="%s"];' % (a, b, rel, c, c))
    lines.append("}")
    return "\n".join(lines)
