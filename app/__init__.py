from flask import Flask
import os
from .routes.book_routes import book_bp

def create_app():
    """
    Application Factory 模式：建立並設定 Flask 實例
    """
    # 建立 Flask 實例，預設 templates 和 static 資料夾都會在 app/ 目錄下
    app = Flask(__name__)
    
    # 基本設定，在實際部署時應從環境變數載入
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key_for_book_notes')
    
    # 註冊我們之前開好的 Blueprint
    app.register_blueprint(book_bp)
    
    return app
