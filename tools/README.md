# Tools — Worked Examples & Reference Implementations

Reference implementations for concepts that are easier to understand with running code than prose.

---

## invariant-examples/

### idempotent-webhook/

A complete worked example of an idempotent webhook receiver with invariant tests.

**The invariant:** processing the same webhook twice must produce exactly one side effect.

This is the kind of test the Quality Gates chapter describes in Tier 2 — not checking whether a specific input produces a specific output, but checking whether a *property* holds for *all* inputs. The test generates random payloads and verifies the invariant holds across every one of them.

Use this as a starting point for writing invariant tests on your own critical paths. The three questions to ask: What must never happen twice? What must always be true after this operation completes? What breaks if operations run out of order?

---

## Contributing

If you have a worked example of an invariant test, contract gate, or policy check that others could learn from, contributions are welcome. Each example should be self-contained with its own README explaining the invariant being tested and how to run it.
