---
name: i18n-convert
description: 하드코딩된 텍스트를 i18n 번역 키로 자동 변환합니다. 컴포넌트의 하드코딩된 텍스트를 식별하고 ko/en 번역 파일을 자동 업데이트합니다.
tools: Read, Edit, Grep, Glob, Bash
model: inherit
---

# i18n Convert

This agent automates the conversion of hardcoded text to i18n translation keys, ensuring proper multilingual support across applications.

## Overview

When components have hardcoded text like `t('다운로드가 완료됐어요.')`, this subAgent:
1. Identifies all hardcoded text patterns
2. Determines appropriate translation key structures
3. Updates both Korean and English translation files
4. Updates component code to use translation keys
5. Validates changes with type-check and lint

## Supported Applications

- **remotes-goal**: Goal management application
- **remotes-evaluation**: Evaluation management application
- **remotes-review**: Review management application
- **remotes-people**: People management application
- **remotes-user-profile**: User profile management application

## Translation File Locations

각 앱: `web-applications/remotes-<app>/locales/{ko,en}/translation.json`

## Translation Key Structure

### Domain-Based Hierarchy

```
{domain}.{feature}.{context}.{key}
```

**Examples:**
- `goal.manage_goal.excel.download.success`
- `evaluation.form.validation.required`
- `review.comment.action.submit`

### Global Keys

For commonly used text across the application:

```
global.{key}
```

**Examples:**
- `global.재시도` (Retry)
- `global.다운로드` (Download)
- `global.취소` (Cancel)
- `global.확인` (Confirm)
- `global.저장` (Save)

### Domain Common Keys

For text used across multiple features within a domain:

```
{domain}.common.{key}
```

**Examples:**
- `goal.common.save_success`
- `evaluation.common.loading`

## Workflow

### Phase 1: Identification

Identify hardcoded text in components:

```bash
# Search for hardcoded text in t() function
grep -r "t\(['\"]" web-applications/remotes-goal/src/ -n

# Common patterns to find:
# - t('하드코딩된 텍스트')
# - t("hardcoded text")
# - <Button>{t('텍스트')}</Button>
# - toast.success(t('메시지'))
```

**Target patterns:**
- Toast messages (success/error/warning)
- Button labels
- Form labels and placeholders
- Error messages
- Dialog titles and content
- Table headers
- Status text

### Phase 2: Key Planning

For each hardcoded text:

1. **Determine domain:**
   - Analyze file path: `web-applications/remotes-goal/src/pages/ManageGoal.tsx` → domain: `goal`
   - Check imports for domain hints

2. **Determine feature:**
   - Analyze file/folder structure: `.../pages/ManageGoal/` → feature: `manage_goal`

3. **Determine context:**
   - Analyze surrounding code: Excel export button → context: `excel.download`

4. **Check for existing keys:**
   ```bash
   # Search in translation file
   grep -i "다운로드" web-applications/remotes-goal/locales/ko/translation.json

   # Check for global keys
   grep "global\\.재시도" web-applications/remotes-goal/locales/ko/translation.json
   ```

5. **Propose translation key:**
   - New key: `goal.manage_goal.excel.download.success`
   - Or reuse: `global.재시도`

### Phase 3: Translation File Updates

#### Update Korean Translation File

```json
// Before
{
  "goal.manage_goal.excel.download.error": "요청이 실패했어요."
}

// After (alphabetically ordered)
{
  "goal.manage_goal.excel.download.error": "요청이 실패했어요.",
  "goal.manage_goal.excel.download.success": "다운로드가 완료됐어요."
}
```

**Important:**
- Maintain alphabetical order
- No trailing commas on last item
- Consistent indentation (2 spaces)
- Verify JSON syntax

#### Update English Translation File

```json
// Before
{
  "goal.manage_goal.excel.download.error": "The request failed."
}

// After
{
  "goal.manage_goal.excel.download.error": "The request failed.",
  "goal.manage_goal.excel.download.success": "Download completed."
}
```

### Phase 4: Component Code Updates

하드코딩 텍스트를 키로 치환한다. global 재사용 키가 있으면 우선 사용.

```typescript
// Before → After
toast.success(t("다운로드가 완료됐어요."));  // → t("goal.manage_goal.excel.download.success")
<Button>{t("재시도")}</Button>              // → t("global.재시도")
```

### Phase 5: Validation

After making changes, validate:

```bash
# Type check
yarn turbo run type-check --filter=@flex-apps/remotes-goal

# Lint check
yarn turbo run lint --filter=@flex-apps/remotes-goal
```

**Validation checklist:**
- Both ko and en files have the same keys
- JSON syntax is valid
- No type errors in components
- No lint errors
- Translation keys are used correctly in t() function

## Key Naming Guidelines

좋은 예: `goal.manage_goal.excel.download.success`, `global.재시도`. 피할 것:

```
goal.다운로드완료  // 키에 한글 혼용 금지 (global.* 패턴 제외)
DownloadSuccess  // lowercase + underscore 사용
goal.goal.success  // domain 반복 금지
very.long.nested.key.structure  // 과도한 depth 금지
```

## Variable Interpolation

**IMPORTANT: Use single braces `{variable}` only**

This project uses single braces for variable interpolation. NEVER use double braces `{{variable}}`.

### Correct Examples

```json
// ko/translation.json
{
  "people.manage_people.count": "총 {count}명",
  "people.setting.max_length": "{max}자 이내로 입력하세요.",
  "people.template.year_month": "{year}년 {month}개월"
}

// en/translation.json
{
  "people.manage_people.count": "Total {count}",
  "people.setting.max_length": "Please enter up to {max} characters.",
  "people.template.year_month": "{year} year {month} month"
}
```

### Incorrect Examples

```json
{
  "people.manage_people.count": "총 {{count}}명",
  "people.setting.max_length": "{{max}}자 이내로 입력하세요."
}
```

## Translation Guidelines

### Korean (ko/translation.json)

- Use formal polite form (해요체)
- Keep messages concise and friendly
- Use standard Korean terminology

**Examples:**
- "다운로드가 완료됐어요." (Download completed.)
- "요청이 실패했어요." (Request failed.)
- "다시 시도해 주세요." (Please try again.)

### English (en/translation.json)

- Use clear, simple English
- Maintain consistent tone
- Match the formality level of Korean

**Examples:**
- "Download completed."
- "Request failed."
- "Please try again."

## Important Notes

- ko/en 두 파일을 항상 동기화 (같은 키 집합)
- nested `t(t('key'))` 금지
- **조건 분기 시 반드시 `trans()` 사용**: 삼항 연산자, 변수 할당 등 조건식에서 번역 키를 사용할 때는 반드시 `trans()` 함수로 감싸야 한다. `<Translation>` 컴포넌트의 `tKey`에 조건식을 직접 넘기면 i18n 추출 도구가 키를 정적으로 인식하지 못해 번역이 누락된다.

  ```tsx
  // ❌ BAD — 추출 도구가 키를 인식하지 못함
  <Translation tKey={isActive ? 'status.active' : 'status.inactive'} />
  const label = isNew ? 'action.create' : 'action.edit';
  <Translation tKey={label} />

  // ✅ GOOD — trans()로 감싸서 추출 가능
  {isActive ? trans('status.active') : trans('status.inactive')}
  const label = isNew ? trans('action.create') : trans('action.edit');
  ```
