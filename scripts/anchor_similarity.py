"""Compute anchor similarity between two observation sets."""
from ai_identity.anchor_detection import detect_anchors
import sys


def parse_obs(text: str) -> list[str]:
    return text.split()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit("usage: anchor_similarity.py seqA seqB")
    anchors_a = set(detect_anchors(parse_obs(sys.argv[1])))
    anchors_b = set(detect_anchors(parse_obs(sys.argv[2])))
    union = anchors_a | anchors_b
    score = len(anchors_a & anchors_b) / len(union) if union else 1.0
    print(score)
