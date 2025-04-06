# import requests
# from bs4 import BeautifulSoup
# import csv
# import smtplib
# import os
# from email.message import EmailMessage


# def scrape_scholarshipRegion(url, save_path):
#     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
#     response = requests.get(url, headers=headers)
#     print(response.status_code)

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')      
#         all_data = soup.find_all("div", class_="tdb_module_loop td_module_wrap td-animation-stack td-cpt-post")[:10]     # GETTING THE PARENT ELEMENT        
        
#         file = open(save_path, "w")     # CREATING THE CSV FILE TO SAVE THE SCRAPED DATA
#         writer = csv.writer(file)        
#         writer.writerow(["Title", "Link"])     # ADDING THE ROW HEADERS

#         for each_data in all_data:     # LOOPING THROUGH "all_data" 
#             scholarship = each_data.find("h3", class_="entry-title td-module-title")
#             link = each_data.find("a")["href"]           
#             formatted_scholarship = scholarship.text.strip()     # EXTRACTING THE TEXT FROM THE HTML CONTENT OF THE SCHOLARSHIP           
#             writer.writerow([formatted_scholarship, link])      # INSERTING THE DATA INTO THE ROWS
        
#         file.close()
#         print("List Saved Successfully")

#     else: 
#         print("Data Not Found💔")

# save_location = r"C:\Users\user\Downloads\Scholarship_Region_List.csv"

# scrape_scholarshipRegion("https://www.scholarshipregion.com/category/scholarships/masters-scholarships/", save_location)


# SCRAPE ✅
# SEND TO MAIL ✅
# AUTOMATE SCRAPING & SENDING TO MAIL 
# AUTOMATE SCRAPING & SENDING TO MAIL OFFLINE (ONLINE DATABASE)

import requests
from bs4 import BeautifulSoup
import csv
import smtplib
import io
from email.message import EmailMessage
import os


def scrape_scholarshipRegion(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)
    print(response.status_code)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')      
        all_data = soup.find_all("div", class_="tdb_module_loop td_module_wrap td-animation-stack td-cpt-post")[:10]

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Title", "Link"])

        for each_data in all_data:
            scholarship = each_data.find("h3", class_="entry-title td-module-title")
            link = each_data.find("a")["href"]
            formatted_scholarship = scholarship.text.strip()
            writer.writerow([formatted_scholarship, link])

        csv_content = output.getvalue()
        output.close()

        send_email_with_attachment(
            sender_email=os.getenv("GMAIL_SENDER_EMAIL"),
            sender_password=os.getenv("GMAIL_APP_PASSWORD"),
            receiver_email=os.getenv("RECEIVER_EMAIL"),
            subject="Scholarship Region List",
            body="How far Senior Man? Check the latest Scholarship Region list.",
            attachment_content=csv_content,
            attachment_filename="Scholarship_Region_List.csv"
        )

    else:
        print("Data Not Found 💔")


def send_email_with_attachment(sender_email, sender_password, receiver_email, subject, body, attachment_content, attachment_filename):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(body)

    msg.add_attachment(attachment_content.encode('utf-8'), maintype="application", subtype="octet-stream", filename=attachment_filename)

    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp.login(sender_email, sender_password)
    smtp.send_message(msg)

    print("Email sent successfully 📧✅")


# Calling the function
scrape_scholarshipRegion("https://www.scholarshipregion.com/category/scholarships/masters-scholarships/")
