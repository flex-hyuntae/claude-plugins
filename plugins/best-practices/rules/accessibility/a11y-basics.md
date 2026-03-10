---
title: 접근성 기본 규칙
impact: HIGH
impactDescription: 모든 사용자가 서비스를 사용할 수 있도록 보장
tags: accessibility, a11y, aria, keyboard, semantic-html
---

## 접근성 기본 규칙

시맨틱 HTML, ARIA 속성, 키보드 네비게이션을 올바르게 사용한다.

### 시맨틱 HTML

**Incorrect (div 남용):**

```tsx
<div onClick={handleClick}>삭제</div>
<div className="header">
  <div className="nav">
    <div onClick={goHome}>홈</div>
  </div>
</div>
```

**Correct (시맨틱 요소):**

```tsx
<button onClick={handleClick}>삭제</button>
<header>
  <nav>
    <a href="/" onClick={goHome}>홈</a>
  </nav>
</header>
```

### ARIA 속성

**Incorrect (ARIA 누락):**

```tsx
<div className="modal">
  <div className="close" onClick={onClose}>X</div>
  <div>모달 내용</div>
</div>

<img src="/logo.png" />

<input onChange={handleSearch} />
```

**Correct (ARIA 제공):**

```tsx
<div role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <button aria-label="닫기" onClick={onClose}>X</button>
  <h2 id="modal-title">모달 제목</h2>
  <div>모달 내용</div>
</div>

<img src="/logo.png" alt="회사 로고" />

<label htmlFor="search">검색</label>
<input id="search" onChange={handleSearch} aria-label="검색어 입력" />
```

### 키보드 네비게이션

**Incorrect (마우스 전용):**

```tsx
<div onClick={handleSelect} className="option">
  옵션 1
</div>
```

**Correct (키보드 지원):**

```tsx
<div
  role="option"
  tabIndex={0}
  onClick={handleSelect}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleSelect();
    }
  }}
  aria-selected={isSelected}
>
  옵션 1
</div>
```
