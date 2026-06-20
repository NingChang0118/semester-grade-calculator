# Changelog

All notable changes to this project will be documented in this file.

## [v1.2.0] - 2026-06-20

### Added

* 新增 GPA 趨勢圖
* 新增學期 GPA 趨勢資料整理
* 新增 GPA 趨勢圖數值標籤

### Changed

* GPA 趨勢圖改用 matplotlib 靜態圖表
* GPA 趨勢資料依學年與學期順序排序
* 學年排序支援擷取數字，提升資料輸入相容性

### Fixed

* 修正 GPA 趨勢圖中文字型顯示問題
* 修正學期順序可能顯示異常的問題

## [v1.1.0] - 2026-06-19

### Added

* 新增課程學分管理
* 新增 GPA 計算功能
* 新增學期 GPA 統計
* 新增累積 GPA 統計
* 新增 GPA 頁面學年／學期篩選
* 新增課程等第顯示
* 新增課程 GPA 點數顯示

### Changed

* 側邊欄改為學年／學期雙層收合導覽
* 課程摘要新增學分資訊
* GPA 頁面改為表格顯示課程資訊

### Fixed

* 修正編輯課程時成績項目未載入問題
* 修正編輯課程需重新選擇課程問題
* 修正舊版資料缺少學分欄位的相容性問題

## [v1.0.0] - 2026-06-19

### Added

* 多門課程管理
* 成績項目管理
* 加權成績計算
* 目標分數推估
* 學年／學期分類
* JSON 資料持久化
* Streamlit Web 介面
* 完整 CRUD 功能