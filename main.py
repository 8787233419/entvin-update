import pandas as pd
from utils import read_csv_from_url,mailToId,changed_text,find_extra_text,find_replaced_text,highlight_text_in_pdf,text_edit,find_difference,remove_character,updates_count

df_old=pd.read_csv(r'C:\Users\Satyam Mani Tripathi\OneDrive\Desktop\EntVin\CSV\DrugsFDA FDA-Approved Drugs.csv')
df_new=pd.read_csv(r'C:\Users\Satyam Mani Tripathi\OneDrive\Desktop\EntVin\CSV\DrugsFDA FDA-Approved Drugs 2.csv')
# df_old=pd.read_csv(r'C:\Users\Satyam Mani Tripathi\OneDrive\Desktop\EntVin\CSV\labels_214998.csv')
# df_new=pd.read_csv(r'C:\Users\Satyam Mani Tripathi\OneDrive\Desktop\EntVin\CSV\labels_214998(in).csv')
# df_old=pd.read_csv(r'C:\Users\Satyam Mani Tripathi\OneDrive\Desktop\EntVin\CSV\210192 old.csv')
# df_new=pd.read_csv(r'C:\Users\Satyam Mani Tripathi\OneDrive\Desktop\EntVin\CSV\210192 new.csv')

if len(df_new['Action Date'])>len(df_old['Action Date']):
    print('new file is added')
    new_file_url=df_new.Url[0]
    old_file_url=df_new.Url[1]
    file_data=read_csv_from_url(new_file_url,old_file_url)   #Gives the latest updated Section ,Subsection and Date in string format
    modified_file_data=remove_character(file_data)
    print(f'file_data={file_data}')
    print(f'file_data_2={modified_file_data}')
    
    if file_data is not "No Changes":    
        count,removed=updates_count(modified_file_data)
        print(count,removed)
    # print(modified_file_data)
    # result={
    #     'Updated_date':df_new['Action Date'][0],
    #     'Changes':file_data,
    #     'URL':file_url
    # }
    # updated_date=df_new['Action Date'][0]
    # df_old=df_new                               #To be checked during integration
    # df_new=None
        if count==1 and removed==False:

        # print(old_file_url)
            a=changed_text(new_file_url,modified_file_data)   #Gives the text under that subsection in new pdf
            # a=new_text(new_file_url,file_data)
            if a is None:
                print('a is none')
            b=changed_text(old_file_url,modified_file_data)   #Gives the text under that subsection in old pdf
            if b is None:
                print('b is none')            
            
            d=find_difference(a,b)
            c=find_difference(b,a)
            print(a)
            print(c)
            print(b)
            print(d)
        elif count==2 and removed==False:
            
            print("no changes")    

        # output_image_file = "highlighted_paragraph.png"
        # pic=highlight_text_in_pdf(new_file_url,c,output_image_file)
        # if pic is not None:
        #     print("image got")
        # else:
        #     print("fail")    

        # bold_a=text_edit(a,c)    
        # bold_b=text_edit(b,d) 
        # print(bold_a)   
    #     mailToId(
    #     receiver_email_id='rishabh@entvin.com',
    #     message=f"""
    # Hi Rishabh,<br><br>

    # Change highlights for the week 05-08-2024:<br>      
    # {file_data}<br><br>

    # Revised file: {new_file_url}<br>
    # Updated Date: {updated_date}<br><br>

    # <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
    #     <tr>
    #         <th>Original (<a href="{old_file_url}">Link</a>)</th>
    #         <th>Revised (<a href="{new_file_url}">Link</a>)</th>
    #     </tr>
    #     <tr>
    #         <td>{bold_b}</td>
    #         <td>{bold_a}</td>
    #     </tr>
    # </table>
    # <br>
    # Best regards,<br>
    # Team EntVin
    # """,
    #     cc='hemant@entvin.com'
    # )

else:
    print('No Changes')    
