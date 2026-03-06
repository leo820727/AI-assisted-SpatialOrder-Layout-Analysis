import fitz

doc = fitz.open("samples/Doc1_4column_rotated.pdf")
page = doc[0]
blocks = page.get_text("blocks")
for b in blocks[:15]:
    print(b)
