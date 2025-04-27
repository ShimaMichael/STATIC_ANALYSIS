import re
from ..core.base import SourceAnalyzer, RuleViolation

class DefaultCasePositionAnalyzer(SourceAnalyzer):
    def analyze(self, content: str) -> list[RuleViolation]:
        violations = []
        switches = re.finditer(r'\bswitch\s*\([^)]+\)\s*\{([^}]+)\}', re.DOTALL)
        
        for switch in switches:
            cases = list(re.finditer(r'(case\s|default\s*:).+?(?=case\s|default\s*:|$)', 
                                   switch.group(1), re.DOTALL))
            default_pos = [i for i,c in enumerate(cases) if 'default' in c.group(0)]
            
            if default_pos and default_pos[0] != len(cases)-1:
                line = content[:switch.start()].count('\n') + 1
                violations.append(RuleViolation(
                    "DEFAULT_NOT_LAST",
                    "Default case is not the last in switch statement",
                    line
                ))
        return violations