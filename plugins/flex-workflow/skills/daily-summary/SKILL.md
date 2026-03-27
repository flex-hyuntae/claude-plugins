---
name: daily-summary
description: "오늘 참여한 Slack 스레드를 시간순으로 요약하고, GitHub PR/Linear/Notion 링크를 추출한다."
---

# Daily Summary

Slack Activity 탭(종 아이콘)의 All/Mentions/Threads/Reactions 데이터를 최대한 캡처하여, 오늘의 활동을 시간순으로 요약한다.

## Constants

- **Slack User ID**: `U03VBV710JY`
- **Workspace**: `flex-cv82520.slack.com`
- **날짜**: 오늘 (YYYY-MM-DD)
- **LOOKBACK_DAYS**: 7 (최근 참여 스레드 탐색 범위)
- **GitHub DM**: `D040QG6LW95`
- **REACTION_EMOJIS**: `thumbsup`, `eyes`, `white_check_mark`
- **봇 알림 채널 (직접 읽기 필요)**:
  - `C02CWLDRP6F` — #alarm-git-pr-frontend (GitHub 봇이 attachment로 멘션하므로 검색 불가)
  - `C03B26ULE21` — 배포 알림 채널 (dev-bot, attachment 형태)
  - `CR2CWKF8Q` — 배포 알림 채널 (dev-bot, attachment 형태)

## Workflow

### Phase 1: Activity 카테고리별 수집

1A~1G를 **병렬로** 실행한다.

**1A — 멘션 (Activity > Mentions):**

`mcp__claude_ai_Slack__slack_search_public_and_private`로 검색:
- query: `to:<@U03VBV710JY> on:{오늘 날짜}`
- include_context: false
- sort: timestamp
- sort_dir: desc
- limit: 20
- response_format: detailed

**1B — 오늘 답장한 스레드:**

`mcp__claude_ai_Slack__slack_search_public_and_private`로 검색:
- query: `from:<@U03VBV710JY> is:thread on:{오늘 날짜}`
- include_context: false
- sort: timestamp
- sort_dir: desc
- limit: 20
- response_format: detailed

**1C — 오늘 시작한 최상위 메시지:**

`mcp__claude_ai_Slack__slack_search_public_and_private`로 검색:
- query: `from:<@U03VBV710JY> -is:thread on:{오늘 날짜}`
- include_context: false
- sort: timestamp
- sort_dir: desc
- limit: 20
- response_format: detailed

**1D — 최근 참여 스레드 (Activity > Threads 근사):**

"팔로잉 중인 스레드" 목록을 근사하기 위해, 최근 7일간 참여한 스레드를 모두 수집한다.

`mcp__claude_ai_Slack__slack_search_public_and_private`로 2개 검색 병렬 실행:

검색 1:
- query: `from:<@U03VBV710JY> is:thread after:{7일 전 날짜}`
- include_context: false
- sort: timestamp
- sort_dir: desc
- limit: 20
- response_format: detailed

검색 2:
- query: `from:<@U03VBV710JY> -is:thread after:{7일 전 날짜}`
- include_context: false
- sort: timestamp
- sort_dir: desc
- limit: 20
- response_format: detailed

두 검색 모두 페이지네이션으로 전체 결과를 수집한다. 결과에서 `(channel_id, parent_ts)` 쌍을 추출하여 "최근 참여 스레드 후보 목록"을 구성한다.

**1E — 봇 알림 채널 직접 읽기:**

Constants의 봇 알림 채널은 검색 API로 멘션을 잡을 수 없다 (봇이 attachment/block 형태로 보내서 텍스트가 비어있음).
`mcp__claude_ai_Slack__slack_read_channel`로 직접 읽는다:
- channel_id: 각 봇 알림 채널 ID
- oldest: 오늘 00:00:00 KST의 Unix timestamp
- response_format: detailed
- limit: 100

봇 채널 메시지의 텍스트는 비어있으므로, 스레드가 있는 메시지(reply_count > 0이고 오늘 답글이 있는)를 추출한다.
해당 스레드의 replies를 `slack_read_thread`로 읽어서 `<@U03VBV710JY>` 멘션이 포함된 스레드만 포함한다.
텍스트에서 멘션을 못 찾으면: GitHub DM 데이터(1F)에서 추출한 PR URL과 매칭하여 관련 스레드를 식별한다.

**1F — GitHub DM 읽기 (Activity > Apps):**

`mcp__claude_ai_Slack__slack_read_channel`로 읽기:
- channel_id: `D040QG6LW95`
- oldest: 오늘 00:00:00 KST의 Unix timestamp
- response_format: detailed
- limit: 100

Review assigned, PR comment, CI/CD 알림 등 GitHub 앱 알림을 캡처한다. PR URL을 추출하여 봇 채널 스레드(1E)와 매칭에 활용한다.

**1G — 리액션 근사 (Activity > Reactions, best-effort):**

`mcp__claude_ai_Slack__slack_search_public_and_private`로 3개 검색 병렬 실행:
- query: `from:<@U03VBV710JY> has::thumbsup: on:{오늘 날짜}`
- query: `from:<@U03VBV710JY> has::eyes: on:{오늘 날짜}`
- query: `from:<@U03VBV710JY> has::white_check_mark: on:{오늘 날짜}`

각 검색 공통:
- include_context: false
- sort: timestamp
- sort_dir: desc
- limit: 20
- response_format: detailed

**페이지네이션 (모든 검색에 적용):**

1A~1G 각각에 대해, 결과가 20개이면 반드시 cursor로 **모든 후속 페이지를 끝까지** 가져온다. 특히 1A(멘션)은 DM/Group DM 메시지가 결과 앞쪽을 차지하여 채널 스레드 멘션이 뒤 페이지로 밀리기 쉽다. 결과가 20개 미만이 나올 때까지 반드시 모든 페이지를 순회한다.

### Phase 2: 스레드 활동 검증

Phase 1 전체 결과에서 등장한 **고유 channel_id 목록**을 추출한다. (DM, Group DM 채널은 제외 — channel ID가 `D`나 Group DM으로 시작하는 것 제외)

핵심: 1D(7일 참여 스레드)에서 발견된 채널도 포함하므로, 기존보다 훨씬 넓은 범위를 스캔한다.

이 채널 목록 각각에 대해 `mcp__claude_ai_Slack__slack_read_channel`로 오늘 메시지를 읽는다:
- oldest: 오늘 00:00:00 KST의 Unix timestamp
- response_format: concise
- limit: 100

읽은 결과에서:
1. 오늘 활동이 있는 스레드를 추출한다 (thread_ts가 있는 메시지 또는 reply_count > 0인 부모 메시지)
2. 1D의 "최근 참여 스레드 후보 목록"과 교차: 오늘 활동이 있는 스레드만 포함
3. 1A~1C에서 이미 발견된 스레드는 스킵 (short-circuit)
4. 후보 목록에 없는 새 스레드는: `slack_read_thread`로 읽어서, 다음 조건 중 하나라도 만족하는 스레드만 포함:
   - `<@U03VBV710JY>` 직접 멘션이 있는 스레드
   - 유저(`U03VBV710JY`)가 메시지를 작성한 적 있는 스레드

### Phase 3: 고유 스레드 목록 구성

**1A 결과** (멘션):
- 각 메시지의 permalink에서 `thread_ts` 파라미터가 있으면 추출 → 부모 메시지 timestamp
- `thread_ts`가 없으면 `message_ts`를 사용 (최상위 메시지에서 멘션된 경우)
- `channel_id`와 `parent_ts`를 추출

**1B 결과** (스레드 답장):
- 각 메시지의 permalink에서 `thread_ts` 파라미터를 추출 → 부모 메시지 timestamp
- `channel_id`와 `thread_ts`를 추출
- 동일 thread_ts는 하나로 합침 (중복 제거)

**1C 결과** (최상위 메시지):
- 답장이 있는 메시지만 포함 (reply_count > 0)
- `channel_id`와 `message_ts`를 추출

**1E 결과** (봇 알림 채널):
- 유저 관련 PR 스레드의 `thread_ts` 또는 `message_ts`를 추출
- `channel_id`와 `parent_ts`를 추출

**1F 결과** (GitHub DM):
- PR URL과 관련 메시지의 `message_ts`를 추출
- 봇 채널(1E) 스레드와 매칭에 사용

**1G 결과** (리액션):
- 스레드에 속한 메시지는 `thread_ts`를 추출
- 최상위 메시지는 `message_ts`를 사용
- `channel_id`와 `parent_ts`를 추출

**Phase 2 결과** (스레드 활동 검증):
- 오늘 활동이 확인된 스레드의 `channel_id`와 `parent_ts`를 추가

모든 결과를 합치고 `channel_id + parent_ts` 기준으로 중복 제거한다.

### Phase 4: 스레드 읽기 + 링크 추출

**4-1. 검색 스니펫에서 먼저 URL 패턴 매칭:**
- GitHub PR: `https://github.com/.*/pull/\d+`
- Linear issue: `https://linear.app/.*/issue/[A-Z]+-\d+`
- Notion page: `https://(www\.)?notion\.so/.*`

**4-2. 스니펫에서 링크를 못 찾은 스레드 또는 요약이 필요한 스레드는 전체 읽기:**

`mcp__claude_ai_Slack__slack_read_thread`로 스레드의 모든 메시지를 읽는다.
- response_format: concise
- 모든 메시지에서 URL 패턴을 검색한다.

**4-3. 봇 채널 스레드 처리:**

봇 알림 채널(C02CWLDRP6F, C03B26ULE21, CR2CWKF8Q)의 스레드는 텍스트가 비어있을 수 있다.
이 경우 GitHub DM 데이터(1F)에서 매칭된 PR URL을 사용하거나, "GitHub PR notification" 으로 표기한다.

**4-4. Slack permalink 생성:**

부모 메시지의 `message_ts`에서 `.`을 제거하여 permalink 생성:
`https://flex-cv82520.slack.com/archives/{channel_id}/p{ts_without_dot}`

### Phase 5: 요약 + 출력

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

## Known Limitations

- **과거 메시지 리액션**: 과거에 작성한 메시지에 오늘 달린 리액션은 캡처 불가 (Slack 검색 API가 리액션 추가 시점을 필터링하지 못함). 단, 대부분의 리액션 대상 메시지는 다른 수집 전략(1A~1D)으로 이미 캡처됨.
- **팔로잉만 한 스레드**: 직접 참여/멘션 없이 팔로잉만 한 스레드는 캡처 불가 (Slack API에 "followed threads" 조회 기능 없음).
- **비-GitHub 앱 알림**: Google Calendar 등 GitHub 외 앱 알림은 미포함.

## 중요 사항

- 모든 스레드를 시간순(오래된 순)으로 출력한다.
- 각 스레드마다 한줄 요약 + 자세한 설명 + 링크를 제공한다.
- 같은 URL이 여러 스레드에서 발견되어도 각 스레드에서 별도로 출력한다.
- 오늘 활동이 없으면: "오늘 Slack 활동이 없습니다." 출력
- 스레드 읽기 실패 시 해당 스레드는 Slack permalink와 "읽기 실패"만 출력
- 봇 채널 스레드의 텍스트가 비어있으면 "GitHub PR notification"으로 표기하고, 가능한 경우 GitHub DM에서 매칭된 PR 정보를 포함한다.
