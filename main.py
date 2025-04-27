from pathlib import Path
from core.analyser import CodeAnalyzer
from rules.function_length import FunctionLengthAnalyzer
from rules.unused_function import UnusedFunctionAnalyzer
from rules.switch_break import SwitchBreakAnalyzer
from rules.default_case_position import DefaultCasePositionAnalyzer
from rules.general_rules import MagicNumberAnalyzer

def main():
    analyzer = CodeAnalyzer()
    analyzer.add_rule(FunctionLengthAnalyzer(max_lines=30))
    analyzer.add_rule(UnusedFunctionAnalyzer())
    analyzer.add_rule(SwitchBreakAnalyzer())
    analyzer.add_rule(DefaultCasePositionAnalyzer())
    analyzer.add_rule(MagicNumberAnalyzer())

    test_file = Path("test.cpp")
    if test_file.exists():
        results = analyzer.analyze_file(test_file)
        for violation in results:
            print(f"{test_file}:{violation.line} - {violation.rule_name}: {violation.message}")
    else:
        print(f"File {test_file} not found")

if __name__ == "__main__":
    main()