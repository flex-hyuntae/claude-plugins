---
name: i18n-convert
description: 하드코딩된 텍스트를 i18n 번역 키로 자동 변환합니다. 컴포넌트의 하드코딩된 텍스트를 식별하고 ko/en 번역 파일을 자동 업데이트합니다.
tools: Read, Edit, Grep, Glob, Bash
model: inherit
---

# i18n Convert

`t('다운로드가 완료됐어요.')` 처럼 하드코딩된 텍스트를 번역 키로 치환하고 ko/en 번역 파일을 동기화한다.

번역 파일: `web-applications/remotes-<app>/locales/{ko,en}/translation.json`

## 키 구조

| 종류 | 형식 | 예시 |
|------|------|------|
| 기본 | `{domain}.{feature}.{context}.{key}` | `goal.manage_goal.excel.download.success` |
| 도메인 공통 (도메인 내 여러 feature 공용) | `{domain}.common.{key}` | `goal.common.save_success` |
| 글로벌 (앱 전역 공용) | `global.{key}` | `global.재시도`, `global.취소`, `global.확인` |

**피할 것**:

```
goal.다운로드완료          // 키에 한글 혼용 금지 (global.* 패턴 제외)
DownloadSuccess           // lowercase + underscore 사용
goal.goal.success         // domain 반복 금지
very.long.nested.key...   // 과도한 depth 금지
```

## Workflow

### 1. 식별

```bash
grep -r "t\(['\"]" web-applications/remotes-goal/src/ -n
```

**대상**: 토스트(success/error/warning) · 버튼 라벨 · 폼 라벨·placeholder · 에러 메시지 · 다이얼로그 제목·본문 · 테이블 헤더 · 상태 텍스트.

### 2. 키 계획

1. **domain** — 파일 경로에서 추론 (`remotes-goal/src/pages/ManageGoal.tsx` → `goal`), import 도 힌트
2. **feature** — 파일·폴더 구조에서 (`.../pages/ManageGoal/` → `manage_goal`)
3. **context** — 주변 코드에서 (Excel export 버튼 → `excel.download`)
4. **기존 키 확인** — 번역 파일에서 텍스트·`global.*` 를 grep. 재사용 가능하면 신규 발급 금지
5. 신규 키 제안 또는 기존 키 재사용 결정

### 3. 번역 파일 업데이트

ko/en 양쪽에 같은 키를 추가한다. **알파벳 순서 유지** · 2 스페이스 인덴트 · JSON 문법 검증.

### 4. 컴포넌트 치환

global 재사용 키가 있으면 우선 사용.

```typescript
// Before → After
toast.success(t("다운로드가 완료됐어요."));  // → t("goal.manage_goal.excel.download.success")
<Button>{t("재시도")}</Button>              // → t("global.재시도")
```

### 5. 검증

```bash
yarn turbo run type-check --filter=@flex-apps/remotes-goal
yarn turbo run lint --filter=@flex-apps/remotes-goal
```

## 규칙

- **ko/en 항상 동기화** (같은 키 집합)
- **변수 보간은 단일 중괄호 `{variable}` 만** — 이 프로젝트는 `{{variable}}` 를 쓰지 않는다. 예: `"총 {count}명"` / `"{max}자 이내로 입력하세요."`
- ko 문구는 **해요체** ("다운로드가 완료됐어요."), en 은 ko 와 같은 격식 수준
- nested `t(t('key'))` 금지
- **조건 분기 시 반드시 `trans()` 사용** — `<Translation>` 의 `tKey` 에 조건식을 직접 넘기면 i18n 추출 도구가 키를 정적으로 인식하지 못해 번역이 누락된다

  ```tsx
  // ❌ BAD — 추출 도구가 키를 인식하지 못함
  <Translation tKey={isActive ? 'status.active' : 'status.inactive'} />
  const label = isNew ? 'action.create' : 'action.edit';
  <Translation tKey={label} />

  // ✅ GOOD — trans()로 감싸서 추출 가능
  {isActive ? trans('status.active') : trans('status.inactive')}
  const label = isNew ? trans('action.create') : trans('action.edit');
  ```
