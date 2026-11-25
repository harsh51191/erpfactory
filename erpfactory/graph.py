from collections import deque
from dataclasses import dataclass

@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    relation: str
    evidence: str

def impact(start: str, edges: list[Edge]) -> dict:
    """Edges point from changed object to potentially affected object."""
    visited = {start}
    queue = deque([start])
    evidence = []
    while queue:
        node = queue.popleft()
        for edge in edges:
            if edge.source != node:
                continue
            if not edge.evidence:
                raise ValueError("Dependency lacks evidence")
            evidence.append(edge.evidence)
            if edge.target not in visited:
                visited.add(edge.target)
                queue.append(edge.target)
    return {"affected": sorted(visited - {start}), "evidence": sorted(set(evidence)),
            "coverage": "synthetic-partial", "requires_review": True}
