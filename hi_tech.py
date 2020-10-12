import threading
import urllib.request
from random import shuffle
from bs4 import BeautifulSoup as soup
import webbrowser
from tkinter import *
import tkinter.font as font

from googlesearch import search



def open_company():
    global  next_company_name
    url=search(current_company_name.get() + " israel student", tld='co.il', lang='he', num=1, start=0, stop=1, pause=0).__next__()
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(url)

def list_length():
    i=0
    while i<len(names):
        yield i
        i+=1
    return -1

def get_next_company_number(gen):
    global next_company_name,current_company_name
    num=next(gen)
    if num!=-1:
        current_company_name.set(next_company_name.get())
        if num==len(names)-1:
            next_company_name.set("NONE")
        else:
            next_company_name.set(names[num+1])
        print(f"Next company: {next_company_name.get()}, current looking at: {current_company_name.get()}")

        t = threading.Thread(target=lambda: open_company())
        t.start()
def labels():
    global top,next_company_name,current_company_name
    upper_text=Label(top,text="Current looking at:")
    upper_text['font']=myFont
    upper_text.grid(row=3,column=3)
    curr_label = Label(top, textvariable=current_company_name)
    curr_label['font'] = myFont
    curr_label.grid(row=3, column=4)

    lower_text=Label(top,text="Next company:")
    lower_text['font']=myFont
    lower_text.grid(row=5,column=3)
    next_label = Label(top, textvariable=next_company_name)
    next_label['font'] = myFont
    next_label.grid(row=5, column=4)
fp = urllib.request.urlopen("https://www.duns100.co.il/en/rating/High_Tech/Largest_High_Tech_Companies")
html = fp.read()
page_soup = soup(html, "html.parser")
tags = page_soup.table.tbody.find_all(attrs={"class": "company-name"})
names = [tag.span.string.strip() for tag in tags]
shuffle (names)
gen = list_length()
top = Tk()
myFont = font.Font(size=30)

next_company_name = StringVar()
next_company_name.set(names[0])
current_company_name=StringVar()
current_company_name.set("")

labels()

top.title("Raviv's Job-Finder Assistant")
# top.configure(background="#6ab04c")
icon = PhotoImage(file="images/job.png")
black_button = PhotoImage(file="images/black_button_subs.png")

top.iconphoto(False, icon)
top.geometry("1920x1080")
button=Label(top,image=black_button)
button.bind("<Button-1>",lambda event: get_next_company_number(gen))
button.grid(pady=(60,60),column=3)

top.mainloop()
