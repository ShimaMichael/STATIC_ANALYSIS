import re
from ..core.base import SourceAnalyzer, RuleViolation

class UnusedFunctionAnalyzer(SourceAnalyzer):
    def __init__(self):
        self.func_pattern = re.compile(r'\b(\w+)\s*\([^)]*\)\s*\{', re.DOTALL)
        
    def analyze(self, content: str) -> list[RuleViolation]:
        violations = []
        functions = set(m.group(1) for m in self.func_pattern.finditer(content))
        called_functions = set(re.findall(r'\b(\w+)\s*\(', content))
        
        for func in functions - called_functions:
            if func != 'main':
                violations.append(RuleViolation(
                    "UNUSED_FUNCTION",
                    f"Function '{func}' is defined but never used",
                    self._find_line_number(content, func)
                ))
        return violations

    def _find_line_number(self, content: str, func_name: str) -> int:
        return content[:content.index(func_name)].count('\n') + 1