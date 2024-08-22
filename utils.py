import requests
import pandas as pd
import io,re
# from io import BytesIO
import fitz
from dotenv import load_dotenv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pdfminer.high_level import extract_text
import fitz  
from PIL import Image

load_dotenv()

import difflib

def remove_character(text):
    cleaned_text = re.sub(r'^[-_]+|[-_]+$', '', text)
    cleaned_text=cleaned_text.replace('\n','')
    return cleaned_text
def text_edit(text, text_for_bold):
    if text is None:
        return None

    normalized_text = re.sub(r'\s+', ' ', text)
    normalized_text_for_bold = re.sub(r'\s+', ' ', text_for_bold)
    
    pattern = re.escape(normalized_text_for_bold)
    
    if re.search(pattern, normalized_text):
        print(10)
        bolded_text = re.sub(pattern, f"<b>{normalized_text_for_bold}</b>", normalized_text)
        return bolded_text
    else:
        print(9)
        return text
        
def find_extra_text(original_para, new_para):
 
    diff = difflib.ndiff(original_para.split(), new_para.split())
    extra_text = ' '.join([word[2:] for word in diff if word.startswith('+ ')])
    return extra_text

def find_replaced_text(original_para, new_para):

    diff = difflib.ndiff(original_para.split(), new_para.split())
    replaced_text = ' '.join([word[2:] for word in diff if word.startswith('- ')])
    return replaced_text

def remove_number_dot_and_extra_space(string):
    # Remove any number and dot from the string
    text= re.sub(r'\.{2,}', ' ', string) 
    return text
def clean_text(text):
    # Remove lines containing "Page xx of xx"
    # Remove lines containing "Reference ID: xxxxxxx"
    # Remove extra whitespace
    # print("text after string", text)
    text = re.sub(r'.*Page \d+ of \d+.*\n?', '', text)
    text = re.sub(r'.*Reference ID: \d+.*\n?', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    # print("text after reference", text)
    text = re.sub(r'This label may not be the latest approved by FDA.','',text)
    # print("text after remove label", text)
    text = re.sub(r'For current labeling information, please visit https://www.fda.gov/drugsatfda', '', text)
    text = re.sub(r'\s*\d+(\.\s*)?$', '', text)
    return text

def remove_newline(string):
    text=re.sub(r'\n','',string)
    return text
def remove_space(string):
    text=re.sub(r' ','',string)
    return text

def read_csv_from_url(new_url,old_url):

    data_1=read_new_csv(new_url)
    if data_1 is None:
        print('no data 1')
        return "No Changes" 
    data_2=read_old_csv(old_url)

    if data_2 is None:
        print('no data 2')
        return data_1

    data_1=remove_character(data_1)
    data_2=remove_character(data_2)

    desired_text=data_1.replace(data_2,'')
    print(desired_text)
    return desired_text

def read_new_csv(new_url):    
    new_response=requests.get(new_url)

    if new_response.status_code==200:
        # print(response.content)
        new_pdf_file = io.BytesIO(new_response.content)

    # Open the PDF using PyMuPDF
        new_doc = fitz.open(stream=new_pdf_file, filetype="pdf")
        
        for i in range(0,1):
            page=new_doc[i]
            text=page.get_text()
            # print(text)
            if 'RECENT MAJOR CHANGES' in text:
                # print ('text found')
                start_index=text.index('RECENT MAJOR CHANGES')+len('RECENT MAJOR CHANGES')+18
                end_index=text.index('INDICATIONS AND USAGE')
                if end_index is None:
                    end_index=text.index('__________________ INDICATIONS AND USAGE_________________')
                if end_index is None:
                    end_index=text.index('__________________ INDICATIONS AND USAGE _________________')
                if end_index is None:
                    end_index=text.index('__________________INDICATIONS AND USAGE_________________')
                if end_index is None:
                    end_index=text.index('------------------------------INDICATIONS AND USAGE------------------------')
                if end_index is None:
                    end_index=text.index('------------------------------ INDICATIONS AND USAGE ------------------------')
                if end_index is None:
                    end_index=text.index('------------------------------INDICATIONS AND USAGE ------------------------')
                if end_index is None:
                    end_index=text.index('------------------------------ INDICATIONS AND USAGE------------------------')
                # print(start_index)
                # print(end_index)
                desired_text = text[start_index:end_index].strip()
                formatted_text = desired_text.replace('\n', '\n')                   
                desired_text=remove_number_dot_and_extra_space(formatted_text)
                print(desired_text)

                return desired_text
            else:
                return None 
    else:
        print('fail')

def read_old_csv(old_url):

    old_response=requests.get(old_url)

    if old_response.status_code==200:
        # print(response.content)
        old_pdf_file = io.BytesIO(old_response.content)
    # Open the PDF using PyMuPDF
        old_doc = fitz.open(stream=old_pdf_file, filetype="pdf")   
        
        for i in range(0,len(old_doc)):
            page=old_doc[i]
            text=page.get_text()
        
            if 'RECENT MAJOR CHANGES' in text:
                # print ('text found')
                start_index=text.index('RECENT MAJOR CHANGES')+len('RECENT MAJOR CHANGES')+18
                end_index=text.index('INDICATIONS AND USAGE')
                if end_index is None:
                    end_index=text.index('__________________INDICATIONS AND USAGE _________________')
                if end_index is None:
                    end_index=text.index('__________________INDICATIONS AND USAGE_________________')
                if end_index is None:
                    end_index=text.index('__________________ INDICATIONS AND USAGE_________________')
                # print(start_index)
                # print(end_index)
                desired_text = text[start_index:end_index].strip()
                formatted_text = desired_text.replace('\n', '\n')                   
                desired_text=remove_number_dot_and_extra_space(formatted_text)
                print(desired_text)
                return desired_text
            else:
                return None
    else:
        print('fail') 
     

def changed_text(new_url,heading):

        
        subsection=heading.split(',')[1].split('(')[0]
        subsection_no=heading.split('(')[1].split(')')[0]
        subsection_no=remove_space(subsection_no)
        section=heading.split(',')[0]
        section=remove_newline(section)
        section=subsection_no.split('.')[0] + '.' + section
        print(subsection_no)
        print(subsection)
        # print(heading.split('(')[1])
        print(subsection_no+subsection)
        new_response=requests.get(new_url)

        if new_response.status_code==200:
            # print(response.content)
            new_pdf_file = io.BytesIO(new_response.content)
            # print(1)
        # Open the PDF using PyMuPDF
            # new_doc = fitz.open(stream=new_pdf_file, filetype="pdf")
            text=""
            # for i in range(0,6):
            #     page=new_doc[i]
            #     text=page.get_text()
            text=extract_text(new_pdf_file)
            text=clean_text(text) 
            # print (text) 
            va=subsection_no+subsection 
            va=re.escape(va) 
            try:
                # print(2)
                start=re.search(rf'\.\s{subsection_no}{subsection}[A-Z]',text)
                if start is None:
                    start=start=re.search(rf'\.\s{subsection_no}\.{subsection}[A-Z]',text)
                # print(start)
                start_index=start.span()[0]+len(subsection_no)+len(subsection)+2
                if start_index:
                    print('pass')
                # point=str(f"{subsection_no}")
                # text = text.split(point)[1]
                        # print(text)
                end=re.search(r'\d+(\.\d+)?[.\s]*[A-Z]',text[start_index+len(va):len(text)])
                end_index=end.span()[0]+start_index+len(va)
                # print(end_index)
                if end_index is None:
                    # page=new_doc[i+1]
                    # text+=page.get_text()
                    end_index=re.search(r'\d+(\.\d+)?[.\s]*\w+',text)
                    desired_text=text[start_index:end_index].strip()
                    # print(desired_text)
                    return desired_text
                else:
                    desired_text=text[start_index:end_index].strip()
                    # print(desired_text)
                    return desired_text
            except Exception as e:
                print(e)
            

    
    # else:
    #     print ('fail1')
    # return


def mailToId(receiver_email_id, message, cc=None, subject="EntVin"):
    username = os.getenv('MAIL_USERNAME')
    password = os.getenv('MAIL_PASSWORD')
    sender_email_id = f"noreply.{username}"

    msg = MIMEMultipart("alternative")  # Specify that the email is multipart/alternative
    msg['From'] = sender_email_id
    msg['To'] = receiver_email_id
    msg['Subject'] = subject

    if cc:
        msg['Cc'] = ", ".join(cc) if isinstance(cc, list) else cc
        receiver_email_id = [receiver_email_id] + (cc if isinstance(cc, list) else [cc])

    # Attach the HTML message
    msg.attach(MIMEText(message, "html"))

    try:
        smtp = smtplib.SMTP(
            os.getenv('MAIL_SERVER'),
            os.getenv('MAIL_PORT'),
            timeout=100
        )

        smtp.starttls()
        smtp.login(username, password)
        smtp.sendmail(sender_email_id, receiver_email_id, msg.as_string())
        smtp.quit()

        print(
            f"Message sent successfully to {receiver_email_id}")
        return True
    except Exception as ex:
        print("Something went wrong....", ex)
        return False           
    
# import fitz  # PyMuPDF
# from PIL import Image
# import io

# def highlight_text_in_pdf(pdf_url, text_to_highlight):
#     # Download the PDF file
#     response = requests.get(pdf_url)
#     pdf_file = io.BytesIO(response.content)

#     try:
#         # Open the PDF file
#         doc = fitz.open(stream=pdf_file, filetype="pdf")
#         text_to_highlight = text_to_highlight.strip()

#         image_paths = []
#         text_found = False

#         for page_num in range(len(doc)):
#             try:
#                 page = doc[page_num]
#                 page_text = page.get_text()

#                 # Search for the text in the current page
#                 text_instances = page.search_for(text_to_highlight)

#                 if text_instances:
#                     # Highlight text found on the current page
#                     for inst in text_instances:
#                         highlight = page.add_highlight_annot(inst)
#                         highlight.update()

#                     # Convert the page to an image after highlighting
#                     pix = page.get_pixmap()
#                     img_data = pix.pil_tobytes(format="PNG")
#                     img = Image.open(io.BytesIO(img_data))
#                     img_path = f"highlighted_page_{page_num + 1}.png"
#                     img.save(img_path)
#                     image_paths.append(img_path)

#                     text_found = True
#                     break

#                 # If not found, check if the text could be split across two pages
#                 elif page_num < len(doc) - 1:
#                     next_page = doc[page_num + 1]
#                     next_page_text = next_page.get_text()

#                     # Combine the end of the current page text with the beginning of the next page text
#                     combined_text = page_text + " " + next_page_text
#                     combined_instances = page.search_for(text_to_highlight)

#                     if combined_text.find(text_to_highlight) != -1:
#                         # Highlight on the current page
#                         for inst in page.search_for(text_to_highlight[:len(page_text)]):
#                             highlight = page.add_highlight_annot(inst)
#                             highlight.update()

#                         # Highlight on the next page
#                         for inst in next_page.search_for(text_to_highlight[len(page_text):]):
#                             highlight = next_page.add_highlight_annot(inst)
#                             highlight.update()

#                         # Convert the current page to an image after highlighting
#                         pix = page.get_pixmap()
#                         img_data = pix.pil_tobytes(format="PNG")
#                         img = Image.open(io.BytesIO(img_data))
#                         img_path = f"highlighted_page_{page_num + 1}.png"
#                         img.save(img_path)
#                         image_paths.append(img_path)

#                         # Convert the next page to an image after highlighting
#                         pix = next_page.get_pixmap()
#                         img_data = pix.pil_tobytes(format="PNG")
#                         img = Image.open(io.BytesIO(img_data))
#                         next_img_path = f"highlighted_page_{page_num + 2}.png"
#                         img.save(next_img_path)
#                         image_paths.append(next_img_path)

#                         text_found = True
#                         break

#             except Exception as page_error:
#                 print(f"Error processing page {page_num + 1}: {page_error}")
#                 continue

#         if text_found:
#             return image_paths
#         else:
#             print("No instances of the text found.")
#             return None

#     except Exception as e:
#         print(f"An error occurred while processing the PDF: {e}")
#         return None
def highlight_text_in_pdf(pdf_url, text_to_highlight, output_image_path):
    # Download the PDF from the URL
    response = requests.get(pdf_url)
    if response.status_code != 200:
        print("Failed to download the PDF.")
        return

    # Save the PDF to a temporary file
    temp_pdf_path = "temp_downloaded_pdf.pdf"
    with open(temp_pdf_path, 'wb') as f:
        f.write(response.content)

    # Open the downloaded PDF file
    pdf = fitz.open(temp_pdf_path)

    # Loop through each page to find the text
    for page_number in range(len(pdf)):
        page = pdf[page_number]
        text_instances = page.search_for(text_to_highlight)

        # Highlight all instances of the text found
        for inst in text_instances:
            highlight = page.add_highlight_annot(inst)
            highlight.update()

        # If text was found and highlighted, save the page as an image
        if text_instances:
            zoom_x = 2.0  # Adjust the zoom level as needed
            zoom_y = 2.0
            mat = fitz.Matrix(zoom_x, zoom_y)
            page_pixmap = page.get_pixmap(matrix=mat)
            page_pixmap.save(output_image_path)
            print(f"Highlighted text found on page {page_number + 1} and saved as {output_image_path}")
            break
    else:
        print("Text not found in the PDF.")

    # Close the PDF and remove the temporary file
    pdf.close()
    os.remove(temp_pdf_path)

def find_difference(old_paragraph, new_paragraph):
    """
    Find the first point of difference between two paragraphs by words
    and return the text from that point to the end in the new paragraph.
    
    :param old_paragraph: The original paragraph.
    :param new_paragraph: The revised paragraph.
    :return: The part of the new paragraph from the first difference to the end.
    """
    # Split paragraphs into words
    if old_paragraph is None:
        return new_paragraph
    if new_paragraph is None:
        return old_paragraph
    old_words = old_paragraph.split()
    new_words = new_paragraph.split()

    # Find the first point of difference
    for i in range(min(len(old_words), len(new_words))):
        if old_words[i] != new_words[i]:
            return " ".join(new_words[i:])
    
    # If no difference is found and the new paragraph is longer, return the extra part
    if len(new_words) > len(old_words):
        return " ".join(new_words[len(old_words):])
    
    # If they are identical or old_paragraph is longer, return an empty string
    return ""


def updates_count(text):
    
    pattern = r"\b([1-9]|1[0-2])\/\d{4}\b"

    matches = [(match.group(0), match.start()) for match in re.finditer(pattern, text)]    

    count=len(matches)
    if count==0:
        pattern = r"\b(0[1-9]|1[0-2])\/\d{4}\b"

        matches = [(match.group(0), match.start()) for match in re.finditer(pattern, text)]  
        count=len(matches)
               
    if 'Removed' in text:
        removed=True
    else:
        removed=False

    return count,removed


# def fetch_data_from_api(application_no):
#     try:
#         api_url=f'https://api.fda.gov/drug/label.json?search=openfda.application_number:NDA{application_no}'
#         response = requests.get(api_url)
#         response.raise_for_status()  # Check if the request was successful
#         data = response.json()  # Assuming the API returns JSON data
#         # changes=data['recent_major_changes']
#         return data
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")
#         return None    