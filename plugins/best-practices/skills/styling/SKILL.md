---
name: styling-best-practices
description: "CSS 및 스타일링 규칙 (vanilla-extract). 스타일 작성 및 리뷰 시 참조한다."
---

# Styling Best Practices

vanilla-extract 기반 CSS 및 스타일링 규칙.

## When to Apply

- vanilla-extract 스타일 파일을 작성할 때
- 디자인 토큰을 적용할 때
- 동적 스타일링이 필요할 때

## Quick Reference

### Styling (HIGH)

- `styling-vanilla-extract` - style.css.ts 분리, style()/styleVariants()/recipe() 패턴, 동적 스타일은 assignInlineVars
- `styling-design-tokens` - 하드코딩 값 대신 디자인 시스템 토큰(vars) 사용

## How to Use

개별 rule 파일에서 상세 설명과 코드 예시를 확인:
```
rules/styling/styling-vanilla-extract.md
rules/styling/styling-design-tokens.md
```

각 rule 파일에는 Incorrect/Correct 코드 예시와 설명이 포함되어 있다.
