import re
from ..core.base import SourceAnalyzer, RuleViolation

class MagicNumberAnalyzer(SourceAnalyzer):
    def analyze(self, content: str) -> list[RuleViolation]:
        violations = []
        numbers = re.finditer(r'\b\d+\b', content)
        for num in numbers:
            if not self._is_constant(content, num.start()):
                line = content[:num.start()].count('\n') + 1
                violations.append(RuleViolation(
                    "MAGIC_NUMBER",
                    f"Magic number detected: {num.group(0)}",
                    line
                ))
        return violations

    def _is_constant(self, content: str, pos: int) -> bool:
        # Check if number is part of constant definition
        prev_text = content[:pos].rsplit(None, 1)[-1]
        return prev_text in {'#define', 'const', '='}