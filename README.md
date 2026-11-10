# 磁力片賽車

以真實台灣山路（五指山）為賽道的 Q 版賽車遊戲，單一 HTML 檔，three.js 製作，手機與電腦都能玩。

## 玩法
競速賽、計時賽（幽靈車）、道具賽、每日挑戰、聯賽、排行榜、車庫改裝、遊戲幣抽獎；白天／黃昏／夜間三種時段。

## 檔案
- `index.html`：遊戲主頁（輕量版，資源另外載入），用 GitHub Pages 開啟即可遊玩
- `assets/`：外部資源（`tw_cars.json` 車輛模型、`real.json` 路線資料）
- `offline/game-single-file.html`：單一檔案離線版，下載後直接開啟即可玩
- `src/`：原始碼 `template.html` 與打包腳本 `build.py`
- `data/`：原始路線與地形資料、車輛 glb 模型
- `tests/`：自動測試腳本

地圖資料 © OpenStreetMap 貢獻者・地形 ASTER GDEM
