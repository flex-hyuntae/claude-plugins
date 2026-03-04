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

```
web-applications/
├── remotes-goal/
│   └── locales/
│       ├── ko/translation.json
│       └── en/translation.json
├── remotes-evaluation/
│   └── locales/
│       ├── ko/translation.json
│       └── en/translation.json
├── remotes-review/
│   └── locales/
│       ├── ko/translation.json
│       └── en/translation.json
├── remotes-people/
│   └── locales/
│       ├── ko/translation.json
│       └── en/translation.json
└── remotes-user-profile/
    └── locales/
        ├── ko/translation.json
        └── en/translation.json
```

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

#### Example 1: Toast Messages

```typescript
// Before
toast.success(t("다운로드가 완료됐어요."));
toast.error(t("요청이 실패했어요."));

// After
toast.success(t("goal.manage_goal.excel.download.success"));
toast.error(t("goal.manage_goal.excel.download.error"));
```

#### Example 2: Button Labels

```typescript
// Before
<Button>{t("재시도")}</Button>
<Button>{t("다운로드")}</Button>

// After
<Button>{t("global.재시도")}</Button>
<Button>{t("global.다운로드")}</Button>
```

#### Example 3: Form Validation

```typescript
// Before
const schema = z.object({
  name: z.string().min(1, t("이름을 입력해주세요"))
});

// After
const schema = z.object({
  name: z.string().min(1, t("goal.form.validation.name_required"))
});
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

### Good Examples

```
goal.manage_goal.excel.download.success
global.재시도
evaluation.form.validation.required
review.common.save_success
```

### Bad Examples

```
goal.다운로드완료  // Don't mix Korean in keys (except global.* pattern)
DownloadSuccess  // Use lowercase with underscores
goal.goal.success  // Don't repeat domain
very.long.nested.key.structure.that.is.hard.to.read  // Too deep
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

## File Size Considerations

Translation files can be large (3000+ lines). When editing:

1. **Read specific sections:**
   ```bash
   # Read lines around a specific key
   grep -A 5 -B 5 "key_name" locales/ko/translation.json
   ```

2. **Use Edit tool carefully:**
   - Ensure `old_string` is unique and exact
   - Include surrounding context for uniqueness
   - Verify JSON structure after edit

3. **Test after changes:**
   - Always run type-check and lint
   - Check application in browser if possible

## Important Notes

- **Always update both files**: Korean and English translations must be in sync
- **Maintain alphabetical order**: Makes it easier to find and manage keys
- **Avoid nested t() calls**: Don't use `t(t('key'))`
- **Check for duplicates**: Search existing keys before creating new ones
- **Use consistent naming**: Follow the domain.feature.context.key pattern
- **Validate thoroughly**: Run type-check and lint after changes
- **Test in browser**: Verify translations display correctly

## Batch Conversion Strategy

For large-scale conversion:

1. **Identify all hardcoded text** in one file/feature
2. **Group by context** (toast messages, button labels, etc.)
3. **Create all translation keys** at once in both files
4. **Update component code** systematically
5. **Validate** once at the end
6. **Test** in application

This approach is more efficient than converting one text at a time.
