#!/usr/bin/env python3
"""공용 자산 사본 동기화 및 검증.

정본은 저장소 최상위의 shared/ 입니다. 각 페르소나 폴더의 shared/ 는 사본이며
항상 정본과 같아야 합니다.

PERSONAS 목록의 폴더에 SKILL.md가 없으면 그 이름을 출력하고 중단합니다. 목록에 오타가
있을 때 SKILL.md가 없는 빈 폴더가 조용히 생기고 배포 압축 파일에까지 들어가는 것을 막습니다.

사용법:
    python3 docs/tools/sync_shared.py            사본을 정본에 맞춰 갱신합니다
    python3 docs/tools/sync_shared.py --check    갱신하지 않고 일치 여부만 확인합니다
"""
import hashlib
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "shared"
ASSETS = ["universal-rules.md", "universal-anti-patterns.md", "output-templates.md"]
PERSONAS = [
    "orchestrator",
    "s1-accounting-reviewer",
    "s2-external-audit-responder",
    "s3-tax-reviewer",
    "s4-capital-market-disclosure-reviewer",
    "s5-fair-trade-reviewer",
    "s6-treasury-reviewer",
    "s7-real-estate-finance-reviewer",
    "s8-legal-issue-reviewer",
    "s9-management-planning-reviewer",
    "s10-internal-accounting-control-reviewer",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    check_only = "--check" in sys.argv
    mismatched, updated = [], []

    missing = [p for p in PERSONAS if not (ROOT / p / "SKILL.md").exists()]
    if missing:
        print("페르소나 폴더가 없거나 SKILL.md가 없습니다 %d건" % len(missing))
        for name in missing:
            print("  " + name)
        return 2

    for asset in ASSETS:
        master = MASTER / asset
        if not master.exists():
            print("정본이 없습니다: %s" % master.relative_to(ROOT))
            return 2
        want = digest(master)
        for persona in PERSONAS:
            copy = ROOT / persona / "shared" / asset
            have = digest(copy) if copy.exists() else None
            if have == want:
                continue
            if check_only:
                mismatched.append("%s/shared/%s" % (persona, asset))
            else:
                copy.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(master, copy)
                updated.append("%s/shared/%s" % (persona, asset))

    if check_only:
        if mismatched:
            print("정본과 다른 사본 %d건" % len(mismatched))
            for item in mismatched:
                print("  " + item)
            return 1
        print("공용 자산 사본 %d건 전량 일치" % (len(ASSETS) * len(PERSONAS)))
        return 0

    if updated:
        print("사본 %d건 갱신" % len(updated))
        for item in updated:
            print("  " + item)
    else:
        print("갱신 대상이 없습니다. 사본 %d건 전량 일치" % (len(ASSETS) * len(PERSONAS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
