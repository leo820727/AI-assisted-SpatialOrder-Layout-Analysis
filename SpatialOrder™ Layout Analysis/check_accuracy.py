import fitz
import os
import random

def verify_accuracy(pdf_path, txt_path):
    print("=== Quality Verification Report ===")
    
    # 1. Read the organized text content into a structured format
    with open(txt_path, 'r', encoding='utf-8') as f:
        txt_lines = f.readlines()
        
    pages_txt = {}
    current_page = None
    for line in txt_lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("--- Page") and line.endswith("---"):
            current_page = int(line.split(" ")[2])
            pages_txt[current_page] = []
        elif current_page is not None:
            pages_txt[current_page].append(line)
            
    doc = fitz.open(pdf_path)
    
    # 2. Extract valid blocks from PDF
    candidates = []
    for page_num, page in enumerate(doc, 1):
        blocks = page.get_text("blocks")
        for b in blocks:
            x0, y0, x1, y1, text, block_no, block_type = b
            if block_type != 0: continue
            
            text = text.strip()
            if not text or "- Page" in text or "Page" in text and y0 > page.rect.height - 100:
                continue
                
            # Determine column
            if x0 < 126: col_idx = 0
            elif x0 < 306: col_idx = 1
            elif x0 < 486: col_idx = 2
            else: col_idx = 3
            
            # Format text identical to how it was extracted
            lines = text.split('\n')
            if len(lines) >= 2 and lines[0].strip().isdigit():
                line_no = lines[0].strip()
                content = " ".join(l.strip() for l in lines[1:])
                clean_text = f"{line_no}. {content}"
            else:
                clean_text = text.replace('\n', ' ')
                
            candidates.append({
                'page': page_num,
                'col': col_idx + 1,
                'text': clean_text,
                'bbox': (round(x0, 2), round(y0, 2), round(x1, 2), round(y1, 2))
            })

    # Pick 3 random candidates
    samples = random.sample(candidates, 3)
    
    success_count = 0
    print(f"\nRandomly selected 3 snippets from PDF for cross-verification:\n")
    
    for idx, sample in enumerate(samples, 1):
        print(f"[{idx}] Target Snippet from PDF:")
        print(f"    - Content   : '{sample['text']}'")
        print(f"    - Page      : {sample['page']}")
        print(f"    - Column    : {sample['col']} (derived from bounding box X0={sample['bbox'][0]})")
        print(f"    - PDF BBox  : {sample['bbox']}")
        
        # Check if the text actually exists in the correct page of the TXT
        if sample['page'] in pages_txt:
            if sample['text'] in pages_txt[sample['page']]:
                print(f"    => [PASS] 100% Exact match found in doc1_clean.txt on Page {sample['page']}.")
                success_count += 1
            else:
                print(f"    => [FAIL] Text not found precisely in TXT output for Page {sample['page']}.")
        else:
            print(f"    => [FAIL] Page {sample['page']} not found in TXT.")
        print("-" * 50)
        
    print(f"\nOverall Accuracy Result: {success_count}/3 ({(success_count/3)*100:.2f}%) accurate.\n")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_pdf = os.path.join(current_dir, "samples", "Doc1_4column_rotated.pdf")
    output_txt = os.path.join(current_dir, "output", "doc1_clean.txt")
    verify_accuracy(input_pdf, output_txt)
