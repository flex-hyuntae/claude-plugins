---
name: daily-summary
description: "오늘 참여한 Slack 스레드를 시간순으로 요약하고, GitHub PR/Linear/Notion 링크를 추출한다."
---

# Daily Summary

오늘 Slack에서 참여한 스레드를 검색하고, 각 스레드를 요약하여 시간순(오래된 순)으로 출력한다.

## Constants

- **Slack User ID**: `U03VBV710JY`
- **Workspace**: `flex-cv82520.slack.com`
- **날짜**: 오늘 (YYYY-MM-DD)
- **봇 알림 채널 (직접 읽기 필요)**:
  - `C02CWLDRP6F` — #alarm-git-pr-frontend (GitHub 봇이 attachment로 멘션하므로 검색 불가)

## Workflow

### Phase 1: Slack 검색

검색 1~3을 **병렬로** 실행한다. response_format은 `detailed`를 사용한다.

**검색 1 — 참여한 스레드 (답장):**

`mcp__claude_ai_Slack__slack_search_public_and_private`로 검색:
- query: `from:<@U03VBV710JY> is:thread on:{오늘 날짜}`
- include_context: false
- sort: timestamp
- sort_dir: desc
- limit: 20
- response_format: detailed

**검색 2 — 내가 시작한 최상위 메시지:**

`mcp__claude_ai_Slack__slack_search_public_and_private`로 검색:
- query: `from:<@U03VBV710JY> -is:thread on:{오늘 날짜}`
- include_context: false
- sort: timestamp
- sort_dir: desc
- limit: 20
- response_format: detailed

**검색 3 — 멘션된 스레드 (타인이 나를 멘션):**

`mcp__claude_ai_Slack__slack_search_public_and_private`로 검색:
- query: `to:<@U03VBV710JY> on:{오늘 날짜}`
- include_context: false
- sort: timestamp
- sort_dir: desc
- limit: 20
- response_format: detailed

결과가 20개 이상이면 cursor로 다음 페이지를 모두 가져온다.

**검색 4 — 봇 알림 채널 직접 읽기:**

Constants의 봇 알림 채널은 검색 API로 멘션을 잡을 수 없다 (봇이 attachment/block 형태로 보내서 텍스트가 비어있음).
`mcp__claude_ai_Slack__slack_read_channel`로 직접 읽는다:
- channel_id: 각 봇 알림 채널 ID
- oldest: 오늘 00:00:00 KST의 Unix timestamp
- response_format: concise

읽은 메시지 중에서 `<@U03VBV710JY>` 멘션이 포함된 스레드만 추출한다.

### Phase 2: 고유 스레드 목록 구성

**검색 1 결과** (스레드 답장):
- 각 메시지의 permalink에서 `thread_ts` 파라미터를 추출 → 부모 메시지 timestamp
- `channel_id`와 `thread_ts`를 추출
- 동일 thread_ts는 하나로 합침 (중복 제거)

**검색 2 결과** (최상위 메시지):
- 답장이 있는 메시지만 포함 (reply_count > 0)
- `channel_id`와 `message_ts`를 추출

**검색 3 결과** (멘션된 메시지):
- 각 메시지의 permalink에서 `thread_ts` 파라미터가 있으면 추출 → 부모 메시지 timestamp
- `thread_ts`가 없으면 `message_ts`를 사용 (최상위 메시지에서 멘션된 경우)
- `channel_id`와 `parent_ts`를 추출

**검색 4 결과** (봇 알림 채널):
- 내 멘션이 포함된 메시지의 `thread_ts` 또는 `message_ts`를 추출
- `channel_id`와 `parent_ts`를 추출

모든 결과를 합치고 `channel_id + parent_ts` 기준으로 중복 제거한다.

### Phase 3: 스레드 읽기 + 링크 추출

**3-1. 검색 스니펫에서 먼저 URL 패턴 매칭:**
- GitHub PR: `https://github.com/.*/pull/\d+`
- Linear issue: `https://linear.app/.*/issue/[A-Z]+-\d+`
- Notion page: `https://(www\.)?notion\.so/.*`

**3-2. 스니펫에서 링크를 못 찾은 스레드 또는 요약이 필요한 스레드는 전체 읽기:**

`mcp__claude_ai_Slack__slack_read_thread`로 스레드의 모든 메시지를 읽는다.
- response_format: concise
- 모든 메시지에서 URL 패턴을 검색한다.

**3-3. Slack permalink 생성:**

부모 메시지의 `message_ts`에서 `.`을 제거하여 permalink 생성:
`https://flex-cv82520.slack.com/archives/{channel_id}/p{ts_without_dot}`

### Phase 4: 요약 + 출력

**정렬**: `parent_ts` 기준 오름차순 (오래된 순).

**각 스레드에 대해 다음 포맷으로 출력:**

```markdown
N. **한줄 요약** ([thread](slack_permalink))
   - 스레드 요약 설명 (자세하게 — 누가, 무엇을, 왜, 결론 포함)
   - 링크
     - https://github.com/org/repo/pull/123
     - https://linear.app/flexteam/issue/CORE-1234 (이슈 제목)
     - https://www.notion.so/page-id
```

**규칙:**
- 한줄 요약: 스레드의 핵심 주제를 한 문장으로
- 요약 설명: 스레드 내용을 자세히 서술. 참여자, 결정사항, 배경 포함
- 링크: 스레드에서 발견된 GitHub PR, Linear 이슈, Notion 페이지만 포함
- 링크가 없는 스레드는 "링크" 섹션 생략
- Linear 이슈는 괄호 안에 이슈 제목 간략히 표기

**전체 출력 형식:**

```markdown
## 오늘의 활동 요약 (YYYY-MM-DD)

1. **한줄 요약** ([thread](slack_permalink))
   - 자세한 요약
   - 링크
     - url1
     - url2

2. **한줄 요약** ([thread](slack_permalink))
   - 자세한 요약
```

## 중요 사항

- 모든 스레드를 시간순(오래된 순)으로 출력한다.
- 각 스레드마다 한줄 요약 + 자세한 설명 + 링크를 제공한다.
- 같은 URL이 여러 스레드에서 발견되어도 각 스레드에서 별도로 출력한다.
- 오늘 활동이 없으면: "오늘 Slack 활동이 없습니다." 출력
- 스레드 읽기 실패 시 해당 스레드는 Slack permalink와 "읽기 실패"만 출력
