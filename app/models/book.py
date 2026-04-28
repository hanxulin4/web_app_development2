import sqlite3
import os

# 資料庫檔案路徑
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """取得資料庫連線，並設定回傳字典格式以便於操作"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化資料庫：讀取 schema.sql 並建立資料表"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    with get_db_connection() as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()

class BookModel:
    """處理 books 資料表的 CRUD 操作"""
    
    @staticmethod
    def get_all():
        """取得所有書籍筆記，依照建立時間排序"""
        with get_db_connection() as conn:
            books = conn.execute('SELECT * FROM books ORDER BY created_at DESC').fetchall()
            return [dict(book) for book in books]

    @staticmethod
    def get_by_id(book_id):
        """根據 ID 取得單一書籍筆記"""
        with get_db_connection() as conn:
            book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
            return dict(book) if book else None

    @staticmethod
    def create(title, author, review, rating, comment):
        """新增一筆書籍筆記"""
        with get_db_connection() as conn:
            cursor = conn.execute(
                '''
                INSERT INTO books (title, author, review, rating, comment)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (title, author, review, rating, comment)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def update(book_id, title, author, review, rating, comment):
        """更新一筆書籍筆記"""
        with get_db_connection() as conn:
            conn.execute(
                '''
                UPDATE books 
                SET title = ?, author = ?, review = ?, rating = ?, comment = ?
                WHERE id = ?
                ''',
                (title, author, review, rating, comment, book_id)
            )
            conn.commit()
            return True

    @staticmethod
    def delete(book_id):
        """刪除一筆書籍筆記"""
        with get_db_connection() as conn:
            conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()
            return True
            
    @staticmethod
    def search(keyword):
        """根據關鍵字搜尋書名或心得"""
        with get_db_connection() as conn:
            search_query = f"%{keyword}%"
            books = conn.execute(
                '''
                SELECT * FROM books 
                WHERE title LIKE ? OR review LIKE ? OR author LIKE ?
                ORDER BY created_at DESC
                ''', 
                (search_query, search_query, search_query)
            ).fetchall()
            return [dict(book) for book in books]
