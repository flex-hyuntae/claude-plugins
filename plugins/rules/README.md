# rules

코드 생성 및 리뷰 시 참고할 코딩 컨벤션과 성능 최적화 규칙 모음.

## 카테고리

| Category | 규칙 수 | 설명 |
|----------|---------|------|
| react | 24 | 성능 최적화, 비동기 패턴, 렌더링 |
| typescript | 3 | 타입 안전성, enum vs union |
| structure | 3 | 컴포넌트 구조, DDD, 데이터 레이어 |
| styling | 2 | vanilla-extract, 디자인 토큰 |
| accessibility | 1 | 시맨틱 HTML, ARIA, 키보드 |
| testing | 1 | AAA 패턴, 동작 기반 테스트 |
| naming | 1 | 네이밍, i18n, 주석 |

## 스킬

| 스킬 | 설명 |
|------|------|
| `add-rule` | 코딩 패턴이나 컨벤션을 규칙으로 추가 |
| `write` | 코드 작성·수정 시 해당 카테고리의 규칙을 자동 참조하여 적용 |

## 사용 예시

### add-rule

```
/add-rule useEffect 내부에서 setState를 호출하지 말고 derived state로 전환
```

코딩 패턴이나 컨벤션을 설명하면, 적절한 카테고리에 규칙 파일을 생성합니다.

### write

```
/write
```

코드를 작성·수정·리팩토링할 때 자동으로 트리거됩니다. 작업 대상 코드에 해당하는 카테고리(react, typescript, styling 등)의 규칙을 읽고 준수하는 코드를 생성합니다.
