#!/usr/bin/env python3
"""서술 기준 자동 점검기.

사용법:
    python3 docs/tools/check_style.py [경로 ...]

경로를 주지 않으면 저장소 전체의 마크다운 문서를 점검합니다.
docs/04_문체기준.md 자체와 개정이력 문서는 대응표·원문을 담고 있으므로 점검 대상에서 제외합니다.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXCLUDE = {"docs/04_문체기준.md", "docs/06_개정이력.md"}

# 1. 영문 업무 용어
JARGON = [
    "universal", "mandatory", "substrate", "hotfix", "cross-ref", "crossref",
    "Bottom Line", "3-tier", "prose", "if-then", "retrofit", "디폴트",
    "Inverted Pyramid", "ROI", "critical", "Critical", "Major", "Minor",
    "prime 부호", "conditional", "quality standard", "defect",
]
# 2. 평서형 '-다' 종결 (문장 끝)
PLAIN_END = re.compile(
    r"(?:했다|한다|이다|된다|있다|없다|같다|아니다|든다|본다|쓴다|낸다|둔다|넣는다|받는다|만든다|따른다|맞춘다|나눈다)"
    r"(?=[.\s)\]」]|$)"
)
# 3. 문장 중간 별표 강조 (*단어*)
STAR_EMPH = re.compile(r"(?<![\*\w])\*(?!\*)[^*\n]{1,40}\*(?!\*)")
# 4. 판정 기호
MARKS = ["❌", "✅", "⏳"]
# 5. 명사·형용사 나열형 종결
NOUN_END = re.compile(r"(?:우선|금지|아님|불가|필요|가능|누락|부재|해당|동일|무관|없음|있음)\.\s*$")


def code_block_lines(lines):
    """코드 블록 내부 줄 번호 집합을 반환합니다."""
    inside, marked = False, set()
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            inside = not inside
            marked.add(i)
            continue
        if inside:
            marked.add(i)
    return marked


def check(path: Path):
    rel = path.relative_to(ROOT).as_posix()
    if rel in EXCLUDE or path.name.startswith("_"):
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    skip = code_block_lines(lines)
    found = []
    for i, line in enumerate(lines, 1):
        if i in skip or line.lstrip().startswith("|---"):
            continue
        # 인라인 코드(`...`)는 파일명·식별자이므로 점검 대상에서 제외합니다.
        line = re.sub(r"`[^`]*`", "", line)
        for word in JARGON:
            if word in line:
                found.append((rel, i, "영문 업무 용어", word))
        if PLAIN_END.search(line):
            found.append((rel, i, "평서형 종결", PLAIN_END.search(line).group()))
        if STAR_EMPH.search(line):
            found.append((rel, i, "문장 중간 별표 강조", STAR_EMPH.search(line).group()[:30]))
        for mark in MARKS:
            if mark in line:
                found.append((rel, i, "판정 기호", mark))
        if NOUN_END.search(line) and not line.lstrip().startswith(("#", "|", "-", "*", ">")):
            found.append((rel, i, "명사 나열형 종결", NOUN_END.search(line).group().strip()))
    return found


def ending_summary(paths):
    """「다」로 끝나는 줄을 정중체(-니다)와 평서체로 나누어 셉니다.
    정중체 「-습니다/-ㅂ니다」도 글자 「다」로 끝나므로, 단순히 「다」 종결만 세면
    정중체 문장이 평서체로 오인됩니다. 이 요약으로 그 혼동을 막습니다."""
    total = polite = 0
    for p in paths:
        rel = p.relative_to(ROOT).as_posix()
        if rel in EXCLUDE or p.name.startswith("_"):
            continue
        lines = p.read_text(encoding="utf-8").splitlines()
        skip = code_block_lines(lines)
        for i, line in enumerate(lines, 1):
            if i in skip:
                continue
            body = re.sub(r"[\s.。!?)\]」』*`]+$", "", line)
            if body.endswith("다"):
                total += 1
                if body.endswith("니다"):
                    polite += 1
    return total, polite


def main():
    targets = [Path(a).resolve() for a in sys.argv[1:]] or sorted(ROOT.rglob("*.md"))
    targets = [p for p in targets if ".git" not in p.parts]
    issues = []
    for p in targets:
        issues.extend(check(p))
    total, polite = ending_summary(targets)
    print("종결 진단 — 「다」로 끝나는 줄 %d건 중 정중체(-니다) %d건, 평서체 %d건"
          % (total, polite, total - polite))
    if not issues:
        print("서술 기준 점검 통과 — 지적 사항이 없습니다. (%d개 문서)" % len(targets))
        return 0
    print("서술 기준 지적 사항 %d건" % len(issues))
    current = None
    for rel, line_no, kind, detail in issues:
        if rel != current:
            print("\n[%s]" % rel)
            current = rel
        print("  %5d행  %-18s %s" % (line_no, kind, detail))
    return 1


if __name__ == "__main__":
    sys.exit(main())
