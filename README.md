# PDF Heading and Title Extractor

This Python utility extracts structured heading information from PDF files and exports the results as JSON. It infers the document's structure by identifying titles and hierarchical headings (e.g., H1, H2, H3). This makes it ideal for generating outlines, improving navigation, and enabling automated document analysis.


---

## Features

* Extracts the document title and hierarchical outline based on font size patterns
* Classifies text blocks into H1, H2, and H3 levels
* Processes multiple PDFs in batch mode from a specified input directory
* Outputs a well-structured JSON file per PDF for downstream processing
* Lightweight and extensible: built with Python and PyMuPDF
* Supports multilingual (English, Japanese, Hindi)
  
---

## Technical Approach (Step-by-Step)

### Step 1: PDF File Loading and Text Extraction

The script uses the [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) library to open and read each PDF.

python
import fitz  # PyMuPDF

doc = fitz.open(pdf_path)  # Load PDF document


* It iterates through each page to extract text blocks using get_text("dict")
* Each block is broken down into lines and spans (the smallest unit containing font and style metadata)

### Step 2: Font Size Collection and Grouping

The spans are analyzed to collect:

* Font size (rounded to 1 decimal)
* Associated text and page number

python
font_sizes[size] += 1
headings_by_size[size].append((text, page_num))
candidate_titles[text] += size


* font_sizes: Tracks how frequently each font size appears
* headings_by_size: Maps each font size to a list of text entries
* candidate_titles: Scores potential titles based on font size weight

### Step 3: Inferring Heading Levels (H1, H2, H3)

The three largest font sizes are assumed to correspond to the top three heading levels.

python
most_common = sorted(font_sizes.items(), key=lambda x: -x[0])[:3]
size_to_level = {
    most_common[0][0]: "H1",
    most_common[1][0]: "H2",
    most_common[2][0]: "H3"
}


### Step 4: Constructing Document Outline

* Iterates over grouped headings by font size
* Associates each heading with its hierarchical level (H1/H2/H3)
* Removes duplicates using a set

python
outline.append({"level": level, "text": text, "page": page_num})


### Step 5: Title Detection

* The candidate with the highest cumulative font size score is considered the most likely title

python
title = sorted(candidate_titles.items(), key=lambda x: -x[1])[0][0]


### Step 6: Batch Processing of PDFs

All .pdf files in the input directory are processed one by one:

python
for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        title, outline = extract_title_and_headings(pdf_path)


Results are written as JSON:

python
with open(out_path, "w") as f:
    json.dump({"title": title, "outline": outline}, f, indent=2)


---

## Output JSON Format

json
{
  "title": "Example Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Introduction",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Problem Statement",
      "page": 2
    }
  ]
}


---

## File Paths

| Purpose      | Path          |
| ------------ | ------------- |
| Input PDFs   | /app/input  |
| Output JSONs | /app/output |

Modify these values in the __main__ block to match your project structure.

---

## Installation

### Requirements

* Python 3.11 or later
* [PyMuPDF](https://pypi.org/project/PyMuPDF/)

## How to Use

1. Clone the repository:
   bash
   git clone https://github.com/PiyushKumar23-12/Round1_a
   
2. Put your PDFs into the input/ folder.

3. Make sure output/ folder exists.

4. Run Docker Desktop/Engine.

5. Build and run the Docker container using the below commands in PowerShell:

   bash
   ```
   docker build -t pdf-outline-extractor .
   docker run --rm -it -v "${PWD}\app\input:/app/input" -v "${PWD}\app\output:/app/output" pdf-outline-extractor
   ```
   

### Key Docker Features

* *Multi-stage build*: Reduces final image size by separating build dependencies
* *Non-root user*: Runs as appuser for enhanced security
* *Optimized caching*: Removes unnecessary files and cache to minimize image size
* *CPU-optimized PyTorch*: Uses CPU-only PyTorch wheels for faster downloads

## Output

Each input PDF will generate a corresponding .json file in the output folder with title and structured outline.

![Sample_output](https://github.com/user-attachments/assets/78b3a220-e0fa-4274-8c05-1d744e87979a)
