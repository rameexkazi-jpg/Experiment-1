# Python Script Sandbox

A lightweight, isolated sandbox for running Python scripts with timeout protection.

## Features

- ✅ Run Python code in an isolated subprocess
- ✅ Automatic timeout (default 10s) to prevent infinite loops
- ✅ Output and error capture
- ✅ Simple CLI and programmatic API
- ✅ No external dependencies beyond Python stdlib

## Usage

### Command Line

Run a Python file:
```bash
python sandbox.py examples/hello.py
```

Run with custom timeout (30 seconds):
```bash
python sandbox.py examples/fibonacci.py 30
```

Run code directly with `-c`:
```bash
python sandbox.py -c "print('Hello'); print(1 + 1)"
```

### Python API

```python
from sandbox import PythonSandbox

sandbox = PythonSandbox(timeout=10)

# Run code string
stdout, stderr, returncode = sandbox.run_code("print('Hello')")
print(stdout)  # "Hello\n"

# Run a file
stdout, stderr, returncode = sandbox.run_file("examples/hello.py")
print(stdout)
```

## Examples

See `examples/` folder:
- `hello.py` - Basic print and math
- `fibonacci.py` - Function and recursion

## Behavior

- **Timeout**: Scripts exceeding the timeout are terminated (default 10s)
- **Output**: All stdout/stderr is captured and returned
- **Errors**: Runtime errors are captured in stderr
- **Exit codes**: Preserved from the executed script
