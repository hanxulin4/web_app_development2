# 讀書筆記本 (Book Notes) - 流程圖文件

本文件根據 PRD 與架構設計，將「讀書筆記本」系統的使用者操作路徑與後端資料流視覺化，確保開發前所有邏輯無遺漏。

## 1. 使用者流程圖（User Flow）

此流程圖展示了使用者進入網站後，可以進行的各種操作與頁面跳轉邏輯。

```mermaid
flowchart LR
    Start([使用者開啟網址]) --> Home[首頁 - 筆記列表]
    
    Home --> Action{選擇操作}
    
    %% 新增流程
    Action -->|點擊「新增筆記」| AddForm[新增表單頁]
    AddForm --> FillAdd[填寫書名、心得、星級、留言]
    FillAdd -->|點擊送出| Home
    
    %% 搜尋流程
    Action -->|輸入關鍵字並搜尋| SearchResult[顯示搜尋結果]
    SearchResult --> Action
    
    %% 編輯流程
    Action -->|對特定筆記點擊「編輯」| EditForm[編輯表單頁]
    EditForm --> FillEdit[修改現有內容]
    FillEdit -->|點擊送出| Home
    
    %% 刪除流程
    Action -->|對特定筆記點擊「刪除」| DeleteConfirm{跳出確認視窗}
    DeleteConfirm -->|確認刪除| Home
    DeleteConfirm -->|取消| Home
```

## 2. 系統序列圖（Sequence Diagram）

以下序列圖以「**使用者新增書籍筆記**」為例，展示從前端到後端資料庫的完整互動流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (View)
    participant Route as Flask 路由 (Controller)
    participant Model as Book Model (Model)
    participant DB as SQLite 資料庫
    
    User->>Browser: 在新增表單填寫書名、心得、評分
    User->>Browser: 點擊「儲存」按鈕
    Browser->>Route: 發送 POST /add 請求 (包含表單資料)
    
    activate Route
    Route->>Model: 呼叫 add_book(書名, 心得, 評分, 留言)
    
    activate Model
    Model->>DB: 執行 INSERT INTO books ...
    DB-->>Model: 資料寫入成功
    Model-->>Route: 回傳處理成功狀態
    deactivate Model
    
    Route-->>Browser: 回傳 HTTP 302 重導向 (Redirect) 至首頁 '/'
    deactivate Route
    
    Browser->>Route: 發送 GET / 請求 (重新載入首頁)
    Route->>Model: 取得最新所有筆記
    Model->>DB: SELECT * FROM books
    DB-->>Model: 回傳資料
    Model-->>Route: 回傳筆記陣列
    Route-->>Browser: 渲染 index.html 並回傳
    Browser->>User: 看到剛剛新增的書籍出現在列表中
```

## 3. 功能清單對照表

在正式進入 API 與路由設計前，先粗略盤點各個功能對應的 URL 路徑與 HTTP 方法，為下一階段的開發作準備：

| 功能名稱 | 對應 URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| **瀏覽首頁 (列表)** | `/` | GET | 顯示所有書籍筆記（支援帶入搜尋參數） |
| **新增筆記 (顯示表單)** | `/add` | GET | 回傳空白的新增表單 HTML |
| **新增筆記 (送出資料)** | `/add` | POST | 接收表單資料並寫入資料庫 |
| **編輯筆記 (顯示表單)** | `/edit/<id>` | GET | 根據筆記 ID，回傳填好舊資料的表單 HTML |
| **編輯筆記 (送出資料)** | `/edit/<id>` | POST | 接收修改後的表單資料並更新資料庫 |
| **刪除筆記** | `/delete/<id>` | POST | 根據筆記 ID 刪除該筆資料 |
