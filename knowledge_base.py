"""
knowledge_base.py
All domain data (fictional, for teaching only): vocabulary, rules, sample cases.

Fact  : tuple, e.g. ("fever", "ali") or ("allergy", "ali", "penicillin")
Rule  : id, english text, head (conclusion), body (list of conditions)
Terms : Capital letter = variable (X), lowercase = constant (ali)
"""


SYMPTOMS = ["fever", "cough", "sore_throat", "sneezing", "runny_nose",
            "headache", "nausea", "vomiting", "diarrhea", "itchy_eyes"]

CONDITIONS = {"flu": "Flu", "common_cold": "Common Cold",
              "gastroenteritis": "Gastroenteritis", "migraine": "Migraine",
              "seasonal_allergy": "Seasonal Allergy"}

GROUPS = {"respiratory_condition": "Respiratory Condition",
          "digestive_condition": "Digestive Condition"}

MEDICATIONS = ["amoxicillin", "aspirin", "ibuprofen"]
ALLERGIES = ["penicillin", "aspirin"]

RULES = [
    {"id": "R01", "english": "Fever, cough and sore throat -> Flu",
     "head": ("flu", "X"),
     "body": [("fever", "X"), ("cough", "X"), ("sore_throat", "X")]},
    {"id": "R02", "english": "Sneezing and runny nose -> Common Cold",
     "head": ("common_cold", "X"),
     "body": [("sneezing", "X"), ("runny_nose", "X")]},
    {"id": "R03", "english": "Nausea, vomiting and diarrhea -> Gastroenteritis",
     "head": ("gastroenteritis", "X"),
     "body": [("nausea", "X"), ("vomiting", "X"), ("diarrhea", "X")]},
    {"id": "R04", "english": "Headache and nausea -> Migraine",
     "head": ("migraine", "X"),
     "body": [("headache", "X"), ("nausea", "X")]},
    {"id": "R05", "english": "Sneezing and itchy eyes -> Seasonal Allergy",
     "head": ("seasonal_allergy", "X"),
     "body": [("sneezing", "X"), ("itchy_eyes", "X")]},
    # rules that use earlier conclusions (multi-step reasoning)
    {"id": "R06", "english": "Flu -> Respiratory Condition",
     "head": ("respiratory_condition", "X"), "body": [("flu", "X")]},
    {"id": "R07", "english": "Common Cold -> Respiratory Condition",
     "head": ("respiratory_condition", "X"), "body": [("common_cold", "X")]},
    {"id": "R08", "english": "Gastroenteritis -> Digestive Condition",
     "head": ("digestive_condition", "X"), "body": [("gastroenteritis", "X")]},
    # contraindication rules
    {"id": "R09", "english": "Penicillin allergy and takes amoxicillin -> amoxicillin contraindicated",
     "head": ("contraindicated", "X", "amoxicillin"),
     "body": [("allergy", "X", "penicillin"), ("takes", "X", "amoxicillin")]},
    {"id": "R10", "english": "Aspirin allergy and takes aspirin -> aspirin contraindicated",
     "head": ("contraindicated", "X", "aspirin"),
     "body": [("allergy", "X", "aspirin"), ("takes", "X", "aspirin")]},
    {"id": "R11", "english": "Gastroenteritis and takes ibuprofen -> ibuprofen contraindicated",
     "head": ("contraindicated", "X", "ibuprofen"),
     "body": [("gastroenteritis", "X"), ("takes", "X", "ibuprofen")]},
]

SAMPLE_CASES = {
    "A: Flu symptoms": {"name": "ali", "symptoms": ["fever", "cough", "sore_throat"],
                        "allergies": [], "medications": []},
    "B: Common Cold symptoms": {"name": "sara", "symptoms": ["sneezing", "runny_nose"],
                                "allergies": [], "medications": []},
    "C: Penicillin allergy + amoxicillin": {"name": "ali", "symptoms": ["fever"],
                                            "allergies": ["penicillin"], "medications": ["amoxicillin"]},
    "D: Stomach illness + ibuprofen (multi-step)": {"name": "omar",
                                                    "symptoms": ["nausea", "vomiting", "diarrhea"],
                                                    "allergies": [], "medications": ["ibuprofen"]},
    "E: Not enough symptoms (nothing derived)": {"name": "zara", "symptoms": ["fever", "cough"],
                                                 "allergies": [], "medications": []},
}


def build_facts(name, symptoms, allergies, medications):
    """Patient form -> set of facts."""
    facts = {("patient", name)}
    facts.update((s, name) for s in symptoms)
    facts.update(("allergy", name, a) for a in allergies)
    facts.update(("takes", name, m) for m in medications)
    return facts


def fact_text(fact):
    """('allergy','ali','penicillin') -> 'allergy(ali, penicillin)'"""
    return fact[0] + "(" + ", ".join(fact[1:]) + ")"


def horn_text(rule):
    """Rule -> Prolog-style Horn clause text."""
    return fact_text(rule["head"]) + " :- " + ", ".join(fact_text(b) for b in rule["body"]) + "."
