from dataclasses import dataclass

@dataclass(frozen=True)
class Grant:
    environment: str
    actions: frozenset[str]
    approved: bool = False

def authorize(grant: Grant, environment: str, action: str) -> None:
    if environment != "synthetic" or grant.environment != environment:
        raise PermissionError("Only synthetic environment supported")
    if not grant.approved or action not in grant.actions:
        raise PermissionError("No scoped grant")
    if action not in {"pr.read", "pr.update"}:
        raise PermissionError("Unsupported action")
