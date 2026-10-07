from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree, _tree
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
)
import matplotlib.pyplot as plt

# Base externa publica disponibilizada pelo scikit-learn.
data = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    data.data,
    data.target,
    test_size=0.20,
    random_state=42,
    stratify=data.target,
)

model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_test)

accuracy = accuracy_score(y_test, pred)
precision = precision_score(y_test, pred)
recall = recall_score(y_test, pred)
f1 = f1_score(y_test, pred)

with open("metricas.txt", "w", encoding="utf-8") as f:
    f.write(f"Accuracy: {accuracy:.4f}\n")
    f.write(f"Precision: {precision:.4f}\n")
    f.write(f"Recall: {recall:.4f}\n")
    f.write(f"F1-score: {f1:.4f}\n\n")
    f.write("Observacao: no dataset do scikit-learn, classe 1 = benign;\n")
    f.write("por isso Precision/Recall/F1 binarios acima usam benign como classe positiva.\n\n")
    f.write(classification_report(y_test, pred, target_names=data.target_names))


def extract_rules(model, feature_names, class_names):
    t = model.tree_
    rules = []

    def walk(node, conditions):
        if t.feature[node] != _tree.TREE_UNDEFINED:
            feature = feature_names[t.feature[node]]
            threshold = t.threshold[node]
            walk(
                t.children_left[node],
                conditions + [f"{feature} <= {threshold:.4f}"],
            )
            walk(
                t.children_right[node],
                conditions + [f"{feature} > {threshold:.4f}"],
            )
        else:
            class_index = t.value[node][0].argmax()
            rules.append(
                "SE " + " E ".join(conditions) +
                f" ENTAO classe = {class_names[class_index]}"
            )

    walk(0, [])
    return rules


rules = extract_rules(model, data.feature_names, data.target_names)
with open("regras.txt", "w", encoding="utf-8") as f:
    f.write("REGRAS EXTRAIDAS DA ARVORE DE DECISAO\n")
    f.write("=" * 70 + "\n\n")
    for i, rule in enumerate(rules, 1):
        f.write(f"R{i}: {rule}\n")

plt.figure(figsize=(24, 12))
plot_tree(
    model,
    feature_names=data.feature_names,
    class_names=data.target_names,
    filled=True,
    rounded=True,
)
plt.tight_layout()
plt.savefig("arvore_decisao.png", dpi=160)
plt.close()

print("Questao 3 executada com sucesso.")
print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-score:  {f1:.4f}")
print(f"Regras extraidas: {len(rules)}")
