# Medical Rule Engine (CT-351 KRR)

Educational demo. Fictional data. Not for medical decisions.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

No Streamlit? Print all sample cases with both traces:

```bash
python inference.py
```

## Files

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit interface (7 tabs) |
| `style.css`, `.streamlit/config.toml` | Dark blue theme |
| `knowledge_base.py` | Symptoms, conditions, 11 rules, sample cases |
| `structures.py` | Frames, script, semantic network |
| `logic.py` | FOL, Description Logic, expressiveness vs tractability |
| `inference.py` | Unification, forward and backward chaining |

## CCP requirement map

| Requirement | Where |
| --- | --- |
| Frames, slots, facets, defaults, script | Frames tab |
| Semantic network (is-a, has-a, part-of) | Semantic Network tab |
| FOL formulas | FOL & DL tab |
| DL subsumption, membership, disjointness | FOL & DL tab |
| Expressiveness vs tractability | FOL & DL tab |
| Horn clauses | Horn Rules tab |
| Forward chaining trace | Forward Chaining tab |
| Backward chaining trace | Backward Chaining tab |
| Sample execution output | `python inference.py` |
