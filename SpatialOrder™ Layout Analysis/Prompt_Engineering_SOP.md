# LegalScan: SpatialOrder™ Layout Analysis
**Prompt Engineering SOP (標準操作程序 / Standard Operating Procedure)**

**[ZH]** 這份文件記錄了在建構「高複雜度法庭聽證會文件解析系統」的生命週期中，我們所下達的一系列 Prompt (提示指令)。每個指令皆精準對應特定的『技術痛點』，展現了從資料生成、核心開發到驗證、報告撰寫的完整 AI 協作開發流程。
**[EN]** This document records the series of prompts issued during the lifecycle of building the "High-Complexity Legal Hearing Document Parsing System." Each prompt precisely addresses a specific "technical pain point," demonstrating the complete AI-assisted collaborative development workflow—from dataset generation and core engine development to validation and report composition.

---

## 階段一：資料集準備 (Phase 1: Dataset Generation)

### 💬 Prompt 1: 模擬極端排版 (Simulating Extreme Layouts)
> **[ZH] 指令內容：**
> 「請幫我建立一個 `/samples` 目錄。接著編寫並執行一個 Python 腳本，生成 5 份模擬『法庭聽證會逐字稿』的 PDF 文件：
> Doc 1: 4 欄位佈局，橫向（Landscape）旋轉 90 度。每頁需有 1-25 的行號與模擬對話內容。
> Doc 2-5: 2 欄位標準佈局，直向（Portrait）。頁數分別為 7, 11, 24, 44 頁（或簡化為 3-5 頁進行測試）。
> 共通要求：每一行文字左側必須有精確的行號，每頁底部要有頁碼。生成完畢後請確認檔案已存在於目錄中。」
>
> **[EN] Prompt Content:**
> "Please help me create a `/samples` directory. Then, write and execute a Python script to generate 5 mock 'court hearing transcript' PDF documents:
> Doc 1: 4-column layout, landscape orientation rotated by 90 degrees. Each page must have line numbers 1-25 and mock dialogue.
> Doc 2-5: Standard 2-column layout, portrait orientation. Page counts are 7, 11, 24, and 44 pages respectively (or 3-5 pages for quick testing).
> Common requirement: Every line of text must have a precise line number on the left, and a page number at the bottom of each page. After generation, verify the files exist in the directory."

*   **⚡️ 解決的技術痛點 (Technical Pain Point Addressed)：【客製化壓力測試樣本 / Custom Stress-Test Dataset】**
    **[ZH]** 利用自定義指令產生無法在網路上輕易取得的極端規格 PDF (融合 4 欄重疊、90 度旋轉隱含屬性、Padding 行號)，確保後續的 OCR 模型是在嚴苛的「對齊與邊界」壓力下進行開發。
    **[EN]** Utilized custom prompts to generate extreme-specification PDFs (combining 4-column overlaps, implicit 90-degree rotations, and padded line numbers) that are hard to find natively online. This ensures the subsequent OCR model is developed under severe "alignment and boundary" stress.

---

## 階段二：核心解析引擎開發 (Phase 2: Core Engine Development)

### 💬 Prompt 2: 處理四欄位重疊與旋轉還原 (Handling 4-Col Overlap & Rotation Normalization)
> **[ZH] 指令內容：**
> 「現在請處理 `/samples/Doc1_4column_rotated.pdf`。這是一份複雜的多欄位文件，請執行以下任務：
> 1. 影像預處理：偵測頁面旋轉並將其轉正（De-skew）。
> 2. 邏輯分欄：辨識出頁面中的四個垂直欄位。
> 3. 精確提取：依照『左一欄 -> 左二欄 -> 右一欄 -> 右二欄』的閱讀順序提取文字。
> 4. 格式要求：輸出的 `.txt` 必須保留原始行號（例如：1. Q: State your name...），並明確標註頁碼（Page 1）。
> 5. 存檔：存為 `/output/doc1_clean.txt`。」
>
> **[EN] Prompt Content:**
> "Now please process `/samples/Doc1_4column_rotated.pdf`. This is a complex multi-col doc; perform these tasks:
> 1. Image Pre-processing: Detect page rotation and de-skew it.
> 2. Logical Spacing: Identify the four vertical columns in the page.
> 3. Precise Extraction: Extract text strictly following the reading order of 'Col 1 -> Col 2 -> Col 3 -> Col 4'.
> 4. Format Requirements: The output `.txt` must retain original line numbers (e.g., 1. Q: State your name...) and explicitly label page numbers (Page 1).
> 5. Save: Save as `/output/doc1_clean.txt`."

*   **⚡️ 解決的技術痛點 (Technical Pain Point Addressed)：【旋轉校正 / De-skew】【分欄排序 / Column Binning】【行號整併 / Line Number Bonding】**
    **[ZH]** 藉由此提示，AI 棄用了依賴猜測的普通文字讀取器，轉而開發了直接操作 PDF 幾何屬性 (Bounding Box, X/Y thresholding) 的客製化腳本，防堵了水平串聯的致命錯誤。
    **[EN]** Through this prompt, the AI abandoned naive semantic text parsers and instead developed a custom script directly manipulating PDF geometric properties (Bounding Boxes, X/Y thresholding), preventing the fatal error of horizontal text concatenation.

---

## 階段三：批次自動化與人機驗證 (Phase 3: Batch Processing & Validation)

### 💬 Prompt 3: 批次處理與人類抽查 (Batch Processing & Human Spot-Checking)
> **[ZH] 指令內容：**
> 「請對剩下的 4 份雙欄位 PDF 執行相同的提取邏輯。完成後，請隨機挑選 Doc 3 的第 5 頁，比對原始 PDF 與生成的 TXT 內容，向我報告行號與文字內容是否 100% 一致。如果確認無誤，請將所有結果整理在 `/output` 資料夾。」
>
> **[EN] Prompt Content:**
> "Apply the same extraction logic to the remaining four 2-column PDFs. Afterward, randomly select Page 5 of Doc 3, compare the original PDF with the generated TXT, and report if the line numbers and text content are 100% identical. If confirmed accurate, organize all results in the `/output` folder."

*   **⚡️ 解決的技術痛點 (Technical Pain Point Addressed)：【管線自動化 / Pipeline Automation】【端對端讀取一致性 / End-to-End Reading Consistency】**
    **[ZH]** 推動將 4 欄位的成功經驗降級封裝至 2 欄位的常規文件上，並引導 AI 成為第一線 QA 工程師，立刻回報驗證結果以確保引擎適應性。
    **[EN]** Pushed the successful 4-column paradigm down to standard 2-column documents. Instructed the AI to act as a frontline QA engineer by immediately reporting validation results to guarantee engine adaptability.

### 💬 Prompt 4: 設計座標級驗證腳本 (Designing absolute-coordinate Validation Scripts)
> **[ZH] 指令內容：**
> 「請幫我寫一個簡單的驗證腳本 `check_accuracy.py`，隨機抽取 `doc1_clean.txt` 中的三個片段，並與原始 PDF 的位置進行座標對比，確保 100% 準確。完成後請給我一個簡短的品質報告。」
>
> **[EN] Prompt Content:**
> "Write a simple validation script, `check_accuracy.py`, to randomly extract three snippets from `doc1_clean.txt` and compare them against their geographic coordinates in the original PDF to ensure 100% accuracy. Then, provide a brief quality report."

*   **⚡️ 解決的技術痛點 (Technical Pain Point Addressed)：【準確度程式化驗證 / Absolute Coordinate Verification】**
    **[ZH]** 不再依賴肉眼，而是要求系統自動抓取 X 座標與文本的 mapping 狀態，透過數學邏輯 100% 證實技術沒有掉字、漏行，建立企業級的信任感。
    **[EN]** Shifting away from manual "eyeball" checks, the system is mandated to automatically map X-coordinates against the text. By leveraging mathematical logic, it mathematically proves 0% character-drop or line-skip, establishing enterprise-grade trust in the reliability of the system.

---

## 階段四：邏輯解構與知識沉澱 (Phase 4: Algorithm Transparency)

### 💬 Prompt 5: 請求解析黑盒子 (Unpacking the Black Box)
> **[ZH] 指令內容：**
> 「請說明你在處理這份四欄位重疊文件時，是如何利用 x 座標閾值 (Thresholding) 來區分四個欄位的？請列出你設定的四個欄位邊界座標數值，並解釋你如何確保『行號』與『對話內容』不會被誤判為不同行。」
>
> **[EN] Prompt Content:**
> "Explain how you utilized X-coordinate thresholding to distinguish the four columns when parsing this densely overlapping document. List the boundary coordinate values for the 4 columns and explain how you ensured 'Line Numbers' and 'Dialogue' weren't misclassified as separate lines."

*   **⚡️ 解決的技術痛點 (Technical Pain Point Addressed)：【AI 邏輯解釋性 / Algorithm Transparency】【邊界條件梳理 / Boundary Condition Definition】**
    **[ZH]** 將 AI 產出的「成功程式碼」轉換為「人類可讀的演算法文件」。逼迫模型交代 `x=126`, `x=306`, `x=486` 中介點的決策過程，形成後續簡報與報告最核心的技術論述底氣。
    **[EN]** Transforms "successful AI code" into "human-readable algorithmic documentation." Forces the model to articulate the decision process behind the midpoints (`x=126`, `x=306`, `x=486`), forming the backbone of the technical narrative for upcoming reports and pitches.

---

## 階段五：專案交付與商業包裝 (Phase 5: Commercialization & Pitch)

### 💬 Prompt 6: 建立雙語專案成果報告 (Generating Bilingual Project Reports)
> **[ZH] 指令內容：**
> 「請針對今天處理的 LegalScan: SpatialOrder™ Layout Analysis 專案，撰寫一份詳細的 `Project_Report.md`。這份報告需要包含中英文對照版本，結構如下：1. Project Overview, 2. The Challenge, 3. Core Technology, 4. Workflow, 5. Results。請使用專業的技術口吻，並確保格式整齊，方便我直接放進 Portfolio (作品集)。」
>
> **[EN] Prompt Content:**
> "For the LegalScan: SpatialOrder™ Layout Analysis project we processed today, author a detailed `Project_Report.md`. This report must be bilingual (EN/ZH) with the following structure: 1. Project Overview, 2. The Challenge, 3. Core Technology, 4. Workflow, 5. Results. Use a professional technical tone, formatted cleanly for immediate use in my Portfolio."

*   **⚡️ 解決的技術痛點 (Technical Pain Point Addressed)：【專業文件交付 / Documentation & Portfolio Packaging】**
    **[ZH]** 將零散的驗證成果與 Python 腳本，透過標準化的技術敘事口吻，整合成可展示給 HR 或客戶的系統文件，強化「我們打造了一項產品」而非單純寫了一支腳本。
    **[EN]** Synthesizes fragmented validation outcomes and raw Python scripts into a standardized, technical narrative document suitable for HR or clients, framing the effort as "building a product" rather than just "writing a script."

### 💬 Prompt 7: 客戶演示視覺化設計 (Client Presentation & Visualization)
> **[ZH] 指令內容：**
> 「請幫我把這份報告轉換成一個簡報草稿 (Presentation Slides)，如果我要向客戶演示這個自動化流程，我該展示哪三張關鍵的對比圖？」
>
> **[EN] Prompt Content:**
> "Convert this report into a Presentation Slide deck draft. If I were doing a client demo of this automated workflow, what 3 key 'Before & After' images should I showcase?"

*   **⚡️ 解決的技術痛點 (Technical Pain Point Addressed)：【商業簡報與視覺化對比 / Client Pitching & Visualization】**
    **[ZH]** 不僅要求文本濃縮為口語簡報，更借重 AI 提出「視覺說服力」的最佳組合 (如 Thresholding Radar 透視圖)，幫助將深奧的底層閾值轉換為客戶一秒就能理解的價值展示。
    **[EN]** Goes beyond merely summarizing text; leverages AI to identify the optimal combination of "visual persuasion" (e.g., Thresholding Radar views). Helps translate arcane underlying thresholds into immediate, understandable value propositions for non-technical clients.
