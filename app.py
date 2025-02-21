import os 
import requests
import time
import logging  
import telebot
from bs4 import BeautifulSoup
import httpx
import re
from threading import Thread
import uvicorn
from fastapi import FastAPI, Request 
from fastapi.responses import JSONResponse
from jj import get_thumbnail_and_title
from pp import process_url  # Import the process_url function
from ad import fetch_metadata 
import vk 
import sm 
from ah import get_ah_data 
from pm import fetch_thumbnail_and_title 
from sg import get_sg_data 
from kik import get_kik_data 
import pv 
from atx import get_atx_data 
import jcm
import sny
import tee
from dsp import fetch_thumbnail_and_title
from hc import fetch_data 
import subprocess
from ulu import main 
from urllib.parse import urlparse 
from dotenv import load_dotenv 
from telebot import types
load_dotenv()

# configuration Section  
BOT_TOKEN = os.getenv('BOT_TOKEN')
API_URL = os.getenv('API_URL')


ADMIN_ID = #Replace_id
AUTHORIZED_USERS = []
AUTHORIZED_GROUPS = [] 


# Initialize the bot with the token from environment variable
bot = telebot.TeleBot(BOT_TOKEN)

app = FastAPI()


WELCOME_MSG = """<b>
╔═══════════════════                                                   
║  Type @#replace_botusername ...              ══════════════════
║  for search movies on ott 
║  Where is Available    !!                       
║         
║ ¶ Developed By : [Lulli]    
╚══════════════════
</b>
"""
IMAGE_URL = "#replace image url"
ANIMATION_STICKER_ID = "#replace_sticker_id"


# Inline keyboard buttons
inline_markup = telebot.types.InlineKeyboardMarkup()
keyboard = [
    [telebot.types.InlineKeyboardButton("Developer", callback_data="developer"), 
     telebot.types.InlineKeyboardButton("Help", callback_data="help")]
]
inline_markup.keyboard = keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        # Send animation sticker
        animation_msg = bot.send_animation(message.chat.id, ANIMATION_STICKER_ID)
        
        # Wait for 5 seconds
        time.sleep(5)
        
        # Delete animation sticker message
        bot.delete_message(message.chat.id, animation_msg.message_id)
        
        # Send photo with welcome message and buttons
        bot.send_photo(message.chat.id, IMAGE_URL, caption=WELCOME_MSG, 
                       parse_mode='HTML', reply_markup=inline_markup)

    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "An error occurred")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        if call.data == "developer":
            bot.send_message(call.message.chat.id, "<b>Developer Name: [Lulli]</b>", 
                             parse_mode='HTML')
        elif call.data == "help":
            bot.send_message(call.message.chat.id, 
                             """<b>Available Commands !!
══════════════════

/start - Welcome 
/ze - Zee5 
/atx - airtelxtream
/pv - primevideo 
/jc - jiocinema 
/sony - sonyliv
/hc - Hoichoi  
/ulu - Ullu ott
/dsp - Only Disney+ 
/pp - Send URL Play Flix
/jj - Send URL Jojo 
/ad - send URL addatimes 
/vk - Send URL Viki 
/sm - Shemaroome 
/ah - Aha  
/sg - Stage URL 
/pm - Planetmarathi 
/kik - Send Klikk URL  
/search - For search movies Url
══════════════════
/auth - Only Admin
            </b>""", parse_mode='HTML')
    except Exception as e:
        bot.send_message(call.message.chat.id, "An error occurred")
        print(f"Error: {e}")

@bot.message_handler(commands=['search'])
def search_command(message):
    query = message.text.replace('/search@Bhadvagiri_bot ', '').split('-')[0].strip()
    region = message.text.split()[-1].lower()
    
    if len(message.text.split()) < 3:
        bot.send_message(message.chat.id, """<b>Please ✅ Write Correct Movie Name Or Series Name, Including Symbols 🥲. </b>

<b>Send /search@replace_bot 🔍 Command With {Movie_Name} -r for region.</b>

<b>For Example:</b><code> /search@#replace_bot_username Venom: The Last Dance -r IN</code>

<b>Region You Can Use 😑 :- </b> 
AR = <b>Argentina</b> 
AU = <b>Australia</b> 
BM = <b>Bermuda</b> 
BE = <b>Belgium</b> 
BR = <b>Brazil</b> 
CA = <b>Canada</b> 
CR = <b>Costa Rica</b> 
Co = <b>Colambia</b> 
DK = <b>Demark</b> 
EG = <b>Egypt</b> 
FR = <b>France</b> 
FI = <b>Finland</b> 
FJ = <b>Fiji</b> 
DE = <b>Germany</b> 
GR = <b>Greece</b> 
HK = <b>Hongkong</b> 
HU = <b>Hungary</b> 
IN = <b>India</b> 
IT = <b>Italy</b> 
ID = <b>Indonesia</b> 
IE = <b>Ireland</b> 
JP = <b>Japan</b> 
JM = <b>Jamaica</b> 
JO = <b>Jordon</b> 
KE = <b>Kenya</b> 
KW = <b>Kuwait</b> 
MY = <b>Malaysia</b> 
MX = <b>Mexico</b> 
MC = <b>Monaco</b> 
MA = <b>Morocco</b> 
NL = <b>Netherlands</b> 
NZ = <b>New Zeland</b> 
NO = <b>Norway</b> 
NG = <b>Nigeria</b> 
PK = <b>Bhikaristhaan</b> 
OM = <b>Oman</b> 
PH = <b>Philippines</b> 
PL = <b>Poland</b> 
PT = <b>Portugal</b> 
QA = <b>Qatar</b> 
RO = <b>Romania</b> 
SA = <b>Saudi Arabia</b> 
SG = <b>Singapore</b> 
ZA = <b>South Africa</b> 
ES = <b>Spain</b> 
CH = <b>Switzerland</b> 
TH = <b>Thailand</b> 
TT = <b>Trinidad and Tobago</b> 
TR = <b>Turkey</b> 
UG = <b>Uganda</b> 
AE = <b>United Arab Emirates</b> 
GB = <b>United Kingdom</b> 
US = <b>America</b> 
UY = <b>Uruguay</b> 
ZM = <b>Zambia</b>
        """, parse_mode='HTML')
        return

    params = {
        'q': query,
        'L': f'en_{region}'
    }
    params['q'] = params['q'].replace(' ', '+')

    try:
        response = requests.get(API_URL, params=params)
        print(response.url)
        if response.status_code == 200:
            data = response.json()
            print(data)
            keyboard = []
            seen_urls = set()
            found = False
            for movie in data['description']:
                if movie['type'] == 'MOVIE' and query.lower() in movie['title'].lower():
                    title = movie['title']
                    found = True
                    if 'offers' in movie:
                        offers = movie['offers']
                        for offer in offers:
                            url = offer['url']
                            if url not in seen_urls:
                                seen_urls.add(url)
                                button = types.InlineKeyboardButton(offer['name'], url=offer['url'])
                                keyboard.append([button])
                    runtime = movie.get('runtime', 'Not available')
                    year = movie.get('year', 'Not available')
                    bot.send_message(message.chat.id, f"{title} ({year}) (Duration: {runtime} min)", reply_markup=types.InlineKeyboardMarkup(keyboard))
                    return
                elif movie['type'] == 'SHOW' and query.lower() in movie['title'].lower():
                    title = movie['title']
                    if 'offers' in movie:
                        offers = movie['offers']
                        for offer in offers:
                            url = offer['url']
                            if url not in seen_urls:
                                seen_urls.add(url)
                                button = types.InlineKeyboardButton(offer['name'], url=offer['url'])
                                keyboard.append([button])
                    runtime = movie.get('runtime', 'Not available')
                    year = movie.get('year', 'Not available')
                    bot.send_message(message.chat.id, f"{title} ({year}) (Duration: {runtime} min)", reply_markup=types.InlineKeyboardMarkup(keyboard))
                    return
            if not found:
                bot.send_message(message.chat.id, f"No results found for {query}.")
        elif response.status_code == 404:
            bot.send_message(message.chat.id, "Movie not found.")
        else:
            bot.send_message(message.chat.id, f"Error ApI down {response.status_code}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")


# Authorized commands
AUTHORIZED_COMMANDS = [
    '/jj', '/pp', '/sm', '/ah', '/pm', '/kik', '/sg', '/vk', '/ad', '/pv', '/atx', '/jc', '/ze', '/dsp', '/hc', '/ulu', '/sony'
]

# Command handlers
COMMAND_HANDLERS = {
    '/jj': lambda message, url=None: jj_command(message),
    '/pp': lambda message, url=None: pp_command(message),
    '/sm': lambda message, url=None: sm_command(message),
    '/ah': lambda message, url=None: ah_command(message),
    '/pm': lambda message, url=None: pm_command(message),
    '/kik': lambda message, url=None: kik_command(message),
    '/sg': lambda message, url=None: sg_command(message),
    '/vk': lambda message, url=None: vk_command(message),
    '/ad': lambda message, url=None: ad_command(message), 
    '/pv': lambda message, url=None: pv_command(message),
    '/atx': lambda message, url=None: atx_command(message),
    '/jc': lambda message, url=None: jc_command(message),
    '/ze': lambda message, url=None: ze_command(message), 
    '/dsp': lambda message, url=None: dsp_command(message),
    '/hc': lambda message, url=None: hc_command(message),
    '/ulu': lambda message, url=None: ulu_command(message), 
    '/sony': lambda message, url=None: sony_command(message),
}


def jj_command(message):
    if url:
        bot.reply_to(message, f"JJ command executed with URL: {url}")
    else:
        bot.reply_to(message, "JJ command executed.")

def pp_command(message):
    if url:
        bot.reply_to(message, f"PP command executed with URL: {url}")
    else:
        bot.reply_to(message, "PP command executed.")

def sm_command(message):
    if url:
        bot.reply_to(message, f"SM command executed with URL: {url}")
    else:
        bot.reply_to(message, "SM command executed.")

def ah_command(message):
    if url:
        bot.reply_to(message, f"AH command executed with URL: {url}")
    else:
        bot.reply_to(message, "AH command executed.")

def pm_command(message):
    if url:
        bot.reply_to(message, f"PM command executed with URL: {url}")
    else:
        bot.reply_to(message, "PM command executed.")

def kik_command(message):
    if url:
        bot.reply_to(message, f"KIK command executed with URL: {url}")
    else:
        bot.reply_to(message, "KIK command executed.")

def sg_command(message):
    if url:
        bot.reply_to(message, f"SG command executed with URL: {url}")
    else: 
             bot.reply_to(message, "SG command executed.")

def vk_command(message):
    if url:
        bot.reply_to(message, f"VK command executed with URL: {url}")
    else:
        bot.reply_to(message, "VK command executed.")

def ad_command(message):
    if url:
        bot.reply_to(message, f"AD command executed with URL: {url}")
    else:
        bot.reply_to(message, "AD command executed.") 

def pv_command(message):
    if url:
        bot.reply_to(message, f"PV command executed with URL: {url}")
    else:
        bot.reply_to(message, "PV command executed.")

def atx_command(message):
    if url:
        bot.reply_to(message, f"ATX command executed with URL: {url}")
    else:
        bot.reply_to(message, "ATX command executed.")


def jc_command(message):
    if url:
        bot.reply_to(message, f"JC command executed with URL: {url}")
    else:
        bot.reply_to(message, "JC command executed.")

def ze_command(message):
    if url:
        bot.reply_to(message, f"ZE command executed with URL: {url}")
    else:
        bot.reply_to(message, "ZE command executed.")

def dsp_command(message):
    if url:
        bot.reply_to(message, f"DSP command executed with URL: {url}")
    else:
        bot.reply_to(message, "DSP command executed.")

def hc_command(message):
    if url:
        bot.reply_to(message, f"HC command executed with URL: {url}")
    else:
        bot.reply_to(message, "HC command executed.")

def ulu_command(message):
    if url:
        bot.reply_to(message, f"ULU command executed with URL: {url}")
    else:
        bot.reply_to(message, "ULU command executed.") 

def sony_command(message):
    if url:
        bot.reply_to(message, f"SONY command executed with URL: {url}")
    else:
        bot.reply_to(message, "SONY command executed.")

@bot.message_handler(commands=['auth'])
def auth_command(message):
    if message.from_user.id == ADMIN_ID:
        args = message.text.split()
        if len(args) > 1:
            # Authorize user
            if args[1].isdigit():
                user_id = int(args[1])
                if user_id not in AUTHORIZED_USERS:
                    AUTHORIZED_USERS.append(user_id)
                    bot.send_message(message.chat.id, f"User {user_id} authorized successfully.")
                else:
                    bot.send_message(message.chat.id, f"User {user_id} already authorized.")
            # Authorize group (if command is used in a group)
            elif message.chat.type in ['group', 'supergroup']:
                chat_id = message.chat.id
                if chat_id not in AUTHORIZED_GROUPS:
                    AUTHORIZED_GROUPS.append(chat_id)
                    bot.send_message(chat_id, "Group authorized successfully.")
                else:
                    bot.send_message(chat_id, "Group already authorized.")
        else:
            # Handle missing arguments
            bot.send_message(message.chat.id, "Please provide a user ID or use this command in a group.")
    else:
        # Handle unauthorized admin access
        bot.send_message(message.chat.id, "Only admins can use this command.")

def is_authorized(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    return user_id in AUTHORIZED_USERS or chat_id in AUTHORIZED_GROUPS or chat_id == ADMIN_ID

@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text.startswith('/'):
        if is_authorized(message):
            command, *args = message.text.split()
            if command in AUTHORIZED_COMMANDS:
                handler = COMMAND_HANDLERS.get(command)
                if handler:
                    handler(message, *args)
                else:
                    bot.reply_to(message, "Invalid command.")
            else:
                #bot.reply_to(message, "Unauthorized command.") 
                return
    else:
        return

# Command handler for the /jj command
@bot.message_handler(commands=['jj'])
def jj_command(message):
    #if message.text.split(): 
    if len(message.text.split()) == 1: 
        bot.send_message(chat_id=message.chat.id, text="Please provide a URL.")
        return
        url = message.text.split()[1]
        thumbnail_url, title = get_thumbnail_and_title(url)
        if thumbnail_url and title:
            bot.send_message(chat_id=message.chat.id, text=f"<b>Thumbnail URL:</b> {thumbnail_url}\n\n\n<b>Title:</b> <b> {title} </b>", parse_mode='HTML')
        elif title:
            bot.send_message(chat_id=message.chat.id, text=f"<b>Title:</b> {title}\nNo thumbnail URL found.", parse_mode='HTML')
        elif thumbnail_url:
            bot.send_message(chat_id=message.chat.id, text=f"<b>Thumbnail URL:</b> {thumbnail_url}\nNo title found.", parse_mode='HTML')
        else:
            bot.send_message(chat_id=message.chat.id, text="No title or thumbnail URL Found in Short Lulli Lele.")
    else:
        bot.send_message(chat_id=message.chat.id, text="Please provide a URL.")
        
# Command handler for the /pp command
@bot.message_handler(commands=['pp'])
def pp_command(message):
    #if message.text.split(): 
    if len(message.text.split()) > 1:
        url = message.text.split()[1]
        output = process_url(url)
        bot.send_message(chat_id=message.chat.id, text=output, parse_mode='HTML')
    else:
        bot.send_message(chat_id=message.chat.id, text="Please provide a URL. https://www.playflix.app") 

# Command handler for the /ad command
@bot.message_handler(commands=['ad'])
def ad_command(message):
    #if message.text.split(): 
    if len(message.text.split()) > 1:
        url = message.text.split()[1]
        metadata = fetch_metadata(url)
        if metadata:
            bot.send_message(chat_id=message.chat.id, 
                             text=f"<b>Thumbnail URL:</b> {metadata['thumbnail_url']}\n\n\n<b>Title:</b> <b>{metadata['title']}</b>", 
                             parse_mode='HTML')
        else:
            bot.send_message(chat_id=message.chat.id, 
                             text="No title or thumbnail URL found.")
    else:
        bot.send_message(chat_id=message.chat.id, 
                         text="Please provide a URL. https://www.addatimes.com") 
         


# Command handler for the /vk command
@bot.message_handler(commands=['vk'])
def vk_command(message):
    #if message.text.split(): 
    if len(message.text.split()) > 1:
        url = message.text.split()[1]
        metadata = vk.fetch_metadata(url)
        if metadata:
            title = metadata['title'].split('|')[0].strip()
            
            bot.send_message(chat_id=message.chat.id, 
                             text=f"<b>Thumbnail URL</b> :- <b>{metadata['thumbnail_url']}</b>\n\n\n<b>Title</b> :- <b>{title}</b>", 
                             parse_mode='HTML')
        else:
            bot.send_message(chat_id=message.chat.id, 
                             text="Failed to retrieve metadata.")
    else:
        bot.send_message(chat_id=message.chat.id, 
                         text="Please Provide URL Link. https://viki.com") 
         
#command handler for sm
@bot.message_handler(commands=['sm'])
def sm_command(message):
    #if message.text.split(): 
    if len(message.text.split()) > 1:
        url = message.text.split()[1]
        landscape_url, portrait_url, title = sm.get_thumbnail_and_title(url)
        
        if landscape_url and portrait_url and title:
            output = f"""
            <b>Landscape URL</b> :- <b>{landscape_url}</b>
            \n<b>Portrait URL</b> :- <a href="{portrait_url}"><b>Click Here</b></a>
            \n<b>Title</b> :- <b>{title}</b>
            """
            bot.send_message(chat_id=message.chat.id, text=output, parse_mode='HTML')
        else:
            bot.send_message(chat_id=message.chat.id, text="No title or thumbnail URL found.")
    else:
        bot.send_message(chat_id=message.chat.id, text="Please provide a URL. https://www.shemaroome.com") 

#command handler for ah
@bot.message_handler(commands=['ah'])
def ah_command(message): 
    if len(message.text.split()) > 1:
        url = message.text.split()[1]  # Get URL from command
        landscape_url, portrait_url, title = get_ah_data(url)
    
        if landscape_url and portrait_url and title:         
            output = f"""
            <b>Landscape URL</b> :- <b>{landscape_url}</b>
            \n<b>Portrait URL</b> :- <a href="{portrait_url}"><b>Click Here</b></a>
            \n<b>Title</b> :- <b>{title}</b>
            """
            bot.send_message(chat_id=message.chat.id, text=output, parse_mode='HTML')
        else:
            bot.send_message(chat_id=message.chat.id, text="No title or thumbnail URL found.") 
    else:   
        bot.send_message(chat_id=message.chat.id, text="Please provide a URL. https://www.aha.com")

#command handler for pm
@bot.message_handler(commands=['pm'])
def pm_command(message): 
    if len(message.text.split()) > 1: 
        
        url = message.text.split()[1]  # Get URL from command
        thumbnail_url, title = fetch_thumbnail_and_title(url)

        if thumbnail_url and title:
            output = f"""
            <b>Thumbnail URL</b> :- <b>{thumbnail_url}</b>
            \n<b>Title</b> :- <b>{title}</b>
            """
            bot.send_message(chat_id=message.chat.id, text=output, parse_mode='HTML')
        else:
            bot.send_message(chat_id=message.chat.id, text="No title or thumbnail URL found.") 
    else:
        bot.send_message(chat_id=message.chat.id, text="Please provide a URL. https://www.planetmarathi.com")

#command handler for sg
@bot.message_handler(commands=['sg'])
def sg_command(message):
    url = message.text.split()[1]  # Get URL from command
    poster_url, title = get_sg_data(url)

    if poster_url and title:
        output = f"""
        <b>Poster URL</b> :- <b>{poster_url}</b>
        \n<b>Title</b> :- <b>{title}</b>
        """
        bot.send_message(chat_id=message.chat.id, text=output, parse_mode='HTML')
    elif poster_url:
        output = f"""
        <b>Poster URL</b> :- <b>{poster_url}</b>
        \nTitle: Not found
        """
        bot.send_message(chat_id=message.chat.id, text=output, parse_mode='HTML')
    elif title:
        output = f"""
        Poster URL: Not found
        \n<b>Title</b> :- <b>{title}</b>
        """
        bot.send_message(chat_id=message.chat.id, text=output, parse_mode='HTML')
    else:
        bot.send_message(chat_id=message.chat.id, text="No title or poster URL found.")


#command handler for kik
@bot.message_handler(commands=['kik'])
def kik_command(message):
    url = message.text.split()[1]  # Get URL from command
    poster_url, title = get_kik_data(url)

    if poster_url and title:
        output = f"""
        <b>Poster URL</b> :- <b>{poster_url}</b>
        \n<b>Title</b> :- <b>{title}</b>
        """
        bot.send_message(chat_id=message.chat.id, text=output, parse_mode='HTML')
    elif poster_url:
        output = f"""
        <b>Poster URL</b> :- <b>{poster_url}</b>
        Title: Not found
        """
        bot.send_message(chat_id=message.chat.id, text=output, parse_mode='HTML')
    elif title:
        output = f"""
        Poster URL: Not found
        <b>Title</b> :- <b>{title}</b>
        """
        bot.send_message(chat_id=message.chat.id, text=output, parse_mode='HTML')
    else:
        bot.send_message(chat_id=message.chat.id, text="No title or poster URL found.")


#command handler for pv
@bot.message_handler(commands=['pv'])
def pv_command(message):
    try:
        url = message.text.split()[1]  # Get URL from command

        # Fetch data
        title_azpv = pv.fetch_title(url)  # Assuming fetch_title returns a string
        covershot_url = pv.scrape_azpv_covershot(url)

        # Build output
        if covershot_url and title_azpv:
            output = f"""
            <b>Thumbnail URL</b> :- <b>{covershot_url}</b>
            \n<b>Title</b> :- <b>{title_azpv}</b>
            """
        elif covershot_url:
            output = f"""
            <b>Thumbnail URL</b> :- <b>{covershot_url}</b>
            Title: Not found
            """
        elif title_azpv:
            output = f"""
            Thumbnail URL: Not found
            \n<b>Title</b> :- <b>{title_azpv}</b>
            """
        else:
            output = "No title or thumbnail URL found."

        bot.send_message(chat_id=message.chat.id, text=output, parse_mode='HTML')

    except IndexError:
        bot.send_message(chat_id=message.chat.id, text="Please provide a valid URL. https://www.primevideo.com")
    except Exception as e:  # Catch any other potential errors
        bot.send_message(chat_id=message.chat.id, text=f"An error occurred: {e}")

#command handler for atx
@bot.message_handler(commands=['atx'])
def atx_command(message):
    chat_id = message.chat.id
    url = message.text.replace('/atx ', '')
    
    try:
        data = get_atx_data(url)
        if data:
            output = f"<b>Title:</b> <b>{data['title']} </b>\n\n<b>Landscape URL:</b> <b>{data['landscape_url']} </b>\n\n<b>Portrait URL:</b> <b> {data['portrait_url']} </b>"
            bot.send_message(chat_id, output, parse_mode='HTML')
        else:
            bot.send_message(chat_id, "<b>Failed to retrieve data.</b>", parse_mode='HTML')
    except Exception as e:
        bot.send_message(chat_id, f"<b>Error:</b> {str(e)}", parse_mode='HTML')

#command handler for jc 
@bot.message_handler(commands=['jc'])
def jc_command(message):
    if len(message.text.split()) > 1:
        url = message.text.split()[1]
        metadata = jcm.fetch_metadata(url)
        
        if metadata:
            bot.send_message(chat_id=message.chat.id, 
                             text=f"<b>Landscape Url :</b> <b>{metadata.get('landscape_image_url')}</b>\n\n<b>Title :</b> <b>{metadata.get('title')}</b>", 
                             parse_mode='HTML')
        else:
            bot.send_message(chat_id=message.chat.id, text="Failed to retrieve metadata.")
    else:
        bot.send_message(chat_id=message.chat.id, text="Please Provide URL Link. https://www.jiocinema.com") 


#command handler for sonyliv
@bot.message_handler(commands=['sony'])
def sony_command(message):
    if len(message.text.split()) > 1:
        url = message.text.split()[1]
        metadata = sny.fetch_metadata(url)
        
        if metadata:
            bot.send_message(chat_id=message.chat.id, 
                             text=f"<b>Landscape Url :</b> <b>{metadata['thumbnail_url']}</b>\n\n<b>Title :</b> <b>{metadata.get('title')}</b>", 
                             parse_mode='HTML')
        else:
            bot.send_message(chat_id=message.chat.id, text="Failed to retrieve metadata.")
    else:
        bot.send_message(chat_id=message.chat.id, text="Please Provide URL Link. https://www.sonyliv.com")

# Command handler for /ze
@bot.message_handler(commands=['ze'])
def ze_command(message): 
    if len(message.text.split()) > 1:

        """
        Handles /ze command to fetch thumbnail URL and title.
    
        Args:
            message (Message): Telegram message object.
        """
        # Get URL from command
        url = message.text.split()[1]
    
        # Fetch thumbnail URL and title
        result = tee.fetch_thumbnail_and_title(url)
    
        if result:
            thumbnail_url, title = result['thumbnail_url'], result['title']
        
            # Create output message
            output = f"""
<b>Thumbnail URL:</b> <b>{thumbnail_url}</b>
\n<b>Title:</b> <b>{title}</b>
"""
        
            # Send message
            bot.send_message(chat_id=message.chat.id, text=output, parse_mode='HTML')
        else:
            # Send error message
            bot.send_message(chat_id=message.chat.id, text="No title or thumbnail URL found.") 

    else:
        bot.send_message(chat_id=message.chat.id, text="Please provide a URL. https://www.zee5.com")
          

# Command handler for /dsp
@bot.message_handler(commands=['dsp'])
def dsp_command(message): 
    if len(message.text.split()) > 1:
        """
        Handles /dsp command to fetch thumbnail URL and title.
    
        Args:
            message (Message): Telegram message object.
        """
        # Get URL from command
        url = message.text.split()[1]
    
        # Fetch thumbnail URL and title
        modified_thumbnail_url , title = fetch_thumbnail_and_title(url)
    
        if modified_thumbnail_url and title:
        # Create output message
            output = f"""
<b>Thumbnail URL:</b> <b>{modified_thumbnail_url}</b>
\n<b>Title:</b> <b>{title}</b>
"""
        # Send message
            bot.send_message(chat_id=message.chat.id, text=output, parse_mode='HTML')
        else:
        # Send error message
            bot.send_message(chat_id=message.chat.id, text="No title or thumbnail URL found.") 
    else:
        bot.send_message(chat_id=message.chat.id, text="Please provide a URL. https://www.disneyplus.com/")
        

@bot.message_handler(commands=['hc'])
def hc_command(message):
    if message.text.split():
        url = message.text.split()[1]
        result = fetch_data(url)
        if result:
            landscape_url, portrait_url, title = result.values()
            output = f"""
            <b>Landscape URL</b> :- <b>{landscape_url}</b>
            \n<b>Portrait URL</b> :- <a href="{portrait_url}"><b>Click Here</b></a>
            \n<b>Title</b>:- <b>{title}</b>
            """
            bot.send_message(chat_id=message.chat.id, text=output, parse_mode='HTML')
        else:
            bot.send_message(chat_id=message.chat.id, text="No title or thumbnail URL found.")
    else:
        bot.send_message(chat_id=message.chat.id, text="Please provide a URL.")


@bot.message_handler(commands=['ulu'])
def ulu_command(message):
    if message.text.split():
        url = message.text.split()[1]
        try:
            # URL validation
            from urllib.parse import urlparse
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                bot.send_message(chat_id=message.chat.id, text="Invalid URL.")
                return
        except ValueError:
            bot.send_message(chat_id=message.chat.id, text="Invalid URL.")
            return

        try:
            # Run (link unavailable) with Cloudinary integration
            with subprocess.Popen(['python', 'ulu.py', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
                output, error = process.communicate()
                print("Output:", output.decode('utf-8'))
                print("Error:", error.decode('utf-8'))

                # Read Cloudinary Image URLs from output
                lines = output.decode('utf-8').split('\n')
                landscape_url = None
                portrait_url = None
                for line in lines:
                    if "Landscape URL:" in line:
                        landscape_url = line.split(": ")[1]
                    elif "Portrait URL:" in line:
                        portrait_url = line.split(": ")[1]

                # Send Cloudinary Image URLs
                if landscape_url and portrait_url:
                    bot.send_message(chat_id=message.chat.id, text=f"Landscape URL: {landscape_url}\n\nPortrait URL: {portrait_url}")
                else:
                    bot.send_message(chat_id=message.chat.id, text="Error uploading images.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error processing URL {url}: {str(e)}")
            bot.send_message(chat_id=message.chat.id, text="Internal error. Please try again.")
        except Exception as e:
            logging.error(f"Error processing URL {url}: {str(e)}")
            bot.send_message(chat_id=message.chat.id, text="Internal error. Please try again.")
    else:
        bot.send_message(chat_id=message.chat.id, text="Please provide a URL.")


def start_bot():
    """Start the Telegram bot"""
    logging.info("Starting the bot...")
    try:
        bot.infinity_polling()
    except Exception as e:
        logging.error(f"Error occurred while polling: {e}")

# FastAPI route
@app.route("/", methods=["GET", "HEAD"])
async def index(request: Request):
    logging.info("Received request to /")
    return JSONResponse(content={"message": "Service is running"}, media_type="application/json", status_code=200)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    
    # Run the bot in a separate thread
    Thread(target=start_bot).start()
    
    # Start FastAPI web server
    uvicorn.run(app, host="0.0.0.0", port=port)
