import PIL.Image
import PIL.ImageTk
import winsound
import time
import threading
from tkinter import *
import tkinter as tk
from urllib.request import urlopen
import requests
from PIL import Image, ImageTk
import io
import math
import webbrowser
import tempfile, base64, zlib
from pynput.keyboard import Key, Controller
import pygetwindow as gw
import ctypes
from tkinter import messagebox


# create global list of values for each item type
armor_price = []
weps_price = []
div_price = []
map_price = []
flask_price = []
accessory_price = []
prophecy_price = []
fossil_price = []
essence_price = []
list_url = []
stop = True
t = []
league_name = "None"
sales = []
photos = []
mute = False
url = 'www.poe.trade/search?league='+league_name
keyboard = Controller()

# find poe.ninja api for respescted league
def league():
    global list_url
    global var
    global league_name
    league_name = var.get()
    list_url.append(
        "https://poe.ninja/api/data/itemoverview?league=" + league_name + "&type=UniqueArmour&date=" + time.strftime(
            "%Y-%m-%d"))
    list_url.append(
        "https://poe.ninja/api/data/itemoverview?league=" + league_name + "&type=UniqueAccessory&date=" + time.strftime(
            "%Y-%m-%d"))
    list_url.append(
        "https://poe.ninja/api/data/itemoverview?league=" + league_name + "&type=UniqueWeapon&date=" + time.strftime(
            "%Y-%m-%d"))
    list_url.append(
        "https://poe.ninja/api/data/itemoverview?league=" + league_name + "&type=Prophecy&date=" + time.strftime(
            "%Y-%m-%d"))
    list_url.append(
        "https://poe.ninja/api/data/itemoverview?league=" + league_name + "&type=DivinationCard&date=" + time.strftime(
            "%Y-%m-%d"))
    list_url.append(
        "https://poe.ninja/api/data/itemoverview?league=" + league_name + "&type=Map&date=" + time.strftime("%Y-%m-%d"))
    list_url.append(
        "https://poe.ninja/api/data/itemoverview?league=" + league_name + "&type=Essence&date=" + time.strftime(
            "%Y-%m-%d"))
    list_url.append(
        "https://poe.ninja/api/data/itemoverview?league=" + league_name + "&type=UniqueFlask&date=" + time.strftime(
            "%Y-%m-%d"))
    list_url.append(
        "https://poe.ninja/api/data/itemoverview?league=" + league_name + "&type=Fossil&date=" + time.strftime(
            "%Y-%m-%d"))


# check how many abyssal sockets there is then return value
def abyss_check(item):
    if item[0] == 'Has 1 Abyssal Socket':
        return 1
    if item[0] == 'Has 2 Abyssal Sockets':
        return 2

    return 0


# return number of sockets on item
def get_sockets(sockets):
    if sockets.count(None) == len(sockets):
        return 0
    else:
        return len(sockets)


# return number of links on item, links default to 0 in-case sockets is a list with value of None
def get_links(sockets):
    links = 0
    for x in range(len(sockets)):
        # print(x, ' occured ', str(sockets).count(str(x)), ' times')
        if str(sockets).count(str(x)) > links:
            links = str(sockets).count(str(x))

    return links


# return if item has been corrupted or not
def get_Corrupted_Value(corrupted):
    if corrupted == True:
        return "Vaaled"
    if corrupted == False:
        return "Clean"
    return "Clean"


# calculate value of item from poe.ninja api based on name, if multiple values for same name then compare
# other factors such as links, abyss sockets, or explicit modifiers
def get_item_value(itemName, itemClass, itemLinks, explicitMods):
    global armor_price
    global weps_price
    global div_price
    global map_price
    global flask_price
    global accessory_price
    global prophecy_price
    global fossil_price
    global essence_price
    global search_list

    if itemName == 'Tabula Rasa':
        itemLinks = 6

    # check if its an abyssal item
    abyss = abyss_check(explicitMods)

    #abyss armor
    if search_list[0].get() == 1:
        # abyssal items take priority since their value is dependant on abyss socket count
        if abyss > 0 and itemName != 'Darkness Enthroned' and itemName != 'Command of the Pit':

            for armor in armor_price:
                explicit = armor.get('explicitModifiers')

                if itemName == armor.get('name'):
                    if 'Has 1 Abyssal Socket' in str(explicit):
                        abyssNum = 1
                    if 'Has 2 Abyssal Sockets' in str(explicit):
                        abyssNum = 2
                    if abyssNum == abyss and armor.get('name') == itemName and armor.get('itemClass') == itemClass and armor.get('name') != "Shroud of the Lightless":
                        url = 'www.poe.trade/search?league='+league_name+'&name='+itemName + '&sockets_a_min=' + str(abyssNum) + '&online=On'
                        return float(armor.get('chaosValue')), url
                    elif abyssNum == abyss and armor.get('name') == itemName and armor.get('itemClass') == itemClass and armor.get('links') == itemLinks:
                        url = 'www.poe.trade/search?league='+league_name+'&name='+itemName + '&sockets_a_min=' + str(abyssNum) + '&link_min=' + str(itemLinks) + '&online=On'
                        return float(armor.get('chaosValue')), url
                    elif abyssNum == abyss and armor.get('name') == itemName and armor.get('itemClass') == itemClass and armor.get('links') <= 4 and itemLinks <= 4:
                        url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&sockets_a_min=' + str(abyssNum) + '&online=On'
                        return float(armor.get('chaosValue')), url
        # armors
        else:
            for armor in armor_price:

                if itemName == 'Volkuur\'s Guidance':
                    if itemName == armor.get('name'):
                        explicit = armor.get('explicitModifiers')
                        if 'Lightning' in explicitMods[2] and 'Lightning' in str(explicit[2]):
                            url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&online=On'
                            return float(armor.get('chaosValue')), url
                        elif 'Fire' in explicitMods[2] and 'Fire' in str(explicit[2]):
                            url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&online=On'
                            return float(armor.get('chaosValue')), url
                        elif 'Cold' in explicitMods[2] and 'Cold' in str(explicit[2]):
                            url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&online=On'
                            return float(armor.get('chaosValue')), url
                        else:
                            continue


                elif itemName == 'Doryani\'s Delusion':
                    if itemName == armor.get('name'):

                        if 'Armor' in explicitMods[2] and armor.get('baseType') == ':Titan Greaves':
                            url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&armor_min=' + str(1) + '&online=On'
                            return float(armor.get('chaosValue')), url
                        elif 'Energy' in explicitMods[2] and armor.get('baseType') == 'Sorcerer Boots':
                            url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&shield_min=' + str(1) + '&online=On'
                            return float(armor.get('chaosValue')), url
                        elif 'Evasion' in explicitMods[2] and armor.get('baseType') == 'Slink Boots':
                            url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&evasion_min=' + str(1) + '&online=On'
                            return float(armor.get('chaosValue')), url
                        else:
                            continue


                elif armor.get('name') == itemName and armor.get('itemClass') == itemClass and armor.get('links') == itemLinks:
                    url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&link_min=' + str(itemLinks) + '&online=On'
                    return float(armor.get('chaosValue')), url
                elif armor.get('name') == itemName and armor.get('itemClass') == itemClass and armor.get('links') <= 4 and itemLinks <= 4:
                    url = 'www.poe.trade/search?league=' + league_name + '&name='+ itemName + '&online=On'
                    return float(armor.get('chaosValue')), url
    #wepons
    if search_list[1].get() == 1:
        # weapons
        for weps in weps_price:
            if weps.get('name') == itemName and weps.get('itemClass') == itemClass and itemLinks == weps.get('links'):
                url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&link_min=' + str(itemLinks) + '&online=On'
                return float(weps.get('chaosValue')), url
            elif weps.get('name') == itemName and weps.get('itemClass') == itemClass and weps.get('links') <= 4 and itemLinks <= 4:
                url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&online=On'
                return float(weps.get('chaosValue')), url
    # accessories
    if search_list[2].get() == 1:
        for acc in accessory_price:
            if itemName == 'Impresence' and acc.get('name') == itemName and acc.get('itemClass') == itemClass:
                for line in explicitMods:
                    if acc.get('variant') in line:
                        url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&online=On'
                        return float(acc.get('chaosValue')), url

            elif acc.get('name') == itemName:
                url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&online=On'
                return float(acc.get('chaosValue')), url
    # maps
    if search_list[3].get() == 1:
        for map in map_price:
            if map.get('name') == itemName:
                url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&online=On'
                return float(map.get('chaosValue')), url
    # flasks
    if search_list[4].get() == 1:
        for flask in flask_price:
            # to help identify different Vinktars
            if itemName == 'Vessel of Vinktar' and flask.get('name') == itemName and flask.get('itemClass') == itemClass:
                for line in explicitMods:
                    if flask.get('variant') == 'Added Attacks' and 'Attacks' in line:
                        url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&online=On'
                        return float(flask.get('chaosValue')), url
                    elif flask.get('variant') == 'Added Spells' and 'Spells' in line:
                        url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&online=On'
                        return float(flask.get('chaosValue')), url
                    elif flask.get('variant') == 'Penetration' and 'Penetrates' in line:
                        url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&online=On'
                        return float(flask.get('chaosValue')), url
                    elif flask.get('variant') == 'Conversion' and 'Converted' in line:
                        url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&online=On'
                        return float(flask.get('chaosValue')), url
            # any other flask
            elif flask.get('name') == itemName and flask.get('itemClass') == itemClass:
                url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&online=On'
                return float(flask.get('chaosValue')), url
    # divination cards
    if search_list[5].get() == 1:
        for div in div_price:
            if div.get('name') == itemName:
                url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&online=On'
                return float(div.get('chaosValue')), url
    # prophecy + fossils + essence
    if search_list[6].get() == 1:
        for pro in prophecy_price:
                if pro.get('name') == itemName:
                    url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&online=On'
                    return float(pro.get('chaosValue')), url
        for essence in essence_price:
                if essence.get('name') == itemName:
                    url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&online=On'
                    return float(essence.get('chaosValue')), url
        for fossil in fossil_price:
                if fossil.get('name') == itemName:
                    url = 'www.poe.trade/search?league=' + league_name + '&name=' + itemName + '&online=On'
                    return float(fossil.get('chaosValue')), url

    return [0,'www.poe.trade/search?']


# rarity identifier for items
def getFrameType(frameType):
    if frameType == 0: return "NORM"
    if frameType == 1: return "MAGIC"
    if frameType == 2: return "RARE"
    if frameType == 3: return "UNI"
    if frameType == 4: return "GEM"
    if frameType == 5: return "CUR"
    if frameType == 6: return "DIV"
    if frameType == 7: return "QUEST"
    if frameType == 8: return "PROF"
    if frameType == 9: return "LEG"

    return frameType


# search through public stash tabs for deals
def find_items(stashes):
    global search_list
    global sales
    global stop
    global mute
    global league_name
    global search_list
    # scan availible stash tabs...
    for stash in stashes:
        accountName = stash['accountName']
        lastCharacterName = stash['lastCharacterName']
        items = stash['items']
        stashName = stash.get('stash')


        # scan items
        for item in items:
            if stop:
                return
            #skip if not from the league we are looking for
            if stash.get('league') != league_name:
                continue

            if item.get('league') == league_name:
                typeLine = item.get('typeLine', None)
                name = re.sub(r'<<.*>>', '', item.get('name', None))
                price = item.get('note', None)
                frameType = item.get('frameType', None)
                socket = item.get('sockets', [None])
                link = get_links(socket)
                corrupted = item.get('corrupted', None)
                explicitMods = item.get('explicitMods', [None])
                image = item.get('icon', None)

                if get_Corrupted_Value(corrupted) == "Vaaled" and search_list[7].get() == 0:
                    continue


                # for divination
                if name is None or name == "":
                    name = typeLine

                ## compare unique that worth at least 1 chaos.
                if price and name and 'chaos' in price:
                    try:
                        if not re.findall(r'\d+', price)[0]:
                            continue
                    except:
                        continue

                    price_normalized = float(re.findall(r'\d+', price)[0])

                    item_value, url = get_item_value(name, frameType, link, explicitMods)

                    if item_value is not 0 and (item_value - price_normalized) > 3.0 and price_normalized is not 0:
                        # unwanted items
                        if 'Atziri' in name or 'Sadima' in name or 'Drillneck' in name or "Precursor's Emblem" in name:
                            continue

                        price = price.replace("~b/o ", "")
                        price = price.replace("~price ", "")

                        if get_Corrupted_Value(corrupted) == "Vaaled":
                            url = url + '&corrupted=1'
                        else:
                            url = url + '&corrupted=0'

                        try:

                            perc_decrease = ((item_value - price_normalized) / item_value) * 100
                            info = " Seller: {}\n".format(lastCharacterName)
                            info2 = " {}-{}% Off\n".format(name, round(perc_decrease))
                            info3 = " {} - {} Links - {}c/{}c\n".format(getFrameType(frameType),link,price_normalized,item_value)

                            msg = "@{} Hi, I would like to buy your {} listed for {} in {} (stash tab \"{}\"; position: left {}, top {})\n".format(
                                lastCharacterName, name, price, league_name, stashName, item.get('x'), item.get('y'),
                                item.get('note'), item_value, price_normalized
                            )

                            if perc_decrease >= 50:
                                if search_list[8].get() == 0:
                                    continue
                                insert_img(image, get_Corrupted_Value(corrupted))
                                insert_text(info, info2, info3, msg, get_Corrupted_Value(corrupted), round(perc_decrease), url)
                                #insert_img(image, get_Corrupted_Value(corrupted))
                                if not mute:
                                    winsound.PlaySound('c:/windows/media/notify.wav', winsound.SND_FILENAME)
                            elif perc_decrease >= 30:
                                if search_list[9].get() == 0:
                                    continue
                                insert_img(image, get_Corrupted_Value(corrupted))
                                insert_text(info, info2, info3, msg, get_Corrupted_Value(corrupted), round(perc_decrease), url)
                                #insert_img(image, get_Corrupted_Value(corrupted))
                                if not mute:
                                    winsound.PlaySound('c:/windows/media/Windows Ding.wav', winsound.SND_FILENAME)
                            elif perc_decrease >= 20:
                                if search_list[10].get() == 0:
                                    continue
                                insert_img(image, get_Corrupted_Value(corrupted))
                                insert_text(info, info2, info3, msg, get_Corrupted_Value(corrupted), round(perc_decrease), url)
                                #insert_img(image, get_Corrupted_Value(corrupted))
                                if not mute:
                                    winsound.PlaySound('sound.wav', winsound.SND_FILENAME)
                            elif perc_decrease >= 10:
                                if search_list[11].get() == 0:
                                    continue
                                insert_img(image, get_Corrupted_Value(corrupted))
                                insert_text(info, info2, info3, msg, get_Corrupted_Value(corrupted), round(perc_decrease), url)
                                #insert_img(image, get_Corrupted_Value(corrupted))
                                if not mute:
                                    winsound.PlaySound('c:/windows/media/Speech On.wav', winsound.SND_FILENAME)
                        except:
                            pass


# initiate search script
def setup():
    global armor_price
    global weps_price
    global div_price
    global map_price
    global flask_price
    global accessory_price
    global prophecy_price
    global fossil_price
    global essence_price
    global stop
    global list_url
    global league_name
    global search_list

    if stop:
        return
    # get the league name to start script
    league()

    url_api = "http://www.pathofexile.com/api/public-stash-tabs?id="

    # get the next change id
    r = requests.get("http://poe.ninja/api/Data/GetStats")

    try:
        next_change_id = r.json().get('next_change_id')
    except ValueError:
        update_launch_button() #call to reset start button
        fail_to_load() #error pop up message
        return

    # get unique armour value
    url_armor = list_url.pop(0)
    r = requests.get(url_armor)
    armor_price = r.json().get('lines')

    # get unique accessory value
    url_acess = list_url.pop(0)
    r = requests.get(url_acess)
    accessory_price = r.json().get('lines')

    # get unique weapons
    url_wep = list_url.pop(0)
    r = requests.get(url_wep)
    weps_price = r.json().get('lines')

    # get prophecies
    url_proph = list_url.pop(0)
    r = requests.get(url_proph)
    prophecy_price = r.json().get('lines')

    # get divination card
    url_div = list_url.pop(0)
    r = requests.get(url_div)
    div_price = r.json().get('lines')

    # get maps
    url_map = list_url.pop(0)
    r = requests.get(url_map)
    map_price = r.json().get('lines')

    # get essence
    url_essence = list_url.pop(0)
    r = requests.get(url_essence)
    essence_price = r.json().get('lines')

    # get flask
    url_flasks = list_url.pop(0)
    r = requests.get(url_flasks)
    flask_price = r.json().get('lines')

    # get fossils
    url_fossils = list_url.pop(0)
    r = requests.get(url_fossils)
    fossil_price = r.json().get('lines')

    while True:
        if stop:
            return
        params = {'id': next_change_id}
        r = requests.get(url_api, params=params)

        ## parsing structure
        data = r.json()

        ## setting next change id
        next_change_id = data['next_change_id']

        ## attempt to find items...
        find_items(data['stashes'])

        ## wait 5 seconds until parsing next structure
        time.sleep(1)


# insert messages into text box
def insert_text(info, info2, info3, data, corruption, percent, url):
    global league_name
    link = url
    T.configure(state="normal")

    # activate copy paste feature
    def copy_button():
        clip = Tk()
        clip.withdraw()
        clip.clipboard_clear()
        clip.clipboard_append(data) #Copy to clipboard
        clip.destroy()
    # open poe.trade url
    def OpenUrl():
        webbrowser.open_new(link)
    #send message to seller if poe is running
    def auto_send():
        global keyboard
        stuff = gw.getAllTitles()
        print(stuff)
        if 'Path of Exile' in stuff:
            abc = gw.getWindowsWithTitle('Path of Exile')[0]
            abc.activate()
            time.sleep(.01)
            message = '\n' + data
            keyboard.type(message)
        else:
            MessageBox = ctypes.windll.user32.MessageBoxW
            MessageBox(None, 'Path of Exile not running.', 'Error', 0)

    if corruption == 'Clean':
        text_canvas = Canvas(T, bd=0, highlightthickness=0, relief='ridge', bg='grey20', width=285, height=110, scrollregion=(0, 0, 1000, 1000))
        button_canvas = Canvas(T, bd=0, highlightthickness=0, relief='ridge', bg='grey20', width=50, height=110)
        c = tk.Button(T, text="Copy", command=copy_button, fg="#d0d0d0", bg='grey20', height=1, width=4, cursor="hand2")
        l = tk.Button(T, text="Link", command=OpenUrl, fg="#d0d0d0", bg='grey20', height=1, width=4, cursor="hand2")
        s = tk.Button(T, text="Send", command=auto_send, fg="#d0d0d0", bg='grey20', height=1, width=4, cursor="hand2")

        if percent >= 50:
            text_canvas.create_text(15,60, font = "12", fill= "red", text = info + info2 + info3, width = 330, anchor=W) #(x,y) width = wrap char lim
            button_canvas.create_window(25, 27, window=l, state=NORMAL) #insert link button to canvas
            button_canvas.create_window(25, 54, window=s, state=NORMAL) #insert send button to canvas
            button_canvas.create_window(25, 81, window=c, state=NORMAL) #insert copy button to canvas
            T.window_create("1.0", window=text_canvas)  # Insert text canvas
            T.window_create("1.0", window=button_canvas)  # Insert buttons canvas

        elif percent >= 30:
            text_canvas.create_text(15,60, font = "12", fill= "yellow", text = info + info2 + info3, width = 330, anchor=W) #(x,y) width = wrap char lim
            button_canvas.create_window(25, 27, window=l, state=NORMAL) #insert link button to canvas
            button_canvas.create_window(25, 54, window=s, state=NORMAL) #insert send button to canvas
            button_canvas.create_window(25, 81, window=c, state=NORMAL) #insert copy button to canvas
            T.window_create("1.0", window=text_canvas)  # Insert Send button
            T.window_create("1.0", window=button_canvas)  # Insert Send button

        elif percent >= 20:
            text_canvas.create_text(15,60, font = "12", fill= "green", text = info + info2 + info3, width = 330, anchor=W) #(x,y) width = wrap char lim
            button_canvas.create_window(25, 27, window=l, state=NORMAL) #insert link button to canvas
            button_canvas.create_window(25, 54, window=s, state=NORMAL) #insert send button to canvas
            button_canvas.create_window(25, 81, window=c, state=NORMAL) #insert copy button to canvas
            T.window_create("1.0", window=text_canvas)  # Insert Send button
            T.window_create("1.0", window=button_canvas)  # Insert Send button

        else:
            text_canvas.create_text(15,60, font = "12", fill= "grey97", text = info + info2 + info3, width = 330, anchor=W) #(x,y) width = wrap char lim
            button_canvas.create_window(25, 27, window=l, state=NORMAL) #insert link button to canvas
            button_canvas.create_window(25, 54, window=s, state=NORMAL) #insert send button to canvas
            button_canvas.create_window(25, 81, window=c, state=NORMAL) #insert copy button to canvas
            T.window_create("1.0", window=text_canvas)  # Insert Send button
            T.window_create("1.0", window=button_canvas)  # Insert Send button
    else:
        text_canvas = Canvas(T, bd=0, highlightthickness=0, relief='ridge', bg='#ff7e7e', width=285, height=110)
        button_canvas = Canvas(T, bd=0, highlightthickness=0, relief='ridge', bg='#ff7e7e', width=50, height=110)
        c = tk.Button(T, text="Copy", command=copy_button, fg="#3f0000", bg='#ff4242', height=1, width=4, cursor="hand2")
        l = tk.Button(T, text="Link", command=OpenUrl, fg="#3f0000", bg='#ff4242', height=1, width=4, cursor="hand2")
        s = tk.Button(T, text="Send", command=auto_send, fg="#3f0000", bg='#ff4242', height=1, width=4, cursor="hand2")

        if percent >= 50:
            text_canvas.create_text(15,60, font = "12", fill= "red", text = info + info2 + info3, width = 330, anchor=W) #(x,y) width = wrap char lim
            button_canvas.create_window(25, 27, window=l, state=NORMAL) #insert link button to canvas
            button_canvas.create_window(25, 54, window=s, state=NORMAL) #insert send button to canvas
            button_canvas.create_window(25, 81, window=c, state=NORMAL) #insert copy button to canvas
            T.window_create("1.0", window=text_canvas)  # Insert text canvas
            T.window_create("1.0", window=button_canvas)  # Insert buttons canvas

        elif percent >= 30:
            text_canvas.create_text(15,60, font = "12", fill= "yellow", text = info + info2 + info3, width = 330, anchor=W) #(x,y) width = wrap char lim
            button_canvas.create_window(25, 27, window=l, state=NORMAL) #insert link button to canvas
            button_canvas.create_window(25, 54, window=s, state=NORMAL) #insert send button to canvas
            button_canvas.create_window(25, 81, window=c, state=NORMAL) #insert copy button to canvas
            T.window_create("1.0", window=text_canvas)  # Insert text canvas
            T.window_create("1.0", window=button_canvas)  # Insert buttons canvas

        elif percent >= 20:
            text_canvas.create_text(15,60, font = "12", fill= "green", text = info + info2 + info3, width = 330, anchor=W) #(x,y) width = wrap char lim
            button_canvas.create_window(25, 27, window=l, state=NORMAL) #insert link button to canvas
            button_canvas.create_window(25, 54, window=s, state=NORMAL) #insert send button to canvas
            button_canvas.create_window(25, 81, window=c, state=NORMAL) #insert copy button to canvas
            T.window_create("1.0", window=text_canvas)  # Insert text canvas
            T.window_create("1.0", window=button_canvas)  # Insert buttons canvas

        else:
            text_canvas.create_text(15,60, font = "12", fill= "grey97", text = info + info2 + info3, width = 330, anchor=W) #(x,y) width = wrap char lim
            button_canvas.create_window(25, 27, window=l, state=NORMAL) #insert link button to canvas
            button_canvas.create_window(25, 54, window=s, state=NORMAL) #insert send button to canvas
            button_canvas.create_window(25, 81, window=c, state=NORMAL) #insert copy button to canvas
            T.window_create("1.0", window=text_canvas)  # Insert text canvas
            T.window_create("1.0", window=button_canvas)  # Insert buttons canvas


    T.configure(state="disabled")


# resize image if too large but keep the ratio
def resize(w, h):
    update_height = 1
    update_width = 1
    if h > 100:
        update_height = 100 / h
    if w > 90:
        update_width = 90 / w

    if update_width > update_height:
        return update_height
    if update_width < update_height:
        return update_width
    if update_width == update_height:
        return update_width

#message user if failed to fetch json
def fail_to_load():
    messagebox.showinfo("Error", "Failed to fetch data.")

# insert images into text box 2
def insert_img(url, corruption):
    global photos
    T.configure(state="normal")
    ratio = 1
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    img_w, img_h = img.size
    if img_w > 90 or img_h > 100:
        ratio = resize(img_w, img_h)
    img = img.resize((math.floor(img_w * ratio), math.floor(img_h * ratio)))
    img_w, img_h = img.size

    if corruption == 'Vaaled':
        background = Image.new('RGBA', (95, 110), (255, 126, 126, 255))
    else:
        background = Image.new('RGBA', (95, 110), (51, 51, 51, 255))

    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(img, offset, mask=img)
    ph = PIL.ImageTk.PhotoImage(background)
    photos.append(ph)
    T.insert('1.0', '\n')
    T.image_create('1.0', image=photos[-1])
    #T.insert('1.0', '\n')
    T.configure(state="disabled")

# status bar update
def get_text(root, val):
    # try to open the file and set the value of val to its contents
    global stop
    global search_list
    global league_name

    if not stop:
        if search_list[7].get() == 1:
            val.set("Searching for Both mispriced items in " + league_name + " ...")
        else:
            val.set("Searching for Clean mispriced items in " + league_name + " ...")
    else:
        val.set("On standby.")
    # schedule the function to be run again after 1000 milliseconds
    root.after(500, lambda: get_text(root, val))


# enable and disable sound alerts
def update_mute_button():
    global mute
    if not mute:
        mute_button.set("Unmute")
        mute = True
    else:
        mute_button.set("Mute")
        mute = False

#start and stop script in new thread
def update_launch_button():
    global stop
    global t
    global T
    if stop:
        T.configure(state="normal")
        T.configure(state="normal")
        T.delete("1.0", tk.END)
        T.delete("1.0", tk.END)
        #T.insert(END, '\n')
        T.configure(state="disabled")
        T.configure(state="disabled")
        stop = False
        t = threading.Thread(target=setup)
        t.start()
        launch_button.set("Stop")

    else:
        stop = True
        launch_button.set("Start")


#Load an image from a web url and return its data base64 encoded for GUI icon
image_byt = urlopen("https://i.imgur.com/MkcamNT.png").read()
image_b64 = base64.encodebytes(image_byt)

# GUI
root = Tk()

topFrame = Frame(root, bg="#111111")
topFrame.pack()
ico = tk.PhotoImage(data=image_b64)

root.geometry("450x203")
root.title("Hermes")
root.tk.call('wm','iconphoto', root._w, ico)
root.resizable(0, 1)
root.attributes('-topmost', True)


logo = PIL.Image.open(urlopen('https://i.imgur.com/D5G6AVZ.jpg'))
temp = PIL.ImageTk.PhotoImage(logo)
label = Label(topFrame, image=temp, bg='#111111')
label.pack(side=LEFT, expand=TRUE, fill=BOTH)

launch_button = tk.StringVar()
btn = Button(topFrame, textvariable=launch_button, command=update_launch_button, height=4, width=7, fg="#d0d0d0", bg = 'grey20',cursor = "hand2")
launch_button.set('Start')
btn.pack(side=LEFT)


padding = Label(topFrame, text="", bg='#111111')
padding.pack(side=LEFT)

mute_button = tk.StringVar()
btn = Button(topFrame, textvariable=mute_button, command=update_mute_button, height=4, width=7, fg="#d0d0d0", bg = 'grey20',cursor = "hand2")
mute_button.set('Mute')
btn.pack(side=LEFT)


padding = Label(topFrame, text="", bg='#111111')
padding.pack(side=LEFT)

#drop down menu for item types
mb=  Menubutton(topFrame, text="Filter", relief=RAISED, height=4, width=7, fg="#d0d0d0", bg = 'grey20', activebackground = 'grey20',cursor = "hand2")
mb.pack(side=LEFT)
mb.menu  =  Menu( mb, tearoff = 0, bg="grey30" )
mb["menu"]  =  mb.menu

#initate filter list to all enabled
search_list = []
Item0 = IntVar(value=1)
Item1 = IntVar(value=1)
Item2 = IntVar(value=1)
Item3 = IntVar(value=1)
Item4 = IntVar(value=1)
Item5 = IntVar(value=1)
Item6 = IntVar(value=1)
Item7 = IntVar(value=1)
Item8 = IntVar(value=1)
Item9 = IntVar(value=1)
Item10 = IntVar(value=1)
Item11 = IntVar(value=1)

search_list.append(Item0)
search_list.append(Item1)
search_list.append(Item2)
search_list.append(Item3)
search_list.append(Item4)
search_list.append(Item5)
search_list.append(Item6)
search_list.append(Item7)
search_list.append(Item8)
search_list.append(Item9)
search_list.append(Item10)
search_list.append(Item11)

mb.menu.add_checkbutton ( label="Armor", variable=Item0)
mb.menu.add_checkbutton ( label="Weapon", variable=Item1)
mb.menu.add_checkbutton ( label="Accessory", variable=Item2)
mb.menu.add_checkbutton ( label="Map", variable=Item3)
mb.menu.add_checkbutton ( label="Flask", variable=Item4)
mb.menu.add_checkbutton ( label="Cards", variable=Item5)
mb.menu.add_checkbutton ( label="Currency", variable=Item6)
mb.menu.add_checkbutton ( label="Vaaled", variable=Item7)
mb.menu.add_checkbutton ( label="50%+ Off", variable=Item8)
mb.menu.add_checkbutton ( label="30%+ Off", variable=Item9)
mb.menu.add_checkbutton ( label="20%+ Off", variable=Item10)
mb.menu.add_checkbutton ( label="10%+ Off", variable=Item11)
mb.pack()

padding = Label(topFrame, text="", bg='#111111')
padding.pack(side=LEFT)

var = StringVar(root)
var.set("Blight")  # initial value
option = OptionMenu(topFrame, var, "Blight", "Hardcore Blight","Standard", "Hardcore")
option.configure(height=4, bd = 1, fg="#d0d0d0", bg = 'grey20', activebackground= 'grey20',cursor = "hand2", indicator=0)
option["menu"].config(bg="grey30")
option["highlightthickness"]=0
option.pack(side=LEFT)

padding = Label(topFrame, text="", bg='#111111')
padding.pack(side=LEFT)

scroll = Scrollbar(root)
scroll.pack(side=RIGHT, fill=Y)
T = Text(root, wrap=WORD, yscrollcommand=scroll.set,height=0, bd=-1, cursor = "arrow", highlightthickness=0, bg='grey20', fg='black')
T.pack(expand=True, fill=BOTH)

scroll.configure(command=T.yview)
padding = Label(topFrame, text="", padx=9000, bg= '#111111')
padding.pack(side=LEFT)

eins = StringVar()
data1 = Label(root, textvariable=eins, bd=1, relief=SUNKEN, anchor=W, fg="#d0d0d0", bg = '#111111')
data1.pack(side=BOTTOM, fill=X)

get_text(root, eins)

root.mainloop()
