import fitz  # PyMuPDF
import difflib
import os
from PIL import Image

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = {}
    for page_num in range(len(doc)):
        page = doc[page_num]
        text[page_num] = page.get_text()
    return text

def detect_changes(old_text, new_text):
    """Detect changes between old and new text."""
    changes = {}
    for page_num in new_text.keys():
        old_page = old_text.get(page_num, "")
        new_page = new_text[page_num]
        diff = difflib.ndiff(old_page.splitlines(), new_page.splitlines())
        changes[page_num] = [line for line in diff if line.startswith('+ ')]
    return changes

def highlight_changes_in_pdf(old_pdf_path, new_pdf_path, output_image_path):
    """Highlight changes in the new PDF compared to the old PDF."""
    old_text = extract_text_from_pdf(old_pdf_path)
    new_text = extract_text_from_pdf(new_pdf_path)
    
    changes = detect_changes(old_text, new_text)

    doc = fitz.open(new_pdf_path)
    for page_num, change_lines in changes.items():
        if change_lines:
            page = doc[page_num]
            for line in change_lines:
                text_to_highlight = line[2:]  # Remove the '+ ' prefix
                text_instances = page.search_for(text_to_highlight)
                for inst in text_instances:
                    highlight = page.add_highlight_annot(inst)
                    highlight.update()
            
            # Save the page as an image
            pix = page.get_pixmap()
            img_path = f"{output_image_path}/highlighted_page_{page_num + 1}.png"
            pix.save(img_path)
            print(f"Highlighted changes saved as {img_path}")

    doc.close()

# Example usage:
highlight_changes_in_pdf('old_test_pdf.pdf', 'New_test_pdf.pdf', 'output_images')