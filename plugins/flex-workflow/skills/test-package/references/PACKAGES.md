# Test Package — 패키지 매트릭스 및 상세 절차

## 지원 패키지 레포

| 레포 | 패키지 prefix | 경로 |
|------|--------------|------|
| flex-frontend-packages | `@flex-packages/*` | `/Users/hyuntae/Projects/flex/flex-frontend-packages` |
| flex-frontend-services | `@flex-services/*` | `/Users/hyuntae/Projects/flex/flex-frontend-services` |
| flex-frontend-design-system | `@flex-ds/*` | `/Users/hyuntae/Projects/flex/flex-frontend-design-system` |

## 1. 정보 수집 질문 템플릿

```
Which package repository do you want to test?
1. flex-frontend-packages
2. flex-frontend-services
3. flex-frontend-design-system
```

```
What is the package name you want to test?
(e.g., @flex-packages/utils, @flex-services/api, @flex-ds/button)
```

```
What is the path to your application repository?
(e.g., /Users/hyuntae/Projects/flex/flex-frontend-apps-performance-management)
```

```
What is the package name in the application's package.json?
(Usually same as the package name, e.g., @flex-packages/utils)
```

## 2. 패키지 레포 유효성 검사

```bash
if [ -d "/Users/hyuntae/Projects/flex/flex-frontend-packages" ]; then
  PACKAGE_REPO="/Users/hyuntae/Projects/flex/flex-frontend-packages"
elif [ -d "/Users/hyuntae/Projects/flex/flex-frontend-services" ]; then
  PACKAGE_REPO="/Users/hyuntae/Projects/flex/flex-frontend-services"
elif [ -d "/Users/hyuntae/Projects/flex/flex-frontend-design-system" ]; then
  PACKAGE_REPO="/Users/hyuntae/Projects/flex/flex-frontend-design-system"
else
  echo "Error: Package repository not found"
  exit 1
fi
```

## 3. 첫 빌드 (전체 패키지)

```bash
cd "$PACKAGE_REPO"
yarn turbo build
```

## 4. protocol 전환

```bash
cd "$PACKAGE_REPO"
yarn packages:change-protocol --protocol=portal
```

- 모든 `workspace:*` 참조를 찾아 `portal:../relative/path` 로 교체
- 로컬 파일시스템 symlink가 가능해진다

원복:

```bash
yarn packages:change-protocol --protocol=workspace
```

## 5. Application package.json 갱신

**Before:**

```json
{
  "dependencies": {
    "@flex-packages/utils": "workspace:*"
  }
}
```

**After:**

```json
{
  "dependencies": {
    "@flex-packages/utils": "portal:../../flex-frontend-packages/packages/utils"
  }
}
```

절차:
1. application의 package.json 읽기
2. dependencies에서 대상 패키지 찾기
3. application → package 상대 경로 계산
4. version을 `portal:relative/path` 로 갱신
5. package.json 쓰기

### 상대 경로 계산 알고리즘

```
Application: /Users/hyuntae/Projects/flex/flex-frontend-apps-performance-management
Package: /Users/hyuntae/Projects/flex/flex-frontend-packages/packages/utils
→ ../../flex-frontend-packages/packages/utils
```

1. 공통 조상 디렉토리 찾기
2. application → 조상까지 올라가는 디렉토리 수 카운트
3. 조상 → package 까지 내려가는 경로 카운트
4. 위로 갈 때마다 `../`, 그 다음 down 경로 append

## 6. Application install

```bash
cd "$APPLICATION_REPO"
yarn install
```

application의 node_modules에 로컬 패키지 symlink가 생성된다.

## 7. 변경 후 재빌드 (대상 패키지만)

```bash
cd "$PACKAGE_REPO"
yarn turbo build --filter={package-name}
```

예:

```bash
yarn turbo build --filter=@flex-packages/utils
```

symlink 덕에 application은 즉시 반영된다.

## 8. 완료 보고

사용자에게 표시:
- 패키지 레포 경로
- 패키지 이름
- application 레포 경로
- 사용된 portal reference
- 변경 후 재빌드 방법 안내

## Error Handling 메시지

```
Error: Package repository not found at {path}
Please ensure the repository is cloned and accessible.

Error: Package {name} not found in {repo}
Available packages:
- @flex-packages/utils
- @flex-packages/api
...

Error: Script 'packages:change-protocol' not found in package.json
This script is required for changing workspace protocol.

Error: Turbo not found. Please ensure turbo is installed:
yarn add -D turbo

Error: package.json not found in {application_path}
Please check the application path is correct.
```
