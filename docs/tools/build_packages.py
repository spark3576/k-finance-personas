#!/usr/bin/env python3
"""배포용 압축 파일 생성.

페르소나별 압축 파일 여섯 개와 전체 압축 파일 한 개를 저장소 최상위에 생성합니다.
페르소나별 압축 파일에는 공용 자산 사본이 포함되어 단독 실행이 가능합니다.

사용법:
    python3 docs/tools/build_packages.py
"""
import hashlib
import os
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PERSONAS = [
    "orchestrator",
    "s1-accounting-reviewer",
    "s2-external-audit-responder",
    "s3-tax-reviewer",
    "s4-capital-market-disclosure-reviewer",
    "s5-fair-trade-reviewer",
]
BUNDLE = "k-finance-personas.zip"
SKIP = {".DS_Store"}


def add_tree(zf: zipfile.ZipFile, folder: str) -> None:
    base = ROOT / folder
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames.sort()
        for name in sorted(filenames):
            if name in SKIP:
                continue
            full = Path(dirpath) / name
            zf.write(full, full.relative_to(ROOT).as_posix())


def build(target: str, folders, extra_files=()) -> Path:
    path = ROOT / target
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in extra_files:
            zf.write(ROOT / name, name)
        for folder in folders:
            add_tree(zf, folder)
    return path


def main() -> int:
    rows = []
    for persona in PERSONAS:
        path = build("%s.zip" % persona, [persona])
        rows.append(path)
    rows.append(build(BUNDLE, ["shared"] + PERSONAS, extra_files=["README.md"]))

    print("%-46s %10s  %s" % ("파일", "크기(byte)", "SHA-256 앞 16자리"))
    for path in rows:
        data = path.read_bytes()
        with zipfile.ZipFile(path) as zf:
            bad = zf.testzip()
        if bad is not None:
            print("무결성 검사 실패: %s (%s)" % (path.name, bad))
            return 1
        print("%-46s %10s  %s" % (path.name, format(len(data), ","),
                                  hashlib.sha256(data).hexdigest()[:16]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
