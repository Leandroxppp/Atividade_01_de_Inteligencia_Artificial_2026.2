import json
from dataclasses import dataclass, field


@dataclass
class KnowledgeBase:
    facts: set[str] = field(default_factory=set)
    rules: list[dict] = field(default_factory=list)

    @staticmethod
    def normalize(text: str) -> str:
        return "_".join(text.strip().lower().split())

    def add_fact(self, fact: str) -> str:
        fact = self.normalize(fact)
        if not fact:
            raise ValueError("O fato não pode ser vazio.")
        self.facts.add(fact)
        return fact

    def add_rule(self, conditions: list[str], conclusion: str) -> dict:
        conditions = [self.normalize(c) for c in conditions if c.strip()]
        conclusion = self.normalize(conclusion)
        if not conditions or not conclusion:
            raise ValueError("A regra precisa de condições e conclusão.")
        rule = {"if": conditions, "then": conclusion}
        if rule not in self.rules:
            self.rules.append(rule)
        return rule

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {"facts": sorted(self.facts), "rules": self.rules},
                f, ensure_ascii=False, indent=2
            )

    @classmethod
    def load(cls, path: str):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        kb = cls()
        kb.facts = set(data.get("facts", []))
        kb.rules = data.get("rules", [])
        return kb


class InferenceEngine:
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
        self.trace: list[dict] = []
        self.questions: list[str] = []

    def reset_trace(self):
        self.trace.clear()
        self.questions.clear()

    def forward(self) -> set[str]:
        self.reset_trace()
        known = set(self.kb.facts)
        changed = True
        while changed:
            changed = False
            for rule in self.kb.rules:
                if all(c in known for c in rule["if"]) and rule["then"] not in known:
                    known.add(rule["then"])
                    self.trace.append({
                        "mode": "forward",
                        "conditions": rule["if"],
                        "conclusion": rule["then"]
                    })
                    changed = True
        return known

    def backward(self, goal: str) -> bool:
        self.reset_trace()
        return self._prove(self.kb.normalize(goal), set())

    def _prove(self, goal: str, visiting: set[str]) -> bool:
        if goal in self.kb.facts:
            self.trace.append({"mode": "fact", "conditions": [], "conclusion": goal})
            return True
        if goal in visiting:
            return False

        visiting = visiting | {goal}
        candidates = [r for r in self.kb.rules if r["then"] == goal]

        for rule in candidates:
            if all(self._prove(cond, visiting.copy()) for cond in rule["if"]):
                self.trace.append({
                    "mode": "backward",
                    "conditions": rule["if"],
                    "conclusion": goal
                })
                return True

        self.questions.append(goal)
        return False

    def mixed(self, goal: str) -> bool:
        goal = self.kb.normalize(goal)
        known = self.forward()
        forward_trace = list(self.trace)
        if goal in known:
            return True

        ok = self._prove(goal, set())
        if ok:
            self.trace = forward_trace + self.trace
        return ok

    def how(self, goal: str) -> list[str]:
        goal = self.kb.normalize(goal)
        lines = []
        for step in self.trace:
            if step["mode"] == "fact":
                lines.append(f"Fato conhecido: {step['conclusion']}")
            elif step["conditions"]:
                lines.append(
                    f"{' E '.join(step['conditions'])}  ->  {step['conclusion']}"
                )
        return list(dict.fromkeys(lines))

    def why_not(self, goal: str) -> list[str]:
        goal = self.kb.normalize(goal)
        rules = [r for r in self.kb.rules if r["then"] == goal]
        if not rules:
            return [f"Não existe regra cuja conclusão seja '{goal}'."]
        known = self.forward()
        missing = []
        for r in rules:
            faltam = [c for c in r["if"] if c not in known]
            if faltam:
                missing.append("Faltaram: " + ", ".join(faltam))
        return missing or ["O objetivo não pôde ser demonstrado com a base atual."]
