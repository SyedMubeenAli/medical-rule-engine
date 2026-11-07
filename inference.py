"""
inference.py
Horn-clause inference: unification, forward chaining, backward chaining.
Run  python inference.py  to print every sample case with both traces.
"""
from knowledge_base import (RULES, SAMPLE_CASES, CONDITIONS, GROUPS,
                            build_facts, fact_text)


def is_variable(term):
    return term[0].isupper()


def unify(pattern, fact, subst):
    """Match ("fever","X") with ("fever","ali"). Returns {"X": "ali"} or None."""
    if len(pattern) != len(fact) or pattern[0] != fact[0]:
        return None
    new = dict(subst)
    for p, f in zip(pattern[1:], fact[1:]):
        if is_variable(p):
            if p in new and new[p] != f:
                return None
            new[p] = f
        elif p != f:
            return None
    return new


def apply_subst(atom, subst):
    return tuple(subst.get(t, t) if is_variable(t) else t for t in atom)


def match_body(body, facts, subst):
    """All substitutions that make every condition of a rule true."""
    if not body:
        return [subst]
    results = []
    for fact in facts:
        s = unify(body[0], fact, subst)
        if s is not None:
            results.extend(match_body(body[1:], facts, s))
    return results


def forward_chain(initial_facts):
    """
    Data-driven: fire any rule whose conditions all hold and whose conclusion
    is new. Repeat until nothing new. Returns (all_facts, trace).
    """
    facts = set(initial_facts)
    trace = []
    while True:
        fired = False
        for rule in RULES:
            for subst in match_body(rule["body"], sorted(facts), {}):
                new_fact = apply_subst(rule["head"], subst)
                if new_fact in facts:
                    continue
                used = [fact_text(apply_subst(b, subst)) for b in rule["body"]]
                trace.append({"step": len(trace) + 1, "rule": rule["id"],
                              "facts_used": ", ".join(used),
                              "new_fact": fact_text(new_fact),
                              "meaning": rule["english"]})
                facts.add(new_fact)
                fired = True
                break
            if fired:
                break
        if not fired:
            return facts, trace


def backward_chain(goal, facts):
    """
    Goal-driven: prove a goal like ("flu","ali") by proving the conditions of
    a rule that concludes it. Returns (True/False, trace lines).
    """
    lines = []

    def prove(g, depth):
        pad = "    " * depth
        lines.append(pad + "? " + fact_text(g))
        if g in facts:
            lines.append(pad + "    known fact  ->  TRUE")
            return True
        rules = [r for r in RULES if unify(r["head"], g, {}) is not None]
        if not rules:
            lines.append(pad + "    not a fact and no rule concludes it  ->  FALSE")
            return False
        for rule in rules:
            subst = unify(rule["head"], g, {})
            needs = [apply_subst(b, subst) for b in rule["body"]]
            lines.append(pad + "    try " + rule["id"] + ", needs: " + ", ".join(fact_text(n) for n in needs))
            if all(prove(n, depth + 2) for n in needs):
                lines.append(pad + "    " + rule["id"] + " succeeded  ->  TRUE")
                return True
            lines.append(pad + "    " + rule["id"] + " failed  ->  FALSE")
        return False

    ok = prove(goal, 0)
    return ok, "\n".join(lines)


def diagnose(name, symptoms, allergies, medications):
    """Forward chaining for one patient, results sorted into groups."""
    initial = build_facts(name, symptoms, allergies, medications)
    all_facts, trace = forward_chain(initial)
    derived = all_facts - initial
    return {
        "initial": initial,
        "trace": trace,
        "conditions": sorted(f[0] for f in derived if f[0] in CONDITIONS),
        "groups": sorted(f[0] for f in derived if f[0] in GROUPS),
        "contraindicated": sorted(f[2] for f in derived if f[0] == "contraindicated"),
        "contra_rules": {t["new_fact"]: t for t in trace if t["new_fact"].startswith("contraindicated")},
    }


def goal_choices(name):
    """Goals the user can pick for backward chaining: label -> fact."""
    goals = {}
    for key, label in {**CONDITIONS, **GROUPS}.items():
        goals[label] = (key, name)
    for med in ("amoxicillin", "aspirin", "ibuprofen"):
        goals["Contraindicated: " + med] = ("contraindicated", name, med)
    return goals


if __name__ == "__main__":
    for title, case in SAMPLE_CASES.items():
        print("=" * 70)
        print("CASE", title)
        res = diagnose(case["name"], case["symptoms"], case["allergies"], case["medications"])
        print("Facts:", ", ".join(sorted(fact_text(f) for f in res["initial"])))
        print("\nFORWARD CHAINING")
        for t in res["trace"]:
            print("  step %d | %s | %s  =>  %s" % (t["step"], t["rule"], t["facts_used"], t["new_fact"]))
        if not res["trace"]:
            print("  no rule fired")
        print("Possible conditions:", res["conditions"] or "none")
        print("Contraindicated    :", res["contraindicated"] or "none")
        if case["medications"]:
            goal = ("contraindicated", case["name"], case["medications"][0])
        elif res["conditions"]:
            goal = (res["conditions"][0], case["name"])
        else:
            goal = ("flu", case["name"])
        ok, text = backward_chain(goal, res["initial"])
        print("\nBACKWARD CHAINING goal:", fact_text(goal), "->", ok)
        print(text)
