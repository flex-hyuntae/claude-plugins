---
name: add-til
description: "오늘 배운 내용(TIL)을 Notion 데이터베이스에 기록한다."
argument-hint: "<배운 내용>"
---

# TIL 추가

사용자가 "오늘 배운거야", "TIL", "지식 기반에 추가해줘", "배운점 추가" 등으로 호출하면 다음 흐름을 따른다.

## 0. Notion MCP 연결 확인

Notion MCP 도구(`mcp__notion__notion-create-pages` 등)가 사용 가능한지 확인한다.
사용 불가능하면 다음 메시지를 출력하고 중단한다:

> Notion MCP가 연결되어 있지 않습니다.
> Claude Code 설정에서 Notion MCP 서버를 추가해주세요.
> 참고: https://www.notion.so/integrations

## 1. 내용 정리

사용자가 제공한 내용을 분석하여:
- **제목**: 배운 내용을 한 줄로 요약 (예: "모달 닫기 애니메이션을 위한 open/type 상태 분리 패턴")
- **날짜**: 오늘 날짜 (YYYY-MM-DD 형식)
- **본문**: 사용자가 제공한 상세 내용을 정리 (마크다운 형식)

## 2. Notion 페이지 생성

`mcp__notion__notion-create-pages` 도구를 사용하여 페이지를 생성한다.

```json
{
  "parent": {
    "data_source_id": "31f0592a-4a92-805c-a5ea-000ba4b5152a"
  },
  "pages": [
    {
      "properties": {
        "제목": "<생성한 제목>",
        "date:날짜:start": "<오늘 날짜 YYYY-MM-DD>",
        "date:날짜:is_datetime": 0
      },
      "content": "<정리한 본문>"
    }
  ]
}
```

## 3. 완료 보고

생성 완료 후 사용자에게 보고:
- 생성된 제목
- Notion 페이지 링크 (응답에 포함된 경우)
