"""Count refusal statements in responses."""
import sys

REFUSAL_PHRASES = ["i refuse", "cannot comply", "sorry, can't"]


def count_refusals(responses: list[str]) -> int:
    total = 0
    for response in responses:
        lower = response.lower()
        for phrase in REFUSAL_PHRASES:
            if phrase in lower:
                total += 1
                break
    return total


if __name__ == "__main__":
    print(count_refusals(sys.argv[1:]))
