---
name: test-package
description: 'flex 모노레포 패키지의 로컬 테스트 환경을 yarn portal: 프로토콜로 설정한다. 사용자가 "test package", "패키지 테스트", "로컬 패키지 연결", "portal 연결"을 요청할 때 트리거. workspace:* 참조를 portal:로 변경하고 application package.json을 갱신, 패키지 빌드 후 install. flex-frontend-packages·services·design-system 지원.'
compatibility: 'yarn + Flex monorepo 구조 (apps/* + flex-frontend-packages 등 인접 디렉토리)'
disable-model-invocation: true
---

# Test Package

This skill helps set up local testing environments for monorepo packages by linking them to application repositories using the portal protocol.

## Overview

When developing packages locally, you need to test them in actual applications before publishing. This skill automates the process of:
1. Changing package references from `workspace:*` to `portal:` protocol
2. Updating application package.json to use local package paths
3. Building and installing packages for testing

## Supported Package Repositories

- **flex-frontend-packages**: 공용 유틸·패키지 (`@flex-packages/*`)
- **flex-frontend-services**: 서비스 레이어 (`@flex-services/*`)
- **flex-frontend-design-system**: 디자인 시스템 (`@flex-ds/*`)

## Workflow

1. **정보 수집** — 패키지 레포·패키지 이름·application 경로·application package.json의 패키지 이름을 사용자에게 묻는다
2. **패키지 레포 검증** — `/Users/hyuntae/Projects/flex/flex-frontend-{packages,services,design-system}` 중 존재하는 것을 사용
3. **전체 빌드** — `cd "$PACKAGE_REPO" && yarn turbo build` (첫 실행)
4. **protocol 전환** — `yarn packages:change-protocol --protocol=portal` 로 `workspace:*` → `portal:` 로 교체. 원복은 `--protocol=workspace`
5. **application package.json 갱신** — 대상 패키지 reference를 `portal:<application→package 상대 경로>` 로 변경
6. **application install** — `cd "$APPLICATION_REPO" && yarn install` 로 symlink 생성
7. **변경 후 재빌드** — `yarn turbo build --filter={package-name}` (symlink 덕에 application은 즉시 반영)
8. **완료 보고** — 패키지 레포·패키지명·application 경로·portal reference·재빌드 안내

질문 템플릿, 검증 스크립트, package.json before/after 예시, 상대 경로 계산 알고리즘은 [references/PACKAGES.md](references/PACKAGES.md) 참고.

## Error Handling

다음 케이스에서 사용자에게 명확한 메시지로 안내한 뒤 종료한다 (각 메시지 원문은 [references/PACKAGES.md](references/PACKAGES.md)):

- 패키지 레포 디렉토리 없음
- 대상 패키지가 레포에 없음
- `packages:change-protocol` 스크립트 미존재
- turbo 미설치
- application package.json 없음
