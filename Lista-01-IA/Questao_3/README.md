# Questão 3 — Árvore de decisão em uma base externa

Foi utilizado o conjunto **Breast Cancer Wisconsin Diagnostic**, disponibilizado pelo scikit-learn. A base possui **569 instâncias, 30 atributos preditores e duas classes: malignant e benign**.

Os dados são separados em **80% para treinamento e 20% para teste**, com `random_state=42` e estratificação. É treinada uma árvore `DecisionTreeClassifier(max_depth=5, random_state=42)`.

Na execução validada, foram obtidos:

| Métrica | Resultado |
|---|---:|
| Accuracy | 0,9211 |
| Precision | 0,9565 |
| Recall | 0,9167 |
| F1-score | 0,9362 |

No dataset do scikit-learn, `target=1` corresponde a **benign**; portanto Precision, Recall e F1 binários acima consideram benign como classe positiva. `metricas.txt` também apresenta o relatório por classe.

O script gera:

- `arvore_decisao.png`: visualização da árvore;
- `regras.txt`: regras **SE...ENTÃO** extraídas de todos os caminhos raiz-folha;
- `metricas.txt`: Accuracy, Precision, Recall, F1-score e relatório de classificação.

## Execução

```bash
pip install scikit-learn matplotlib
python questao3.py
```
