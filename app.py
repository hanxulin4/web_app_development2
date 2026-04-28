import os
from app import create_app
from app.models.book import init_db

# 透過工廠函式建立 app
app = create_app()

if __name__ == '__main__':
    # 啟動前，確認資料庫與資料表是否已經初始化
    init_db()
    
    # 啟動開發伺服器
    app.run(debug=True)
