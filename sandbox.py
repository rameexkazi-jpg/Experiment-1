#!/usr/bin/env python3
"""Simple Python sandbox for running basic scripts safely."""

import subprocess
import sys
import tempfile
import os
from pathlib import Path
from typing import Tuple, Optional


class PythonSandbox:
    """Run Python code in an isolated subprocess with timeout and output capture."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def run_code(self, code: str) -> Tuple[str, str, int]:
        """
        Execute Python code and return output, errors, and exit code.

        Args:
            code: Python code to execute as a string

        Returns:
            Tuple of (stdout, stderr, return_code)
        """
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return '', f'Error: Script exceeded timeout of {self.timeout}s', 124
        except Exception as e:
            return '', f'Error: {str(e)}', 1
        finally:
            os.unlink(temp_file)

    def run_file(self, filepath: str) -> Tuple[str, str, int]:
        """Execute a Python file and return output, errors, and exit code."""
        if not os.path.exists(filepath):
            return '', f'Error: File not found: {filepath}', 1

        with open(filepath, 'r') as f:
            code = f.read()

        return self.run_code(code)


def main():
    """CLI interface for the sandbox."""
    if len(sys.argv) < 2:
        print("Usage: python sandbox.py <script.py> [timeout_seconds]")
        print("   or: python sandbox.py -c '<code>' [timeout_seconds]")
        sys.exit(1)

    timeout = 10

    if sys.argv[1] == '-c':
        if len(sys.argv) < 3:
            print("Error: -c requires code argument")
            sys.exit(1)
        code = sys.argv[2]
        if len(sys.argv) > 3:
            timeout = int(sys.argv[3])
    else:
        filepath = sys.argv[1]
        if len(sys.argv) > 2:
            timeout = int(sys.argv[2])

        if not os.path.exists(filepath):
            print(f"Error: File not found: {filepath}")
            sys.exit(1)

        with open(filepath, 'r') as f:
            code = f.read()

    sandbox = PythonSandbox(timeout=timeout)
    stdout, stderr, returncode = sandbox.run_code(code)

    if stdout:
        print(stdout, end='')
    if stderr:
        print(stderr, end='', file=sys.stderr)

    sys.exit(returncode)


if __name__ == '__main__':
    main()
