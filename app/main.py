import os
import json
import fitz
import re
import unicodedata
from collections import defaultdict, Counter

def has_letter(text):
    return any(unicodedata.category(c).startswith("L") for c in text)

def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

def detect_heading(text):
    wc = len(text.split())
    if wc <= 3 and text.isupper():
        return "H1"
    elif wc <= 7:
        return "H2"
    else:
        return "H3"

def extract_title_and_headings(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    titles = []
    seen = set()
    for pno, page in enumerate(doc):
        for blk in page.get_text("dict")["blocks"]:
            if "lines" not in blk:
                continue
            for line in blk["lines"]:
                raw = " ".join(span["text"] for span in line["spans"])
                text = clean_text(raw)
                if len(text) < 4 or len(text) > 50:
                    continue
                if not has_letter(text):
                    continue
                key = f"{pno}-{text}"
                if key in seen:
                    continue
                seen.add(key)
                level = detect_heading(text)
                headings.append({"level": level, "text": text, "page": pno + 1})
                if pno == 0 and level in ("H1", "H2"):
                    titles.append(text)
    title = " | ".join(titles[:2]) if titles else "Unknown Title"
    return title, headings


def process_all_pdfs(input_dir, output_dir):
    for f in os.listdir(input_dir):
        if not f.lower().endswith(".pdf"):
            continue
        path = os.path.join(input_dir, f)
        title, outline= extract_title_and_headings(path)
        out = {"title": title, "outline": outline}
        json_path = os.path.join(output_dir, f.replace(".pdf", ".json"))
        with open(json_path, "w", encoding="utf-8") as wf:
            json.dump(out, wf, ensure_ascii=False, indent=2)
        print(f"\n✅ JSON created for {f}")

        
    

if __name__ == "__main__":
    input_dir = "/app/input"
    output_dir = "/app/output"
    os.makedirs(output_dir, exist_ok=True)
    process_all_pdfs(input_dir, output_dir)