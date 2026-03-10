---
name: react-best-practices
description: "React 성능 최적화 및 패턴 규칙. 컴포넌트 작성, 리뷰, 리팩토링 시 참조한다."
---

# React Best Practices

React 성능 최적화 및 패턴 규칙.

## When to Apply

- React 컴포넌트나 훅을 작성할 때
- 코드 리뷰에서 성능 이슈를 검토할 때
- 기존 React 코드를 리팩토링할 때

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Async Performance | CRITICAL | `async-` |
| 2 | React Patterns | MEDIUM | `react-` |
| 3 | Re-render Optimization | MEDIUM | `rerender-` |
| 4 | Rendering Performance | MEDIUM | `rendering-` |
| 5 | JavaScript Performance | LOW-MEDIUM | `js-` |
| 6 | Advanced Patterns | LOW | `advanced-` |

## Quick Reference

### Async Performance (CRITICAL)

- `async-defer-await` - 필요한 시점까지 await 지연
- `async-parallel-promises` - 독립적인 작업에 Promise.all() 사용
- `async-suspense-boundaries` - Suspense로 컨텐츠 스트리밍

### React Patterns (MEDIUM)

- `react-modal-controlled-state` - 모달 open/type 상태 분리, onClose에서 초기화

### Re-render Optimization (MEDIUM)

- `rerender-memo-extract` - Memoized component로 추출
- `rerender-memo-default-value` - Memoized component의 기본값 상수 추출
- `rerender-narrow-dependencies` - Effect 의존성 좁히기
- `rerender-derived-state` - 파생 boolean 구독
- `rerender-derived-state-no-effect` - Effect 없이 렌더 중 파생 state 계산
- `rerender-functional-setstate` - 함수형 setState로 안정적인 콜백
- `rerender-lazy-state-init` - useState 지연 초기화
- `rerender-simple-expression-memo` - 단순 표현식 메모 불필요
- `rerender-move-effect-to-event` - Effect 대신 이벤트 핸들러에 로직 배치
- `rerender-transitions` - 비긴급 업데이트에 startTransition 사용
- `rerender-useref-transient` - 자주 변하는 값에 useRef 사용

### Rendering Performance (MEDIUM)

- `rendering-conditional-render` - && 대신 삼항 연산자로 조건부 렌더링

### JavaScript Performance (LOW-MEDIUM)

- `js-index-maps` - 반복 조회에 Map 인덱스 구축
- `js-cache-property-access` - 루프 내 속성 접근 캐싱
- `js-length-check-first` - 비용 큰 비교 전 배열 길이 확인
- `js-early-exit` - 함수에서 조기 반환
- `js-hoist-regexp` - RegExp를 루프 밖으로 호이스트
- `js-set-map-lookups` - O(1) 조회에 Set/Map 사용
- `js-tosorted-immutable` - 불변성을 위해 toSorted() 사용

### Advanced Patterns (LOW)

- `advanced-event-handler-refs` - ref에 이벤트 핸들러 저장

## How to Use

개별 rule 파일에서 상세 설명과 코드 예시를 확인:
```
rules/react/async-defer-await.md
rules/react/rerender-memo-extract.md
```

각 rule 파일에는 Incorrect/Correct 코드 예시와 설명이 포함되어 있다.
