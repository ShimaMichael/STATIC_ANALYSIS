import re
from ..core.base import SourceAnalyzer, RuleViolation

class FunctionLengthAnalyzer(SourceAnalyzer):
    def __init__(self, max_lines=50):
        self.max_lines = max_lines
        self.func_pattern = re.compile(r'\b(\w+)\s*\([^)]*\)\s*\{', re.DOTALL)

    def analyze(self, content: str) -> list[RuleViolation]:
        violations = []
        for match in self.func_pattern.finditer(content):
            func_name = match.group(1)
            start_pos = match.end() - 1  # Position of opening brace
            end_pos = self._find_brace_end(content, start_pos)
            
            if end_pos == -1:
                continue  # Unclosed brace, skip for now

            line_count = self._count_body_lines(content, start_pos, end_pos)
            if line_count > self.max_lines:
                line_number = content.count('\n', 0, start_pos) + 1
                violations.append(RuleViolation(
                    "FUNCTION_LENGTH",
                    f"Function '{func_name}' exceeds {self.max_lines} lines ({line_count} lines)",
                    location=line_number
                ))
        return violations
