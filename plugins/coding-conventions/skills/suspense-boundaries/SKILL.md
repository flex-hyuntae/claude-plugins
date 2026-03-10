---
name: suspense-boundaries
title: 전략적 Suspense Boundary 배치
impact: HIGH
impactDescription: 초기 paint 속도 향상
tags: async, suspense, streaming, layout-shift
---

## 전략적 Suspense Boundary 배치

async component에서 JSX를 반환하기 전에 data를 await하는 대신, Suspense boundary를 사용해 wrapper UI를 먼저 보여준다.

**Incorrect (data fetching에 wrapper가 blocking됨):**

```tsx
async function Page() {
  const data = await fetchData() // Blocks entire page

  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <div>
        <DataDisplay data={data} />
      </div>
      <div>Footer</div>
    </div>
  )
}
```

중간 섹션만 data가 필요한데 전체 layout이 대기한다.

**Correct (wrapper가 즉시 표시되고, data가 streaming됨):**

```tsx
function Page() {
  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <div>
        <Suspense fallback={<Skeleton />}>
          <DataDisplay />
        </Suspense>
      </div>
      <div>Footer</div>
    </div>
  )
}

async function DataDisplay() {
  const data = await fetchData() // Only blocks this component
  return <div>{data.content}</div>
}
```

Sidebar, Header, Footer는 즉시 render된다. DataDisplay만 data를 기다린다.

**대안 (component 간 promise 공유):**

```tsx
function Page() {
  // Start fetch immediately, but don't await
  const dataPromise = fetchData()

  return (
    <div>
      <div>Sidebar</div>
      <div>Header</div>
      <Suspense fallback={<Skeleton />}>
        <DataDisplay dataPromise={dataPromise} />
        <DataSummary dataPromise={dataPromise} />
      </Suspense>
      <div>Footer</div>
    </div>
  )
}

function DataDisplay({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise) // Unwraps the promise
  return <div>{data.content}</div>
}

function DataSummary({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise) // Reuses the same promise
  return <div>{data.summary}</div>
}
```

두 component가 같은 promise를 공유하므로 fetch는 한 번만 발생한다. Layout은 즉시 render되고, 두 component가 함께 대기한다.

**이 패턴을 사용하지 않아야 할 때:**

- layout 결정에 필요한 핵심 data (위치에 영향)
- SEO에 중요한 above the fold content
- suspense overhead가 불필요한 작고 빠른 query
- layout shift를 피하고 싶을 때 (loading → content 점프)

**Trade-off:** 초기 paint 속도 vs layout shift 가능성. UX 우선순위에 따라 선택한다.
