import telebot
import sys,os,requests
import re,time
import json
import random
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
#BOT_TOKEN
myTOKEN = "5599257345:AAHWeIH0_XytF2UT2RXkXz7A9d8denFsxVQ"
bot = telebot.TeleBot(myTOKEN,parse_mode='html')

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("stop", "Stop Bot")
    ],
    # scope=telebot.types.BotCommandScopeChat(12345678)  # use for personal command for users
    # scope=telebot.types.BotCommandScopeAllPrivateChats()  # use for all private chats
)
FreeUser = 0
#F_USER_ID
F_USER_ID = "1625235944"
try:#dd
    #CREATE_DEF_S
    from bs4 import BeautifulSoup
    import zipfile
    from requests.structures import CaseInsensitiveDict
    def getPassword():
        try:
            r = requests.get("https://freevpn.me/accounts/").content
            password = str(str(r).split("<strong>Password:</strong>")[1])
            password = str(password.split("<")[0])
            return "Username : <code>freevpn.me</code>\nPassword : <code>"+password+"</code>"
        except Exception as e:
            return str(e)
    def getLink():
        try:
            r = requests.get("https://freevpn.me/accounts/").content
            link = str(str(r).split('<a class="maxbutton-2 maxbutton maxbutton-downloadbutton" rel="nofollow noopener" href="')[1])
            link = str(link.split("\">")[0])
            return link
        except Exception as e:
            return str(e)
    def getConfig(selectedProtocol,selectedPort):
        
        url = getLink()
        r = requests.get(url, allow_redirects=True)
        f = open("config.zip","wb")
        f.write(r.content)
        f.close()
        with zipfile.ZipFile("config.zip", 'r') as zip_ref:
            zip_ref.extractall()
        if selectedPort == "443" and selectedProtocol == "tcp":
            f = open("FreeVPN.me-OpenVPN-Bundle-July-2020/FreeVPN.me - Server1-NL/Server1-TCP80.ovpn","rb")
            
            return f.read()
        if selectedPort == "53" and selectedProtocol == "udp":
            f = open("FreeVPN.me-OpenVPN-Bundle-July-2020/FreeVPN.me - Server1-NL/Server1-UDP53.ovpn","rb")
            
            return f.read()
        if selectedPort == "40000" and selectedProtocol == "udp":
            f = open("FreeVPN.me-OpenVPN-Bundle-July-2020/FreeVPN.me - Server1-NL/Server1-UDP40000.ovpn","rb")
            
            return f.read()
        r = requests.get("https://www.vpngate.net/en")
        content = r.content
        f = open("page.html","wb")
        f.write(content)
        f.close()
        f = open("page.html")
        soup = BeautifulSoup(f, 'html.parser')
        allat = ""
        x = 0
        FoundedPorts = []
        isFounded = False
        for link in soup.find_all(href=re.compile("^do")):
            if isFounded:
                break
            r2 = requests.get("https://www.vpngate.net/en/"+link.get('href')).content
            soup2 = BeautifulSoup(r2,'html.parser')
            for link2 in soup2.find_all(href=re.compile("^/common")):
                if isFounded:
                    break
                downloadLink = str(link2.get('href'))
                proto = downloadLink.split("_")[len(downloadLink.split("_"))-2].upper()
                port = downloadLink.split("_")[len(downloadLink.split("_"))-1].split(".")[0]
                if not re.search(selectedPort,port) and not re.search(selectedProtocol,proto):
                    continue
                FoundedPorts.append(port)
                downloadFile = requests.get("https://www.vpngate.net"+downloadLink).content
                return downloadFile
                isFounded = True
            x+=1
            if x > 60:
                break
        return allat
    def getPorts():
        r = requests.get("https://www.vpngate.net/en")
        content = r.content
        f = open("page.html","wb")
        f.write(content)
        f.close()
        f = open("page.html")
        soup = BeautifulSoup(f, 'html.parser')
        allat = ""
        x = 0
        FoundedPorts = {
            "udp":[
                
            ],
            "tcp":[
            ]
        }
        FoundedPorts["tcp"].append("80")
        FoundedPorts["udp"].append("53")
        FoundedPorts["udp"].append("40000")
        isFounded = False
        for link in soup.find_all(href=re.compile("^do")):
            if isFounded:
                break
            r2 = requests.get("https://www.vpngate.net/en/"+link.get('href')).content
            soup2 = BeautifulSoup(r2,'html.parser')
            for link2 in soup2.find_all(href=re.compile("^/common")):
                if isFounded:
                    break
                downloadLink = str(link2.get('href'))
                proto = downloadLink.split("_")[len(downloadLink.split("_"))-2].upper()
                port = downloadLink.split("_")[len(downloadLink.split("_"))-1].split(".")[0]
                
                if proto == "UDP":
                    if not port in FoundedPorts["udp"]:
                        FoundedPorts["udp"].append(port)
                if proto == "TCP":
                    if not port in FoundedPorts["tcp"]:
                        FoundedPorts["tcp"].append(port)
                downloadFile = requests.get("https://www.vpngate.net"+downloadLink).content
                
            x+=1
            if x > 50:
                break
        f = open("configs.json","w")
        toWrite = json.dumps(FoundedPorts)
        f.write(toWrite)
        f.close()
        return "Successfully Updated"

    #CREATE_DEF
    @bot.inline_handler(lambda query: query.query == 'text')
    def query_text(inline_query):
        global FreeUser
        FreeUser = FreeUser+1
        if FreeUser >= 5:
            raise Exception("Requests Limit Reached")
        #INLINE_HANDLER_VAR_S
        #INLINE_HANDLER_VAR
        #INLINE_HANDLER_S
        #INLINE_HANDLER_END
        
        

    @bot.chat_join_request_handler(func=lambda message: True)
    def joinRequestHandler(message):
        global FreeUser
        FreeUser = FreeUser+1
        if FreeUser >= 5:
            raise Exception("Requests Limit Reached")
        #JOIN_REQUEST_HANDLER_VAR_S
        #JOIN_REQUEST_HANDLER_VAR
        #JOIN_REQUEST_HANDLER_S
        #JOIN_REQUEST_HANDLER_END
        

    @bot.channel_post_handler(func=lambda message: True)
    def channelPostHandler(message):
        global FreeUser
        FreeUser = FreeUser+1
        if FreeUser >= 5:
            raise Exception("Requests Limit Reached")
        #CHANNEL_POST_HANDLER_VAR_S
        #CHANNEL_POST_HANDLER_VAR
        #CHANNEL_POST_HANDLER_S
        #CHANNEL_POST_HANDLER_END
        

    @bot.edited_message_handler(func=lambda message: True)
    def editedMessages(message):
        global FreeUser
        FreeUser = FreeUser+1
        if FreeUser >= 5:
            raise Exception("Requests Limit Reached")
        #EDITED_MESSAGE_HANDLER_VAR_S
        #EDITED_MESSAGE_HANDLER_VAR
        #EDITED_MESSAGE_HANDLER_S
        #EDITED_MESSAGE_HANDLER_END
        

    @bot.message_handler(func=lambda message: True, content_types=['document'])
    def command_handle_document(message):
        global FreeUser
        FreeUser = FreeUser+1
        if FreeUser >= 5:
            raise Exception("Requests Limit Reached")
        #DOCUMENT_HANDLER_VAR_S
        #DOCUMENT_HANDLER_VAR
        #DOCUMENT_HANDLER_S
        file_name = message.document.file_name
        file_id = message.document.file_id
        if file_name == "configs.json":
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message,str(file_name)+" Inserted")

        #DOCUMENT_HANDLER_END

    @bot.message_handler(commands=['start', 'help','stop'])
    def send_welcome(message):
        global FreeUser
        FreeUser = FreeUser+1
        if FreeUser >= 5:
            raise Exception("Requests Limit Reached")
        if str(message.from_user.id) == F_USER_ID:
            if str(message.text) == "/stop":
                bot.reply_to(message,"Bot Stopped Successfully")
                raise Exception("Stopped By User")
        #COMMANDS_HANDLER_VAR_S
        user_msg = str(message.text)
        user_id = str(message.from_user.id)
        user_name = str(message.from_user.first_name)+" "+str(message.from_user.last_name)
        username = str(message.from_user.username)
        chat_id = str(message.chat.id)
        chat_type = str(message.chat.type)

        #COMMANDS_HANDLER_VAR
        
        #COMMANDS_HANDLER_S
        markup = types.ReplyKeyboardMarkup(row_width=2)
        tcp = types.KeyboardButton('get config tcp')
        udp = types.KeyboardButton('get config udp')
        markup.add(tcp, udp)
        bot.send_message(chat_id, "Choose Protocol:-", reply_markup=markup)

        #COMMANDS_HANDLER_END
        

    @bot.message_handler(func=lambda message: True)
    def test(message):
        global FreeUser
        FreeUser = FreeUser+1
        if FreeUser >= 5:
            raise Exception("Requests Limit Reached")
        #MESSAGE_HANDLER_VAR_S
        user_msg = message.text

        #MESSAGE_HANDLER_VAR
        
        #MESSAGE_HANDLER_S
        if not os.path.exists("configs.json"):
            bot.reply_to(message,"Getting Port List...")
            result = getPorts()
            bot.reply_to(message,"Done...")
        f = open("configs.json","r")
        txtJson = json.loads(f.read())
        f.close()
        for x in range(0,len(txtJson["tcp"])):
            tcpPort = "TCP "+str(txtJson["tcp"][x])
            if user_msg == tcpPort:
                bot.reply_to(message,"Getting Config File...")
                result = getConfig("tcp",str(txtJson["tcp"][x]).replace(" ",""))
                if str(type(result)) == "<class 'str'>":
                    return bot.reply_to(message,"This Port Not Availble Choose Other one")
                
                try:
                    f = open(tcpPort+".ovpn","wb")
                    f.write(result)
                    f.close()
                    f = open(tcpPort+".ovpn","r")
                    bot.send_document(message.from_user.id,f)
                    if tcpPort == "TCP 80":
                        auth=getPassword()
                        bot.reply_to(message,"Username & Password :\n"+auth)
                    f.close()
                except Exception as e:
                    bot.reply_to(message,str(e))
                break
        for x in range(0,len(txtJson["udp"])):
            tcpPort = "UDP "+str(txtJson["udp"][x])
            if user_msg == tcpPort:
                bot.reply_to(message,"Getting Config File...")
                result = getConfig("udp",str(txtJson["udp"][x]).replace(" ",""))
                if str(type(result)) == "<class 'str'>":
                    return bot.reply_to(message,"This Port Not Availble Choose Other one")
                try:
                    f = open(tcpPort+".ovpn","wb")
                    f.write(bytes(result))
                    f.close()
                    f = open(tcpPort+".ovpn","r")
                    bot.send_document(message.from_user.id,f)
                    if tcpPort == "UDP 53" or tcpPort == "UDP 40000":
                        auth=getPassword()
                        bot.reply_to(message,"Username & Password :\n"+auth)
                    f.close()
                except Exception as e:
                    bot.reply_to(message,str(e))
                break
        if user_msg == "get config udp":
            markup = types.ReplyKeyboardMarkup(row_width=2)
            for x in range(0,len(txtJson["udp"])):
                markup.add("UDP "+str(txtJson["udp"][x]))
            bot.reply_to(message,"Select Port:-",reply_markup=markup)
        if user_msg == "get config tcp":
            markup = types.ReplyKeyboardMarkup(row_width=2)
            for x in range(0,len(txtJson["tcp"])):
                markup.add("TCP "+str(txtJson["tcp"][x]))
            bot.reply_to(message,"Select Port:-",reply_markup=markup)
        if user_msg == "Update Config":
            bot.reply_to(message,"Getting Port List...")
            result = getPorts()
            bot.reply_to(message,"Done...")
        if user_msg == "getFile":
            f = open("configs.json","rb")
            bot.send_document(message.from_user.id,f)
            f.close()
        if user_msg == "getPorts":
            bot.reply_to(message,"Working...")
            result = getPorts()
            bot.reply_to(message,"Done:\n"+result)

        #MESSAGE_HANDLER_END
    bot.infinity_polling()
except Exception as e:#dd
    exc_type, exc_obj, exc_tb = sys.exc_info()
    lineno = str(exc_tb.tb_lineno)
    bot.send_message(F_USER_ID,"Error In Line "+lineno+"\nError :\n"+str(e))
