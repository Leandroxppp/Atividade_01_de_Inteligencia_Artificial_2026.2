# Questão 5 — Shell Genérico para Sistemas Baseados em Conhecimento

O programa implementa uma infraestrutura genérica para construção e consulta de bases de conhecimento. **Nenhum domínio é fixado no código**: os fatos e regras são cadastrados pelo usuário ou carregados de um arquivo JSON.

## Funcionalidades

- editor de fatos;
- editor de regras `SE ... ENTÃO ...`;
- encadeamento para frente (Forward Chaining);
- encadeamento para trás (Backward Chaining);
- encadeamento misto;
- mecanismo de explicação **COMO?** quando uma hipótese é comprovada;
- mecanismo de explicação **POR QUÊ?** quando uma hipótese não pode ser comprovada;
- visualização da base;
- salvar e carregar bases em JSON;
- interface textual interativa.

## Execução

No terminal, dentro da pasta `Questao_5`:

```bash
python app.py
```

No Windows também pode ser usado:

```bash
py app.py
```

## Exemplo de teste

Cadastre os fatos:

```text
animal tem pelos
animal amamenta
```

Depois cadastre:

```text
SE: animal tem pelos; animal amamenta
ENTÃO: animal e mamifero
```

Consulte a hipótese `animal e mamifero`. O sistema deverá confirmá-la e apresentar a trilha utilizada na explicação **COMO?**.

Para demonstrar **POR QUÊ?**, consulte uma hipótese que não possa ser provada com os fatos e regras disponíveis.

## Arquivos

- `app.py`: interface e editor da base.
- `engine.py`: representação da BC e mecanismos de inferência/explicação.
- `bc_exemplo.json`: pequena BC apenas para demonstração.

A separação entre interface, base e motor permite utilizar o mesmo shell em outros domínios sem alterar sua infraestrutura.
