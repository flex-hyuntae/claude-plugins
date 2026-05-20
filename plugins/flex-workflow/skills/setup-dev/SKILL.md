---
name: setup-dev
description: 'flex frontend 앱(remotes-*) 개발 환경을 한 번에 부트스트랩한다. 사용자가 "setup dev", "개발 환경 띄워줘", "dev 띄우기", "/setup-dev <앱이름>", "<앱> 개발 환경" 형태로 호출하면 트리거. yarn install → web-applications/remotes-<app>/.env.local 보장(.env.example 복사) → yarn turbo run dev --filter="@flex-apps/remotes-<app>" 순서로 실행. worktree 진입 직후 의존성·env·dev 서버 부팅이 한 커맨드로 끝나도록.'
compatibility: 'flex-frontend-apps-* 모노레포 (web-applications/remotes-* 구조, turbo + yarn workspaces)'
argument-hint: "<appname> (예: brain, ai, custom-page — 'remotes-' 접두사 있어도 OK)"
---

# Setup Dev

flex 모노레포(`flex-frontend-apps-*`)에서 특정 remote 앱의 개발 환경을 부트스트랩한다.

## 0. 인자 정규화

사용자가 넘긴 `<appname>` 을 정규화한다:

- `brain`, `ai`, `custom-page` 등 단순 이름 → 그대로 사용
- `remotes-brain` → `brain` (접두사 제거)
- `@flex-apps/remotes-brain` → `brain` (스코프·접두사 제거)

이후 흐름에서 정규화된 이름을 `<app>` 으로 부른다.

인자가 비어있으면 다음 안내 후 중단:

> 어느 앱을 띄울지 알려주세요. 예: `/flex-workflow:setup-dev brain`. 사용 가능한 앱은 `web-applications/remotes-*` 디렉토리에서 확인 가능합니다.

## 1. 모노레포 루트 확인

현재 cwd 가 flex frontend 모노레포 루트인지 확인:

```bash
test -f package.json && test -d web-applications
```

둘 다 통과하지 않으면 다음 안내 후 중단:

> 모노레포 루트에서 실행해주세요. (`package.json` 과 `web-applications/` 가 함께 있는 디렉토리)

## 2. 대상 앱 디렉토리 검증

```bash
APP_DIR="web-applications/remotes-<app>"
test -d "$APP_DIR" && test -f "$APP_DIR/package.json"
```

없으면 어떤 후보가 있는지 보여주고 중단:

```bash
ls web-applications/ | grep ^remotes- | sed 's/^remotes-//'
```

> `<app>` 에 해당하는 앱을 찾지 못했습니다. 위 목록 중에서 골라주세요.

## 3. yarn install

```bash
yarn
```

이미 install 된 worktree 일 수 있어도 worktree 마다 독립적으로 가져가는 게 안전하므로 무조건 실행한다. 실패하면 stderr 첫 20줄을 사용자에게 보여주고 중단.

## 4. .env.local 보장

```bash
ENV_LOCAL="$APP_DIR/.env.local"
ENV_EXAMPLE="$APP_DIR/.env.example"

if [ -f "$ENV_LOCAL" ]; then
  echo "✓ $ENV_LOCAL 이미 존재 — 건드리지 않음"
elif [ -f "$ENV_EXAMPLE" ]; then
  cp "$ENV_EXAMPLE" "$ENV_LOCAL"
  echo "✓ $ENV_EXAMPLE → $ENV_LOCAL 복사 완료"
else
  echo "⚠ $ENV_EXAMPLE 도 $ENV_LOCAL 도 없음 — env 설정 없이 진행"
fi
```

기존 `.env.local` 은 절대 덮어쓰지 않는다 (사용자가 직접 채운 값 보존).

## 5. Dev 서버 부팅

```bash
yarn turbo run dev --filter="@flex-apps/remotes-<app>"
```

이 명령은 long-running 이므로 **background 로 실행**한다 (Bash tool 의 `run_in_background: true`). 사용자가 직접 끌 때까지 살아있어야 함.

부팅 직후 stdout 첫 몇 줄에 포트·URL 이 찍히면 그걸 사용자에게 보고한다.

## 6. 완료 보고

다음 형식으로 요약:

```
✅ setup-dev 완료 (<app>)
- yarn install: ok
- .env.local: <복사함 | 이미 있었음 | example 없음>
- dev 서버: background 로 부팅 중 (filter @flex-apps/remotes-<app>)
  → 로그 추적: BashOutput 으로 확인 가능
  → URL: <감지된 경우>
```

## 주의

- 이 스킬은 **반드시 모노레포 루트** 에서 호출되어야 한다. 서브패키지 안에서 호출하면 2번 검증에서 막힘.
- worktree 안에서 호출해도 동일하게 동작한다 (worktree 자체가 완전한 체크아웃이므로).
- `.envrc` (direnv) 가 있는 레포는 별도로 `direnv allow` 가 필요할 수 있음 — 본 스킬은 손대지 않는다.
