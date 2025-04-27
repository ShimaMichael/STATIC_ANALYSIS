from pathlib import Path
from .base import SourceAnalyzer, RuleViolation

class CodeAnalyzer:
    def __init__(self):
        self.analyzers: list[SourceAnalyzer] = []

    def add_rule(self, analyzer: SourceAnalyzer):
        self.analyzers.append(analyzer)

    def analyze_file(self, file_path: Path) -> list[RuleViolation]:
        content = file_path.read_text()
        return [violation 
                for analyzer in self.analyzers 
                for violation in analyzer.analyze(content)]