# 路由設計文件（Routes）

**專案名稱：** 個人任務管理系統  
**文件版本：** v1.0  
**撰寫日期：** 2026-04-21  
**依據文件：** [PRD.md](./PRD.md)｜[ARCHITECTURE.md](./ARCHITECTURE.md)｜[DB_DESIGN.md](./DB_DESIGN.md)｜[FLOWCHART.md](./FLOWCHART.md)

---

## 1. 路由總覽表格

| 功能 ID | 功能名稱 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---------|----------|-----------|----------|----------|------|
| F04 | 顯示任務清單 | `GET` | `/tasks` | `tasks/index.html` | 查詢所有任務，依建立時間降冪排序後渲染頁面 |
| F01 | 新增任務 | `POST` | `/tasks` | — | 接收表單資料，建立新 Task，重導向回 `/tasks` |
| F02 | 切換完成狀態 | `POST` | `/tasks/<id>/toggle` | — | 切換 `is_done` 狀態，重導向回 `/tasks` |
| F03 | 刪除任務 | `POST` | `/tasks/<id>/delete` | — | 刪除指定任務，重導向回 `/tasks` |
| — | 根路徑重導向 | `GET` | `/` | — | 直接重導向至 `/tasks` |

> 💡 HTML Form 僅支援 GET / POST，因此切換與刪除均使用 `POST`，符合原 FLOWCHART.md 設計。  
> 💡 篩選功能（F05）由前端 `filter.js` 處理，**不需要額外路由**。

---

## 2. 每個路由的詳細說明

---

### 2.1 GET `/` — 根路徑重導向

| 項目 | 內容 |
|------|------|
| **輸入** | 無 |
| **處理邏輯** | 直接 `redirect(url_for('tasks.index'))` |
| **輸出** | 302 重導向至 `/tasks` |
| **錯誤處理** | 無 |

---

### 2.2 GET `/tasks` — 顯示任務清單（F04）

| 項目 | 內容 |
|------|------|
| **輸入** | 無（篩選由前端 JS 處理） |
| **處理邏輯** | 呼叫 `Task.get_all()` 取得所有任務 |
| **輸出** | 渲染 `tasks/index.html`，傳入 `tasks` 清單 |
| **錯誤處理** | 若資料庫錯誤，回傳 500；清單為空時模板顯示空狀態提示 |

**傳入模板的 context 變數：**

```python
render_template("tasks/index.html", tasks=tasks)
```

| 變數 | 型別 | 說明 |
|------|------|------|
| `tasks` | `list[Task]` | 所有任務，依 `created_at DESC` 排序 |

---

### 2.3 POST `/tasks` — 新增任務（F01）

| 項目 | 內容 |
|------|------|
| **輸入** | Form 欄位：`title`（字串，必填） |
| **處理邏輯** | 驗證 title 非空 → 呼叫 `Task.create(title)` → redirect |
| **輸出** | 成功：302 重導向至 `GET /tasks` |
| **錯誤處理** | title 為空時：flash 錯誤訊息，重導向回 `/tasks`（不中斷頁面） |

**驗證規則：**
- `title.strip()` 後不得為空字串
- 最長 200 字元（由 Model 層的 `String(200)` 限制）

---

### 2.4 POST `/tasks/<id>/toggle` — 切換完成狀態（F02）

| 項目 | 內容 |
|------|------|
| **輸入** | URL 參數：`id`（int，任務主鍵） |
| **處理邏輯** | 呼叫 `Task.toggle(id)` 切換 `is_done` 狀態 |
| **輸出** | 302 重導向至 `GET /tasks` |
| **錯誤處理** | 若 `id` 不存在，`Task.get_by_id` 自動 abort(404) |

---

### 2.5 POST `/tasks/<id>/delete` — 刪除任務（F03）

| 項目 | 內容 |
|------|------|
| **輸入** | URL 參數：`id`（int，任務主鍵） |
| **處理邏輯** | 呼叫 `Task.delete(id)` 從資料庫移除該筆記錄 |
| **輸出** | 302 重導向至 `GET /tasks` |
| **錯誤處理** | 若 `id` 不存在，`Task.get_by_id` 自動 abort(404) |

---

## 3. Jinja2 模板清單

| 模板路徑 | 繼承自 | 說明 |
|----------|--------|------|
| `app/templates/base.html` | — | 基底模板，含 `<head>`、導覽列、CSS/JS 引入、flash 訊息區塊 |
| `app/templates/tasks/index.html` | `base.html` | 任務清單主頁，含新增表單、篩選按鈕與任務卡片列表 |

### `base.html` 提供的 block

| Block 名稱 | 說明 |
|------------|------|
| `{% block title %}` | 頁面標題（`<title>` 標籤內容） |
| `{% block content %}` | 各頁面的主體內容 |

### `tasks/index.html` 使用的模板變數

| 變數 | 說明 |
|------|------|
| `tasks` | `list[Task]`，所有任務物件清單 |
| `get_flashed_messages()` | Flask flash 訊息（新增失敗提示等） |

### 任務元素的 HTML data 屬性

前端 `filter.js` 依賴每個任務的 `data-done` 屬性進行篩選切換：

```html
<div class="task-item" data-done="{{ 'true' if task.is_done else 'false' }}">
  ...
</div>
```

---

## 4. Blueprint 架構說明

所有任務路由封裝在 `tasks` Blueprint 中，prefix 為 `/tasks`：

```python
# app/routes/tasks.py
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
```

根路徑 `/` 的重導向在 `app/__init__.py` 或獨立的 `main.py` 路由中處理。

### 路由名稱（url_for 用）

| 功能 | `url_for` 名稱 |
|------|----------------|
| 任務清單 | `url_for("tasks.index")` |
| 新增任務 | `url_for("tasks.create")` |
| 切換狀態 | `url_for("tasks.toggle", id=task.id)` |
| 刪除任務 | `url_for("tasks.delete", id=task.id)` |

---

## 相關文件

- [PRD.md](./PRD.md) — 產品需求文件（已完成）
- [ARCHITECTURE.md](./ARCHITECTURE.md) — 系統架構設計（已完成）
- [FLOWCHART.md](./FLOWCHART.md) — 流程圖（已完成）
- [DB_DESIGN.md](./DB_DESIGN.md) — 資料庫設計（已完成）
- [API_Design.md](./API_Design.md) — 本文件
