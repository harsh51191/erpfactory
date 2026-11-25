from pathlib import Path
import sys
root=Path(__file__).resolve().parents[1]
for source in (root/"vendors/sap/skills").glob("*/SKILL.md"):
    for dest_root in (".agents/skills",".claude/skills"):
        target=root/dest_root/source.parent.name/"SKILL.md"
        if "--check" in sys.argv:
            if not target.exists() or target.read_bytes()!=source.read_bytes():
                raise SystemExit(f"Out of sync: {target}")
        else:
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(source.read_bytes())
