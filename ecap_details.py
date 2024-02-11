#!/usr/bin/env python
import json
import os
from pathlib import Path

import bs4
import requests as req

url = "http://gecgudlavalleruonlinepayments.com/Default.aspx"
data_url = "https://gecgudlavalleruonlinepayments.com/ajax/StudentProfile,App_Web_studentprofile.aspx.a2a1b31c.ashx?_method=ShowStudentProfileNew&_session=rw"

usrname = None
passwd = None


def get_login_details():
    if not Path("login_details.json").exists():
        print("Enter login details")
        rollnum = input("roll num: ")
        passwrd = input("password: ")
        with open("login_details.json", "w") as f:
            data = {"RollNo": rollnum, "PassWd": passwrd}
            json.dump(data, f, indent=4)
    with open("login_details.json") as f:
        global usrname, passwd
        data = json.load(f)
        usrname = data["RollNo"]
        passwd = data["PassWd"]


DATA = ""
DETAILS = ""


def make_soup(data):
    return bs4.BeautifulSoup(data, features="lxml")


get_login_details()
rollnum = input("(roll num)> ")
data_url_post_data = f"RollNo={rollnum}\nisImageDisplay=false"

session = req.Session()
DATA = session.get(url).text

soup = make_soup(DATA)

view_state = soup.select("#__VIEWSTATE")[0]["value"]
view_state_generator = soup.select("#__VIEWSTATEGENERATOR")[0]["value"]
event_validation = soup.select("#__EVENTVALIDATION")[0]["value"]
imgBtn2x = 1 >> 1
imgBtn2y = 1 >> 1

data = {
    "__VIEWSTATE": view_state,
    "__VIEWSTATEGENERATOR": view_state_generator,
    "__EVENTVALIDATION": event_validation,
    "txtId1": "",
    "txtPwd1": "",
    "txtId2": usrname,
    "txtPwd2": passwd,
    "imgBtn2.x": imgBtn2x,
    "imgBtn2.y": imgBtn2y,
}

res = session.post(url, data)

data = res.text
soup = make_soup(data)
msg = soup.select("#lblUser")[0]
print(f"Login succesful {msg.text}")

table_test = session.post(data_url, data=data_url_post_data)
DETAILS = table_test.text

with open(rollnum + ".html", "w") as f:
    f.write(DETAILS)
    print(f"saved to {rollnum}.html(open in browser)")

ch = input("remove login details?[y/N]: ")
if ch:
    os.remove("login_details.json")
