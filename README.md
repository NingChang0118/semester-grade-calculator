# Semester Grade Calculator

> 一個為學生打造的學期成績管理與目標分數推估工具。

Semester Grade Calculator 是一套使用 Python 開發的成績計算工具，支援 CLI 與 Streamlit Web 介面。

使用者可以建立多門課程、管理各項成績占比、設定目標分數，並即時計算目前成績、剩餘占比與達標所需分數。

---

## ✨ 功能特色

### 課程管理

* 新增課程
* 編輯課程
* 刪除課程
* 支援多門課程管理
* 支援學年與學期分類

### 成績計算

* 加權成績計算
* 剩餘占比計算
* 目標分數推估
* 達標所需平均分數計算
* 成績狀態提醒
* 加分項目支援
* 成績占比驗證

### 資料儲存

* 使用 JSON 本機儲存
* 自動載入已儲存課程
* 支援舊版資料相容

### Web 介面

* Streamlit 響應式介面
* 自訂 CSS 視覺設計
* 課程摘要卡片
* 學年 → 學期 → 科目階層式導覽
* 儲存後自動返回查看頁面

---

## 🛠️ 技術棧

### 核心技術

* Python 3.13
* dataclasses
* JSON

### CLI

* 純 Python CLI

### Web

* Streamlit

---

## 📁 專案結構

```text
semester-grade-calculator/
├─ data/
│  └─ courses.json
├─ streamlit_ui/
│  ├─ __init__.py
│  ├─ styles.py
│  ├─ components.py
│  └─ pages.py
├─ grade_calculator.py
├─ storage.py
├─ course_manager.py
├─ main.py
├─ app.py
├─ requirements.txt
└─ README.md
```

---

## 🚀 快速開始

### 1. 複製專案

```bash
git clone <repository-url>
cd semester-grade-calculator
```

### 2. 建立虛擬環境

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安裝套件

```bash
pip install -r requirements.txt
```

### 4. 啟動 Web 版本

```bash
streamlit run app.py
```

啟動後，瀏覽器會自動開啟：

```text
http://localhost:8501
```

---

## 💻 CLI 版本

若要使用 CLI 版本：

```bash
python main.py
```

---

## 📊 核心計算功能

系統可根據已完成成績與剩餘占比，自動推估：

* 目前已取得分數
* 剩餘占比
* 達成目標所需平均分數

例如：

```text
目標分數：85

目前成績：52

剩餘占比：40%

需要平均分數：82.5
```

---

## 💾 資料格式

所有課程資料皆儲存在：

```text
data/courses.json
```

範例：

```json
[
    {
        "name": "資料結構",
        "target_score": 85,
        "academic_year": "113 學年",
        "semester": "下學期",
        "items": [
            {
                "name": "期中考",
                "weight": 30,
                "score": 82,
                "completed": true,
                "is_bonus": false
            }
        ]
    }
]
```

---

## 🗺️ 開發路線圖

### v1.1

* [ ] 課程學分管理
* [ ] GPA 計算
* [ ] 學期 GPA 計算
* [ ] 累積 GPA 計算
* [ ] 成績回饋短句

### v1.2

* [ ] 成績趨勢圖
* [ ] 課程搜尋
* [ ] 課程排序
* [ ] 匯出 Excel

### Future

* [ ] 帳號系統
* [ ] 資料庫支援
* [ ] 雲端同步
* [ ] 多裝置使用
* [ ] 資料分享功能

---

## 📄 授權

本專案採用 MIT License。

---

## 👨‍💻 作者

由中原大學資訊工程學系學生開發。

如果你有任何建議或想法，歡迎提出 Issue 或交流討論。

