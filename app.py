"""
app.py - Medical Diagnostic & Contraindication Rule Engine (CT-351 KRR)
Run:  streamlit run app.py
"""
import html
from pathlib import Path

import streamlit as st

import logic
import structures
from inference import diagnose, backward_chain, goal_choices
from knowledge_base import (SYMPTOMS, CONDITIONS, GROUPS, MEDICATIONS,
                            ALLERGIES, RULES, SAMPLE_CASES, fact_text, horn_text, build_facts)

st.set_page_config(page_title="Medical Rule Engine", layout="wide")

CSS_PATH = Path(__file__).parent / "style.css"
st.markdown("<style>" + CSS_PATH.read_text(encoding="utf-8") + "</style>", unsafe_allow_html=True)

st.markdown('<div class="kicker">CT-351 · Knowledge Representation & Reasoning</div>',
            unsafe_allow_html=True)
st.title("Medical Rule Engine")

MEMBERS = [("Muhammad Affan Mushahid", "AI-23017"),
           ("Saim Masood", "AI-23043"),
           ("Syed Mubeen Ali", "AI-23016"),
           ("Muhammad Hasan Kashif", "AI-23015")]
cards = "".join('<div class="member"><div class="m-name">%s</div><div class="m-roll">%s</div></div>'
                % (html.escape(n), html.escape(r)) for n, r in MEMBERS)
st.markdown('<div class="members">%s</div>' % cards, unsafe_allow_html=True)


def show(rows):
    """Themed table that wraps long text (all columns shown, no row index)."""
    cols = list(rows[0].keys())
    head = "".join("<th>%s</th>" % html.escape(str(c)) for c in cols)
    body = "".join("<tr>" + "".join("<td>%s</td>" % html.escape(str(r[c])) for c in cols) + "</tr>"
                   for r in rows)
    st.markdown('<div class="kr-table"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
                % (head, body), unsafe_allow_html=True)


# ---------------- patient input (kept in session state) ----------------
for key, default in [("name", "ali"), ("sym", []), ("alg", []), ("med", [])]:
    st.session_state.setdefault(key, default)


def load_sample():
    case = SAMPLE_CASES[st.session_state["sample"]]
    st.session_state.update(name=case["name"], sym=list(case["symptoms"]),
                            alg=list(case["allergies"]), med=list(case["medications"]))


def clean_name(text):
    name = "".join(c for c in text.strip().lower() if c.isalnum() or c == "_")
    return name if name and name[0].isalpha() else "patient1"


name = clean_name(st.session_state["name"])
result = diagnose(name, st.session_state["sym"], st.session_state["alg"], st.session_state["med"])

tabs = st.tabs(["Patient", "Frames", "Semantic Network", "FOL & DL", "Horn Rules",
                "Forward Chaining", "Backward Chaining"])

# ---------------- 1. Patient ----------------
with tabs[0]:
    c1, c2 = st.columns([3, 1], vertical_alignment="bottom")
    c1.selectbox("Sample case", list(SAMPLE_CASES), key="sample")
    c2.button("Load sample", on_click=load_sample)
    st.text_input("Patient name (one word)", key="name")
    st.multiselect("Symptoms", SYMPTOMS, key="sym")
    st.multiselect("Allergies", ALLERGIES, key="alg")
    st.multiselect("Medications taken", MEDICATIONS, key="med")

    st.subheader("Result")
    if not st.session_state["sym"] and not st.session_state["med"]:
        st.info("Select symptoms or medications to see a result.")
    else:
        if result["conditions"]:
            st.success("Possible conditions: " + ", ".join(CONDITIONS[c] for c in result["conditions"]))
        else:
            st.info("No condition rule matched the symptoms.")
        if result["contraindicated"]:
            for fact, t in result["contra_rules"].items():
                st.error("%s  (rule %s: %s)" % (fact, t["rule"], t["meaning"]))
        else:
            st.success("No contraindication found.")

# ---------------- 2. Frames ----------------
with tabs[1]:
    st.write("A frame describes a concept with slots. Each slot has facets: type, default value "
             "and allowed values. Patient inherits the slots of Person (is-a).")
    for fname, frame in structures.FRAMES.items():
        title = fname + ("  (is-a " + frame["parent"] + ")" if frame["parent"] else "")
        with st.expander(title, expanded=(fname == "Patient")):
            show(structures.frame_rows(fname))

    sc = structures.SCRIPT
    st.subheader("Script: " + sc["name"])
    st.write("A script is a fixed sequence of events. **Entry condition:** " + sc["entry"])
    show([{"Step": n, "Who": who, "Action": action} for n, who, action in sc["steps"]])
    st.write("**End state:** " + sc["end"])

# ---------------- 3. Semantic network ----------------
with tabs[2]:
    st.graphviz_chart(structures.to_dot())
    st.caption("Blue = is-a · Green = has-a · Orange = part-of")
    show([{"From": a, "Relation": r, "To": b} for a, r, b in structures.LINKS])

# ---------------- 4. FOL & DL ----------------
with tabs[3]:
    st.header("First-Order Logic")
    show([{"ID": i, "English": e, "FOL": f} for i, e, f in logic.FOL])
    show([{"Symbol": s, "Meaning": m} for s, m in logic.QUANTIFIERS])
    st.header("Description Logic")
    show([{"Kind": k, "Axiom": n, "Meaning": m} for k, n, m in logic.DL])
    st.header("Expressiveness vs tractability")
    show([{"Logic": n, "Expressiveness": e, "Tractability": t, "In this project": p}
          for n, e, t, p in logic.LIMITS])

# ---------------- 5. Horn rules ----------------
with tabs[4]:
    st.write("Each rule is a Horn clause: one conclusion, then `:-`, then the conditions. "
             "Capital letters are variables, lowercase are constants.")
    show([{"ID": r["id"], "Rule": r["english"], "Horn clause": horn_text(r)} for r in RULES])

# ---------------- 6. Forward chaining ----------------
with tabs[5]:
    st.write("Forward chaining starts from the known facts and fires rules until nothing new appears.")
    st.write("**Known facts:** " + ", ".join(sorted(fact_text(f) for f in result["initial"])))
    if result["trace"]:
        show([{"Step": t["step"], "Rule": t["rule"], "Facts used": t["facts_used"],
               "New fact": t["new_fact"]} for t in result["trace"]])
        st.write("No more rules apply. Stop.")
    else:
        st.info("No rule fired. Nothing can be derived from these facts.")

# ---------------- 7. Backward chaining ----------------
with tabs[6]:
    st.write("Backward chaining starts from a goal and checks which facts are needed to prove it.")
    goals = goal_choices(name)
    # start on the first goal that can be proven for this patient (if any)
    first_proven = next((i for i, g in enumerate(goals.values())
                         if backward_chain(g, result["initial"])[0]), 0)
    label = st.selectbox("Goal to prove", list(goals), index=first_proven)
    goal = goals[label]
    ok, text = backward_chain(goal, result["initial"])
    if ok:
        st.success("%s is PROVEN." % fact_text(goal))
    else:
        st.warning("%s could NOT be proven from the known facts." % fact_text(goal))
    st.code(text, language="text")
