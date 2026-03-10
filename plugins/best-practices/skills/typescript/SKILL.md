---
name: typescript-best-practices
description: "TypeScript 타입 안전성 규칙. 코드 생성 및 리뷰 시 참조한다."
---

# TypeScript Best Practices

TypeScript 타입 안전성을 보장하는 규칙.

## When to Apply

- TypeScript 코드를 생성하거나 수정할 때
- 타입 정의를 설계할 때
- 코드 리뷰에서 타입 안전성을 검토할 때

## Quick Reference

### TypeScript (HIGH)

- `ts-no-type-assertion` - `as` type assertion, non-null assertion `!` 사용 금지
- `ts-no-any` - `any` 타입 사용 금지, unknown 또는 구체적 타입으로 대체
- `ts-enum-vs-union` - enum 대신 union type 사용, 번들 사이즈 및 tree-shaking 이점

## How to Use

개별 rule 파일에서 상세 설명과 코드 예시를 확인:
```
rules/typescript/ts-no-type-assertion.md
rules/typescript/ts-enum-vs-union.md
```

각 rule 파일에는 Incorrect/Correct 코드 예시와 설명이 포함되어 있다.
