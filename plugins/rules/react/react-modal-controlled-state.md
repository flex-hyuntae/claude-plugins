---
title: Modal Controlled State 패턴
impact: MEDIUM
impactDescription: 모달 닫기 애니메이션 정상 동작
tags: react, modal, animation, state
---

## Modal Controlled State 패턴

동적 type을 가진 모달을 controlled state로 관리할 때, open 상태와 content type 상태를 분리한다.
모달 닫기 애니메이션 중 Content가 언마운트되지 않도록 `onClose`에서 type을 초기화한다.

**Incorrect (애니메이션 중 Content 언마운트):**

```tsx
<Modal
  open={type != null}
  onOpenChange={open => { if (!open) setType(null); }}
>
  <Modal.Content type={type!} />
</Modal>
```

**Correct (open/type 분리, onClose에서 초기화):**

```tsx
const [isOpen, setIsOpen] = useState(false);
const [type, setType] = useState<Type | null>(null);

// trigger: setType(t); setIsOpen(true);

<Modal open={isOpen} onOpenChange={setIsOpen} onClose={() => setType(null)}>
  {type && <Modal.Content type={type} />}
</Modal>
```
