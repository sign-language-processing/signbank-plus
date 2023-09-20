
from load_data import load_file

COLUMNS = ["pid", "eid", "Lang", "Original", "Cleaned (from Original)", "Annotation", "Expanded (from Annotation)"]
ARRAY_COLUMNS = ["texts", "pred_general_specific_5", "gold_texts",
                 "expanded_texts"]

SKIP = {
    (4, "10815"),
    (14, "1"),
    (14, "2"),
    (14, "3"),
    (14, "4"),
    (14, "5"),
    (14, "10"),
    (14, "11"),
    (14, "12"),
    (14, "15"),
    (16, "484"),
    (26, "308"),
    (34, "323"),
    (125, "29"),
    (140, "2"),
    (145, "1"),
    (151, "1001"),
}
if __name__ == "__main__":
    # \begin{longtable}[ht]{lll*{4}{m{0.19\linewidth}}}
    print(r"\begin{longtable}[ht]{lll*{4}{m{0.20\linewidth}}}")
    print(r"\toprule")
    print(" & ".join(COLUMNS) + r"\\")
    print(r"\midrule")
    data = list(load_file("benchmark", array_fields=ARRAY_COLUMNS))

    puddle_done = set()
    for instance in data:
        pid = instance["puddle_id"]
        eid = instance["example_id"]

        t = (int(pid), str(eid))
        if t in SKIP:
            continue

        if pid in puddle_done:
            continue

        if len(" ".join(instance["texts"]).strip()) > 200:
            continue

        print(f"{pid} & {eid} & \\texttt{{{instance['spoken_language']}}} &", end=" ")
        for i, c in enumerate(ARRAY_COLUMNS):
            fixed = [text.replace("\\", "\\textbackslash{}") for text in instance[c]]
            fixed = [text.replace("&", "\\&") for text in fixed]
            fixed = [text.replace("_", "\\_") for text in fixed]
            print("\\texttt{[" + ", ".join(fixed) + "]}", end=" ")
            if i < len(ARRAY_COLUMNS) - 1:
                print("&", end=" ")
        print(r"\\ \midrule")

        puddle_done.add(pid)


    print(r"\bottomrule")
    print(r"\end{longtable}")