import requests
import selectorlib
import smtplib,ssl
import time

URL = "https://programmer100.pythonanywhere.com/tours/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrape(url):
    ''' Scrape the page source from the URL'''
    response = requests.get(url,headers=HEADERS)
    source = response.text
    return source

def extract(source):
    '''Extract the tours name value based on id which we specified in yaml in css tag '''
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465
    context = ssl.create_default_context()
    sender_email = "sharmabruno310@gmail.com"
    sender_password = "vpci hqxm ewis cvbc"
    user_email = "sharmabruno310@gmail.com"


    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, user_email,message)
    print("Email was sent!!")


def store(extracted):
    with open("data.txt","a") as file: #open file in append mode so that it doesn't override the values
        file.write(extracted + "\n")

def read(extracted_data):
    with open("data.txt","r") as file:
        return file.read()

if __name__ == "__main__":
    # print(scrape(url=URL))
    while True:
        scraped = scrape(url=URL)
        extracted = extract(source=scraped)
        print(extracted)

        content = read(extracted)
        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
                send_email(message=f"Subject: New Tour Found\nMIME-Version: 1.0\nContent-Type: text/html\n\n "
                                   f"<html><body><p>Hey, We found a new tour for you!!</p>" \
                                     f"<p><b>Tour Name:</b> <strong>{extracted}</strong></p></body></html>")
        time.sleep(2)



