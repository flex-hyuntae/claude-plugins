---
title: 테스트 코드 품질
impact: MEDIUM
impactDescription: 안정적이고 유지보수 가능한 테스트
tags: testing, aaa-pattern, test-quality
---

## 테스트 코드 품질

AAA 패턴을 준수하고, 의미있는 테스트를 작성한다. 구현 세부사항이 아닌 동작을 테스트한다.

### AAA 패턴 (Arrange, Act, Assert)

**Incorrect (구조 없는 테스트):**

```typescript
it('should work', () => {
  const result = calculate(createUser({ role: 'admin' }), [
    createItem({ price: 100 }),
    createItem({ price: 200 }),
  ]);
  expect(result.total).toBe(270);
  expect(result.discount).toBe(30);
  expect(result.items).toHaveLength(2);
});
```

**Correct (AAA 패턴):**

```typescript
it('관리자에게 10% 할인을 적용한다', () => {
  // Arrange
  const admin = createUser({ role: 'admin' });
  const items = [
    createItem({ price: 100 }),
    createItem({ price: 200 }),
  ];

  // Act
  const result = calculate(admin, items);

  // Assert
  expect(result.total).toBe(270);
  expect(result.discount).toBe(30);
});
```

### 동작 기반 테스트

**Incorrect (구현 세부사항 테스트):**

```typescript
it('setState를 호출한다', () => {
  const setState = vi.fn();
  vi.spyOn(React, 'useState').mockReturnValue([0, setState]);

  render(<Counter />);
  fireEvent.click(screen.getByText('+'));

  expect(setState).toHaveBeenCalledWith(1);
});
```

**Correct (사용자 관점 테스트):**

```typescript
it('+ 버튼 클릭 시 카운트가 증가한다', () => {
  render(<Counter />);

  fireEvent.click(screen.getByText('+'));

  expect(screen.getByText('1')).toBeInTheDocument();
});
```

### Brittle Test 방지

**Incorrect (깨지기 쉬운 선택자):**

```typescript
const button = container.querySelector('.btn-primary > span:first-child');
```

**Correct (안정적인 선택자):**

```typescript
const button = screen.getByRole('button', { name: '저장' });
```
