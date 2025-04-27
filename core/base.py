from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class RuleViolation:
    rule_name: str
    message: str
    line: int = 0

class SourceAnalyzer(ABC):
    @abstractmethod
    def analyze(self, content: str) -> list[RuleViolation]:
        pass