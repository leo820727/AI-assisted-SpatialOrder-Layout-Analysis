import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape, portrait
from reportlab.lib.units import inch

def generate_pdf(filename, num_columns, is_landscape, num_pages):
    # Set page size (A4 is also fine, but standard transcript is often letter)
    pagesize = landscape(letter) if is_landscape else portrait(letter)
    width, height = pagesize
    
    # Initialize Canvas
    c = canvas.Canvas(filename, pagesize=pagesize)
    
    # Define margins and layout
    margin_x = 0.5 * inch
    margin_top = 0.75 * inch
    bottom_margin = 0.75 * inch
    
    # Calculate column properties
    usable_width = width - 2 * margin_x
    col_width = usable_width / num_columns
    
    # Calculate row properties for exactly 25 lines
    usable_height = height - margin_top - bottom_margin
    line_spacing = usable_height / 25
    line_start_y = height - margin_top - line_spacing # Top line Y coordinate
    
    for page in range(1, num_pages + 1):
        for col in range(num_columns):
            base_x = margin_x + col * col_width
            
            # Draw line numbers and content for 25 lines
            for line_index in range(1, 26):
                y = line_start_y - (line_index - 1) * line_spacing
                
                # Draw Line Number
                c.setFont("Helvetica", 10)
                c.drawString(base_x, y, str(line_index))
                
                # Draw Mock Text
                c.setFont("Helvetica", 10)
                
                if col % 2 == 0:
                    speaker = "Q."
                    text = f"Could you state your name for the record?"
                else:
                    speaker = "A."
                    text = f"Yes, I am a witness in column {col+1}."
                
                # Make some random dialogue just for variation
                if line_index % 3 == 0:
                    text = "[Witness nods]"
                    speaker = ""
                elif line_index % 5 == 0:
                    speaker = "THE COURT:"
                    text = "Please answer the question clearly."
                elif line_index % 7 == 0:
                    speaker = "MR. SMITH:"
                    text = "Objection, Your Honor. Hearsay."
                elif line_index % 9 == 0:
                    speaker = "THE COURT:"
                    text = "Overruled. You may answer."
                    
                # Small padding from line number
                content_x = base_x + 0.3 * inch
                
                if speaker:
                    c.drawString(content_x, y, f"{speaker} {text}")
                else:
                    c.drawString(content_x, y, text)
                    
            # Draw vertical separator line between columns
            if col < num_columns - 1:
                line_x = base_x + col_width - 0.2 * inch
                c.setLineWidth(0.5)
                # Draw from top of text area down to bottom of text area
                c.line(line_x, height - margin_top, line_x, bottom_margin)
                
        # Draw Page Number at bottom center
        c.setFont("Helvetica", 10)
        c.drawCentredString(width / 2.0, bottom_margin / 2.0, f"- Page {page} -")
        
        # Finish the page
        c.showPage()
        
    c.save()

def main():
    # 1. 建立 /samples 目錄 (在當前路徑下建立)
    output_dir = "samples"
    os.makedirs(output_dir, exist_ok=True)
    
    # 2. 生成 Doc 1: 4 欄位佈局，橫向（Landscape）旋轉 90 度，這裡設定 5 頁做測試
    path1 = os.path.join(output_dir, "Doc1.pdf")
    generate_pdf(path1, num_columns=4, is_landscape=True, num_pages=5)
    print(f"Generated: {path1} (Landscape, 4 columns, 5 pages)")
    
    # 3. 生成 Doc 2-5: 2 欄位標準佈局，直向（Portrait）。頁數分別為 7, 11, 24, 44 頁
    docs = [
        ("Doc2.pdf", 7),
        ("Doc3.pdf", 11),
        ("Doc4.pdf", 24),
        ("Doc5.pdf", 44)
    ]
    
    for filename, pages in docs:
        path = os.path.join(output_dir, filename)
        generate_pdf(path, num_columns=2, is_landscape=False, num_pages=pages)
        print(f"Generated: {path} (Portrait, 2 columns, {pages} pages)")

if __name__ == "__main__":
    main()
