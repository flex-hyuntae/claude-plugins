---
name: add-best-practice
description: "코딩 패턴이나 컨벤션을 rules/에 추가한다."
disable-model-invocation: true
argument-hint: "<패턴 설명>"
---

# Best Practice 추가

사용자가 "패턴 추가", "컨벤션 추가", "앞으로 이렇게 작성해줘", "add convention", "add pattern" 등으로 호출하면 다음 흐름을 따른다.

## 1. 저장 절차

1. 해당 카테고리의 `rules/` 디렉토리에서 기존 파일들과 **중복 확인**
2. 적절한 카테고리와 prefix 결정
3. `rules/<category>/<prefix>-<name>.md` 파일 생성
4. 해당 카테고리의 `skills/<category>/SKILL.md` Quick Reference에 추가
5. **버전 bump 필수**: `.claude-plugin/plugin.json`과 `marketplace.json`의 version을 동일하게 올린다

## 2. Rule 파일 형식

```yaml
---
title: Rule Title
impact: LOW|MEDIUM|HIGH|CRITICAL
impactDescription: Optional impact description
tags: tag1, tag2
---
```

## 3. 카테고리 / prefix 가이드

| Category | Prefix | 예시 |
|----------|--------|------|
| react | `async-` | await, Promise, Suspense |
| react | `react-` | 모달, 상태 관리 패턴 |
| react | `rerender-` | memo, derived state |
| react | `rendering-` | conditional render |
| react | `js-` | 캐싱, 조기 반환 |
| react | `advanced-` | ref, initialization |
| typescript | `ts-` | type assertion, generic |
| structure | `struct-` | 폴더 구조, DDD, 데이터 레이어 |
| styling | `styling-` | vanilla-extract, 디자인 토큰 |
| accessibility | `a11y-` | ARIA, 키보드, 시맨틱 HTML |
| testing | `test-` | AAA 패턴, 테스트 품질 |
| naming | `naming-` | 네이밍, i18n, 주석 |

새 카테고리가 필요하면 `rules/<new-category>/`와 `skills/<new-category>/SKILL.md`를 함께 생성한다.

## 4. 완료 보고

저장 완료 후 사용자에게 보고:
- 저장된 위치 (rule 파일 경로)
- 저장된 내용 요약
- 버전 변경 내역
