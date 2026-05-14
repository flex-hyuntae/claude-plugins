---
name: add-til
description: '오늘 배운 내용(TIL)을 Obsidian vault(GitHub repo)에 토픽 노트로 기록하고 자동 커밋·푸시한다. 사용자가 "오늘 배운거야", "TIL", "TIL 추가", "지식 기반에 추가", "배운점 추가", "/add-til"로 호출할 때 트리거. 기존 노트와 자동 양방향 연결([[노트명]] 링크). 기술 용어는 영어 원문 유지, 설명은 한국어.'
compatibility: '~/Projects/flex/til vault clone + git push 권한 필요'
argument-hint: "<배운 내용>"
---

# TIL 추가

사용자가 "오늘 배운거야", "TIL", "지식 기반에 추가해줘", "배운점 추가" 등으로 호출하면 다음 흐름을 따른다.

## 0. Vault 경로 확인

TIL vault 경로: `~/Projects/flex/til`
GitHub repo: `flex-hyuntae/til` (private)

해당 디렉토리가 존재하는지 확인한다. 없으면 다음 메시지를 출력하고 중단한다:

> TIL vault가 없습니다. 먼저 `gh repo clone flex-hyuntae/til ~/Projects/flex/til` 로 클론해주세요.

## 1. 내용 정리

사용자가 제공한 내용을 분석하여:
- **토픽 제목**: 배운 내용의 핵심 주제 (예: "AG-Grid 셀 상태 관리", "webpack bail 옵션과 child compiler")
- **카테고리**: 기존 `Topics/` 서브폴더 목록을 확인하고, 가장 적절한 카테고리를 선택한다. 적합한 카테고리가 없으면 새 서브폴더를 생성한다.
- **날짜**: 오늘 날짜 (YYYY-MM-DD 형식)
- **태그**: 관련 기술 키워드 (예: `[webpack, css, vanilla-extract]`)
- **본문**: 사용자가 제공한 상세 내용을 마크다운으로 정리
- **연결 노트**: 기존 Topics/ 하위의 모든 서브폴더에서 노트를 확인하여 관련 있는 노트를 `[[노트명]]` 링크로 연결

## 2. 기존 노트 확인

`~/Projects/flex/til/Topics/` 하위의 모든 서브폴더에서 기존 노트 목록을 확인한다.
- 내용이 기존 토픽과 겹치면 기존 노트를 업데이트할지 새로 만들지 사용자에게 확인한다.
- 관련 있는 기존 노트가 있으면 `[[노트명]]` 으로 양방향 연결한다 (새 노트에서 기존 노트 링크 + 기존 노트에도 새 노트 링크 추가).

## 작성 규칙

- 기술 용어는 영어로 작성한다 (예: reconciliation, call stack, linked list, bailout, bitmask, shallow comparison)
- 설명 문장은 한국어로 작성하되, 널리 쓰이는 기술 용어는 음역하지 않고 영어 원문 그대로 쓴다

## 3. 토픽 노트 생성

`~/Projects/flex/til/Topics/<카테고리>/<토픽 제목>.md` 파일을 생성한다. 새 카테고리인 경우 서브폴더를 먼저 생성하고, `graph.json`의 `colorGroups`에 새 색상 그룹을 추가한다.

```markdown
---
date: <오늘 날짜 YYYY-MM-DD>
tags: [<태그들>]
---

# <토픽 제목>

## 요약

<한두 줄 요약>

## 상세 내용

<정리한 본문>

## 연결 노트

- [[관련 토픽 1]]
- [[관련 토픽 2]]
```

## 4. Git 커밋 & 푸시

```bash
cd ~/Projects/flex/til
git add -A
git commit -m "feat: <토픽 제목> 추가"
git push
```

## 5. 완료 보고

생성 완료 후 사용자에게 보고:
- 생성된 토픽 제목
- 연결된 기존 노트 목록
- Obsidian Graph View에서 확인하도록 안내
