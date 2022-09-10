import telebot
import sys,os,requests
import re,time
import json
import random
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
#BOT_TOKEN
myTOKEN = "5553808071:AAH_XIrU4IGxayQilPeLNGU-dsySmgd1L5Q"
bot = telebot.TeleBot(myTOKEN)

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("stop", "Stop Bot")
    ],
    # scope=telebot.types.BotCommandScopeChat(12345678)  # use for personal command for users
    # scope=telebot.types.BotCommandScopeAllPrivateChats()  # use for all private chats
)
#CREATE_DEF_S
import hmac
import hashlib
import urllib
users = [
    {"tg_id":None,"id":None,"api_key":"","api2_key":""}
]
def new_user2(message):
    for x in range(len(users)):
        t_id = users[x]["tg_id"]
        if t_id == message.from_user.id:
            users[x]["api2_key"] = message.text
            reply = "Login Success Make Sure API Enabled"
            msg = bot.reply_to(message,reply)
            break
def new_user1(message):
    for x in range(len(users)):
        t_id = users[x]["tg_id"]
        if t_id == message.from_user.id:
            users[x]["api_key"] = message.text
            reply = "Enter API SECRET KEY:"
            msg = bot.reply_to(message,reply)
            bot.register_next_step_handler(msg, new_user2)
            break
def new_user(message):
    users.append({"tg_id":message.from_user.id,"id":message.text,"api_key":"","api2_key":""})
    reply = "Enter API PUBLIC KEY:"
    msg = bot.reply_to(message,reply)
    bot.register_next_step_handler(msg, new_user1)
def Login2(message):
    try:
        api = adflyAPI(message)
        txtJson = api.getUrls()
        PublisherInfo = api.getMe()
        data = PublisherInfo["data"]
        WithdrawInfo = api.getWithdraw()
        totalEarn = str(WithdrawInfo["data"]["withdrawal"]["total"])
        u_id = "Your ID: <code>"+str(data["user_id"])+"</code>\n"
        u_user = "Your Username: <code>"+str(data["username"])+"</code>\n"
        u_name = "Full Name: <code>"+str(data["full_name"])+"</code>\n"
        u_withdraw = "Withdraw Type: <code>"+str(data["withdraw_type"])+"</code>\n"
        u_withdrawE = "Withdraw Email: <code>"+str(data["withdraw_email"])+"</code>\n"
        u_totalEarn = "\nYour Balance: <b>"+totalEarn+"</b>\n"
        
        reply = u_id+u_name+u_user+u_withdraw+u_withdrawE+u_totalEarn
        return bot.reply_to(message,reply,parse_mode="html")
    except:
        bot.reply_to(message,"Sorry Account Not Exists")
def Login(message):
    reply = "Now Enter Password:"
    msg = bot.reply_to(message,reply)
    bot.register_next_step_handler(msg, login2)
# Commands
bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("stop", "Stop Bot"),
        telebot.types.BotCommand("new", "Create New Account"),
        telebot.types.BotCommand("getme", "Get Account Info"),
        telebot.types.BotCommand("status", "View Status"),
        telebot.types.BotCommand("withdraw", "withdraw cash")
    ],
    # scope=telebot.types.BotCommandScopeChat(12345678)  # use for personal command for users
    # scope=telebot.types.BotCommandScopeAllPrivateChats()  # use for all private chats
)
def CreateAccount(name,password,email,username):
    from requests.structures import CaseInsensitiveDict
    url = "http://api.adf.ly/v1/register"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    data = {
        "name":name,
        "password":password,
        "password2":password,
        "email":email,
        "email2":email,
        "username":username
    }
    resp = requests.post(url, headers=headers, data=json.dumps(data))
    print(resp.status_code)
def CheckUser(user_id):
    for x in range(len(users)):
        tg_id = users[x]["tg_id"]
        if tg_id == user_id:
            return x
    return False
def getRespone(url):
    # INIT
    BASE_HOST = 'https://api.adf.ly'
    r = requests.get(BASE_HOST+url)
    return json.loads(r.content)
class adflyAPI():
    
    # KEYS
    USER_ID = 0
    SECRET_KEY = ''
    PUBLIC_KEY = ''
    
    def getParam(self):
        # SETUP Parameters
        params = dict()
        params['_user_id'] = self.USER_ID
        params['_api_key'] = self.PUBLIC_KEY
        params['_timestamp'] = int(time.time())
        queryParts = []
        keys = params.keys()
        keys = sorted(keys)
        for key in keys:
            quoted_key = urllib.parse.quote_plus(str(key))
            if params[key] is None:
                params[key] = ''
            
            quoted_value = urllib.parse.quote_plus(str(params[key]))
            queryParts.append('%s=%s' % (quoted_key, quoted_value))
        # INITILAIZE PARAMETERS
        init_params ='&'.join(queryParts)
        return init_params
    def getHash(self):
        # SETUP Parameters
        params = dict()
        params['_user_id'] = self.USER_ID
        params['_api_key'] = self.PUBLIC_KEY
        params['_timestamp'] = int(time.time())
        queryParts = []
        keys = params.keys()
        keys = sorted(keys)
        for key in keys:
            quoted_key = urllib.parse.quote_plus(str(key))
            if params[key] is None:
                params[key] = ''
            
            quoted_value = urllib.parse.quote_plus(str(params[key]))
            queryParts.append('%s=%s' % (quoted_key, quoted_value))
        # INITILAIZE PARAMETERS
        init_params ='&'.join(queryParts)
        # GENERATE HMAC
        x = hmac.new(self.SECRET_KEY.encode(),init_params.encode(),hashlib.sha256).hexdigest()
        return "_hash="+str(x)
    def getUrls(self,user_id):
        self.USER_ID = users[user_id]["id"]
        self.PUBLIC_KEY = users[user_id]["api_key"]
        self.SECRET_KEY = users[user_id]["api2_key"]
        url = "/v1/urls?"
        urlParam = self.getParam()
        urlHash = self.getHash()
        fullUrl = url+urlParam+"&"+urlHash
        return getRespone(fullUrl)
    def getMe(self,user_id):
        self.USER_ID = users[user_id]["id"]
        self.PUBLIC_KEY = users[user_id]["api_key"]
        self.SECRET_KEY = users[user_id]["api2_key"]
        url = "/v1/account?"
        urlParam = self.getParam()
        urlHash = self.getHash()
        fullUrl = url+urlParam+"&"+urlHash
        return getRespone(fullUrl)
    def getWithdraw(self,user_id):
        self.USER_ID = users[user_id]["id"]
        self.PUBLIC_KEY = users[user_id]["api_key"]
        self.SECRET_KEY = users[user_id]["api2_key"]
        url = "/v1/withdraw?"
        urlParam = self.getParam()
        urlHash = self.getHash()
        fullUrl = url+urlParam+"&"+urlHash
        return getRespone(fullUrl)
    def withdraw(self,user_id):
        self.USER_ID = users[user_id]["id"]
        self.PUBLIC_KEY = users[user_id]["api_key"]
        self.SECRET_KEY = users[user_id]["api2_key"]
        url = "/v1/requestWithdraw?"
        urlParam = self.getParam()
        urlHash = self.getHash()
        fullUrl = url+urlParam+"&"+urlHash
        return getRespone(fullUrl)
@bot.message_handler(commands=['getme'])
def send_welcome(message):
    isExists = CheckUser(message.from_user.id)
    if not isExists:
        return bot.reply_to(message,"User Not Exists Try To /new")
    api = adflyAPI()
    PublisherInfo = api.getMe(isExists)
    data = PublisherInfo["data"]
    WithdrawInfo = api.getWithdraw(isExists)
    totalEarn = str(WithdrawInfo["data"]["withdrawal"]["total"])
    u_id = "Your ID: <code>"+str(data["user_id"])+"</code>\n"
    u_user = "Your Username: <code>"+str(data["username"])+"</code>\n"
    u_name = "Full Name: <code>"+str(data["full_name"])+"</code>\n"
    u_withdraw = "Withdraw Type: <code>"+str(data["withdraw_type"])+"</code>\n"
    u_withdrawE = "Withdraw Email: <code>"+str(data["withdraw_email"])+"</code>\n"
    u_totalEarn = "\nYour Balance: <b>"+totalEarn+"</b>\n"
    
    reply = u_id+u_name+u_user+u_withdraw+u_withdrawE+u_totalEarn
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add('💵 Withdraw','💰 Balance','My Account')
    return bot.reply_to(message,reply,parse_mode="html")
    
@bot.message_handler(commands=['withdraw'])
def try_withdraw(message):
    isExists = CheckUser(message.from_user.id)
    if not isExists:
        return bot.reply_to(message,"User Not Exists Try To /new")
    api = adflyAPI()
    result = api.withdraw(isExists)
    if len(result["errors"]) > 0:
        errorMsg = result["errors"][0]["msg"]
        return bot.reply_to(message,errorMsg)
@bot.message_handler(commands=['new'])
def add_new_user(message):
    reply = "Enter Adfly User ID:"
    msg = bot.reply_to(message,reply)
    bot.register_next_step_handler(msg, new_user)
@bot.message_handler(commands=['login'])
def try_Login(message):
    reply = "Enter Username Or Email:"
    msg = bot.reply_to(message,reply)
    bot.register_next_step_handler(msg, login)
@bot.message_handler(commands=['status'])
def view_status(message):
    isExists = CheckUser(message.from_user.id)
    if not isExists:
        return bot.reply_to(message,"User Not Exists Try To /new")
    api = adflyAPI()
    PublisherInfo = api.getMe(isExists)
    data = PublisherInfo["data"]
    WithdrawInfo = api.getWithdraw(isExists)
    totalEarn = str(WithdrawInfo["data"]["withdrawal"]["total"])
    u_date = "Your ID: <code>"+str(data["user_id"])+"</code>\n"
    u_user = "Your Username: <code>"+str(data["username"])+"</code>\n"
    u_name = "Full Name: <code>"+str(data["full_name"])+"</code>\n"
    u_withdraw = "Withdraw Type: <code>"+str(data["withdraw_type"])+"</code>\n"
    u_withdrawE = "Withdraw Email: <code>"+str(data["withdraw_email"])+"</code>\n"
    u_totalEarn = "\nYour Balance: <b>"+totalEarn+"</b>\n"
    
    reply = u_id+u_name+u_user+u_withdraw+u_withdrawE+u_totalEarn
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add('💵 Withdraw','💰 Balance','My Account')
    return bot.reply_to(message,reply,parse_mode="html")

#CREATE_DEF
@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    print("hi")
    #INLINE_HANDLER_VAR_S
    #INLINE_HANDLER_VAR
    #INLINE_HANDLER_S
    #INLINE_HANDLER_END
    
    

@bot.chat_join_request_handler(func=lambda message: True)
def joinRequestHandler(message):
    print("hi")
    #JOIN_REQUEST_HANDLER_VAR_S
    #JOIN_REQUEST_HANDLER_VAR
    #JOIN_REQUEST_HANDLER_S
    #JOIN_REQUEST_HANDLER_END
    

@bot.channel_post_handler(func=lambda message: True)
def channelPostHandler(message):
    print("hi")
    #CHANNEL_POST_HANDLER_VAR_S
    #CHANNEL_POST_HANDLER_VAR
    #CHANNEL_POST_HANDLER_S
    #CHANNEL_POST_HANDLER_END
    

@bot.edited_message_handler(func=lambda message: True)
def editedMessages(message):
    print("hi")
    #EDITED_MESSAGE_HANDLER_VAR_S
    #EDITED_MESSAGE_HANDLER_VAR
    #EDITED_MESSAGE_HANDLER_S
    #EDITED_MESSAGE_HANDLER_END
    

@bot.message_handler(func=lambda message: True, content_types=['document'])
def command_handle_document(message):
    print("hi")
    #DOCUMENT_HANDLER_VAR_S
    #DOCUMENT_HANDLER_VAR
    #DOCUMENT_HANDLER_S
    #DOCUMENT_HANDLER_END

@bot.message_handler(commands=['start', 'help','stop'])
def send_welcome(message):
    #COMMANDS_HANDLER_VAR_S
    #COMMANDS_HANDLER_VAR
    
    #COMMANDS_HANDLER_S
    reply = "Welcome To Adfly BOT This is not offical Bot It'll Just Help You To Manage Your Adfly Account\n* This bot is not taking your personal info"
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add('💵 Withdraw','💰 Balance','My Account')
    bot.reply_to(message,reply,reply_markup=markup)

    #COMMANDS_HANDLER_END
    

@bot.message_handler(func=lambda message: True)
def test(message):
    #MESSAGE_HANDLER_VAR_S
    #MESSAGE_HANDLER_VAR
    
    #MESSAGE_HANDLER_S
    if message.text == "My Account":
        isExists = CheckUser(message.from_user.id)
        if not isExists:
            return bot.reply_to(message,"User Not Exists Try To /new")
        api = adflyAPI()
        PublisherInfo = api.getMe(isExists)
        data = PublisherInfo["data"]
        WithdrawInfo = api.getWithdraw(isExists)
        totalEarn = str(WithdrawInfo["data"]["withdrawal"]["total"])
        u_id = "Your ID: <code>"+str(data["user_id"])+"</code>\n"
        u_user = "Your Username: <code>"+str(data["username"])+"</code>\n"
        u_name = "Full Name: <code>"+str(data["full_name"])+"</code>\n"
        u_withdraw = "Withdraw Type: <code>"+str(data["withdraw_type"])+"</code>\n"
        u_withdrawE = "Withdraw Email: <code>"+str(data["withdraw_email"])+"</code>\n"
        u_totalEarn = "\nYour Balance: <b>"+totalEarn+"</b>\n"
        
        reply = u_id+u_name+u_user+u_withdraw+u_withdrawE+u_totalEarn
        markup = types.ReplyKeyboardMarkup(row_width=2)
        markup.add('💵 Withdraw','💰 Balance','My Account')
        return bot.reply_to(message,reply,parse_mode="html",reply_markup=markup)
    if message.text == "💰 Balance":
        isExists = CheckUser(message.from_user.id)
        if not isExists:
            return bot.reply_to(message,"User Not Exists Try To /new")
        api = adflyAPI()
        WithdrawInfo = api.getWithdraw(isExists)
        totalEarn = str(WithdrawInfo["data"]["withdrawal"]["total"])
        u_totalEarn = "\nYour Balance: <b>"+totalEarn+"</b>\n"
        reply = u_totalEarn
        return bot.reply_to(message,reply,parse_mode="html")
    if message.text == "💵 Withdraw":
        isExists = CheckUser(message.from_user.id)
        if not isExists:
            return bot.reply_to(message,"User Not Exists Try To /new")
        api = adflyAPI()
        result = api.withdraw(isExists)
        if len(result["errors"]) > 0:
            errorMsg = result["errors"][0]["msg"]
            return bot.reply_to(message,errorMsg)

    #MESSAGE_HANDLER_END
bot.infinity_polling()