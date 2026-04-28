-- 讀書筆記本 (Book Notes) 資料庫建表語法
-- 使用 SQLite 語法

CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT,
    review TEXT,
    rating INTEGER DEFAULT 0,
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
