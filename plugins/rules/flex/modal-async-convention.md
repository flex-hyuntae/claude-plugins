---
title: Modal 내 API 호출 컨벤션
impact: MEDIUM
impactDescription: 닫힌 모달의 불필요한 훅 초기화/네트워크 호출 방지
tags: modal, react-query, suspense, async, flex
---

## Modal 내 API 호출 컨벤션

Modal 안에서 데이터 fetch가 필요하면 **`Modal.Content` 하위 컴포넌트**에서 호출한다. Modal이 닫힌 상태에서는 Content가 unmount되므로 불필요한 훅 초기화와 네트워크 호출이 발생하지 않는다.

**Incorrect (Modal 외부에서 조회 — 닫혀 있어도 호출됨):**

```tsx
function ConnectionSettings({ connectionId }: Props) {
  // 모달이 닫혀 있어도 이 훅은 실행된다
  const { data: connection } = useSuspenseQuery(connectionQueryOptions(connectionId));

  return (
    <Modal open={isOpen} onOpenChange={setIsOpen}>
      <Modal.Content>
        <ConnectionDetail connection={connection} />
      </Modal.Content>
    </Modal>
  );
}
```

**Correct (Content 하위에서 조회 — 열릴 때만 실행):**

```tsx
function ConnectionSettings({ connectionId }: Props) {
  return (
    <Modal open={isOpen} onOpenChange={setIsOpen}>
      <Modal.Content>
        <QueryAsyncBoundary pendingFallback={<Skeleton />} rejectedFallback={<ErrorView />}>
          <ConnectionDetail connectionId={connectionId} />
        </QueryAsyncBoundary>
      </Modal.Content>
    </Modal>
  );
}

function ConnectionDetail({ connectionId }: { connectionId: string }) {
  // 모달이 열려서 Content가 mount될 때만 호출된다
  const { data: connection } = useSuspenseQuery(connectionQueryOptions(connectionId));
  return <View connection={connection} />;
}
```

**핵심 원칙:**

- `Modal.Content` 내부는 `QueryAsyncBoundary`로 감싸 Suspense/Error를 **Modal 범위 안에서** 처리한다. 바깥 페이지의 로딩/에러 상태에 영향을 주지 않는다.
- 외부에서는 `connectionId`처럼 **식별자만** 넘긴다. 상세 데이터(name, 상태 등)는 Content 내부에서 자체 조회한다.
- 외부에서 이미 데이터를 갖고 있더라도, 상세 fetch가 필요한 필드면 내부 조회를 선호한다 — prop drilling과 prefetch 동기화 부담을 줄인다.
