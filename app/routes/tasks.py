"""
app/routes/tasks.py
--------------------
Tasks Blueprint — 個人任務管理系統

負責處理所有任務相關的 HTTP 路由（Controller 層）。
每個函式只定義路由裝飾器與 docstring，實作邏輯待下一階段補充。

Blueprint 名稱：tasks
URL Prefix：/tasks

依據文件：docs/ROUTES.md
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models.task import Task

# ── Blueprint 建立 ─────────────────────────────────────────────
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# ── F04：顯示任務清單 ──────────────────────────────────────────
@tasks_bp.route("/", methods=["GET"])
def index():
    """
    顯示所有任務清單。

    URL:     GET /tasks
    Template: tasks/index.html
    Context:
        tasks (list[Task]): 所有任務，依建立時間降冪排序

    Flow:
        1. 呼叫 Task.get_all() 取得所有任務
        2. 渲染 tasks/index.html 並傳入 tasks 清單
    """
    pass


# ── F01：新增任務 ──────────────────────────────────────────────
@tasks_bp.route("/", methods=["POST"])
def create():
    """
    接收表單資料並建立新任務。

    URL:    POST /tasks
    Input:  form["title"] (str) — 任務名稱，必填

    Flow:
        1. 從 request.form 取得 title
        2. 驗證 title 非空（strip 後不為空字串）
           - 若為空：flash 錯誤訊息，redirect 回 GET /tasks
        3. 呼叫 Task.create(title) 建立新任務
        4. redirect 至 GET /tasks（Post/Redirect/Get 模式）

    Error:
        - title 為空 → flash("請輸入任務名稱", "error")，redirect(url_for("tasks.index"))
    """
    pass


# ── F02：切換任務完成狀態 ─────────────────────────────────────
@tasks_bp.route("/<int:id>/toggle", methods=["POST"])
def toggle(id: int):
    """
    切換指定任務的完成狀態（已完成 ↔ 未完成）。

    URL:   POST /tasks/<id>/toggle
    Input: URL 參數 id (int) — 任務主鍵

    Flow:
        1. 呼叫 Task.toggle(id)
           - 若 id 不存在，Task.get_by_id 自動 abort(404)
        2. redirect 至 GET /tasks

    Error:
        - 任務不存在 → 404 Not Found（由 Task.get_by_id 處理）
    """
    pass


# ── F03：刪除任務 ─────────────────────────────────────────────
@tasks_bp.route("/<int:id>/delete", methods=["POST"])
def delete(id: int):
    """
    刪除指定任務。

    URL:   POST /tasks/<id>/delete
    Input: URL 參數 id (int) — 任務主鍵

    Flow:
        1. 呼叫 Task.delete(id)
           - 若 id 不存在，Task.get_by_id 自動 abort(404)
        2. redirect 至 GET /tasks

    Error:
        - 任務不存在 → 404 Not Found（由 Task.get_by_id 處理）
    """
    pass
