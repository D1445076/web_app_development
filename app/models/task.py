"""
app/models/task.py
------------------
Task Model — 個人任務管理系統

定義 task 資料表結構，並提供完整的 CRUD 靜態方法。
使用 Flask-SQLAlchemy 2.x ORM，透過物件操作資料庫，
自動防止 SQL Injection。

資料表欄位：
    id         (int)      — 主鍵，自動遞增
    title      (str)      — 任務名稱，必填，最長 200 字元
    is_done    (bool)     — 完成狀態，預設 False（未完成）
    created_at (datetime) — 建立時間，自動填入（UTC）

依據文件：docs/DB_DESIGN.md
"""

from datetime import datetime
from flask import abort
from app import db


class Task(db.Model):
    """SQLAlchemy ORM Model — 對應資料庫的 task 資料表。"""

    __tablename__ = "task"

    # ── 欄位定義 ──────────────────────────────────────────────
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        comment="主鍵，唯一識別每筆任務"
    )
    title = db.Column(
        db.String(200),
        nullable=False,
        comment="任務名稱，最長 200 字元"
    )
    is_done = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        comment="完成狀態：False=未完成，True=已完成"
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        comment="任務建立時間（UTC），用於清單排序"
    )

    # ── 字串表示 ──────────────────────────────────────────────
    def __repr__(self) -> str:
        status = "✅" if self.is_done else "⬜"
        return f"<Task {self.id} {status} '{self.title}'>"

    # ── CRUD 方法 ─────────────────────────────────────────────

    @staticmethod
    def create(title: str) -> "Task":
        """
        建立新任務並寫入資料庫。

        Args:
            title (str): 任務名稱，不得為空字串。

        Returns:
            Task: 已儲存的 Task 物件（含 id 與 created_at）。

        Raises:
            ValueError: 若 title 為空字串。

        Example:
            task = Task.create("完成作業")
        """
        title = title.strip()
        if not title:
            raise ValueError("任務名稱不得為空。")

        task = Task(title=title, is_done=False)
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def get_all() -> list["Task"]:
        """
        取得所有任務，依建立時間降冪排序（最新優先）。

        Returns:
            list[Task]: Task 物件清單，若無任務則回傳空清單。

        Example:
            tasks = Task.get_all()
        """
        return Task.query.order_by(Task.created_at.desc()).all()

    @staticmethod
    def get_by_id(task_id: int) -> "Task":
        """
        依主鍵取得單筆任務。

        Args:
            task_id (int): 任務的 id。

        Returns:
            Task: 對應的 Task 物件。

        Raises:
            404 HTTPException: 若指定 id 的任務不存在。

        Example:
            task = Task.get_by_id(1)
        """
        task = Task.query.get(task_id)
        if task is None:
            abort(404, description=f"找不到 id={task_id} 的任務。")
        return task

    @staticmethod
    def toggle(task_id: int) -> "Task":
        """
        切換任務的完成狀態（已完成 ↔ 未完成）。

        Args:
            task_id (int): 要切換狀態的任務 id。

        Returns:
            Task: 更新後的 Task 物件。

        Raises:
            404 HTTPException: 若指定 id 的任務不存在。

        Example:
            task = Task.toggle(1)
            # task.is_done 已從 False 切換為 True（或反之）
        """
        task = Task.get_by_id(task_id)
        task.is_done = not task.is_done
        db.session.commit()
        return task

    @staticmethod
    def delete(task_id: int) -> None:
        """
        刪除指定任務。

        Args:
            task_id (int): 要刪除的任務 id。

        Raises:
            404 HTTPException: 若指定 id 的任務不存在。

        Example:
            Task.delete(1)
        """
        task = Task.get_by_id(task_id)
        db.session.delete(task)
        db.session.commit()
