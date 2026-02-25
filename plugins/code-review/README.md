# code-review

종합 코드 리뷰 플러그인. SOLID 원칙, React/TypeScript 모범 사례 기반으로 PR을 리뷰하고 GitHub에 한국어 코멘트를 작성합니다.

## 에이전트

| 에이전트 | 설명 |
|----------|------|
| `code-review` | PR URL을 받아 15개 카테고리 기반 종합 코드 리뷰 수행, S1/S2/S3 심각도별 GitHub 코멘트 작성 |

> 에이전트는 슬래시 커맨드가 아닌, 사용자의 의도를 인식하여 자동으로 실행됩니다.

## 사용 예시

### code-review

```
코드 리뷰 해줘
코드 리뷰 해줘 https://github.com/owner/repo/pull/123
```

PR의 모든 파일을 분석하여 SOLID, React, TypeScript, 성능, 접근성, 보안 등 15개 카테고리로 리뷰합니다. 이슈는 해당 라인에 직접 코멘트로 남기고, 전체 요약을 제출합니다.
