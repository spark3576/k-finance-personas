# k-finance-personas (V1.5)

한국 FP&A 직무를 위한 멀티-에이전트 페르소나 라이브러리.
오케스트레이터 1개 + 코어 분과 서브에이전트 5개로 구성된 V1.5 라이브러리.

---

## 비전

**1차 목표 (Phase 1, 진행 중)**: 페르소나 라이브러리가 본업에서 *잘 돌아가는지* 검증.
**2차 목표 (D 빌드 부산물)**: MCP 서버 인프라 학습 — 페르소나의 진짜 멀티-에이전트화.
**3차 목표 (그 후)**: 안정화된 페르소나를 팀에 배포 — *AI 에이전트 디자이너* 포지셔닝의 가시적 작동.

---

## V1.5 라이브러리 구성

| 페르소나 | 토대 | V1.5 디폴트 모드 | 버전 |
|---|---|---|---|
| **O1** 재무 통합 오케스트레이터 | 사용자 직무 정체성 | CFO-mode | V1.5 |
| **S1** 회계 검토자 | K-IFRS, 일반회계원칙 | 회계처리 결정 | V0.4 |
| **S2** 외부감사 응대자 | 외감법, 감사기준서 | 소명 논리 개발 | V0.4 |
| **S3** 세무 검토자 | 법인세·부가세·국세기본법 | 세무 리스크 검토 | V0.4 |
| **S4** 자본시장·공시 검토자 | 자본시장법·외감법·K-IFRS 1024·거래소 공시 규정 | 공시 의무 평가 | **V0.1 (V1.5 신규)** |
| **S5** 공정거래 검토자 | 공정거래법·시행령·고시·공정위 의결례·심사기준 | 공정거래법 사전 평가 | **V0.1 (V1.5 신규)** |

---

## 디렉토리 구조

```
k-finance-personas/
├── README.md                                    ← 본 문서
├── orchestrator/                                ← V1.5 호출 분기 룰 갱신
│   ├── SKILL.md
│   ├── references/full-manual.md
│   └── shared/ (V1.5 갱신)
├── s1-accounting-reviewer/                      ← V0.4 그대로
│   ├── SKILL.md
│   ├── references/full-manual.md
│   └── shared/ (V1.5 갱신)
├── s2-external-audit-responder/                 ← V0.4 그대로
│   ├── SKILL.md
│   ├── references/full-manual.md
│   └── shared/ (V1.5 갱신)
├── s3-tax-reviewer/                             ← V0.4 그대로
│   ├── SKILL.md
│   ├── references/full-manual.md
│   └── shared/ (V1.5 갱신)
├── s4-capital-market-disclosure-reviewer/       ← V1.5 신규
│   ├── SKILL.md
│   ├── references/full-manual.md
│   └── shared/ (V1.5)
├── s5-fair-trade-reviewer/                      ← V1.5 신규
│   ├── SKILL.md
│   ├── references/full-manual.md
│   └── shared/ (V1.5)
└── shared/                                      ← 마스터 universal 자산 (V1.5)
    ├── universal-rules.md                       ← R8 출처 S4·S5 추가
    ├── universal-anti-patterns.md               ← AP14·AP15 추가
    └── output-templates.md                      ← V0.4 그대로
```

각 페르소나 폴더 내 `shared/`는 마스터 `shared/`의 사본 — claude.ai 개별 Skills 등록 시 페르소나 폴더 단독으로 작동 가능하게 하기 위함. md5 동기화 검증 완료.

---

## 사용 환경

### claude.ai 웹·앱 (Pro/Max/Team/Enterprise + Code Execution 활성)

각 페르소나 폴더(`orchestrator/`·`s1-accounting-reviewer/` 등 6개)를 ZIP으로 만들어 *Personal Skills*에 업로드.

```bash
cd k-finance-personas/
zip -r orchestrator.zip orchestrator/
zip -r s1-accounting-reviewer.zip s1-accounting-reviewer/
zip -r s2-external-audit-responder.zip s2-external-audit-responder/
zip -r s3-tax-reviewer.zip s3-tax-reviewer/
zip -r s4-capital-market-disclosure-reviewer.zip s4-capital-market-disclosure-reviewer/
zip -r s5-fair-trade-reviewer.zip s5-fair-trade-reviewer/
```

각 ZIP을 claude.ai의 Personal Skills에 등록.

### Claude Code

```bash
git clone https://github.com/[user]/k-finance-personas ~/.claude/skills/k-finance-personas
```

또는 마스터 ZIP `k-finance-personas-v1.5.zip` 압축 해제 후 `~/.claude/skills/`에 배치.

---

## V1.5 변경 (V0.4 → V1.5, 2026-05-09)

### 신규 빌드

- **S4 자본시장·공시 검토자** — V1에서 O1 직접 처리하던 공시 영역을 분과 페르소나로 분리. 자본시장법 §161·§159·§162·§163 + 거래소 공시 규정 + 금감원 공시 모범규준 + K-IFRS 1024 cross-ref. V1.5 디폴트 모드: 공시 의무 평가.
- **S5 공정거래 검토자** — V1에서 시그널만 표시하던 공정거래 영역을 정량 결론 분과로 분리. 공정거래법 §11·§24·§26·§27·§45·§47·§36 + 시행령 + 시행규칙 + 고시 + 심사기준 + 공정위 의결례 + 대법원 판례 cross-ref. AP6 *최강화* 적용. V1.5 디폴트 모드: 공정거래법 사전 평가.

### O1 갱신

- **호출 분기 룰 V1.5 확장** — 7개 라우팅 신설:
  1. 공시 의무 평가 / 주요사항보고서 → S4
  2. 정기·수시공시 작성 검토 → S4
  3. 특수관계자 거래 공시 정합성 → S4 + S1
  4. 계열사 거래 / 기업결합 / §11 / §45·§47 → S5
  5. 회계처리 변경 → 공시 영향 → S1 → S4 연쇄
  6. 계열사 거래 → 공시 의무 → S5 → S4 연쇄
  7. 다중 분과 + 위법 인접 → S1+S2+S3+S4+S5 통합

### shared/ universal 자산 갱신

- **universal-rules.md V1.5** — R2·R3·R4·R7·R8 페르소나별 변형에 S4·S5 추가. R8 추천 출처에 S4(DART·금감원·거래소·자본시장법)·S5(공정위·심사기준·대법원 판례) 합류. R3 Level 3 발동 패턴: S5 *라이브러리에서 가장 빈번*.
- **universal-anti-patterns.md V1.5** — AP14(공시 의무 과소 평가, S4 특화)·AP15(부당지원행위 과소 평가, S5 특화) 신규. AP1·AP2·AP5·AP6·AP7·AP9 변형에 S4·S5 영역 추가.
- **output-templates.md** — V0.4 그대로 유지 (변경 없음).

### S1·S2·S3 변경

코드 변경 없음. shared/ 갱신만 따라 자동 동기화.

---

## V0.4 변경 이력 (2026-05-08, 회고)

작동 시험 1차(임차인 인테리어)·2차(PRS 약정) 결함 반영:

1. **AP1 hotfix** — 호출자 미제공 회사명·인명 단정 차단. 추론 결과는 `가능성: [X] (확정 필요)` 형태만 허용. (이전 AP1 = 결정 대체는 AP12로 이전)
2. **R4·R8 mandatory 강화** — [제3자 시선 검증]·[외부 자료 검색] 박스 mandatory. 거래 복잡도 무관 적용.
3. **양식 일관성 강제** — shared/output-templates.md §7의 7개 mandatory 요소를 모든 산출물에 적용.
4. **AP12·AP13 신규** — 결정 대체(AP12)·양식 일관성 위반(AP13).
5. **shared/ universal 자산 신규** — universal-rules.md / universal-anti-patterns.md / output-templates.md

---

## ADBC 사다리 좌표

```
A. K-FP&A 페르소나 라이브러리 (진행 중)
   ├ V1 (O1+S1+S2+S3 = 4개) ✅ V0.4 안정화 완료
   ├ V1.5 (+S4 +S5 = 6개) ✅ 본 빌드 (2026-05-09)
   └ V2 (+S6~S9 = 10개) ⏳ D 단계 부산물

D. 한국 법령 모니터 ⏳ V1.5 안정화 후 진입
   ├ MCP 서버 인프라 빌드
   ├ 법령 모니터링 데이터 흐름
   └ 부산물: 페르소나 라이브러리 MCP 서버화 + S6~S9 substrate

B. DART 디텍터 ⏳ D 인프라 재활용

C. 데이터 저널리즘 인사이트 발굴기 ⏳ B 데이터 흐름 재활용
```

**전체 진척**: V1.5 완료 시 약 12% (4단계 중 1단계의 50%).

---

## 운영 원칙 (V0.4 → V1.5 상속)

1. 입력·출력 게이트는 사람에게 (AP12)
2. 회사 내부 정보 시스템 입력 절대 금지
3. 모든 출력 = 출처 + 불확실성 표기 (AP1·AP3·AP4)
4. 단일 substrate 누적 구조
5. 매 단계 Stop-or-Continue 게이트
6. 베일 걷기 의무

---

## 다음 마일스톤

| 트리거 | 시점 | 액션 |
|---|---|---|
| V1.5 안정화 시험 | 본업 1~2건 누적 | V0.x 진화 결함 substrate 누적 |
| 1조 현물출자 v0.3 진화 | 호출자 V1·V3·V4 확정 시점 | S4·S5가 본문 분과로 등장 — 페르소나 진화 능력 마지막 검증 |
| Phase 1 정량 평가 | V1.5 안정화 후 | agent_time_tracker.xlsx 활용 본업 시간 회수율 정량 |
| **D 단계 substrate 정의** | V1.5 안정화 + Phase 1 정량 평가 후 | **새 대화 — 법령 모니터 + MCP 서버 인프라 명세** |

---

*Last updated: 2026-05-09 (V1.5 빌드)*
