---
name: test-package
description: 모노레포 패키지의 로컬 테스트 환경을 portal 프로토콜로 설정합니다
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

- **flex-frontend-packages**: Shared utilities and common packages
- **flex-frontend-services**: Service layer packages
- **flex-frontend-design-system**: Design system components

## Workflow

### 1. Gather Information

Ask the user for required information:

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

### 2. Validate Package Repository

```bash
# Check if package repository exists
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

### 3. Build All Packages (First Time)

```bash
cd "$PACKAGE_REPO"

# Run full build first
yarn turbo build
```

This ensures all packages and their dependencies are built.

### 4. Change Protocol to Portal

```bash
cd "$PACKAGE_REPO"

# Change workspace:* to portal:path
yarn packages:change-protocol --protocol=portal
```

This script will:
- Find all `workspace:*` references in package.json files
- Replace them with `portal:../relative/path` references
- Allow packages to be symlinked from local filesystem

**Note:** To revert back to workspace protocol:
```bash
yarn packages:change-protocol --protocol=workspace
```

### 5. Update Application package.json

Locate the package in the application's package.json and update its reference:

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

**Steps:**
1. Read the application's package.json
2. Find the target package in dependencies
3. Calculate the relative path from application to package
4. Update the version to `portal:relative/path`
5. Write back to package.json

### 6. Install in Application

```bash
cd "$APPLICATION_REPO"

# Install with new portal reference
yarn install
```

This will create a symlink from the application's node_modules to the local package.

### 7. Rebuild Target Package for Changes

After making changes to the package, rebuild only that package:

```bash
cd "$PACKAGE_REPO"

# Build only the changed package
yarn turbo build --filter={package-name}
```

Example:
```bash
yarn turbo build --filter=@flex-packages/utils
```

The changes will be immediately reflected in the application since it's symlinked.

### 8. Confirm Setup

Show the user:
- Package repository path
- Package name
- Application repository path
- Portal reference used
- Instructions for rebuilding after changes

## Relative Path Calculation

Calculate the relative path from application to package:

```bash
# Example paths:
# Application: /Users/hyuntae/Projects/flex/flex-frontend-apps-performance-management
# Package: /Users/hyuntae/Projects/flex/flex-frontend-packages/packages/utils

# Relative path: ../../flex-frontend-packages/packages/utils
```

**Algorithm:**
1. Find common ancestor directory
2. Count directories up from application to ancestor
3. Count directories down from ancestor to package
4. Build relative path with `../` for each up, then append down path

## Error Handling

### Package repository not found
```
Error: Package repository not found at {path}
Please ensure the repository is cloned and accessible.
```

### Package not found
```
Error: Package {name} not found in {repo}
Available packages:
- @flex-packages/utils
- @flex-packages/api
...
```

### Protocol script not available
```
Error: Script 'packages:change-protocol' not found in package.json
This script is required for changing workspace protocol.
```

### Turbo not available
```
Error: Turbo not found. Please ensure turbo is installed:
yarn add -D turbo
```

### Application package.json not found
```
Error: package.json not found in {application_path}
Please check the application path is correct.
```
