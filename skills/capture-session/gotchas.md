# Gotchas

- **Logging routine work as conceptual shifts**: Not every session has shifts. If the operator built three files and made no new discoveries, capture-session has nothing to capture. Don't force evolution entries from implementation sessions — that inflates the evolution log with non-shifts and makes it harder to find real ones later.

- **Cleaning too aggressively**: The transcript cleaner should fix grammar and strip tool dumps, not rewrite what the operator said. The operator's reasoning, hesitations, and self-corrections are often where the real insight lives. "Wait, actually..." followed by a pivot is a shift marker, not noise to clean.

- **Updating research-state.yaml without evolution.md**: Never update the state file without a corresponding evolution entry. The state says *what you believe now*. The evolution log says *why you changed your mind*. State without provenance is a future "why does it say this?" question with no answer.
