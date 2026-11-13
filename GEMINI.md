# Project Coding & Behavioral Rules (Karpathy Guidelines)

Derived from Andrej Karpathy's core principles to avoid common LLM pitfalls:

## 1. Think Before Coding
- **Don't assume. Don't hide confusion. Surface tradeoffs.**
- State assumptions explicitly. If uncertain or multiple interpretations exist, ask or present them.
- If a simpler approach exists, propose it. Push back on unnecessary complexity.
- If something is unclear, stop, name what is confusing, and clarify.

## 2. Simplicity First
- **Minimum code that solves the problem. Nothing speculative.**
- No unrequested features or premature abstractions for single-use logic.
- No unrequested "configurability" or defensive code for impossible scenarios.
- Prefer 50 clear, direct lines over 200 lines of indirection.

## 3. Surgical Changes
- **Touch only what you must. Clean up only your own mess.**
- Do not touch, "clean up", or reformat unrelated adjacent code, comments, or imports.
- Match existing project style, conventions, and patterns.
- Remove only imports, variables, or functions that your own edit made obsolete.

## 4. Goal-Driven Execution
- **Define success criteria and verify.**
- Formulate each fix or feature with a verifiable goal (test case, API check, or build validation).
- Verify every change end-to-end before considering it done.

