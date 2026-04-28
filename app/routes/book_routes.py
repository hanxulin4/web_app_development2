from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.book import BookModel

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
    query = request.args.get('query', '').strip()
    if query:
        books = BookModel.search(query)
    else:
        books = BookModel.get_all()
    
    return render_template('index.html', books=books, query=query)

@book_bp.route('/add', methods=['GET'])
def add_page():
    """
    新增筆記頁面
    - 單純渲染空白的 form.html
    """
    # 傳遞 book=None 讓表單知道現在是新增模式
    return render_template('form.html', book=None)

@book_bp.route('/add', methods=['POST'])
def add_submit():
    """
    建立筆記
    - 接收表單傳來的資料 (title, author, review, rating, comment)
    - 呼叫 BookModel.create 將資料寫入資料庫
    - 重導向至首頁 '/'
    """
    title = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    review = request.form.get('review', '').strip()
    rating_str = request.form.get('rating', '0')
    comment = request.form.get('comment', '').strip()

    # 基礎輸入驗證：書名為必填
    if not title:
        flash('書名是必填欄位！', 'danger')
        # 如果失敗，回傳原本填寫的資料讓使用者不用重打
        book_data = {'title': title, 'author': author, 'review': review, 'rating': rating_str, 'comment': comment}
        return render_template('form.html', book=book_data)

    try:
        rating = int(rating_str)
    except ValueError:
        rating = 0

    BookModel.create(title, author, review, rating, comment)
    flash('筆記新增成功！', 'success')
    return redirect(url_for('book_bp.index'))

@book_bp.route('/edit/<int:book_id>', methods=['GET'])
def edit_page(book_id):
    """
    編輯筆記頁面
    - 根據 book_id 呼叫 BookModel.get_by_id 取得該筆記資料
    - 若找不到資料則回傳 404
    - 將資料傳遞給 form.html 渲染 (此時表單內會有舊資料)
    """
    book = BookModel.get_by_id(book_id)
    if not book:
        flash('找不到該筆記！', 'danger')
        return redirect(url_for('book_bp.index'))
    
    return render_template('form.html', book=book)

@book_bp.route('/edit/<int:book_id>', methods=['POST'])
def edit_submit(book_id):
    """
    更新筆記
    - 接收表單傳來的新資料
    - 呼叫 BookModel.update 更新資料庫中該 book_id 的資料
    - 重導向至首頁 '/'
    """
    title = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    review = request.form.get('review', '').strip()
    rating_str = request.form.get('rating', '0')
    comment = request.form.get('comment', '').strip()

    if not title:
        flash('書名是必填欄位！', 'danger')
        book_data = {'id': book_id, 'title': title, 'author': author, 'review': review, 'rating': rating_str, 'comment': comment}
        return render_template('form.html', book=book_data)

    try:
        rating = int(rating_str)
    except ValueError:
        rating = 0

    success = BookModel.update(book_id, title, author, review, rating, comment)
    if success:
        flash('筆記更新成功！', 'success')
    else:
        flash('筆記更新失敗！', 'danger')
        
    return redirect(url_for('book_bp.index'))

@book_bp.route('/delete/<int:book_id>', methods=['POST'])
def delete_submit(book_id):
    """
    刪除筆記
    - 根據 book_id 呼叫 BookModel.delete 刪除該筆資料
    - 重導向至首頁 '/'
    """
    success = BookModel.delete(book_id)
    if success:
        flash('筆記已刪除！', 'success')
    else:
        flash('刪除失敗，找不到該筆記。', 'danger')
        
    return redirect(url_for('book_bp.index'))
