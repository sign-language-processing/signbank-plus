from clean_rules import clean_instance
from load_data import load_file

def calc_IoU(gold_row, pred_row):
    gold_row = set(gold_row)
    pred_row = set(pred_row)
    union = gold_row.union(pred_row)
    intersection = gold_row.intersection(pred_row)
    if len(union) == 0:
        return 1
    return len(intersection) / len(union)


def main():
    gold_field = "gold_texts"
    other_fields = ["texts", "pred_rules", "pred_general", "pred_specific_5", "pred_general_specific_5",
                    "pred_general_specific_5_gpt_4"]

    all_instances = load_file("benchmark", array_fields=other_fields + [gold_field])

    # Rule based cleaning
    for instance in all_instances:
        instance_deep_copy = instance.copy()
        instance_deep_copy["texts"] = instance_deep_copy["texts"].copy()
        clean_instance(instance_deep_copy)
        instance["pred_rules"] = instance_deep_copy["texts"]

    gold_rows = [instance[gold_field] for instance in all_instances]
    print("|method|IoU|Average Tokens|")
    print("|---|---|---|")
    for field in other_fields:
        field_rows = [instance[field] for instance in all_instances]
        IoU = []
        for gold_row, field_row in zip(gold_rows, field_rows):
            IoU.append(calc_IoU(gold_row, field_row))

        tokens = [int(instance[field + '_tokens']) for instance in all_instances]
        avg_tokens = sum(tokens) / len(tokens)
        print(f"|{field}|{sum(IoU) / len(IoU):.3f}|{avg_tokens:.1f}|")


if __name__ == "__main__":
    main()
