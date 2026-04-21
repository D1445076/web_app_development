"""
app/__init__.py
---------------
Flask 應用程式工廠（Application Factory）

負責：
1. 建立 Flask app 實例
2. 載入設定（SECRET_KEY、資料庫路徑）
3. 初始化 SQLAlchemy
4. 註冊 Blueprint（routes/tasks.py）
5. 提供 init_db() 函式（建立資料表）

依據文件：docs/ARCHITECTURE.md
"""

import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# ── 全域 SQLAlchemy 實例 ───────────────────────────────────────
# 在這裡建立，讓 app/models/ 可以直接 from app import db 匯入
db = SQLAlchemy()


def create_app() -> Flask:
    """
    應用程式工廠：建立並設定 Flask app 實例。

    Returns:
        Flask: 已設定完成的 Flask 應用程式。
    """
    app = Flask(__name__, instance_relative_config=True)

    # ── 設定 ──────────────────────────────────────────────────
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-please-change")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        app.instance_path, "database.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ── 確保 instance/ 資料夾存在 ─────────────────────────────
    os.makedirs(app.instance_path, exist_ok=True)

    # ── 初始化 SQLAlchemy ─────────────────────────────────────
    db.init_app(app)

    # ── 註冊 Blueprint ────────────────────────────────────────
    from app.routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp)

    # ── 根路徑重導向至 /tasks ──────────────────────────────────
    @app.route("/")
    def index():
        return redirect(url_for("tasks.index"))

    return app


def init_db(app: Flask = None) -> None:
    """
    初始化資料庫：建立所有資料表。

    在首次部署或重置資料庫時呼叫。

    使用方式：
        python -c "from app import create_app, init_db; init_db(create_app())"

    Args:
        app (Flask): Flask app 實例；若為 None 則自動建立。
    """
    if app is None:
        app = create_app()

    with app.app_context():
        db.create_all()
        print("✅ 資料庫初始化完成：instance/database.db")
