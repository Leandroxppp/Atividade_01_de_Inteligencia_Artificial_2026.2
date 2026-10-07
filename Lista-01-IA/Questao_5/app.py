import os
from engine import KnowledgeBase, InferenceEngine

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
GRAY = "\033[90m"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def title(text):
    print(f"\n{CYAN}{BOLD}{'═' * 66}{RESET}")
    print(f"{CYAN}{BOLD}  {text}{RESET}")
    print(f"{CYAN}{BOLD}{'═' * 66}{RESET}")

def pause():
    input(f"\n{GRAY}Pressione ENTER para voltar ao menu...{RESET}")

def pretty(text):
    return text.replace("_", " ")

def banner():
    clear()
    print(f"""{CYAN}{BOLD}
╔════════════════════════════════════════════════════════════════╗
║             SHELL DE SISTEMA BASEADO EM CONHECIMENTO          ║
║                Lista 01 — Inteligência Artificial              ║
╚════════════════════════════════════════════════════════════════╝{RESET}
{GRAY}Base genérica • Regras SE–ENTÃO • Inferência • Explicações{RESET}
""")

def menu(kb):
    print(f"{BLUE}{BOLD} BASE DE CONHECIMENTO{RESET}")
    print(f" {GREEN}●{RESET} {len(kb.facts)} fato(s)    {YELLOW}●{RESET} {len(kb.rules)} regra(s)\n")
    print(f" {BOLD}1{RESET}  Adicionar fato")
    print(f" {BOLD}2{RESET}  Adicionar regra SE–ENTÃO")
    print(f" {BOLD}3{RESET}  Encadeamento para frente  {GRAY}(Forward Chaining){RESET}")
    print(f" {BOLD}4{RESET}  Encadeamento para trás     {GRAY}(Backward Chaining){RESET}")
    print(f" {BOLD}5{RESET}  Encadeamento misto")
    print(f" {BOLD}6{RESET}  Consultar hipótese + explicação")
    print(f" {BOLD}7{RESET}  Visualizar base de conhecimento")
    print(f" {BOLD}8{RESET}  Salvar base")
    print(f" {BOLD}9{RESET}  Carregar base")
    print(f" {BOLD}0{RESET}  Sair")

def add_fact(kb):
    title("EDITOR DA BASE — NOVO FATO")
    print("Exemplo: animal tem pelos")
    fact = input("\nDigite o fato: ")
    try:
        f = kb.add_fact(fact)
        print(f"\n{GREEN}✓ Fato adicionado:{RESET} {pretty(f)}")
    except ValueError as e:
        print(f"\n{RED}✗ {e}{RESET}")
    pause()

def add_rule(kb):
    title("EDITOR DA BASE — NOVA REGRA")
    print("Informe as condições separadas por ponto e vírgula.")
    print(f"{GRAY}Ex.: animal tem pelos; animal amamenta{RESET}")
    conditions = input("\nSE: ").split(";")
    conclusion = input("ENTÃO: ")
    try:
        r = kb.add_rule(conditions, conclusion)
        print(f"\n{GREEN}✓ Regra cadastrada com sucesso!{RESET}")
        print(f"{BOLD}SE{RESET} " + " E ".join(pretty(x) for x in r["if"]))
        print(f"{BOLD}ENTÃO{RESET} {pretty(r['then'])}")
    except ValueError as e:
        print(f"\n{RED}✗ {e}{RESET}")
    pause()

def forward(kb):
    title("FORWARD CHAINING — ENCADEAMENTO PARA FRENTE")
    e = InferenceEngine(kb)
    known = e.forward()
    inferred = sorted(known - kb.facts)
    print(f"{BOLD}Fatos iniciais:{RESET}")
    for f in sorted(kb.facts):
        print(f"  • {pretty(f)}")
    print(f"\n{BOLD}Novas conclusões inferidas:{RESET}")
    if inferred:
        for f in inferred:
            print(f"  {GREEN}→ {pretty(f)}{RESET}")
    else:
        print(f"  {GRAY}Nenhuma nova conclusão foi produzida.{RESET}")
    if e.trace:
        print(f"\n{BOLD}Raciocínio utilizado:{RESET}")
        for i, s in enumerate(e.trace, 1):
            print(f"  {i}. {' E '.join(pretty(x) for x in s['conditions'])} → {pretty(s['conclusion'])}")
    pause()

def query(kb, mode):
    names = {"backward":"BACKWARD CHAINING", "mixed":"ENCADEAMENTO MISTO", "query":"CONSULTA E EXPLICAÇÃO"}
    title(names[mode])
    goal = input("Qual hipótese deseja verificar? ")
    e = InferenceEngine(kb)
    ok = e.backward(goal) if mode in ("backward","query") else e.mixed(goal)

    print("\n" + "─" * 66)
    if ok:
        print(f"{GREEN}{BOLD}✓ HIPÓTESE CONFIRMADA{RESET}: {pretty(kb.normalize(goal))}")
        print(f"\n{CYAN}{BOLD}COMO?{RESET}")
        steps = e.how(goal)
        if steps:
            for i, step in enumerate(steps, 1):
                print(f"  {i}. {pretty(step)}")
        else:
            print("  A hipótese já consta como fato conhecido.")
    else:
        print(f"{RED}{BOLD}✗ HIPÓTESE NÃO COMPROVADA{RESET}: {pretty(kb.normalize(goal))}")
        print(f"\n{YELLOW}{BOLD}POR QUÊ?{RESET}")
        for reason in e.why_not(goal):
            print(f"  • {pretty(reason)}")
    pause()

def show_kb(kb):
    title("BASE DE CONHECIMENTO")
    print(f"{GREEN}{BOLD}FATOS{RESET}")
    if not kb.facts:
        print(f"  {GRAY}(nenhum fato cadastrado){RESET}")
    for i, f in enumerate(sorted(kb.facts), 1):
        print(f"  F{i}: {pretty(f)}")

    print(f"\n{YELLOW}{BOLD}REGRAS{RESET}")
    if not kb.rules:
        print(f"  {GRAY}(nenhuma regra cadastrada){RESET}")
    for i, r in enumerate(kb.rules, 1):
        cond = " E ".join(pretty(c) for c in r["if"])
        print(f"  R{i}: SE {cond} ENTÃO {pretty(r['then'])}")
    pause()

def save(kb):
    title("SALVAR BASE DE CONHECIMENTO")
    path = input("Nome do arquivo [bc.json]: ").strip() or "bc.json"
    try:
        kb.save(path)
        print(f"\n{GREEN}✓ Base salva em '{path}'.{RESET}")
    except OSError as e:
        print(f"\n{RED}✗ Não foi possível salvar: {e}{RESET}")
    pause()

def load():
    title("CARREGAR BASE DE CONHECIMENTO")
    path = input("Nome do arquivo [bc.json]: ").strip() or "bc.json"
    try:
        kb = KnowledgeBase.load(path)
        print(f"\n{GREEN}✓ Base carregada: {len(kb.facts)} fato(s), {len(kb.rules)} regra(s).{RESET}")
        pause()
        return kb
    except (OSError, ValueError) as e:
        print(f"\n{RED}✗ Não foi possível carregar: {e}{RESET}")
        pause()
        return None

def main():
    kb = KnowledgeBase()
    while True:
        banner()
        menu(kb)
        op = input(f"\n{CYAN}Escolha uma opção › {RESET}").strip()

        if op == "1": add_fact(kb)
        elif op == "2": add_rule(kb)
        elif op == "3": forward(kb)
        elif op == "4": query(kb, "backward")
        elif op == "5": query(kb, "mixed")
        elif op == "6": query(kb, "query")
        elif op == "7": show_kb(kb)
        elif op == "8": save(kb)
        elif op == "9":
            loaded = load()
            if loaded is not None: kb = loaded
        elif op == "0":
            clear()
            print(f"{GREEN}{BOLD}Shell encerrado. Até mais!{RESET}\n")
            break
        else:
            print(f"\n{RED}Opção inválida.{RESET}")
            pause()

if __name__ == "__main__":
    main()
