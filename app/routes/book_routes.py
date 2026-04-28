from flask import Blueprint, render_template, request, redirect, url_for

# 建立 Blueprint (藍圖)，方便在主程式 app.py 中註冊並管理路由
book_bp = Blueprint('book_bp', __name__)

@book_bp.route('/', methods=['GET'])
def index():
    """
    首頁與搜尋列表
    - 接收 query 參數（可選）
    - 呼叫 BookModel 取得書籍清單
    - 渲染 index.html，將清單傳遞給模板
    """
    pass

@book_bp.route('/add', methods=['GET'])
def add_page():
    """
    新增筆記頁面
    - 單純渲染空白的 form.html
    """
    pass

@book_bp.route('/add', methods=['POST'])
def add_submit():
    """
    建立筆記
    - 接收表單傳來的資料 (title, author, review, rating, comment)
    - 呼叫 BookModel.create 將資料寫入資料庫
    - 重導向至首頁 '/'
    """
    pass

@book_bp.route('/edit/<int:book_id>', methods=['GET'])
def edit_page(book_id):
    """
    編輯筆記頁面
    - 根據 book_id 呼叫 BookModel.get_by_id 取得該筆記資料
    - 若找不到資料則回傳 404
    - 將資料傳遞給 form.html 渲染 (此時表單內會有舊資料)
    """
    pass

@book_bp.route('/edit/<int:book_id>', methods=['POST'])
def edit_submit(book_id):
    """
    更新筆記
    - 接收表單傳來的新資料
    - 呼叫 BookModel.update 更新資料庫中該 book_id 的資料
    - 重導向至首頁 '/'
    """
    pass

@book_bp.route('/delete/<int:book_id>', methods=['POST'])
def delete_submit(book_id):
    """
    刪除筆記
    - 根據 book_id 呼叫 BookModel.delete 刪除該筆資料
    - 重導向至首頁 '/'
    """
    pass
