import re
import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.base import SourceAnalyzer, RuleViolation

class FunctionLengthAnalyzer(SourceAnalyzer):
   def __init__(self, max_lines=50):
       self.max_lines = max_lines
       self.func_pattern = re.compile(
           r'\b([a-zA-Z_][a-zA-Z0-9_:]*)\s*\(([^)]*)\)\s*\{',
           re.DOTALL
       )
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
   def _find_brace_end(self, content: str, start_pos: int) -> int:
       depth = 1
       pos = start_pos + 1
       while pos < len(content) and depth > 0:
           if content[pos] == '{':
               depth += 1
           elif content[pos] == '}':
               depth -= 1
           pos += 1
       return pos - 1 if depth == 0 else -1
   def _count_body_lines(self, content: str, start: int, end: int) -> int:
       body = content[start:end+1]
       return body.count('\n') + 1  # Include last line