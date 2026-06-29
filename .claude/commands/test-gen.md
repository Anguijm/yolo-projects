---
scope: global
---
Usage: `/test-gen <path>` or `/test-gen <path>::<func_name>`

Generate pytest cases for the target file or function provided in the
argument.

Steps:

1. Read the target file. If a specific function was named, only test that
   function; otherwise test every public function.
2. For each function, generate test cases covering:
   - The happy path with typical input.
   - One degenerate case (empty / zero / None / single-element).
   - One boundary case (max length, very large value, negative).
   - One error case (invalid input → expected exception).
3. Place the tests in `tests/test_<module_name>.py`. Create the `tests/`
   directory if it doesn't exist. Add an empty `tests/__init__.py` if absent.
4. Use plain `assert` statements (not `unittest.TestCase` methods).
5. Run `pytest tests/test_<module_name>.py -v` and report whether the new
   tests pass against the existing implementation. If a generated test fails
   because of a real bug in the target, surface that as a finding rather
   than rewriting the test to pass.

Do not modify the target file. Tests only.
