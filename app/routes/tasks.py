"""
app/routes/tasks.py
--------------------
Tasks Blueprint — 個人任務管理系統

負責處理所有任務相關的 HTTP 路由（Controller 層）。

Blueprint 名稱：tasks
URL Prefix：/tasks

依據文件：docs/ROUTES.md
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.task import Task

# ── Blueprint 建立 ─────────────────────────────────────────────
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# ── F04：顯示任務清單 ──────────────────────────────────────────
@tasks_bp.route("/", methods=["GET"])
def index():
    """
    顯示所有任務清單。

    URL:      GET /tasks
    Template: tasks/index.html
    Context:  tasks (list[Task])
    """
    tasks = Task.get_all()
    return render_template("tasks/index.html", tasks=tasks)


# ── F01：新增任務 ──────────────────────────────────────────────
@tasks_bp.route("/", methods=["POST"])
def create():
    """
    接收表單資料並建立新任務。

    URL:   POST /tasks
    Input: form["title"] (str) — 任務名稱，必填
    """
    title = request.form.get("title", "").strip()

    if not title:
        flash("請輸入任務名稱！", "error")
        return redirect(url_for("tasks.index"))

    try:
        Task.create(title)
    except Exception as e:
        flash(f"新增失敗：{e}", "error")

    return redirect(url_for("tasks.index"))


# ── F02：切換任務完成狀態 ─────────────────────────────────────
@tasks_bp.route("/<int:id>/toggle", methods=["POST"])
def toggle(id: int):
    """
    切換指定任務的完成狀態（已完成 ↔ 未完成）。

    URL:   POST /tasks/<id>/toggle
    Input: URL 參數 id (int)
    """
    Task.toggle(id)
    return redirect(url_for("tasks.index"))


# ── F03：刪除任務 ─────────────────────────────────────────────
@tasks_bp.route("/<int:id>/delete", methods=["POST"])
def delete(id: int):
    """
    刪除指定任務。

    URL:   POST /tasks/<id>/delete
    Input: URL 參數 id (int)
    """
    Task.delete(id)
    return redirect(url_for("tasks.index"))
