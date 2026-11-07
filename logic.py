"""
logic.py
Formal layer: First-Order Logic formulas, Description Logic axioms,
and the expressiveness vs tractability discussion.
These are written down for the report. The Horn clauses in inference.py are what run.
"""

# (id, english, FOL formula)
FOL = [
    ("F1", "Ali is a patient.", "Patient(Ali)"),
    ("F2", "Ali has the symptom fever.", "HasSymptom(Ali, Fever)"),
    ("F3", "Anyone with fever, cough and sore throat may have Flu (R01).",
     "∀x ((HasSymptom(x,Fever) ∧ HasSymptom(x,Cough) ∧ HasSymptom(x,SoreThroat)) → Flu(x))"),
    ("F4", "Anyone who may have Flu has a respiratory condition (R06).",
     "∀x (Flu(x) → RespiratoryCondition(x))"),
    ("F5", "A penicillin allergy with amoxicillin is a contraindication (R09).",
     "∀x ((Allergy(x,Penicillin) ∧ Takes(x,Amoxicillin)) → Contraindicated(x,Amoxicillin))"),
    ("F6", "Some patient has fever.",
     "∃x (Patient(x) ∧ HasSymptom(x,Fever))"),
    ("F7", "Nothing is both a medication and a medical condition.",
     "∀x (Medication(x) → ¬MedicalCondition(x))"),
]

QUANTIFIERS = [
    ("∀ (for all)", "True for every object. Used in rules."),
    ("∃ (there exists)", "True for at least one object."),
    ("∧ (and)", "Both sides must be true."),
    ("→ (implies)", "If the left side is true, the right side is true."),
    ("¬ (not)", "Reverses truth. Used only in F7."),
]

# Description Logic: (kind, notation, plain English)
DL = [
    ("Subsumption", "Patient ⊑ Person", "Every Patient is a Person."),
    ("Subsumption", "Flu ⊑ RespiratoryCondition", "Every Flu case is a respiratory condition."),
    ("Subsumption", "CommonCold ⊑ RespiratoryCondition", "Every Common Cold is a respiratory condition."),
    ("Subsumption", "RespiratoryCondition ⊑ MedicalCondition", "Every respiratory condition is a medical condition."),
    ("Subsumption", "Gastroenteritis ⊑ DigestiveCondition", "Every Gastroenteritis is a digestive condition."),
    ("Subsumption", "DigestiveCondition ⊑ MedicalCondition", "Every digestive condition is a medical condition."),
    ("Subsumption", "Amoxicillin ⊑ Medication", "Amoxicillin is a medication."),
    ("Disjointness", "Medication ⊓ MedicalCondition ⊑ ⊥", "Nothing is both a medication and a medical condition."),
    ("Disjointness", "RespiratoryCondition ⊓ DigestiveCondition ⊑ ⊥", "Nothing is both respiratory and digestive."),
    ("Disjointness", "Patient ⊓ Medication ⊑ ⊥", "A patient is never a medication."),
    ("Membership", "Ali : Patient", "Ali is an individual of class Patient."),
    ("Membership", "FluCase1 : Flu", "FluCase1 is an individual of class Flu."),
]

# (logic, expressiveness, tractability, in this project)
LIMITS = [
    ("Propositional logic", "Low. No variables: 'Ali has fever' and 'Sara has fever' are different symbols.",
     "Decidable, but SAT is NP-complete.",
     "Needs one symbol per patient and symptom (fever_ali, cough_ali). Does not scale."),
    ("First-order logic", "High. Variables, quantifiers and relations.",
     "Semi-decidable. A prover may run forever on a false statement.",
     "Good for stating F1 to F7, but too costly to run a general prover on them."),
    ("Description logic", "Medium. Classes, individuals and restrictions.",
     "Decidable for common DLs.",
     "Fits the class hierarchy (Flu ⊑ RespiratoryCondition) and disjointness."),
    ("Horn clauses", "Lower. One conclusion per rule, no negated conclusions.",
     "Chaining is fast (linear for propositional Horn).",
     "R01 to R11 are Horn clauses, so a simple chaining loop runs them."),
]
