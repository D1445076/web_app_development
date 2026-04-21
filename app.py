"""
app.py
------
Flask 應用程式入口點

執行方式：
    flask run          （開發環境，需先設 FLASK_APP=app.py）
    python app.py      （直接執行，debug 模式）

依據文件：docs/ARCHITECTURE.md
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
