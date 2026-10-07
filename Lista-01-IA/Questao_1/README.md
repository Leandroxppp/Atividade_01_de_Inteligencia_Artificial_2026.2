# Questão 1 — Construção manual de árvores de decisão

## (i) Ampliação da base

A base original possui 14 exemplos e 4 atributos preditores. Foram acrescentados os atributos **Emprego** e **Patrimônio** e os exemplos **E15 a E30**, resultando em **30 exemplos e 6 atributos preditores**. A tabela completa está em `risco_credito_ampliado.csv`.

Distribuição da classe na base ampliada: **11 Alto, 10 Baixo e 9 Moderado**.

Atributos preditores: `Historia_Credito`, `Divida`, `Garantia`, `Renda`, `Emprego` e `Patrimonio`. Classe-alvo: `Risco`.

## (ii) Construção manual

### Entropia inicial

A entropia da classe é:

```text
H(S) = - Σ p(c) log2 p(c)
H(S) = 1,5801 bits
```

### ID3 — ganho de informação

Cálculos na raiz:

| Atributo | Ganho de informação |
|---|---:|
| Historia_Credito | 0,3279 |
| Divida | 0,1542 |
| Garantia | 0,2876 |
| Renda | 0,9734 |
| Emprego | 0,9481 |
| **Patrimonio** | **1,2627** |

Portanto, o ID3 escolhe **Patrimônio** como raiz. Aplicando novamente o ganho de informação apenas nos subconjuntos ainda impuros, obtém-se:

```text
Patrimonio?
├── Baixo → Alto
├── Alto → Baixo
└── Medio
    └── Emprego?
        ├── Instavel → Alto
        └── Estavel
            └── Renda?
                ├── 15-35k → Moderado
                └── >35k
                    └── Historia_Credito?
                        ├── Ruim → Moderado
                        └── Boa → Baixo
```

### C4.5 — Gain Ratio

Na raiz, calculando `Gain Ratio = Gain / SplitInfo`:

| Atributo | Gain Ratio |
|---|---:|
| Historia_Credito | 0,2094 |
| Divida | 0,1562 |
| Garantia | 0,3132 |
| Renda | 0,6282 |
| **Emprego** | **1,0000** |
| Patrimonio | 0,7991 |

Assim, o C4.5 escolhe **Emprego** como raiz. A continuação recursiva produz:

```text
Emprego?
├── Instavel → Alto
└── Estavel
    └── Patrimonio?
        ├── Alto → Baixo
        └── Medio
            └── Renda?
                ├── 15-35k → Moderado
                └── >35k
                    └── Historia_Credito?
                        ├── Ruim → Moderado
                        └── Boa → Baixo
```

### CART — índice Gini

A impureza inicial é `Gini(S) = 0,6644`. Considerando divisões binárias do tipo valor versus demais valores, as melhores reduções de Gini na raiz são:

| Atributo | Melhor teste | Redução de Gini |
|---|---|---:|
| Historia_Credito | Boa vs. demais | 0,0959 |
| Divida | Alta vs. demais | 0,0717 |
| Garantia | Adequada vs. demais | 0,1011 |
| Renda | >35k vs. demais | 0,2681 |
| **Emprego** | **Estavel vs. Instavel** | **0,3487** |
| Patrimonio | Baixo vs. demais | 0,3011 |

Logo, o primeiro corte do CART é **Emprego = Instável?**. Continuando com o menor Gini ponderado em cada subconjunto:

```text
Emprego = Instavel?
├── SIM → Alto
└── NÃO (Estavel)
    └── Patrimonio = Medio?
        ├── NÃO (Alto) → Baixo
        └── SIM
            └── Renda = 15-35k?
                ├── SIM → Moderado
                └── NÃO (>35k)
                    └── Historia_Credito = Boa?
                        ├── SIM → Baixo
                        └── NÃO (Ruim) → Moderado
```

## (iii) Bases de conhecimento — regras SE...ENTÃO

### Regras do ID3

1. SE Patrimonio = Baixo ENTÃO Risco = Alto.
2. SE Patrimonio = Alto ENTÃO Risco = Baixo.
3. SE Patrimonio = Medio E Emprego = Instavel ENTÃO Risco = Alto.
4. SE Patrimonio = Medio E Emprego = Estavel E Renda = 15-35k ENTÃO Risco = Moderado.
5. SE Patrimonio = Medio E Emprego = Estavel E Renda = >35k E Historia_Credito = Ruim ENTÃO Risco = Moderado.
6. SE Patrimonio = Medio E Emprego = Estavel E Renda = >35k E Historia_Credito = Boa ENTÃO Risco = Baixo.

### Regras do C4.5

1. SE Emprego = Instavel ENTÃO Risco = Alto.
2. SE Emprego = Estavel E Patrimonio = Alto ENTÃO Risco = Baixo.
3. SE Emprego = Estavel E Patrimonio = Medio E Renda = 15-35k ENTÃO Risco = Moderado.
4. SE Emprego = Estavel E Patrimonio = Medio E Renda = >35k E Historia_Credito = Ruim ENTÃO Risco = Moderado.
5. SE Emprego = Estavel E Patrimonio = Medio E Renda = >35k E Historia_Credito = Boa ENTÃO Risco = Baixo.

### Regras do CART

1. SE Emprego = Instavel ENTÃO Risco = Alto.
2. SE Emprego = Estavel E Patrimonio != Medio ENTÃO Risco = Baixo.
3. SE Emprego = Estavel E Patrimonio = Medio E Renda = 15-35k ENTÃO Risco = Moderado.
4. SE Emprego = Estavel E Patrimonio = Medio E Renda != 15-35k E Historia_Credito != Boa ENTÃO Risco = Moderado.
5. SE Emprego = Estavel E Patrimonio = Medio E Renda != 15-35k E Historia_Credito = Boa ENTÃO Risco = Baixo.

## (iv) Comparação e escolha

| Algoritmo | Critério | Tipo de divisão | Nº de regras | Observação |
|---|---|---|---:|---|
| ID3 | Ganho de informação | múltipla | 6 | simples e interpretável |
| C4.5 | Gain Ratio | múltipla | 5 | regras compactas e diretamente legíveis |
| CART | Índice Gini | binária | 5 | usa testes binários e pode introduzir negações |

Para esta base, escolho a base de regras do **C4.5**. Ela obteve uma representação compacta, com cinco regras, e mantém condições categóricas fáceis de interpretar. Além disso, o Gain Ratio corrige a tendência do ganho de informação de favorecer atributos apenas por produzirem muitas partições.

> Os cálculos e árvores desta questão correspondem exatamente à base `risco_credito_ampliado.csv`, que também é reutilizada na Questão 2.
