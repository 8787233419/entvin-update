# # import requests
# # import fitz
# # from PIL import Image
# # import io
# # import os

# # def highlight_text_in_pdf(pdf_url, text_to_highlight, output_image_path):
# #     # Download the PDF from the URL
# #     response = requests.get(pdf_url)
# #     if response.status_code != 200:
# #         print("Failed to download the PDF.")
# #         return

# #     # Save the PDF to a temporary file
# #     temp_pdf_path = "temp_downloaded_pdf.pdf"
# #     with open(temp_pdf_path, 'wb') as f:
# #         f.write(response.content)

# #     # Open the downloaded PDF file
# #     pdf = fitz.open(temp_pdf_path)

# #     # Loop through each page to find the text
# #     for page_number in range(len(pdf)):
# #         page = pdf[page_number]
# #         text_instances = page.search_for(text_to_highlight)

# #         # Highlight all instances of the text found
# #         for inst in text_instances:
# #             highlight = page.add_highlight_annot(inst)
# #             highlight.update()

# #         # If text was found and highlighted, save the page as an image
# #         if text_instances:
# #             zoom_x = 2.0  # Adjust the zoom level as needed
# #             zoom_y = 2.0
# #             mat = fitz.Matrix(zoom_x, zoom_y)
# #             page_pixmap = page.get_pixmap(matrix=mat)
# #             page_pixmap.save(output_image_path)
# #             print(f"Highlighted text found on page {page_number + 1} and saved as {output_image_path}")
# #             break
# #     else:
# #         print("Text not found in the PDF.")

# #     # Close the PDF and remove the temporary file
# #     pdf.close()
# #     os.remove(temp_pdf_path)

# # # Example usage
# # pdf_file_url = "https://www.accessdata.fda.gov/drugsatfda_docs/label/2024/214998s009lbl.pdf"

# # # text_to_highlight = "ethinyl estradiol"
# # # text_to_highlight = """norethindrone may be used with mavacamten. However, CAMZYOS may reduce the
# # # effectiveness of certain other combined hormonal contraceptives (CHC). If these CHCs are used,
# # # advise patients to add nonhormonal contraception (such as condoms) during concomitant use and
# # # for 4 months after the last dose of CAMZYOS"""
# # output_image_file = "highlighted_paragraph.png"

# # highlight_text_in_pdf(pdf_file_url, text_to_highlight, output_image_file)

# import requests
# import fitz
# from PIL import Image
# import io
# import os

# def highlight_text_in_pdf(pdf_url, text_to_highlight, output_image_path):
#     # Download the PDF from the URL
#     response = requests.get(pdf_url)
#     if response.status_code != 200:
#         print("Failed to download the PDF.")
#         return

#     # Save the PDF to a temporary file
#     temp_pdf_path = "temp_downloaded_pdf.pdf"
#     with open(temp_pdf_path, 'wb') as f:
#         f.write(response.content)

#     # Open the downloaded PDF file
#     pdf = fitz.open(temp_pdf_path)

#     # Store information about where the text was found
#     found_pages = []

#     # Loop through each page to find the text
#     for page_number in range(len(pdf)):
#         page = pdf[page_number]
#         text_instances = page.search_for(text_to_highlight)

#         # Highlight all instances of the text found
#         for inst in text_instances:
#             highlight = page.add_highlight_annot(inst)
#             highlight.update()

#         if text_instances:
#             found_pages.append(page_number)
#             zoom_x = 2.0  # Adjust the zoom level as needed
#             zoom_y = 2.0
#             mat = fitz.Matrix(zoom_x, zoom_y)
#             page_pixmap = page.get_pixmap(matrix=mat)
#             img_bytes = page_pixmap.tobytes(output="png")

#             # Save the image
#             output_img_path = f"{output_image_path}_page_{page_number + 1}.png"
#             with open(output_img_path, "wb") as img_file:
#                 img_file.write(img_bytes)
#             print(f"Highlighted text found on page {page_number + 1} and saved as {output_img_path}")
    
#     # Handling the case where text might span two pages
#     if len(found_pages) > 0:
#         for i in range(len(found_pages) - 1):
#             if found_pages[i + 1] == found_pages[i] + 1:
#                 print(f"Text might span across page {found_pages[i] + 1} and {found_pages[i + 1] + 1}.")
#                 # You may want to merge these two pages' images manually or through additional code.

#     if not found_pages:
#         print("Text not found in the PDF.")

#     # Close the PDF and remove the temporary file
#     pdf.close()
#     os.remove(temp_pdf_path)

# # Example usage
# pdf_file_url = "https://www.accessdata.fda.gov/drugsatfda_docs/label/2024/214998s009lbl.pdf"
# text_to_highlight ="""CAMZYOS may cause fetal toxicity when administered to a pregnant female, based on findings
# in animal studies. Confirm absence of pregnancy in females of reproductive potential prior to
# treatment and advise patients to use effective contraception"""
# output_image_file = "highlighted_paragraph"

# highlight_text_in_pdf(pdf_file_url, text_to_highlight, output_image_file)
import re


def updates_count(data):
    count=re.findall(r'\b(?:[1-9]|1[0-2])\/\d{4}\b',data)

    print(count)


updates_count('Dosage and Administration, Pregnancy Testing before Removed 4/2024 Initiation of JULUCA (2.1) Warnings and Precautions, Embryo Fetal Toxicity (5.3) Removed 4/2024')    

text = "Some important dates are 04/2024, 12/2025, and 13/2023."

pattern = r"\b(0[1-9]|1[0-2])\/\d{4}\b"

matches = [(match.group(0), match.start()) for match in re.finditer(pattern, text)]

print(matches[0][0],len(matches))