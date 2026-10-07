import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
)

# Mesma base e mesma divisao treino/teste da Questao 3.
data = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    data.data,
    data.target,
    test_size=0.20,
    random_state=42,
    stratify=data.target,
)

# PRISM classico trabalha com atributos categoricos. Os atributos continuos
# sao discretizados em tercis calculados APENAS no treino, evitando leakage.
cuts = np.quantile(X_train, [1 / 3, 2 / 3], axis=0)


def discretize(X):
    return np.array(
        [
            [
                0 if value <= cuts[0, j] else 1 if value <= cuts[1, j] else 2
                for j, value in enumerate(row)
            ]
            for row in X
        ],
        dtype=np.int8,
    )


A_train = discretize(X_train)
A_test = discretize(X_test)


def prism(X, y):
    """Induz regras PRISM para cada classe.

    Para cada classe, mantem apenas os positivos ainda nao cobertos mais todos
    os negativos. Em cada regra, escolhe atributo=valor de maior precisao para
    a classe alvo (desempate por quantidade de positivos cobertos).
    """
    learned_rules = []
    all_indices = set(range(len(y)))

    for target_class in sorted(np.unique(y)):
        remaining_positives = set(np.where(y == target_class)[0])
        negative_indices = all_indices - set(np.where(y == target_class)[0])

        while remaining_positives:
            candidate = set(remaining_positives) | negative_indices
            conditions = []
            available = set(range(X.shape[1]))

            while candidate and any(y[i] != target_class for i in candidate):
                best = None

                for feature in available:
                    for value in np.unique(X[list(candidate), feature]):
                        covered = {
                            i for i in candidate if X[i, feature] == value
                        }
                        if not covered:
                            continue

                        positives = sum(y[i] == target_class for i in covered)
                        precision = positives / len(covered)
                        score = (precision, positives, -len(covered))

                        if best is None or score > best[0]:
                            best = (score, feature, int(value), covered)

                if best is None:
                    break

                _, feature, value, candidate = best
                conditions.append((feature, value))
                available.remove(feature)

                if not available:
                    break

            covered_positives = {
                i for i in candidate if y[i] == target_class
            }
            if not covered_positives:
                break

            learned_rules.append((conditions, int(target_class)))
            remaining_positives -= covered_positives

    return learned_rules


rules = prism(A_train, y_train)

# Na classificacao, usa-se a primeira regra satisfeita. Se nenhuma regra
# disparar, usa-se a classe majoritaria do conjunto de treino.
values, counts = np.unique(y_train, return_counts=True)
default_class = int(values[np.argmax(counts)])


def predict_one(row):
    for conditions, target_class in rules:
        if all(row[feature] == value for feature, value in conditions):
            return target_class
    return default_class


pred = np.array([predict_one(row) for row in A_test])
feature_names = data.feature_names
labels = ["baixo", "medio", "alto"]

with open("regras_prism.txt", "w", encoding="utf-8") as f:
    f.write("REGRAS GERADAS PELO PRISM\n")
    f.write("=" * 62 + "\n\n")
    for k, (conditions, target_class) in enumerate(rules, 1):
        antecedent = " E ".join(
            f"{feature_names[feature]} = {labels[value]}"
            for feature, value in conditions
        )
        f.write(
            f"R{k}: SE {antecedent} "
            f"ENTAO classe = {data.target_names[target_class]}\n"
        )

accuracy = accuracy_score(y_test, pred)
precision = precision_score(y_test, pred)
recall = recall_score(y_test, pred)
f1 = f1_score(y_test, pred)

with open("metricas_prism.txt", "w", encoding="utf-8") as f:
    f.write("METRICAS DO PRISM\n")
    f.write("=" * 42 + "\n\n")
    f.write(f"Accuracy:  {accuracy:.4f}\n")
    f.write(f"Precision: {precision:.4f}\n")
    f.write(f"Recall:    {recall:.4f}\n")
    f.write(f"F1-score:  {f1:.4f}\n\n")
    f.write("RELATORIO DE CLASSIFICACAO\n")
    f.write("=" * 42 + "\n")
    f.write(classification_report(y_test, pred, target_names=data.target_names))

print("=" * 58)
print("QUESTAO 4 - PRISM")
print("=" * 58)
print(f"Quantidade de regras geradas: {len(rules)}")
print()
print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-score:  {f1:.4f}")
print()
print("Arquivos gerados:")
print("- regras_prism.txt")
print("- metricas_prism.txt")
print("=" * 58)
