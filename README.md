# k-finance-personas

한국 기업의 재무 실무를 위한 검토 페르소나 라이브러리입니다. 통합 오케스트레이터 한 개와 분과 검토자 열 개로 구성되며, 회계·외부감사·내부회계·세무·자본시장 공시·공정거래·자금·부동산금융·경영관리·법무 영역에서 사전 검토 산출물을 생성합니다.

## 구성

| 묶음 | 식별자 | 분과 | 토대 |
|---|---|---|---|
| — | orchestrator | 통합 오케스트레이터 | 열 개 분과의 배정과 통합 판단 |
| 재무보고 | s1-accounting-reviewer | 회계 | 한국채택국제회계기준, 일반회계원칙 |
| 재무보고 | s2-external-audit-responder | 외부감사 응대 | 외부감사법, 감사기준서 |
| 재무보고 | s10-internal-accounting-control-reviewer | 내부회계 | 외부감사법, 내부회계관리제도 설계·운영 개념체계 |
| 외부규제 | s3-tax-reviewer | 세무 | 법인세법, 부가가치세법, 국세기본법 |
| 외부규제 | s4-capital-market-disclosure-reviewer | 자본시장·공시 | 자본시장법, 거래소 공시 규정 |
| 외부규제 | s5-fair-trade-reviewer | 공정거래 | 공정거래법 |
| 재무자문 | s6-treasury-reviewer | 자금 | 상법상 자금조달 절차, 약정 조항, 자본시장법 |
| 재무자문 | s7-real-estate-finance-reviewer | 부동산금융 | 부동산투자회사법, 자본시장법상 부동산집합투자기구 규정 |
| 재무자문 | s9-management-planning-reviewer | 경영관리·기획 | 가치평가 방법론, 감정평가 기준 |
| 법무연계 | s8-legal-issue-reviewer | 법무 | 상법, 민법, 개별 규제 법령 |

묶음은 읽기의 단위이며 배정의 단위가 아닙니다. 나누는 기준은 담당 법령이 아니라 결론이 무엇에 잠기는가입니다. 재무보고 분과의 결론은 회계기준과 감사기준에, 외부규제 분과의 결론은 법령 조항과 정량 임계치에, 재무자문 분과의 결론은 입력 가정에 잠깁니다. 법무연계 분과는 실체 판단을 보유하지 않고 경로만 보유합니다.

## 동작 방식

페르소나는 호출을 받으면 사안의 영향도를 스스로 판단하여 산출물의 형식을 권고하고, 호출자에게 선택을 요청합니다. 형식은 요약형, 표준형, 상세형 세 가지이며 표준형이 기본값입니다.

모든 산출물은 결론을 입력 가정에 잠급니다. 같은 가정을 입력하면 같은 결론이 나오며, 가정이 바뀔 때 어떤 결론이 갈리는지 표로 제시합니다.

산출물은 호출자가 검토하기 위한 초안입니다. 최종 결정과 외부 응대는 호출자의 영역입니다.

## 폴더 구조

```
k-finance-personas/
├── README.md                  본 문서
├── CLAUDE.md                  Claude Code 세션 진입 지침
├── HANDOFF.md                 세션 인계서
├── docs/                      운영 문서
├── shared/                    공용 자산 정본
├── orchestrator/              통합 오케스트레이터
├── s1-accounting-reviewer/    회계 검토자
├── s2-external-audit-responder/
├── s3-tax-reviewer/
├── s4-capital-market-disclosure-reviewer/
├── s5-fair-trade-reviewer/
├── s6-treasury-reviewer/
├── s7-real-estate-finance-reviewer/
├── s8-legal-issue-reviewer/
├── s9-management-planning-reviewer/
└── s10-internal-accounting-control-reviewer/
```

각 페르소나 폴더는 `SKILL.md`, 상세 매뉴얼(`references/full-manual.md`), 공용 자산 사본(`shared/`)으로 구성됩니다. 사본을 두는 이유는 페르소나 폴더 하나만으로도 단독 실행이 가능하도록 하기 위함입니다. 사본은 정본과 항상 일치해야 하며, `docs/tools/sync_shared.py`로 동기화하고 검증합니다.

## 공용 자산

| 파일 | 내용 |
|---|---|
| `shared/universal-rules.md` | 행동 규칙 R1부터 R10까지 |
| `shared/universal-anti-patterns.md` | 오류 유형 AP1부터 AP21까지 |
| `shared/output-templates.md` | 산출물 서식과 형식별 구성 요건 |

## 운영 문서

| 파일 | 내용 |
|---|---|
| `docs/00_현황판.md` | 현재 진행 상태와 다음 작업 |
| `docs/01_설계도.md` | 구조와 구성 요소, 상호 관계 |
| `docs/02_시험기록.md` | 시험 누적 기록과 결함 이력 |
| `docs/03_결정기록.md` | 확정된 결정과 그 근거 |
| `docs/04_문체기준.md` | 문서와 산출물의 서술 기준 |
| `docs/05_후속작업.md` | 환경별 후속 작업 목록 |
| `docs/06_개정이력.md` | 판번호별 변경 내역 |

## 사용 환경

### Claude Code

저장소를 내려받은 뒤 각 페르소나 폴더를 `~/.claude/skills/` 아래에 연결합니다.

```bash
git clone https://github.com/spark3576/k-finance-personas.git
mkdir -p "$HOME/.claude/skills"
for p in orchestrator s1-accounting-reviewer s2-external-audit-responder \
         s3-tax-reviewer s4-capital-market-disclosure-reviewer s5-fair-trade-reviewer \
         s6-treasury-reviewer s7-real-estate-finance-reviewer s8-legal-issue-reviewer \
         s9-management-planning-reviewer s10-internal-accounting-control-reviewer; do
  ln -sfn "$PWD/k-finance-personas/$p" "$HOME/.claude/skills/$p"
done
```

### claude.ai

각 페르소나 폴더를 압축하여 개인 스킬로 등록합니다. 압축 파일은 `docs/tools/build_packages.py`로 생성합니다.

```bash
python3 docs/tools/build_packages.py
```

저장소 최상위에 페르소나별 압축 파일 열한 개와 전체 압축 파일 한 개가 생성됩니다. 압축 파일은 형상 관리 대상에서 제외되어 있습니다.

## 검증

문서를 수정한 뒤에는 다음 두 가지를 실행합니다.

```bash
python3 docs/tools/check_style.py     # 서술 기준 점검
python3 docs/tools/sync_shared.py     # 공용 자산 사본 동기화 및 검증
```
