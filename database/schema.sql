-- ============================================================
-- 個人任務管理系統 - SQLite Schema
-- 版本：v1.0
-- 日期：2026-04-21
-- 依據：docs/DB_DESIGN.md
-- ============================================================

-- 任務資料表
CREATE TABLE IF NOT EXISTS task (
    id         INTEGER      PRIMARY KEY AUTOINCREMENT,  -- 主鍵，自動遞增
    title      VARCHAR(200) NOT NULL,                   -- 任務名稱，必填，最長 200 字元
    is_done    BOOLEAN      NOT NULL DEFAULT 0,         -- 完成狀態：0=未完成, 1=已完成
    created_at DATETIME     NOT NULL DEFAULT (datetime('now'))  -- 建立時間（UTC）
);

-- 加速依建立時間排序的查詢（清單預設以最新任務優先顯示）
CREATE INDEX IF NOT EXISTS idx_task_created_at ON task (created_at DESC);
