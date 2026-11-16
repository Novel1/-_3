from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Optional


@dataclass
class Rule:
    name: str
    conditions: Dict[str, Any]           
    conclusions: Dict[str, Any]          
    explanation: str                     
    priority: int = 0                     

    def matches(self, facts: Dict[str, Any]) -> bool:
        for key, expected in self.conditions.items():
            if facts.get(key) != expected:
                return False
    
        if all(facts.get(k) == v for k, v in self.conclusions.items()):
            return False
        return True


@dataclass
class FiredRule:
    rule_name: str
    explanation: str
    new_facts: Dict[str, Any]


class InferenceEngine:

    def __init__(self, rules: List[Rule]):
        self.rules = sorted(rules, key=lambda r: -r.priority)
        self.trace: List[FiredRule] = []

    def run(self, initial_facts: Dict[str, Any], max_iterations: int = 100) -> Dict[str, Any]:
        facts = dict(initial_facts)
        self.trace = []
        for _ in range(max_iterations):
            fired_any = False
            for rule in self.rules:
                if rule.matches(facts):
                    facts.update(rule.conclusions)
                    self.trace.append(FiredRule(rule.name, rule.explanation, dict(rule.conclusions)))
                    fired_any = True
            if not fired_any:
                break
        return facts

    def explain(self) -> str:
        if not self.trace:
            return 
        lines = []
        for i, fr in enumerate(self.trace, 1):
            lines.append(f"{i}. Правило «{fr.rule_name}»: {fr.explanation} "
                         f"→ выведено: {fr.new_facts}")
        return "\n".join(lines)
