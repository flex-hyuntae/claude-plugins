#!/usr/bin/env python3
"""Materialize the shared Drill instructions for Claude Code and Codex."""

from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHARED = ROOT / "shared" / "drill"
CLAUDE = ROOT / "plugins" / "drill"
CODEX = ROOT / "plugins" / "drill-codex"

CONTENT_DIRECTORIES = ("skills", "references", "templates")

CODEX_DELEGATION = """# Codex 하위 에이전트 위임

이 플러그인의 `drill-*` 분석 역할은 Claude의 고정 Agent 정의가 아니다. 각 역할 문서는 **Codex 하위 에이전트에 줄 역할 프롬프트**다.

## 호출 규칙

1. 해당 역할 문서를 읽고, 그 문서의 입력 계약과 현재 작업 입력을 함께 전달해 Codex 하위 에이전트를 시작한다.
2. 역할 문서의 읽기 전용 경계를 유지한다. 분석 역할은 파일·티켓·PR을 수정하거나 사용자에게 직접 질문하지 않는다.
3. 반환값은 역할 문서의 출력 형식으로 압축한다. 원본 본문과 대량 로그를 메인 컨텍스트에 복사하지 않는다.
4. 하위 에이전트를 사용할 수 없는 실행 환경이면, 같은 역할 문서를 읽고 메인에서 동일한 읽기 전용 분석을 수행한다. 병렬 실행을 했다고 말하지 않는다.

## 역할 문서

| 역할 | 참조 |
| --- | --- |
| 소스 요약 | `references/agents/drill-plan-source.md` |
| 코드 후보 탐색 | `references/agents/drill-code-explore.md` |
| 구현 설계 | `references/agents/drill-design.md` |
| 의존 그래프 | `references/agents/drill-deps.md` |
| PR·티켓 차이 분석 | `references/agents/drill-review.md` |
| QA TC 초안 | `references/agents/drill-qa.md` |
"""


def copy_tree(source: Path, destination: Path) -> None:
    for path in source.rglob("*"):
        relative = path.relative_to(source)
        target = destination / relative
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def transform_codex_skill(content: str) -> str:
    content = re.sub(r"^compatibility:.*\n", "", content, flags=re.MULTILINE)
    content = re.sub(r"^disable-model-invocation:.*\n", "", content, flags=re.MULTILINE)
    content = content.replace("/drill:", "$drill-codex:")
    content = content.replace("AskUserQuestion", "사용자 확인")
    content = content.replace("`Task`", "Codex 하위 에이전트")
    note = (
        "> **Codex 위임 규칙**: `drill-*` 분석 역할이 나오면 "
        "[Codex 하위 에이전트 위임](../../references/CODEX-DELEGATION.md)을 먼저 읽고 "
        "해당 역할 문서를 프롬프트로 사용한다.\n\n"
    )
    frontmatter_end = content.find("\n---", 3)
    if frontmatter_end == -1:
        raise ValueError("SKILL.md frontmatter is incomplete")
    body_start = frontmatter_end + len("\n---\n")
    return content[:body_start] + "\n" + note + content[body_start:]


def transform_codex_reference(content: str) -> str:
    return content.replace("/drill:", "$drill-codex:").replace(
        "AskUserQuestion", "사용자 확인"
    )


def sync_claude() -> None:
    for directory in CONTENT_DIRECTORIES:
        copy_tree(SHARED / directory, CLAUDE / directory)
    copy_tree(SHARED / "agents", CLAUDE / "agents")


def sync_codex() -> None:
    for directory in CONTENT_DIRECTORIES:
        copy_tree(SHARED / directory, CODEX / directory)

    for skill in (CODEX / "skills").glob("*/SKILL.md"):
        skill.write_text(transform_codex_skill(skill.read_text()))

    for reference in (CODEX / "references").glob("*.md"):
        reference.write_text(transform_codex_reference(reference.read_text()))

    role_directory = CODEX / "references" / "agents"
    role_directory.mkdir(parents=True, exist_ok=True)
    for source in (SHARED / "agents").glob("*.md"):
        content = re.sub(r"^(tools|model):.*\n", "", source.read_text(), flags=re.MULTILINE)
        (role_directory / source.name).write_text(transform_codex_reference(content))

    (CODEX / "references" / "CODEX-DELEGATION.md").write_text(CODEX_DELEGATION)


def main() -> None:
    sync_claude()
    sync_codex()
    print("Synced shared Drill instructions for Claude Code and Codex.")


if __name__ == "__main__":
    main()
