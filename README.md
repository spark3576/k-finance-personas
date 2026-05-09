# k-finance-personas (V0.4)

한국 FP&A 직무를 위한 멀티-에이전트 페르소나 라이브러리.
오케스트레이터 1개 + 코어 분과 서브에이전트 3개로 구성된 V1 라이브러리.

---

## V0.4 — 작동 시험 1차·2차 결함 반영 hotfix

**시험 케이스**:
- 1차: 임차인 시설 인테리어 비용 1억 보전 (단순 거래, K-IFRS 1116 인센티브)
- 2차: PRS 차액결제형 약정 통합 검토 (복잡 거래, 4분과 동시, v0.1 → v0.2 진화)

**식별된 결함**:
1. 회사명 환각 (1차·2차 모두) — 호출자 미제공 회사명을 거래 단서로부터 추론 단정
2. 양식 일관성 부족 — 1차에서 [제3자 시선 검증]·[자기 피드백]·R8 박스 누락. 2차에서는 발현. 거래 복잡도에 따라 양식 일관성이 달라짐
3. Footer 양식 미적용 (1차·2차 모두)
4. R8 외부 자료 검색 박스 미발현 (1차)

**V0.4 조치**:
1. **AP1 hotfix** — 회사명·인명 환각 단정 차단 룰 universal 적용 (이전 AP1 = 결정 대체는 AP12로 분리)
2. **양식 mandatory 강제** — shared/output-templates.md §7의 7개 요소를 모든 산출물에 mandatory. 거래 복잡도 무관
3. **AP12·AP13 신규** — 결정 대체(AP12, 이전 AP1)·양식 일관성 위반(AP13) 명시

---

## 비전

**1차 목표 (Phase 1, 지금~3개월)**: 페르소나 라이브러리가 본업에서 *잘 돌아가는지* 검증.
**2차 목표 (D 빌드 부산물)**: MCP 서버 인프라 학습 — 페르소나의 진짜 멀티-에이전트화.
**3차 목표 (그 후)**: 안정화된 페르소나를 팀에 배포 — *AI 에이전트 디자이너* 포지셔닝의 가시적 작동.

---

## 구조 (V0.4)

```
k-finance-personas/
├── README.md                                  ← 이 파일
├── orchestrator/                              ← O1 재무 통합 오케스트레이터 (V0.4)
│   ├── SKILL.md
│   └── references/full-manual.md
├── s1-accounting-reviewer/                    ← S1 회계 검토자 (V0.4)
│   ├── SKILL.md
│   └── references/full-manual.md
├── s2-external-audit-responder/               ← S2 외부감사 응대자 (V0.4)
│   ├── SKILL.md
│   └── references/full-manual.md
├── s3-tax-reviewer/                           ← S3 세무 검토자 (V0.4)
│   ├── SKILL.md
│   └── references/full-manual.md
└── shared/                                    ← V0.4 universal 자산 (신규)
    ├── universal-rules.md                     ← R1~R8 통합 정의 + R4·R8 mandatory 강화
    ├── universal-anti-patterns.md             ← AP1~AP13 통합 정의 + AP1 hotfix
    └── output-templates.md                    ← Header·Footer·제3자 시선 검증·자기 피드백 등 mandatory 양식
```

---

## 페르소나 라이브러리 (V0.4)

| ID | 페르소나 | 토대 | V1 디폴트 모드 | 버전 |
|---|---|---|---|---|
| O1 | 재무 통합 오케스트레이터 | 사용자 직무 정체성 | CFO-mode (활성) | V0.4 (← V0.2) |
| S2 | 외부감사 응대자 | 외감법, 감사기준서 | 소명 논리 개발 | V0.4 (← V0.3) |
| S1 | 회계 검토자 | K-IFRS, 일반회계원칙 | 회계처리 결정 | V0.4 (← V0.2) |
| S3 | 세무 검토자 | 법인세·부가세·국세기본법 | 세무 리스크 검토 | V0.4 (← V0.2) |

V1.5 이후 추가 예정: S4 자본시장·공시 / S5 공정거래 / S6 FP&A 분석가 / S7 자금 운영자 / S8 경영보고자 / S9 시스템 PM

---

## 사용법

### Claude Code (개발자 환경)

```bash
git clone https://github.com/<your-username>/k-finance-personas.git ~/.claude/skills/k-finance-personas
```

각 페르소나 폴더(`orchestrator/`, `s2-external-audit-responder/` 등)가 자동 인식. `git pull`로 진화 자동 동기화.

### claude.ai (웹·앱)

각 페르소나 폴더를 ZIP으로 묶어 Personal Skills로 업로드:

1. `orchestrator/` 폴더를 압축 → `orchestrator.zip`
2. claude.ai → Settings → Features → Skills → "+" 버튼 → "Create skill" → ZIP 업로드 (V0.3 ZIP을 *교체* 업로드)
3. S2·S1·S3도 동일 절차 (총 4번 업로드)

요건: Pro / Max / Team / Enterprise 플랜 + Code Execution 활성화.

페르소나 V0.x 진화 시 — 해당 ZIP을 다시 만들어 재업로드.

**주의**: shared/ 폴더는 각 페르소나 ZIP에 포함되지 *않음*. 각 SKILL.md가 `../shared/...`를 참조하므로 Claude Code 환경에서는 정상 작동, claude.ai Skills 환경에서는 universal 자산이 산출물 양식 강제는 SKILL.md 본문에 박힌 mandatory 룰로 충분히 작동. (Phase 1 검증 단계엔 충분.)

---

## 운영 원칙 (V0.4)

V1 라이브러리는 다음 6개 원칙 위에 작동한다:

1. **입력·출력 게이트는 사람에게** — 페르소나는 결정을 대체하지 않음. (AP12)
2. **회사 내부 정보 시스템 입력 절대 금지** — 공개 정보만 사용.
3. **모든 출력 = 출처 + 불확실성 표기** — 환각 방지. (AP1·AP3·AP4)
4. **단일 substrate 누적 구조** — 새 페르소나는 기존 골격 위에 빌드.
5. **매 단계 Stop-or-Continue 게이트** — 진화·확장은 검증 후.
6. **베일 걷기 의무** — 위임할 수 있는 것과 직접 만들어야 할 것의 구분.

---

## 호출 분기 룰 (V0.4)

| 입력 신호 | 호출 페르소나 |
|---|---|
| 외감 응대 / 감사 자료 wrap-up | S2 |
| 결산 / 회계처리 결정 / 분개 심사 | S1 |
| 신규 거래 세무 영향 / 세무 신고·조사 | S3 |
| 외감 시 회계 판단 깊이 | S2 → S1 연쇄 호출 |
| 회계처리 변경 → 세무 영향 | S1 → S3 연쇄 호출 |
| 신규 거래 회계 + 세무 + 공시 통합 (단순) | O1 → S1 + S3 + 공시 직접 |
| 다중 분과 + 위법 인접 거래 (복잡) | O1 → S1 + S2 + S3 + 공시·공정거래 직접 (2차 시험 PRS 패턴) |
| 사내 자문 / 분과 간 통합 판단 | O1 직접 처리 |

---

## V0.4 진화 이력

| 버전 | 일자 | 주요 변경 |
|---|---|---|
| V0.1 | 2026-05-05 | 페르소나별 정체성·위임 불가 영역 1차 작성 |
| V0.2 | 2026-05-05 | O1 격 가변형·라이브러리 9개·다면성 / S1·S3 행동 규칙·출력 양식 |
| V0.3 | 2026-05-07 | S2 R4·R8 도입 (객관성 확보·외부 자료 검색) — *제3자 시선 검증 박스* 신설 |
| **V0.4** | **2026-05-08** | **AP1 hotfix (환각 차단) + R4·R8 mandatory + universal shared/ 자산 + AP12·AP13 신규** |

---

## 자산 출처

이 라이브러리는 ADBC 학습 사다리(A 단계)의 산출물.
ADBC = A. K-FP&A 페르소나 라이브러리 → D. 한국 법령 모니터 → B. DART 디텍터 → C. 데이터 저널리즘 인사이트 발굴기.

각 페르소나의 상세 매뉴얼·진화 이력은 해당 폴더의 `references/full-manual.md` 참조.
Universal 자산은 `shared/` 폴더 참조.

---

## 라이선스

(추후 결정 — Phase 1 완료 후)
