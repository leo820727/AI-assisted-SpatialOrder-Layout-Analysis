import fitz
import os

def process_pdf_2col(input_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = fitz.open(input_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for page_num, page in enumerate(doc, 1):
            f.write(f"--- Page {page_num} ---\n")
            
            if page.rotation != 0:
                pass
            
            blocks = page.get_text("blocks")
            
            # Midpoint for 2 columns on letter portrait (width 612): 306
            columns = {0: [], 1: []}
            
            for b in blocks:
                x0, y0, x1, y1, text, block_no, block_type = b
                
                if block_type != 0:
                    continue
                
                text = text.strip()
                if not text:
                    continue
                    
                if "- Page" in text or "Page" in text and y0 > page.rect.height - 100:
                    continue
                    
                if x0 < 306:
                    col_idx = 0
                else:
                    col_idx = 1
                    
                columns[col_idx].append({'y0': y0, 'text': text})
            
            for col_idx in range(2):
                col_blocks = sorted(columns[col_idx], key=lambda block: block['y0'])
                
                for block in col_blocks:
                    text = block['text']
                    lines = text.split('\n')
                    if len(lines) >= 2 and lines[0].strip().isdigit():
                        line_no = lines[0].strip()
                        content = " ".join(l.strip() for l in lines[1:])
                        out_line = f"{line_no}. {content}"
                    else:
                        out_line = text.replace('\n', ' ')
                    
                    f.write(out_line + "\n")
            
            f.write("\n")
            
    print(f"Successfully processed Doc and saved to output")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for i in range(2, 6):
        input_pdf = os.path.join(current_dir, "samples", f"Doc{i}.pdf")
        output_txt = os.path.join(current_dir, "output", f"doc{i}_clean.txt")
        if os.path.exists(input_pdf):
            process_pdf_2col(input_pdf, output_txt)
