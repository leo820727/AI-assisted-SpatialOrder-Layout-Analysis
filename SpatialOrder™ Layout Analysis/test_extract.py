import pdfplumber

with pdfplumber.open("samples/Doc1_4column_rotated.pdf") as pdf:
    page = pdf.pages[0]
    print(f"Page width: {page.width}, height: {page.height}")
    
    # 邏輯分欄: 4 欄位
    w = page.width
    col_width = w / 4.0
    
    for i in range(4):
        bbox = (i * col_width, 0, (i + 1) * col_width, page.height)
        col_page = page.crop(bbox)
        text = col_page.extract_text()
        print(f"\n--- Column {i+1} ---")
        lines = text.split('\n')
        for idx, line in enumerate(lines[:5]): # just print first 5 lines
            print(line)
