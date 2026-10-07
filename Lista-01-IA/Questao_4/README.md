# Questão 4 — Geração direta de regras com PRISM

Foi utilizada **a mesma base e a mesma divisão treino/teste da Questão 3**: Breast Cancer Wisconsin Diagnostic, com 80% para treino, 20% para teste, `random_state=42` e estratificação.

Como o PRISM trabalha naturalmente com atributos categóricos, os 30 atributos contínuos são discretizados em três faixas (`baixo`, `medio`, `alto`) usando tercis calculados **somente no conjunto de treinamento**, evitando vazamento de informação.

O `prism.py` implementa a indução direta de regras: para cada classe, escolhe sucessivamente a condição `atributo = valor` de maior precisão para a classe-alvo até formar uma regra; os positivos cobertos são então retirados e o processo continua.

Na execução validada, foram geradas **37 regras** e obtidos:

| Métrica | Resultado |
|---|---:|
| Accuracy | 0,9474 |
| Precision | 0,9583 |
| Recall | 0,9583 |
| F1-score | 0,9583 |

Arquivos produzidos:

- `regras_prism.txt`: base de regras gerada diretamente pelo PRISM;
- `metricas_prism.txt`: métricas e relatório de classificação.

## Execução

```bash
pip install scikit-learn numpy
python prism.py
```
