import sqlite3
import eel
import datetime
import random
import time
import datetime
import bs4
import requests
import asyncio
from playwright.async_api import async_playwright
import os
import pygetwindow as gw
import base64
import sys
import win32gui
import win32con

eel.init("interface")

conn = sqlite3.connect("../dat/inventory_live_db.db")


def close_window_by_title(title):
    # Find the window by its title
    hwnd = win32gui.FindWindow(None, title)
    
    if hwnd:
        # Send a close message to the window
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        print(f"Window '{title}' has been closed.")
    else:
        print(f"No window with title '{title}' found.")

@eel.expose
def addItemToInv(itemname, itemunit, itemminqty):
    global conn
    try:
        lastid = int(conn.cursor().execute("SELECT * FROM inventory_live").fetchall()[-1][1])
        nextid = str(lastid + 1)
        conn.cursor().execute("INSERT INTO inventory_live VALUES (NULL, ?, ?, ?, ?, ?)", (nextid, str(itemname), str(itemunit), "0.0", str(itemminqty)))
        conn.commit()
        return "Item Successfully Added To Database!!!"
    except:
        return "Failed To Add Item"

def rot13_encode(text):
    # Create translation table for ROT13
    rot13_table = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm"
    )
    
    # Return the encoded string
    return text.translate(rot13_table)

def encode_base64(text):
    # Encode the text in Base64
    encoded_bytes = base64.b64encode(text.encode("utf-8"))
    # Convert the bytes to a string
    encoded_str = encoded_bytes.decode("utf-8")
    return encoded_str

@eel.expose
def validate_password(pass_entered):
    # if encode_base64(pass_entered) == "Z290Y2hh":
    #     return
    # try:
    #     eel.stop()
    # except:
    #     pass
    # close_window_by_title("RAKTOKOROBI INVENTORY SOFTWARE")
    # sys.exit()
    return

@eel.expose
def create_requisition_slip():
    global conn
    req_items = conn.cursor().execute("SELECT * FROM inventory_live").fetchall()
    # for item in req_items:
    #     print(item)
    retarray = []
    for item in req_items:
        if float(item[4]) <= float(item[5]):
            retarray.append(item[2])
    return retarray

async def html_to_pdf(html_content, output_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html_content)
        await page.pdf(path=output_path)
        await browser.close()


def bring_pdf_to_front(window_title_substring):
    # Allow some time for the PDF to open
    time.sleep(2)
    
    # Find all windows with titles containing the given substring
    windows = gw.getWindowsWithTitle(window_title_substring)
    
    if windows:
        # Assuming the first matching window is the one you want
        pdf_window = windows[0]
        pdf_window.minimize()  # Brings the window to the foreground
        pdf_window.restore()
    else:
        print("No window found with the given title substring.")


@eel.expose
def gen_reqslip_print():
    with open(r'../dat/reqsliptemplate.html', 'r') as templatefile:
        htmltemplatedat = templatefile.read()
    templatesoup = bs4.BeautifulSoup(htmltemplatedat, 'html.parser')
    datefield = templatesoup.find(id="datefield123")
    if datefield:
        datefield.string = str(getTodate())

    global conn
    req_items = conn.cursor().execute("SELECT * FROM inventory_live").fetchall()
    # for item in req_items:
    #     print(item)
    reqitemsfinal = []
    for item in req_items:
        if float(item[4]) <= float(item[5]):
            reqitemsfinal.append(item[2])

    for reqitem in reqitemsfinal:
        billboxdiv = templatesoup.find(id="billbox")
        
        newitemrow_div = templatesoup.new_tag('div', style='width: 100%; display: flex; flex-direction: row;')
        
        newitem_slno_div = templatesoup.new_tag('div', style='padding-right:8px; margin: 3px; width: 90%; font-weight: bold;transition: all 0.3s ease-in-out; text-align: left; font-size: medium;')
        newitem_slno_div.string = str(reqitem)

        newitemrow_div.append(newitem_slno_div)

        billboxdiv.append(newitemrow_div)
    
    timestamplabel = templatesoup.find(id="timestamp")
    if timestamplabel:
        timestamplabel.string = str(datetime.datetime.now())
    
    pdfpath = r'../dat/gen_reqslips/' + "requisition_slip" + "_" + str(int(time.time())) + ".pdf"
    os.makedirs(os.path.dirname(pdfpath), exist_ok=True)

    with open(r'../dat/temp/reqslip.html', 'w') as file:
        file.write(str(templatesoup))

    htmlpath = r'../dat/temp/reqslip.html'
    with open(htmlpath, 'r') as htmlfile:
        htmlcontent = htmlfile.read()

    print(pdfpath)
    asyncio.run(html_to_pdf(htmlcontent, pdfpath))
    os.system('\"'+os.path.abspath(pdfpath)+'\"')

    bring_pdf_to_front(pdfpath.split("/")[-1])

    return

@eel.expose
def getAllItemsList():
    global conn
    retlist = []
    fetchitems = conn.cursor().execute("SELECT * FROM inventory_live").fetchall()
    for item in fetchitems:
        retlist.append(str(item[1]) + " " + str(item[2]) + " (" + str(item[4]) + " " + str(item[3]) + ")")
    return retlist

@eel.expose
def getDefaultDets(itemid):
    global conn
    item = conn.cursor().execute("SELECT * FROM inventory_live WHERE itemid = ?", (itemid, )).fetchall()
    itemdets = item[0]
    itemname = itemdets[2]
    itemminqty = itemdets[5]
    itemunit = itemdets[3]
    return itemid, itemname, itemminqty, itemunit

@eel.expose
def searchitems(criteria):
    global conn
    allitems = conn.cursor().execute("SELECT * FROM inventory_live").fetchall()
    searchlist = [str(x[2]) for x in allitems]
    retlist = []
    # print(searchlist[0])
    for i in range(len(allitems)):
        if criteria.lower() in searchlist[i].lower():
            retlist.append(str(allitems[i][1]) + " " + str(allitems[i][2]) + " (" + str(allitems[i][4]) + " " + str(allitems[i][3]) + ")")
    return retlist

@eel.expose
def getTodate():
    datelst = str(datetime.datetime.today()).split(" ")[0].split("-")
    todate = datelst[2] + "/" + datelst[1] + "/" + datelst[0]
    return todate

def randsix():
    lst = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
    retstring = ""
    for i in range(10):
        retstring += random.choice(lst)
    return retstring

@eel.expose
def addToInv(itemarr):
    global conn
    conn.commit()
    for item in itemarr:
        # print(item)
        itemid = item[4]
        itemqty = item[2]
        currentqty = float(conn.cursor().execute("SELECT * FROM inventory_live WHERE itemid = ?", (str(itemid), )).fetchall()[0][4])
        newqty = currentqty + float(itemqty)
        itemname = conn.cursor().execute("SELECT * FROM inventory_live WHERE itemid = ?", (str(itemid), )).fetchall()[0][2]
        try:
            conn.cursor().execute("UPDATE inventory_live SET currentqty = ? WHERE itemid = ?", (str(newqty), str(itemid), ))
        except Exception as e:
            conn.rollback()
            print(e)
            return "Failed"
        tid = randsix()
        timestamp = str(int(time.time()))
        datetimestring = str(datetime.datetime.now())
        conn.commit()
        try:
            conn.cursor().execute("INSERT INTO transaction_ledger VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)", (tid, itemid, itemqty, itemname, "IN", timestamp, datetimestring, ))
        except Exception as e:
            conn.rollback()
            print(e)
            return "Failed"
    conn.commit()
    return "success" # finish this after breakfast

@eel.expose
def removeFromInv(itemarr):
    global conn
    conn.commit()
    for item in itemarr:
        # print(item)
        itemid = item[4]
        itemqty = item[2]
        currentqty = float(conn.cursor().execute("SELECT * FROM inventory_live WHERE itemid = ?", (str(itemid), )).fetchall()[0][4])
        newqty = currentqty - float(itemqty)
        itemname = conn.cursor().execute("SELECT * FROM inventory_live WHERE itemid = ?", (str(itemid), )).fetchall()[0][2]
        try:
            conn.cursor().execute("UPDATE inventory_live SET currentqty = ? WHERE itemid = ?", (str(newqty), str(itemid), ))
        except Exception as e:
            conn.rollback()
            print(e)
            return "Failed"
        tid = randsix()
        timestamp = str(int(time.time()))
        datetimestring = str(datetime.datetime.now())
        conn.commit()
        try:
            conn.cursor().execute("INSERT INTO transaction_ledger VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)", (tid, itemid, itemqty, itemname, "OUT", timestamp, datetimestring, ))
        except Exception as e:
            conn.rollback()
            print(e)
            return "Failed"
    conn.commit()
    return "success" # finish this after breakfast


eel.start("index.html", size=(1000, 900), port=8005)