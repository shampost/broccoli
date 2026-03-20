# Broccoli

Broccoli is a small, educational interpreter for a toy language called **Broccoli Lang**. The goal of the project is to explore how programming languages work end-to-end: turning text into tokens, parsing those tokens into an abstract syntax tree (AST), and evaluating the AST to produce results.

## What Broccoli Lang supports (so far)

### Values
- Integers and floats
- Boolean literals: `True`, `False`

### Expressions
- Arithmetic: `+`, `-`, `*`, `/`
- Unary minus: `-x`
- Parentheses for grouping: `( ... )`

### Variables
- Declare a variable with `var`:
  - `var x = 10`
- Reassign an existing variable:
  - `x = x + 1`

### Comparisons and boolean logic
- Comparisons: `<`, `<=`, `>`, `>=`, `==`
- Boolean operators:
  - `&` (and)
  - `|` (or)
  - `!` (not)

### Control flow
- `if` blocks with curly braces:
  ```text
  if (x > 0) {
      print x
  }
  ```
- `while` loops with curly braces:
  ```text
  while (x < 5) {
      x = x + 1
  }
  ```

### Output
- `print` evaluates an expression and outputs its value:
  - `print x`

## Example program

```text
var a = 0
var b = 12
var c = 123

if (a < 5 & b > 10) {
    print c
}
```

## Notes / limitations

This is a work-in-progress learning project, and the language is intentionally small.

- Identifiers are currently limited to alphabetic characters.
- Error handling exists for invalid characters, invalid tokens, and mismatched brackets, but messages and recovery are still evolving.
- Semantics (especially around blocks and scope) may change as the language grows.

## License

MIT