# 流程圖文件（Flowchart）

**專案名稱：** 個人任務管理系統  
**文件版本：** v1.0  
**撰寫日期：** 2026-04-13  
**依據文件：** [PRD.md](./PRD.md)｜[ARCHITECTURE.md](./ARCHITECTURE.md)

---

## 1. 使用者流程圖（User Flow）

描述使用者從開啟網頁到完成各項操作的完整路徑。

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 任務清單]

    B --> F{選擇篩選條件}
    F -->|全部| B
    F -->|待完成| B1[顯示未完成任務]
    F -->|已完成| B2[顯示已完成任務]

    B --> C{要執行什麼操作？}

    C -->|新增任務| D[在輸入框輸入任務名稱]
    D --> D1{輸入框是否為空？}
    D1 -->|是| D2[顯示提示訊息] --> D
    D1 -->|否| D3[點擊新增按鈕]
    D3 --> D4[POST /tasks]
    D4 --> D5[任務出現在清單頂端]
    D5 --> B

    C -->|標記完成| E[點擊任務旁的 checkbox]
    E --> E1[PUT /tasks/id/toggle]
    E1 --> E2{目前狀態？}
    E2 -->|未完成| E3[標記為已完成\n顯示刪除線]
    E2 -->|已完成| E4[取消完成\n回復正常樣式]
    E3 --> B
    E4 --> B

    C -->|刪除任務| G[點擊垃圾桶按鈕]
    G --> G1[POST /tasks/id/delete]
    G1 --> G2[任務從清單移除]
    G2 --> B

    C -->|篩選任務| F
```

---

## 2. 系統序列圖（System Sequence Diagram）

以下為各主要功能的後端資料流，描述「使用者操作」到「資料庫變更」的完整過程。

### 2.1 新增任務（F01）

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as "Flask Route (tasks.py)"
    participant Model as "Task Model (task.py)"
    participant DB as "SQLite (database.db)"
    participant Template as "Jinja2 Template"

    User->>Browser: 輸入任務名稱，點擊「新增」
    Browser->>Route: POST /tasks（form data: title）

    alt 標題為空
        Route-->>Browser: 回傳錯誤提示（400）
        Browser-->>User: 顯示「請輸入任務名稱」
    else 標題有值
        Route->>Model: Task(title=title, is_done=False)
        Model->>DB: INSERT INTO task (title, is_done, created_at)
        DB-->>Model: 成功，回傳新 Task id
        Model-->>Route: 新 Task 物件
        Route-->>Browser: redirect → GET /tasks
        Browser->>Route: GET /tasks
        Route->>Model: Task.query.order_by(created_at.desc()).all()
        Model->>DB: SELECT * FROM task ORDER BY created_at DESC
        DB-->>Model: 任務清單
        Model-->>Route: [Task, ...]
        Route->>Template: render_template('tasks/index.html', tasks=[...])
        Template-->>Browser: 完整 HTML
        Browser-->>User: 顯示含新任務的清單
    end
```

---

### 2.2 標記任務完成 / 取消完成（F02）

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as "Flask Route (tasks.py)"
    participant Model as "Task Model (task.py)"
    participant DB as "SQLite (database.db)"
    participant Template as "Jinja2 Template"

    User->>Browser: 點擊任務旁的 checkbox
    Browser->>Route: POST /tasks/{id}/toggle

    Route->>Model: Task.query.get(id)
    Model->>DB: SELECT * FROM task WHERE id = {id}
    DB-->>Model: Task 物件

    alt Task.is_done == False
        Route->>Model: task.is_done = True
        Model->>DB: UPDATE task SET is_done=1 WHERE id={id}
        DB-->>Model: 成功
    else Task.is_done == True
        Route->>Model: task.is_done = False
        Model->>DB: UPDATE task SET is_done=0 WHERE id={id}
        DB-->>Model: 成功
    end

    Model-->>Route: 更新後的 Task
    Route-->>Browser: redirect → GET /tasks
    Browser->>Route: GET /tasks
    Route->>Model: Task.query.order_by(created_at.desc()).all()
    Model->>DB: SELECT * FROM task ORDER BY created_at DESC
    DB-->>Model: 任務清單
    Model-->>Route: [Task, ...]
    Route->>Template: render_template('tasks/index.html', tasks=[...])
    Template-->>Browser: 完整 HTML（已更新完成狀態）
    Browser-->>User: 顯示更新後的任務清單
```

---

### 2.3 刪除任務（F03）

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as "Flask Route (tasks.py)"
    participant Model as "Task Model (task.py)"
    participant DB as "SQLite (database.db)"
    participant Template as "Jinja2 Template"

    User->>Browser: 點擊垃圾桶按鈕
    Browser->>Route: POST /tasks/{id}/delete

    Route->>Model: Task.query.get(id)
    Model->>DB: SELECT * FROM task WHERE id = {id}
    DB-->>Model: Task 物件

    alt Task 存在
        Route->>Model: db.session.delete(task)
        Model->>DB: DELETE FROM task WHERE id={id}
        DB-->>Model: 成功
        Model-->>Route: 刪除完成
        Route-->>Browser: redirect → GET /tasks
        Browser->>Route: GET /tasks
        Route->>Model: Task.query.order_by(created_at.desc()).all()
        Model->>DB: SELECT * FROM task ORDER BY created_at DESC
        DB-->>Model: 剩餘任務清單
        Model-->>Route: [Task, ...]
        Route->>Template: render_template('tasks/index.html', tasks=[...])
        Template-->>Browser: 完整 HTML（已移除該任務）
        Browser-->>User: 顯示更新後的清單
    else Task 不存在
        Route-->>Browser: 404 Not Found
        Browser-->>User: 顯示錯誤頁面
    end
```

---

### 2.4 依狀態篩選任務（F05）

> 篩選功能由前端 JavaScript 處理，無需後端請求。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant JS as "filter.js（前端）"

    Note over Browser: 頁面已載入全部任務（HTML 中含 data-done 屬性）

    User->>Browser: 點擊「待完成」篩選按鈕
    Browser->>JS: click event 觸發
    JS->>JS: 讀取所有任務元素的 data-done 屬性
    JS->>JS: 隱藏 data-done="true" 的元素
    JS->>Browser: 更新 DOM 顯示
    Browser-->>User: 僅顯示「待完成」任務（無頁面重整）

    User->>Browser: 點擊「已完成」篩選按鈕
    Browser->>JS: click event 觸發
    JS->>JS: 隱藏 data-done="false" 的元素
    JS->>Browser: 更新 DOM 顯示
    Browser-->>User: 僅顯示「已完成」任務

    User->>Browser: 點擊「全部」篩選按鈕
    Browser->>JS: click event 觸發
    JS->>JS: 顯示所有任務元素
    JS->>Browser: 更新 DOM 顯示
    Browser-->>User: 顯示全部任務
```

---

## 3. 功能清單對照表

| 功能 ID | 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
|---------|----------|----------|-----------|------|
| F01 | 新增任務 | `/tasks` | `POST` | 接收表單資料，建立新 Task 並存入 DB |
| F02 | 標記完成 / 取消 | `/tasks/<id>/toggle` | `POST` | 切換指定任務的 `is_done` 狀態 |
| F03 | 刪除任務 | `/tasks/<id>/delete` | `POST` | 從 DB 刪除指定任務 |
| F04 | 顯示任務清單 | `/tasks` | `GET` | 查詢所有任務，渲染 index.html |
| F05 | 依狀態篩選 | —（前端處理） | —（JS） | filter.js 切換 DOM 顯示，無需路由 |

> 💡 HTML Form 只支援 GET / POST，因此使用 `POST` 代替 `DELETE` / `PATCH`。

---

## 相關文件

- [PRD.md](./PRD.md) — 產品需求文件（已完成）
- [ARCHITECTURE.md](./ARCHITECTURE.md) — 系統架構設計（已完成）
- [DB_Schema.md](./DB_Schema.md) — 資料庫設計（待產出）
- [API_Design.md](./API_Design.md) — 路由與 API 設計（待產出）
