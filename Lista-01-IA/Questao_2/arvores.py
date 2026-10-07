import csv
import math
from collections import Counter, defaultdict

TARGET = "Risco"


def entropy(rows):
    counts = Counter(row[TARGET] for row in rows)
    n = len(rows)
    return -sum((v / n) * math.log2(v / n) for v in counts.values() if v)


def split(rows, attribute):
    groups = defaultdict(list)
    for row in rows:
        groups[row[attribute]].append(row)
    return groups


def gain(rows, attribute):
    return entropy(rows) - sum(
        len(group) / len(rows) * entropy(group)
        for group in split(rows, attribute).values()
    )


def split_info(rows, attribute):
    return -sum(
        (len(group) / len(rows)) * math.log2(len(group) / len(rows))
        for group in split(rows, attribute).values()
    )


def gain_ratio(rows, attribute):
    info = split_info(rows, attribute)
    return gain(rows, attribute) / info if info else 0.0


def majority(rows):
    return Counter(row[TARGET] for row in rows).most_common(1)[0][0]


def build_tree(rows, attributes, criterion):
    classes = {row[TARGET] for row in rows}
    if len(classes) == 1:
        return next(iter(classes))
    if not attributes:
        return majority(rows)

    score = gain_ratio if criterion == "c45" else gain
    best = max(attributes, key=lambda a: score(rows, a))
    remaining = [a for a in attributes if a != best]

    return {
        "atributo": best,
        "ramos": {
            value: build_tree(group, remaining, criterion)
            for value, group in split(rows, best).items()
        },
    }


def text_tree(tree, indent=""):
    if isinstance(tree, str):
        return indent + "=> " + tree + "\n"
    out = indent + tree["atributo"] + "?\n"
    for value, subtree in tree["ramos"].items():
        out += indent + f"|- {value}\n"
        out += text_tree(subtree, indent + "|  ")
    return out


def extract_rules(tree, prefix=None):
    prefix = prefix or []
    if isinstance(tree, str):
        return ["SE " + " E ".join(prefix) + " ENTAO Risco = " + tree]
    result = []
    attribute = tree["atributo"]
    for value, subtree in tree["ramos"].items():
        result += extract_rules(subtree, prefix + [f"{attribute} = {value}"])
    return result


with open("risco_credito_ampliado.csv", encoding="utf-8") as f:
    data = list(csv.DictReader(f))

attributes = [c for c in data[0] if c not in ("Exemplo", TARGET)]

with open("resultados.txt", "w", encoding="utf-8") as out:
    for name, criterion in [("ID3", "id3"), ("C4.5", "c45")]:
        tree = build_tree(data, attributes, criterion)
        out.write("=" * 70 + "\n")
        out.write(name + "\n")
        out.write("=" * 70 + "\n")
        out.write(text_tree(tree))
        out.write("\nREGRAS\n")
        for i, rule in enumerate(extract_rules(tree), 1):
            out.write(f"R{i}: {rule}\n")
        out.write("\n")

# CART via scikit-learn (Gini + divisao binaria).
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier, export_text, _tree

frame = pd.read_csv("risco_credito_ampliado.csv")
X = frame[attributes]
y = frame[TARGET]

pre = ColumnTransformer(
    [("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), attributes)]
)
X_encoded = pre.fit_transform(X)
feature_names = list(pre.get_feature_names_out())
model = DecisionTreeClassifier(criterion="gini", random_state=42).fit(X_encoded, y)


def cart_rules(model, feature_names):
    tree = model.tree_
    names = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else None
        for i in tree.feature
    ]
    result = []

    def walk(node, conditions):
        if tree.feature[node] != _tree.TREE_UNDEFINED:
            name = names[node].replace("cat__", "")
            threshold = tree.threshold[node]
            walk(tree.children_left[node], conditions + [f"{name} <= {threshold:.2f}"])
            walk(tree.children_right[node], conditions + [f"{name} > {threshold:.2f}"])
        else:
            class_index = tree.value[node][0].argmax()
            target = model.classes_[class_index]
            result.append("SE " + " E ".join(conditions) + f" ENTAO Risco = {target}")

    walk(0, [])
    return result


with open("resultados.txt", "a", encoding="utf-8") as out:
    out.write("=" * 70 + "\n")
    out.write("CART\n")
    out.write("=" * 70 + "\n")
    out.write(export_text(model, feature_names=feature_names))
    out.write("\nREGRAS\n")
    for i, rule in enumerate(cart_rules(model, feature_names), 1):
        out.write(f"R{i}: {rule}\n")

print("Questao 2 executada com sucesso.")
print("Arvores e regras de ID3, C4.5 e CART gravadas em resultados.txt.")
