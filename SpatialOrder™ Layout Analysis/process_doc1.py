import fitz
import os

def process_pdf(input_path, output_path):
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = fitz.open(input_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for page_num, page in enumerate(doc, 1):
            f.write(f"--- Page {page_num} ---\n")
            
            # 1. 影像預處理： 偵測頁面旋轉並將其轉正（De-skew）
            if page.rotation != 0:
                print(f"Page {page_num} is rotated by {page.rotation} degrees. Deskewing...")
                # By setting rotation to 0, subsequent text extraction respects the unrotated visual layout.
                # However, our Doc1.pdf is standard landscape (0 rotation visually, just width > height).
            
            blocks = page.get_text("blocks")
            
            # 邏輯分欄
            # bases: 36, 216, 396, 576
            # midpoints: 126, 306, 486
            columns = {0: [], 1: [], 2: [], 3: []}
            page_numbers = []
            
            for b in blocks:
                x0, y0, x1, y1, text, block_no, block_type = b
                
                # Filter out image blocks
                if block_type != 0:
                    continue
                
                text = text.strip()
                if not text:
                    continue
                    
                # Check for page number block usually at the bottom center
                if "- Page" in text or "Page" in text and y0 > page.rect.height - 100:
                    page_numbers.append(text)
                    continue
                    
                # 辨識出頁面中的四個垂直欄位
                if x0 < 126:
                    col_idx = 0
                elif x0 < 306:
                    col_idx = 1
                elif x0 < 486:
                    col_idx = 2
                else:
                    col_idx = 3
                    
                columns[col_idx].append({'y0': y0, 'text': text})
            
            # 精確提取：依照 左一欄 -> 左二欄 -> 右一欄 -> 右二欄 的閱讀順序
            for col_idx in range(4):
                # Sort blocks within the column by their Y coordinate (top to bottom)
                col_blocks = sorted(columns[col_idx], key=lambda block: block['y0'])
                
                for block in col_blocks:
                    text = block['text']
                    # Handle PyMuPDF grouping line number and text with newline
                    lines = text.split('\n')
                    if len(lines) >= 2 and lines[0].strip().isdigit():
                        line_no = lines[0].strip()
                        content = " ".join(l.strip() for l in lines[1:])
                        out_line = f"{line_no}. {content}"
                    else:
                        out_line = text.replace('\n', ' ')
                    
                    f.write(out_line + "\n")
            
            f.write("\n")
            
    print(f"Successfully processed {input_path} and saved to {output_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_pdf = os.path.join(current_dir, "samples", "Doc1_4column_rotated.pdf")
    output_txt = os.path.join(current_dir, "output", "doc1_clean.txt")
    process_pdf(input_pdf, output_txt)
