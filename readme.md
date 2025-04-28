
---

# Static Code Analyzer for C/C++

A modular static analysis tool for enforcing code quality rules in C/C++ projects, inspired by LDRA-style guidelines. Designed for extensibility and incremental rule implementation.

## Features

### Current Rule Set
1. **Function Length Check**  
   - Warns when functions exceed configured line count threshold
   - Configurable maximum line limit (default: 50)

2. **Switch Statement Validation**  
   - Detects missing `break`/`return`/`exit` in case statements  
   - Ensures `default` case is last in switch blocks

3. **Code Quality Checks**  
   - Identifies unused functions within files  
   - Detects magic numbers without constant definitions

4. **Extensible Architecture**  
   - Easy to add new rules through modular structure  
   - Clear separation between analysis logic and reporting

## Installation

### Requirements
- Python 3.6+
- Tested on Windows/Linux/macOS

### Setup
```bash
git clone https://github.com/ShimaMichael/STATIC_ANALYSIS.git
cd static-analyzer
```

## Usage

### Basic Analysis
```bash
python main.py path/to/source.cpp
```

### Example Output
```
test.cpp:42 - FUNCTION_LENGTH: Function 'calculate_metrics' exceeds 30 lines (47 lines)
test.cpp:15 - MISSING_BREAK: Switch case missing break/return/exit
test.cpp:87 - MAGIC_NUMBER: Magic number detected: 42
```

## Configuration

Modify `main.py` to configure rules:
```python
analyzer.add_rule(FunctionLengthAnalyzer(max_lines=30))  # Custom threshold
analyzer.add_rule(MagicNumberAnalyzer())                 # Enable magic number detection
```

## Project Structure

```
static-analyzer/
├── core/              # Framework components
│   ├── base.py        # Base classes and interfaces
│   └── analyzer.py    # Analysis coordination logic
│
├── rules/             # Rule implementations
│   ├── function_rules.py  # Function-related checks
│   ├── switch_rules.py    # Switch statement validation
│   └── general_rules.py   # General code quality rules
│
└── main.py            # Entry point and rule configuration
```

## Extending the Tool

### Creating New Rules

1. Create new analyzer class in appropriate rules file:
```python
class NewCustomRule(SourceAnalyzer):
    def __init__(self, parameters):
        # Initialize rule configuration
        
    def analyze(self, content: str) -> list[RuleViolation]:
        # Implement analysis logic
        return []
```

2. Register rule in `main.py`:
```python
analyzer.add_rule(NewCustomRule(config_params))
```

### Example Rule Template
```python
class ExampleAnalyzer(SourceAnalyzer):
    def __init__(self, threshold=5):
        self.threshold = threshold
        self.pattern = re.compile(r'some_pattern')

    def analyze(self, content: str) -> list[RuleViolation]:
        violations = []
        # Analysis logic here
        return violations
```

## Limitations

1. **Parser Limitations**  
   - Uses regex-based parsing instead of full AST  
   - May struggle with:  
     * Complex template metaprogramming  
     * Macros and preprocessor directives  
     * Nested code structures  

2. **Scope Detection**  
   - Function usage tracking is file-level only  
   - No cross-file analysis

3. **Error Handling**  
   - Basic error reporting  
   - No suppression comments support

For production use, consider integrating with:
- LLVM/Clang AST parsing
- Preprocessor handling
- Cross-file analysis

## Contributing

1. Fork the repository  
2. Create feature branch (`git checkout -b new-feature`)  
3. Commit changes  
4. Push to branch  
5. Create new Pull Request
