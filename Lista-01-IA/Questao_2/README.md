# Questão 2 — Árvores geradas computacionalmente

Esta questão reutiliza **exatamente a mesma base ampliada da Questão 1**, presente em `risco_credito_ampliado.csv`.

O script `arvores.py` gera:

- **ID3**, implementado por entropia e ganho de informação;
- **C4.5**, em implementação didática para os atributos categóricos desta atividade, usando Gain Ratio;
- **CART**, usando `DecisionTreeClassifier(criterion="gini")` do scikit-learn após codificação one-hot.

Para cada algoritmo, `resultados.txt` apresenta a **árvore** e a **base de regras SE...ENTÃO** extraída dos caminhos até as folhas.

> O scikit-learn não possui implementação nativa de C4.5. Por isso, a seleção recursiva por Gain Ratio foi implementada no próprio script para os atributos categóricos desta base.

## Execução

```bash
pip install pandas scikit-learn
python arvores.py
```

Saída principal: `resultados.txt`.
