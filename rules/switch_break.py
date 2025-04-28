import re
import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.base import SourceAnalyzer, RuleViolation

class SwitchBreakAnalyzer(SourceAnalyzer):
    def analyze(self, content: str) -> list[RuleViolation]:
        violations = []
        switch_blocks = re.finditer(r'\bswitch\s*\([^)]+\)\s*\{([^}]+)\}', content, re.DOTALL)
        
        for switch in switch_blocks:
            cases = re.finditer(r'(case\s+.+?:|default\s*:)([^}]*)', switch.group(1))
            for case in cases:
                if not re.search(r'\b(break|return|exit)\s*;', case.group(2)):
                    line = content[:switch.start()].count('\n') + 1
                    violations.append(RuleViolation(
                        "MISSING_BREAK",
                        f"Switch case missing break/return/exit",
                        line
                    ))
        return violations