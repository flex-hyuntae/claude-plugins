---
name: structure-best-practices
description: "프로젝트 구조와 코드 구성 규칙. 새 기능 설계 및 리팩토링 시 참조한다."
---

# Structure Best Practices

프로젝트 구조와 코드 구성 규칙.

## When to Apply

- 새 기능의 디렉토리 구조를 설계할 때
- 컴포넌트 폴더를 생성할 때
- 데이터 레이어를 설계할 때

## Quick Reference

### Structure (MEDIUM-HIGH)

- `struct-component-structure` - 컴포넌트 폴더 구조 (index.tsx + style.css.ts)
- `struct-ddd-directory` - DDD 기반 도메인별 디렉토리 구조
- `struct-data-layer-cohesion` - 데이터 조작을 query/mutation 훅 내부에서 처리

## How to Use

개별 rule 파일에서 상세 설명과 코드 예시를 확인:
```
rules/structure/struct-component-structure.md
rules/structure/struct-ddd-directory.md
```

각 rule 파일에는 Incorrect/Correct 코드 예시와 설명이 포함되어 있다.
