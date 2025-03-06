import requests
import selectorlib
import smtplib,ssl
import time
import sqlite3

# Establish a connection to Db
connection = sqlite3.connect("Database.db")

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
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO EVENTS VALUES (?,?,?)",row)
    connection.commit()

def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    Event_name,Event_city,Event_date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM EVENTS where Event_name=? and Event_city=? and Event_date=?",(Event_name,Event_city,Event_date))
    rows= cursor.fetchall()
    print(rows)
    return rows

if __name__ == "__main__":
    # print(scrape(url=URL))
    while True:
        scraped = scrape(url=URL)
        extracted = extract(source=scraped)
        print(extracted)


        if extracted != "No upcoming tours":
            rows= read(extracted)
            if not rows: # This means if row not in database as row variable contain the select query from db
                store(extracted)
                send_email(message=f"Subject: New Tour Found\nMIME-Version: 1.0\nContent-Type: text/html\n\n "
                                   f"<html><body><p>Hey, We found a new tour for you!!</p>" \
                                     f"<p><b>Tour Name:</b> <strong>{extracted}</strong></p></body></html>")
        time.sleep(2)



