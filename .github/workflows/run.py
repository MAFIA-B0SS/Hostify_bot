import telebot
import socket,sys,os,requests
import re,time
import json
import random
from googletrans import Translator
from telebot import types
from datetime import datetime
from html2image import Html2Image
from html.parser import HTMLParser
newCommands = 0
BOT_TOKEN = os.environ.get("CODER_NINJA")
bot = telebot.TeleBot(BOT_TOKEN)
def PostRandom(Lan=""):
    groupsIds = {"python":"-1001567978602","php":"-699912702","pytelegrambotapi":"-1001540211939"}
    
    f = open("commands.json","r")
    txtJson = json.loads(f.read())
    f.close()
    AllLang = ["en","ar"]
    selectedLang = random.choice(AllLang)
    AllPLan = []
    AllExamples = []
    for language in txtJson["Languages"]:
        AllPLan.append(language)    
    selectedLan = Lan or random.choice(AllPLan)
    for command in txtJson["Languages"][selectedLan]["commands"]:
        for x in range(len(txtJson["Languages"][selectedLan]["commands"][command][selectedLang])):
            theTitle = str(txtJson["Languages"][selectedLan]["commands"][command][selectedLang][0])
            theExample = str(txtJson["Languages"][selectedLan]["commands"][command][selectedLang][1])
            toAppend = theTitle+"\n------\n"+styleExample(theExample)
            AllExamples.append(toAppend)
    randomPost = random.choice(AllExamples)
    for g_lan in groupsIds.keys():
        if str(g_lan) == str(selectedLan):
            sendTo = str(groupsIds[g_lan])
            bot.send_message(sendTo,randomPost,parse_mode="html",disable_web_page_preview=True)
    bot.send_message("1625235944","Posted !")


newCommandProg = {
    "userid":{
        "id":"","lan":"","lang":"","input":"","example":""
    }
}
userActions = {
}
Colors = []
AdminID = "1625235944"
bot.send_message(AdminID,"Bot Started...")
inDevelop = False
Admins = [1625235944]
# Classes
class Keywords:
    _language = ""
    _keyword = ""
    _color = ""
    _isBold = False
    _isRegex = False
    _isItalic = False
    def __init__(self,userid):
        self._userid = userid
    def setLanguage(self,language):
        self._language = language
    def setColor(self,color):
        self._color = color
    def isBold(self,bold):
        self._isBold = bold
    def isItalic(self,italic):
        self._isItalic = italic
    def setKeyword(self,keyword):
        self._keyword = keyword
# Custom Filters

class UserLang(telebot.custom_filters.SimpleCustomFilter):
    key='user_lang'
    @staticmethod
    def check(message: telebot.types.Message):
        return getLang(message.from_user.id)
class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key='is_admin'
    @staticmethod
    def check(message: telebot.types.Message):
        return message.from_user.id in Admins
bot.add_custom_filter(IsAdmin())
bot.add_custom_filter(UserLang())

# Commands Managment
editCommandProg = {
    
}
delCommandProg = {
    "language":"","commandID":"" 
}
bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("languages", "Get Programming Languages"),
        telebot.types.BotCommand("start", "Change Language"),
        telebot.types.BotCommand("new", "New Command"),
        telebot.types.BotCommand("edit", "Edit Command"),
        telebot.types.BotCommand("python", "Run Python"),
        telebot.types.BotCommand("php", "Run PHP"),
        telebot.types.BotCommand("c", "Run C"),
        telebot.types.BotCommand("cpp", "Run C++"),
        telebot.types.BotCommand("cs", "Run C#"),
        telebot.types.BotCommand("java", "Run Java"),
        telebot.types.BotCommand("html", "HTML Viewer"),
        telebot.types.BotCommand("examples", "See Examples"),
        telebot.types.BotCommand("stackoverflow", "Search In Stackoverflow"),
        telebot.types.BotCommand("cancel", "Cancel Command")
    ],
    # scope=telebot.types.BotCommandScopeChat(12345678)  # use for personal command for users
    # scope=telebot.types.BotCommandScopeAllPrivateChats()  # use for all private chats
)

commands = []
current_path = os.path.abspath(os.getcwd())
# Check If Commands FILE IS EXISTS
if not os.path.exists("commands.json"):
    try:
        chatInfo = bot.get_chat(-765340268)
        fileId = chatInfo.pinned_message.document.file_id
        file_name = chatInfo.pinned_message.document.file_name
        file_info = bot.get_file(fileId)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
    except Exception as e:
        bot.send_message(AdminID,str(e))

def UpdateFile(txtJson=None):
    if txtJson == None:
        f = open("commands.json","rb")
        msg = bot.send_document("-765340268",f)
        bot.pin_chat_message(msg.chat.id,msg.id)
        f.close()
    else:
        toWrite = json.dumps(txtJson)
        f = open("commands.json","w")
        f.write(toWrite)
        f.close()
        UpdateFile()

def delCommand_commandID(message):
    try:
        f = open("commands.json","r")
        txtJson = json.loads(f.read())
        f.close()
        del txtJson["Languages"][delCommandProg["language"]]["commands"][message.text]
        f = open("commands.json","w")
        toWrite = json.dumps(txtJson)
        f.write(toWrite)
        f.close()
        bot.reply_to(message,"Deleted Successfully")
    except:
        bot.reply_to(message,"Unable To Delete This Command")

def delCommand_lan(message):
    f = open("commands.json","r")
    txtJson = json.loads(f.read())
    f.close()
    markup = types.ReplyKeyboardMarkup()
    delCommandProg["language"] = message.text
    for commandID in txtJson["Languages"][message.text]["commands"]:
        markup.add(str(commandID))
    msg = bot.reply_to(message,"Now Choose Command ID To Delete:-",reply_markup=markup)
    bot.register_next_step_handler(msg, delCommand_commandID)

def unescape(html):
    return html.replace("<code>","").replace("</code>","").replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace("&#39;", "'").replace("amp;","")

def temp_def(message):
    f = open("commands.json","r")
    txtJson = json.loads(f.read())
    f.close()
    for language in txtJson["Languages"]:
        for commandID in txtJson["Languages"][language]["commands"]:
            for lang in txtJson["Languages"][language]["commands"][commandID]:
                try:
                    example = txtJson["Languages"][language]["commands"][commandID][lang][1]
                    example = unescape(example)
                    txtJson["Languages"][language]["commands"][commandID][lang][1] = example
                except:
                    continue
    toWrite = json.dumps(txtJson)
    f = open("commands.json","w")
    f.write(toWrite)
    f = open("commands.json","rb")
    bot.send_document(AdminID,f)
    f.close()

def cs_code_run(message):
    code = str(message.text)
    from requests.structures import CaseInsensitiveDict
    code = code.replace("+","w3plussign").replace("=","w3equalsign")
    url = "https://try.w3schools.com/try_cs.php?x=0.853301095038766"
    
    headers = CaseInsensitiveDict()
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; rv:103.0) Gecko/20100101 Firefox/103.0"
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    headers["Accept-Language"] = "en-US,en;q=0.5"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Referer"] = "https://www.w3schools.com/"
    headers["Origin"] = "https://www.w3schools.com"
    headers["Connection"] = "keep-alive"
    headers["Cookie"] = "snconsent=eyJwdWJsaXNoZXIiOjAsInZlbmRvciI6MywiZ2xDb25zZW50cyI6IiIsImN2Q29uc2VudHMiOnt9fQ.AnoAJwArAC4ANwA9AEYAUwBZAF0AbAB1AHoAfACDAIcAiACPAJAAkwCVAJ8AogCnAKsAwADEAMoA0wDaAOQA5gDvAPEBAwEKARABHgEjATcBPQFCAUMBRgFHAVIBbwFzAYEBhQGKAY0BlwGdAZ8BqAGuAbQBuAG9AcEBxQHiAeYB6wHuAe8B9QH3AfkCCgILAhwCJgIvAjACOAI-AkACSAJLAk8C3QLhAukDDAMTAyIDIwMxAzQDNQM9A0cDYANjA2oDgwOIA5oDowOqA9MD1QPZA-sEAAQDBAcECQQKBBAEFgQbBB0EKwQ9BEQERwRJBEsEUwRnBG8EdwR9BIAEigSOBKIEpASxBLUEuwS_BMoEywTOBOQE9AT2BPwFBAUGBQoFFQUbBSAFQQVMBVQFVQVfBXsFhwWIBYsFoAWiBakFrwWwBbkF1wXoBewF9QYEBgwGEwYWBhwGIgYpBisGLwYwBjcGQwZQBmYGcwZ1BoEGgwaNBpIGoQajBqcGsAa0BrkGvQbEBtEG1gblBukG9gb6BwgHEAcSByEHIwcoBy0HLgcwBzIHMwc1B0MHSgdOB1YHWAdhB2sHfQeJB5YHmAeqB6sHrAevB7AHsQe6B9MH1wfYB-sH8wf3B_wH_wgECAgIEAgUCBYIGAgaCCgIKgg3CDsIPQhDCEwIUghVCFkIXAhhCGMIZghsCHYIgQiHCIoImgidCKgIqwisCK4IsQi6CM0I2AjnCOoI9Aj7CQEJBQkICQwJEgkVCRgJGwkeCR8JIAkhCScJMgk1CTYJNwlCCUgJSQlTCVgJWglgCWMJZQlnCWsJbglwCXIJeQmICY8JmwmdCZ4JoQmkCagJrQmxCbQJtgm4CbwJvQnACcEJwgnDCcUJzgnPCdUJ3gnfCeQJ5gnnCe4J8An4CgMKBAoHCggKCQoLCgwKDwoRChcKGAokCikKLAotCjAKMQoyCjQKNgo9CkQKRQpJCkoKTApSClMKVQpWClcKWgpbClwKYAphCmIKZAplCm0Kbgp1CnkKfAp-Cn8KggqHCooKkwqZCpoKqQqzCs8K0ArSCtQK4ArjCucK6AruCvEK9Qr8Cv0LAAsBCwILBQsGCwsLDgsPCxILFAsWCxcLGAscCx4LHwshCyILJAsmCygLLAsuCy8LMQszCzULOQs6CzsLPAs-C0ALQQtCC0MLRAtGC0cLSAtJC0sLTQtOC08LUQtSC1QLVQtcC10LXwtgC2ELYgtkC2ULZgtnC2gLagtrC2wLbwtxC3ILcwt7C3wLfQt-C4MLhQuGC4wLkQuSC5MLlAuVC5YLmAuaC50LngufC6MLpAulC6cLqQuqC6sLrwuyC7MLtQu3C7gLugu7C70LwAvBC8ILxAvIC8kLygvLC9AL0QvUC9oL3QveC-ML5QvoC-wL7QvvC_IL8wv3C_kL-gv8C_4MAAwBDAIMAwwEDAUMBgwRDBIMFQwWDBcMGQwbDCAMIgwlDCgMLAwtDC4MLwwwDDQMNgw3DDgMOgw_DEAMSQxNDE4MTwxSDFMMWgxbDF8MZAxlDGwMbgxvDHAMcQxzDHQMdQx2DHoMfAx9DIkMigyLDI4MjwyRDJMMlgyXDJkMmgybDJwMngyfDKAMogyjDKQMpQymDKgMqQysDK0MsgyzDLUMuQy8DMQMxgzIDNEM2AzaDN0M3wzgDOQM6QzrDOwM8g; euconsent-v2=CPbV7RgPbV7RgDlBEAENCVCsAP_AAH_AACiQI3Nf_X__b3_n-_7___t0eY1f9_7__-0zjhfdt-8N3f_X_L8X_2M7vF36tr4KuR4ku3bBIQdtHOncTUmx6olVrzPsbk2cr7NKJ7Pkmnsbe2dYGH9_n93T_ZKZ7______7________________________-_____9________________________________wRuAJMNW4gC7EscGTaMIoUQIwrCQ6gUAFFAMLRFYQOrgp2VwE-oIWACAVARgRAgxBRgwCAAQCAJCIgJADwQCIAiAQAAgAVAIQAEbAILACwMAgAFANCxAigCECQgyICI5TAgIkSignsrEEoO9jTCEOssAKBR_RUICJQAgWBkJCwcxwBICXCyQLMUL5ACMEKAUAAA; _ga=GA1.2.1519819545.1656513682; __gads=ID=d2608ebe69ec6311-222348e1c1cd0026:T=1656513708:S=ALNI_MYSBd6zUVD7USzVjPI8EeuMmjb65g; cto_bundle=g9Ui3V9uMzVLTmo4TldDJTJGTE1HN0xLNERwQ3NNeEpUV3AwNGhuY0hXN3NTR0RSNUpYJTJCdSUyQk1uMVQ0JTJGRnI3ZGxzWjRGWSUyRlB4QiUyRnBwS0ZWMiUyQmlUek1qR0pnRTViUU5YZ0h4QlYwSHdkJTJCQnZYZzgwZEpBdUNTeHNpSTV0ZXB5YkNscTNjZHI; __gpi=UID=000006c593e7599d:T=1656964584:RT=1659183549:S=ALNI_MZm_s8pD6rMzdczO5LrC5nSZAg6Sg; usprivacy=1YNY; _gid=GA1.2.1203900387.1659183516; _gat=1"
    headers["Upgrade-Insecure-Requests"] = "1"
    headers["Sec-Fetch-Dest"] = "empty"
    headers["Sec-Fetch-Mode"] = "no-cors"
    headers["Sec-Fetch-Site"] = "same-site"
    headers["Sec-Fetch-User"] = "?1"
    headers["TE"] = "trailers"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Pragma"] = "no-cache"
    headers["Cache-Control"] = "no-cache"

    data = "code="+code


    resp = requests.post(url, headers=headers, data=data)
    content = resp.text
    content = content.split("<pre>")[1]
    content = content.split("</pre>")[0]
    bot.reply_to(message,str(content))

def python_code_run(message):
    code = str(message.text)
    from requests.structures import CaseInsensitiveDict
    code = code.replace("+","w3plussign").replace("=","w3equalsign")
    url = "https://try.w3schools.com/try_python.php?x=0.6939115188785611"
    
    headers = CaseInsensitiveDict()
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; rv:103.0) Gecko/20100101 Firefox/103.0"
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    headers["Accept-Language"] = "en-US,en;q=0.5"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Referer"] = "https://www.w3schools.com/"
    headers["Origin"] = "https://www.w3schools.com"
    headers["Connection"] = "keep-alive"
    headers["Cookie"] = "snconsent=eyJwdWJsaXNoZXIiOjAsInZlbmRvciI6MywiZ2xDb25zZW50cyI6IiIsImN2Q29uc2VudHMiOnt9fQ.AnoAJwArAC4ANwA9AEYAUwBZAF0AbAB1AHoAfACDAIcAiACPAJAAkwCVAJ8AogCnAKsAwADEAMoA0wDaAOQA5gDvAPEBAwEKARABHgEjATcBPQFCAUMBRgFHAVIBbwFzAYEBhQGKAY0BlwGdAZ8BqAGuAbQBuAG9AcEBxQHiAeYB6wHuAe8B9QH3AfkCCgILAhwCJgIvAjACOAI-AkACSAJLAk8C3QLhAukDDAMTAyIDIwMxAzQDNQM9A0cDYANjA2oDgwOIA5oDowOqA9MD1QPZA-sEAAQDBAcECQQKBBAEFgQbBB0EKwQ9BEQERwRJBEsEUwRnBG8EdwR9BIAEigSOBKIEpASxBLUEuwS_BMoEywTOBOQE9AT2BPwFBAUGBQoFFQUbBSAFQQVMBVQFVQVfBXsFhwWIBYsFoAWiBakFrwWwBbkF1wXoBewF9QYEBgwGEwYWBhwGIgYpBisGLwYwBjcGQwZQBmYGcwZ1BoEGgwaNBpIGoQajBqcGsAa0BrkGvQbEBtEG1gblBukG9gb6BwgHEAcSByEHIwcoBy0HLgcwBzIHMwc1B0MHSgdOB1YHWAdhB2sHfQeJB5YHmAeqB6sHrAevB7AHsQe6B9MH1wfYB-sH8wf3B_wH_wgECAgIEAgUCBYIGAgaCCgIKgg3CDsIPQhDCEwIUghVCFkIXAhhCGMIZghsCHYIgQiHCIoImgidCKgIqwisCK4IsQi6CM0I2AjnCOoI9Aj7CQEJBQkICQwJEgkVCRgJGwkeCR8JIAkhCScJMgk1CTYJNwlCCUgJSQlTCVgJWglgCWMJZQlnCWsJbglwCXIJeQmICY8JmwmdCZ4JoQmkCagJrQmxCbQJtgm4CbwJvQnACcEJwgnDCcUJzgnPCdUJ3gnfCeQJ5gnnCe4J8An4CgMKBAoHCggKCQoLCgwKDwoRChcKGAokCikKLAotCjAKMQoyCjQKNgo9CkQKRQpJCkoKTApSClMKVQpWClcKWgpbClwKYAphCmIKZAplCm0Kbgp1CnkKfAp-Cn8KggqHCooKkwqZCpoKqQqzCs8K0ArSCtQK4ArjCucK6AruCvEK9Qr8Cv0LAAsBCwILBQsGCwsLDgsPCxILFAsWCxcLGAscCx4LHwshCyILJAsmCygLLAsuCy8LMQszCzULOQs6CzsLPAs-C0ALQQtCC0MLRAtGC0cLSAtJC0sLTQtOC08LUQtSC1QLVQtcC10LXwtgC2ELYgtkC2ULZgtnC2gLagtrC2wLbwtxC3ILcwt7C3wLfQt-C4MLhQuGC4wLkQuSC5MLlAuVC5YLmAuaC50LngufC6MLpAulC6cLqQuqC6sLrwuyC7MLtQu3C7gLugu7C70LwAvBC8ILxAvIC8kLygvLC9AL0QvUC9oL3QveC-ML5QvoC-wL7QvvC_IL8wv3C_kL-gv8C_4MAAwBDAIMAwwEDAUMBgwRDBIMFQwWDBcMGQwbDCAMIgwlDCgMLAwtDC4MLwwwDDQMNgw3DDgMOgw_DEAMSQxNDE4MTwxSDFMMWgxbDF8MZAxlDGwMbgxvDHAMcQxzDHQMdQx2DHoMfAx9DIkMigyLDI4MjwyRDJMMlgyXDJkMmgybDJwMngyfDKAMogyjDKQMpQymDKgMqQysDK0MsgyzDLUMuQy8DMQMxgzIDNEM2AzaDN0M3wzgDOQM6QzrDOwM8g; euconsent-v2=CPbV7RgPbV7RgDlBEAENCVCsAP_AAH_AACiQI3Nf_X__b3_n-_7___t0eY1f9_7__-0zjhfdt-8N3f_X_L8X_2M7vF36tr4KuR4ku3bBIQdtHOncTUmx6olVrzPsbk2cr7NKJ7Pkmnsbe2dYGH9_n93T_ZKZ7______7________________________-_____9________________________________wRuAJMNW4gC7EscGTaMIoUQIwrCQ6gUAFFAMLRFYQOrgp2VwE-oIWACAVARgRAgxBRgwCAAQCAJCIgJADwQCIAiAQAAgAVAIQAEbAILACwMAgAFANCxAigCECQgyICI5TAgIkSignsrEEoO9jTCEOssAKBR_RUICJQAgWBkJCwcxwBICXCyQLMUL5ACMEKAUAAA; _ga=GA1.2.1519819545.1656513682; __gads=ID=d2608ebe69ec6311-222348e1c1cd0026:T=1656513708:S=ALNI_MYSBd6zUVD7USzVjPI8EeuMmjb65g; cto_bundle=g9Ui3V9uMzVLTmo4TldDJTJGTE1HN0xLNERwQ3NNeEpUV3AwNGhuY0hXN3NTR0RSNUpYJTJCdSUyQk1uMVQ0JTJGRnI3ZGxzWjRGWSUyRlB4QiUyRnBwS0ZWMiUyQmlUek1qR0pnRTViUU5YZ0h4QlYwSHdkJTJCQnZYZzgwZEpBdUNTeHNpSTV0ZXB5YkNscTNjZHI; __gpi=UID=000006c593e7599d:T=1656964584:RT=1659183549:S=ALNI_MZm_s8pD6rMzdczO5LrC5nSZAg6Sg; usprivacy=1YNY; _gid=GA1.2.1203900387.1659183516; _gat=1"
    headers["Upgrade-Insecure-Requests"] = "1"
    headers["Sec-Fetch-Dest"] = "empty"
    headers["Sec-Fetch-Mode"] = "no-cors"
    headers["Sec-Fetch-Site"] = "same-site"
    headers["Sec-Fetch-User"] = "?1"
    headers["TE"] = "trailers"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Pragma"] = "no-cache"
    headers["Cache-Control"] = "no-cache"

    data = "code="+code


    resp = requests.post(url, headers=headers, data=data)
    content = resp.text
    content = content.split("<pre>")[1]
    content = content.split("</pre>")[0]
    bot.reply_to(message,str(content))

def getEmptyExamples(message):
    userLang = getLang(str(message.from_user.id))
    result = []
    f = open("commands.json","r")
    txtJson = json.loads(f.read())
    f.close()
    for language in txtJson["Languages"]:
        if str(message.text) == str(language):
            for command in txtJson["Languages"][language]["commands"]:
                try:
                    txtJson["Languages"][language]["commands"][command][userLang]["example"]
                    continue
                except:
                    result.append(str(command))
    return result
def edit_push(message,toEdit):
    
    user_id = message.from_user.id
    content_type = ""
    f = open("commands.json","r")
    txtJson = json.loads(f.read())
    f.close()
    if toEdit == "fileId":
        if message.content_type == "document":
            message.text = message.document.file_id
            content_type = "document"
        elif message.content_type == "photo":
            message.text = message.photo[0].file_id
            content_type = "photo"
        else:
            return bot.reply_to(message,"Not Supported..., File,Documents & images Only ")
    for language in txtJson["Languages"]:
        selectedLanguage = editCommandProg[user_id]["lan"]
        selectedLang = editCommandProg[user_id]["lang"]
        for command in txtJson["Languages"][selectedLanguage]["commands"]:
            if str(command) == editCommandProg[user_id]["id"]:
                if toEdit == "ID":
                    msgTx = message.text
                    enContent = txtJson["Languages"][selectedLanguage]["commands"][command]["en"]
                    arContent = txtJson["Languages"][selectedLanguage]["commands"][command]["ar"]
                    del txtJson["Languages"][selectedLanguage]["commands"][command]
                    txtJson["Languages"][selectedLanguage]["commands"][msgTx] = {"ar":arContent,"en":enContent}
                    break
                else:
                    if user_id != int(AdminID):
                        original = txtJson["Languages"][selectedLanguage]["commands"][command][selectedLang][toEdit]
                        question = "Someone Need To Change "+toEdit+"\nFrom:\n"+original+"\nto:\n"+message.text
                        msg = bot.send_message("-1001604626385",question)
                        bot.send_poll("-1001604626385","is that's right ?\n id : #"+str(msg.id),["yes","no"],reply_to_message_id=msg.id)
                        return
                    if toEdit == "fileId":
                        txtJson["Languages"][selectedLanguage]["commands"][command][selectedLang]['type'] = content_type
                    if toEdit == "password":
                        the_user_id =txtJson["Languages"][selectedLanguage]["commands"][command][selectedLang]["from_user_id"]
                        if the_user_id == message.from_user.id:
                            something=1
                        else:
                            return bot.reply_to(message,"Sorry But You Don't Have Permission")
                    txtJson["Languages"][selectedLanguage]["commands"][command][selectedLang][toEdit] = message.text
    f = open("commands.json","w")
    toWrite = json.dumps(txtJson)
    f.write(toWrite)
    f.close()
    bot.reply_to(message,"Edited Successfully")


def edit_lan_commit(message):
    msgTx = message.text
    toEdit = ""
    toEdit2 = ""
    if msgTx == "User Input":
        msg = bot.reply_to(message,"Enter New User Input :-")
        bot.register_next_step_handler(msg, edit_push,"input")
    elif msgTx == "Example":
        f = open("commands.json","r")
        txtJson = json.loads(f.read())
        f.close()
        selectedLan = editCommandProg[message.from_user.id]["lan"]
        selectedLang = editCommandProg[message.from_user.id]["lang"]
        commandID = editCommandProg[message.from_user.id]["id"]
        old_example = txtJson["Languages"][selectedLan]["commands"][commandID][selectedLang]["example"]
        try:
            bot.send_message(message.chat.id,old_example)
        except:
            bot.reply_to(message,"Example is Empty")
        msg = bot.reply_to(message,"Enter New Example :-")
        bot.register_next_step_handler(msg, edit_push,"example")
    elif msgTx == "ID":
        msg = bot.reply_to(message,"Enter New ID :-")
        bot.register_next_step_handler(msg, edit_push,"ID")
    elif msgTx == "Attached File":
        msg = bot.reply_to(message,"Send New File :-")
        bot.register_next_step_handler(msg, edit_push,"fileId")
    elif msgTx == "File Password":
        msg = bot.reply_to(message,"Enter New Password")
        bot.register_next_step_handler(msg, edit_push,"password")
    
def edit_lan_what(message):
    msgTx = message.text
    msgTx = msgTx.replace(" ","_")
    isExists = checkIfExist(editCommandProg[message.from_user.id]["lan"],msgTx,editCommandProg[message.from_user.id]["lang"])
    if isExists:
        editCommandProg[message.from_user.id]["id"] = msgTx
        markup = types.ReplyKeyboardMarkup(row_width=2)
        userinput = types.KeyboardButton('User Input')
        Example = types.KeyboardButton('Example')
        CommandID = types.KeyboardButton('ID')
        file_id = types.KeyboardButton('Attached File')
        file_pass = types.KeyboardButton('File Password')
        markup.add(userinput, Example, CommandID,file_id,file_pass)
        msg = bot.reply_to(message,"Choose What To Edit :-",reply_markup=markup)
        bot.register_next_step_handler(msg, edit_lan_commit)

def edit_lan_lang(message):
    msgTx = message.text
    f = open("commands.json","r")
    txtJson = json.loads(f.read())
    f.close()
    markup = types.ReplyKeyboardMarkup()
    if msgTx == "ar" or msgTx == "en":
        for commandID in txtJson["Languages"][editCommandProg[message.from_user.id]["lan"]]["commands"]:
            if txtJson["Languages"][editCommandProg[message.from_user.id]["lan"]]["commands"][commandID][msgTx]["input"] != "":
                markup.add(str(commandID))
        editCommandProg[message.from_user.id]["lang"] = msgTx
        msg = bot.reply_to(message,"Now Enter Command ID:-",reply_markup=markup)
        bot.register_next_step_handler(msg, edit_lan_what)
    else:
        bot.reply_to(message,"Unsupported Language")

def edit_lan_step(message):
    f = open("commands.json","r")
    txtJson = json.loads(f.read())
    f.close()
    txtJson["Languages"][message.text]
    
    editCommandProg[message.from_user.id]["lan"] = message.text
    msg = bot.reply_to(message,"Enter Example Language :-")
    bot.register_next_step_handler(msg, edit_lan_lang)

def checkPLangage(PLanguage):
    if os.path.exists("commands.json"):
        f = open("commands.json","r")
        txtJson = json.loads(f.read())
        f.close()
        for language in txtJson["Languages"]:
            if str(language) == PLanguage:
                return True
        return False
    else:
        return False

def checkIfExistUserInput(lang,u_input):
    f = open("commands.json","r")
    txt = f.read()
    txtJson = json.loads(txt)
    f.close()
    for language in txtJson["Languages"]:
        for command in txtJson["Languages"][language]["commands"]:
            for TAE in txtJson["Languages"][language]["commands"][command][lang]:
                try:
                    commandTitle = txtJson["Languages"][language]["commands"][command][lang]["input"]
                    if str(commandTitle) == u_input:
                        return True
                except:
                    continue
    return False

def checkIfExist(lan,commandID,lang="none"):
    f = open("commands.json","r")
    txt = f.read()
    txtJson = json.loads(txt)
    f.close()
    for language in txtJson["Languages"]:
        if lan == str(language):
            for command in txtJson["Languages"][language]["commands"]:
                
                if str(command) == commandID:
                    if lang != "none":
                        try:
                            txtJson["Languages"][language]["commands"][command][lang]["input"]
                            return True
                        except:
                            return False
                    else:
                        return True
    return False
def new_command_password_step(message,documentType):
    userid = message.from_user.id
    the_password = message.text
    if message.text == "/none":
        if userid == 1625235944:
            AddNewCommand(message,newCommandProg[userid]["lan"],newCommandProg[userid]["id"],newCommandProg[userid]["input"],newCommandProg[userid]["example"],newCommandProg[userid]["file_id"],newCommandProg[userid]["lang"],documentType)
        else:
            AddNewCommandUser(message,newCommandProg[userid]["lan"],newCommandProg[userid]["id"],newCommandProg[userid]["input"],newCommandProg[userid]["example"],newCommandProg[userid]["file_id"],newCommandProg[userid]["lang"],documentType)
    else:
        if userid == 1625235944:
            AddNewCommand(message,newCommandProg[userid]["lan"],newCommandProg[userid]["id"],newCommandProg[userid]["input"],newCommandProg[userid]["example"],newCommandProg[userid]["file_id"],newCommandProg[userid]["lang"],documentType,the_password)
        else:
            AddNewCommandUser(message,newCommandProg[userid]["lan"],newCommandProg[userid]["id"],newCommandProg[userid]["input"],newCommandProg[userid]["example"],newCommandProg[userid]["file_id"],newCommandProg[userid]["lang"],documentType,the_password)
def file_attch_step(message):
    documentType = message.content_type
    if str(message.content_type) != "text":
        if message.content_type == "photo":
            newCommandProg[message.from_user.id]["file_id"] = message.photo[0].file_id
        elif message.content_type == "document":
            newCommandProg[message.from_user.id]["file_id"] = message.document.file_id
        else:
            return bot.reply_to(message,"Not Supported File ,document and Image Allowed !\n"+str(e))
    else:
        newCommandProg[message.from_user.id]["file_id"] = ""
    userid = message.from_user.id
    try:
        f = open("commands.json",'r')
        txtJson = json.loads(f.read())
        f.close()
        lan = newCommandProg[message.from_user.id]["lan"]
        txtJson["Languages"][lan]["passwords"]
        msg = bot.reply_to(message,"Enter Password Or /none:")
        bot.register_next_step_handler(msg,new_command_password_step,documentType)
    except:
        if userid == 1625235944:
            AddNewCommand(message,newCommandProg[userid]["lan"],newCommandProg[userid]["id"],newCommandProg[userid]["input"],newCommandProg[userid]["example"],newCommandProg[userid]["file_id"],newCommandProg[userid]["lang"],documentType)
        else:
            AddNewCommandUser(message,newCommandProg[userid]["lan"],newCommandProg[userid]["id"],newCommandProg[userid]["input"],newCommandProg[userid]["example"],newCommandProg[userid]["file_id"],newCommandProg[userid]["lang"],documentType)

def example_step(message):
    if str(message.text) == "/cancel":
        return bot.reply_to(message,"Command Cancelled !")
    msgTx = str(message.text)
    newCommandProg[message.from_user.id]["example"] = msgTx
    userLang = getLang(str(message.from_user.id))
    if userLang == "en":
        msg = bot.reply_to(message,"Send Any File If You Want As Attachment or send anything to Ignore")
        bot.register_next_step_handler(msg, file_attch_step)
    else:
        msg = bot.reply_to(message,"قم بأرسال اي ملف اذا كنت تريد وضعه مع المثال او ارسل اي شئ للتجاهل")
        bot.register_next_step_handler(msg, file_attch_step)
    
def lang_step2(message): 
    if str(message.text) == "/cancel":
        return bot.reply_to(message,"Command Cancelled !")
    newCommandProg[message.from_user.id]["input"] = str(message.text)
    answer = newCommandProg[message.from_user.id]["lang"]
    
    if answer == "ar":
        isExists = checkIfExistUserInput("ar",newCommandProg[message.from_user.id]["input"])
        if isExists:
            return bot.reply_to(message,"هذا  الأمر موجود مسبقا")
    elif answer == "en":
        isExists = checkIfExistUserInput("en",newCommandProg[message.from_user.id]["input"])
        if isExists:
            return bot.reply_to(message,"This Example Allready Exists")
    else:
        return bot.reply_to(message,"not valid\nAvailable Language\nar\nen")
    userLang = getLang(str(message.from_user.id))
    if userLang == "en":
        msg = bot.reply_to(message,"Now Enter The Example")
        bot.register_next_step_handler(msg, example_step)
    else:
        msg = bot.reply_to(message,"الان قم بكتابة المثال")
        bot.register_next_step_handler(msg, example_step)
    command_id_step(message)
def command_id_step(message):
    if str(message.text) == "/cancel":
        return bot.reply_to(message,"Command Cancelled !")
    userLang = getLang(str(message.from_user.id))
    msgTx = str(message.text)
    newCommandProg[message.from_user.id]['input'] = msgTx
    msgTx = msgTx.replace(" ","_")
    newCommandProg[message.from_user.id]["lang"] = userLang
    isExists = checkIfExist(newCommandProg[message.from_user.id]["lan"],msgTx,userLang)
    if isExists:
        return bot.reply_to(message,"Command Allready Exists")
    newCommandProg[message.from_user.id]["id"] = msgTx
    if userLang == "en":
        msg = bot.reply_to(message,"Enter Example")
        bot.register_next_step_handler(msg, example_step)
    else:
        msg = bot.reply_to(message,"قم الان بكتابة المثال تأكد من ان الكود صحيح")
        bot.register_next_step_handler(msg, example_step)

def lan_step(message):
    if str(message.text) == "/cancel":
        return bot.reply_to(message,"Command Cancelled !")
    userLang = getLang(str(message.from_user.id))
    msgTx = str(message.text)
    msgTx = msgTx.replace(" ","")
    msgTx = msgTx.lower()
    isValid = checkPLangage(msgTx)
    if not isValid:
        if userLang == "en":
            return bot.reply_to(message,"Invalid Programming Language")
        else:
            return bot.reply_to(message,"لغة برمجة غير صالحة")
    newCommandProg[message.from_user.id]["lan"] = msgTx
    markup = types.ReplyKeyboardMarkup()
    emptyExamples = getEmptyExamples(message)
    for x in emptyExamples:
        markup.add(str(x))
    if userLang == "en":
        msg = bot.reply_to(message,"Enter Input",reply_markup=markup)
        bot.register_next_step_handler(msg, command_id_step)
    else:
        msg = bot.reply_to(message,"قم بأدخال ما سيدخله المستخدم ليحصل علي المثال",reply_markup=markup)
        bot.register_next_step_handler(msg, command_id_step)

def getAllCommands(lang):
    f = open("commands.json","r")
    txt = str(f.read())
    f.close()
    txtJson = json.loads(txt)
    AllCommands = ""
    for language in txtJson["Languages"]:
        for command in txtJson["Languages"][language]["commands"]:
            theCommand = txtJson["Languages"][language]["commands"][command][lang]["0"]
            AllCommands += str(theCommand) + " #"+str(language)+"\n"
    return AllCommands

def UserLang(id,lang):
    f = open("users.json","r")
    txt = f.read()
    txtJson = json.loads(txt)
    f.close()
    for x in range(len(txtJson["users"])):
        if txtJson["users"][x]["id"] == id:
            txtJson["users"][x]["lang"] = lang
            break
    f = open("users.json","w")
    toWrite = json.dumps(txtJson)
    f.write(toWrite)
    f.close()
    if lang == "ar":
        bot.send_message(id,"تم تحديث اللغة الان قم بأرسال \n/languages")
    if lang == "en":
        bot.send_message(id,"Language Updated ! Now Send\n/languages")

def lang_step(message): 
    answer = str(message.text)
    if answer == "العربية":
        UserLang(message.from_user.id,"ar")
        f = open("commands.json","r")
        txtJson = json.loads(f.read())
        f.close()
        markup = types.ReplyKeyboardMarkup(row_width=2)
        for language in txtJson["Languages"]:
            markup.add("عرض اوامر "+str(language))
            
        bot.reply_to(message,"Available Languages:-",reply_markup=markup)
    if answer == "English":
        UserLang(message.from_user.id,"en")
        f = open("commands.json","r")
        txtJson = json.loads(f.read())
        f.close()
        markup = types.ReplyKeyboardMarkup(row_width=2)
        for language in txtJson["Languages"]:
            markup.add("-» "+str(language))
            
        bot.reply_to(message,"Available Languages:-",reply_markup=markup)

def addUser (from_user):
    f = open("usersPost.json","r")
    txtJson = json.loads(f.read())
    f.close()
    isFounded = False
    for userid in txtJson["users"]:
        if userid == from_user.id:
            True
            break
    if not isFounded:
        txtJson["users"][from_user.id] = {"Pending":[],"Published":[]}
        f = open("usersPost.json","w")
        toWrite = json.dumps(txtJson)
        f.write(toWrite)
        f.close()
    try:
        isFounded = False
        f = open("users.json","r")
        txt = str(f.read())
        txtJson = json.loads(txt)
        f.close()
        for x in range(len(txtJson["users"])):
            uid = str(txtJson["users"][x]["id"])
            if uid == str(from_user.id):
                return "Founded"
        fullname = str(from_user.first_name)+" "+str(from_user.last_name)
        txtJson["users"].append({"id":from_user.id,"name":fullname,"user":"@"+from_user.username,"lang":"en"})
        f = open("users.json","w")
        toWrite = json.dumps(txtJson)
        f.write(toWrite)
        f.close()
    except:
        txtJson ={
            "users":[
                
            ]
        }
        fullname = str(from_user.first_name)+" "+str(from_user.last_name)
        txtJson["users"].append({"id":from_user.id,"name":fullname,"user":"@"+str(from_user.username),"lang":"en"})
        f = open("users.json","w")
        toWrite = json.dumps(txtJson)
        f.write(toWrite)
        f.close()
        return "new User : "+str(from_user.id)
def code_run(message,lan=""):
    if lan == "python":
        python_code_run(message)
    if lan == "php":
        php_code_run(message)
    if lan == "c":
        c_code_run(message)
    if lan == "cpp":
        cpp_code_run(message)
    if lan == "java":
        php_code_run(message)
    if lan == "html":
        php_code_run(message)
def code_run_output(message,content):
    content = unescape(content)
    content = "#Output :\n"+content
    bot.reply_to(message,content)
def python_code_run(message):
    code = str(message.text)
    from requests.structures import CaseInsensitiveDict
    code = code.replace("+","w3plussign").replace("=","w3equalsign")
    url = "https://try.w3schools.com/try_python.php?x=0.6939115188785611"
    
    headers = CaseInsensitiveDict()
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; rv:103.0) Gecko/20100101 Firefox/103.0"
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    headers["Accept-Language"] = "en-US,en;q=0.5"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Referer"] = "https://www.w3schools.com/"
    headers["Origin"] = "https://www.w3schools.com"
    headers["Connection"] = "keep-alive"
    headers["Cookie"] = "snconsent=eyJwdWJsaXNoZXIiOjAsInZlbmRvciI6MywiZ2xDb25zZW50cyI6IiIsImN2Q29uc2VudHMiOnt9fQ.AnoAJwArAC4ANwA9AEYAUwBZAF0AbAB1AHoAfACDAIcAiACPAJAAkwCVAJ8AogCnAKsAwADEAMoA0wDaAOQA5gDvAPEBAwEKARABHgEjATcBPQFCAUMBRgFHAVIBbwFzAYEBhQGKAY0BlwGdAZ8BqAGuAbQBuAG9AcEBxQHiAeYB6wHuAe8B9QH3AfkCCgILAhwCJgIvAjACOAI-AkACSAJLAk8C3QLhAukDDAMTAyIDIwMxAzQDNQM9A0cDYANjA2oDgwOIA5oDowOqA9MD1QPZA-sEAAQDBAcECQQKBBAEFgQbBB0EKwQ9BEQERwRJBEsEUwRnBG8EdwR9BIAEigSOBKIEpASxBLUEuwS_BMoEywTOBOQE9AT2BPwFBAUGBQoFFQUbBSAFQQVMBVQFVQVfBXsFhwWIBYsFoAWiBakFrwWwBbkF1wXoBewF9QYEBgwGEwYWBhwGIgYpBisGLwYwBjcGQwZQBmYGcwZ1BoEGgwaNBpIGoQajBqcGsAa0BrkGvQbEBtEG1gblBukG9gb6BwgHEAcSByEHIwcoBy0HLgcwBzIHMwc1B0MHSgdOB1YHWAdhB2sHfQeJB5YHmAeqB6sHrAevB7AHsQe6B9MH1wfYB-sH8wf3B_wH_wgECAgIEAgUCBYIGAgaCCgIKgg3CDsIPQhDCEwIUghVCFkIXAhhCGMIZghsCHYIgQiHCIoImgidCKgIqwisCK4IsQi6CM0I2AjnCOoI9Aj7CQEJBQkICQwJEgkVCRgJGwkeCR8JIAkhCScJMgk1CTYJNwlCCUgJSQlTCVgJWglgCWMJZQlnCWsJbglwCXIJeQmICY8JmwmdCZ4JoQmkCagJrQmxCbQJtgm4CbwJvQnACcEJwgnDCcUJzgnPCdUJ3gnfCeQJ5gnnCe4J8An4CgMKBAoHCggKCQoLCgwKDwoRChcKGAokCikKLAotCjAKMQoyCjQKNgo9CkQKRQpJCkoKTApSClMKVQpWClcKWgpbClwKYAphCmIKZAplCm0Kbgp1CnkKfAp-Cn8KggqHCooKkwqZCpoKqQqzCs8K0ArSCtQK4ArjCucK6AruCvEK9Qr8Cv0LAAsBCwILBQsGCwsLDgsPCxILFAsWCxcLGAscCx4LHwshCyILJAsmCygLLAsuCy8LMQszCzULOQs6CzsLPAs-C0ALQQtCC0MLRAtGC0cLSAtJC0sLTQtOC08LUQtSC1QLVQtcC10LXwtgC2ELYgtkC2ULZgtnC2gLagtrC2wLbwtxC3ILcwt7C3wLfQt-C4MLhQuGC4wLkQuSC5MLlAuVC5YLmAuaC50LngufC6MLpAulC6cLqQuqC6sLrwuyC7MLtQu3C7gLugu7C70LwAvBC8ILxAvIC8kLygvLC9AL0QvUC9oL3QveC-ML5QvoC-wL7QvvC_IL8wv3C_kL-gv8C_4MAAwBDAIMAwwEDAUMBgwRDBIMFQwWDBcMGQwbDCAMIgwlDCgMLAwtDC4MLwwwDDQMNgw3DDgMOgw_DEAMSQxNDE4MTwxSDFMMWgxbDF8MZAxlDGwMbgxvDHAMcQxzDHQMdQx2DHoMfAx9DIkMigyLDI4MjwyRDJMMlgyXDJkMmgybDJwMngyfDKAMogyjDKQMpQymDKgMqQysDK0MsgyzDLUMuQy8DMQMxgzIDNEM2AzaDN0M3wzgDOQM6QzrDOwM8g; euconsent-v2=CPbV7RgPbV7RgDlBEAENCVCsAP_AAH_AACiQI3Nf_X__b3_n-_7___t0eY1f9_7__-0zjhfdt-8N3f_X_L8X_2M7vF36tr4KuR4ku3bBIQdtHOncTUmx6olVrzPsbk2cr7NKJ7Pkmnsbe2dYGH9_n93T_ZKZ7______7________________________-_____9________________________________wRuAJMNW4gC7EscGTaMIoUQIwrCQ6gUAFFAMLRFYQOrgp2VwE-oIWACAVARgRAgxBRgwCAAQCAJCIgJADwQCIAiAQAAgAVAIQAEbAILACwMAgAFANCxAigCECQgyICI5TAgIkSignsrEEoO9jTCEOssAKBR_RUICJQAgWBkJCwcxwBICXCyQLMUL5ACMEKAUAAA; _ga=GA1.2.1519819545.1656513682; __gads=ID=d2608ebe69ec6311-222348e1c1cd0026:T=1656513708:S=ALNI_MYSBd6zUVD7USzVjPI8EeuMmjb65g; cto_bundle=g9Ui3V9uMzVLTmo4TldDJTJGTE1HN0xLNERwQ3NNeEpUV3AwNGhuY0hXN3NTR0RSNUpYJTJCdSUyQk1uMVQ0JTJGRnI3ZGxzWjRGWSUyRlB4QiUyRnBwS0ZWMiUyQmlUek1qR0pnRTViUU5YZ0h4QlYwSHdkJTJCQnZYZzgwZEpBdUNTeHNpSTV0ZXB5YkNscTNjZHI; __gpi=UID=000006c593e7599d:T=1656964584:RT=1659183549:S=ALNI_MZm_s8pD6rMzdczO5LrC5nSZAg6Sg; usprivacy=1YNY; _gid=GA1.2.1203900387.1659183516; _gat=1"
    headers["Upgrade-Insecure-Requests"] = "1"
    headers["Sec-Fetch-Dest"] = "empty"
    headers["Sec-Fetch-Mode"] = "no-cors"
    headers["Sec-Fetch-Site"] = "same-site"
    headers["Sec-Fetch-User"] = "?1"
    headers["TE"] = "trailers"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Pragma"] = "no-cache"
    headers["Cache-Control"] = "no-cache"

    data = "code="+code
    
    resp = requests.post(url, headers=headers, data=data)
    content = resp.text
    content = content.split("<pre>")[1]
    content = content.split("</pre>")[0]
    code_run_output(message,content)

def c_code_run(message):
    code = str(message.text)
    from requests.structures import CaseInsensitiveDict
    code = code.replace("+","w3plussign").replace("=","w3equalsign")
    url = "https://try.w3schools.com/try_c.php?x=0.6922869137942772"
    
    headers = CaseInsensitiveDict()
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; rv:103.0) Gecko/20100101 Firefox/103.0"
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    headers["Accept-Language"] = "en-US,en;q=0.5"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Referer"] = "https://www.w3schools.com/"
    headers["Origin"] = "https://www.w3schools.com"
    headers["Connection"] = "keep-alive"
    headers["Cookie"] = "snconsent=eyJwdWJsaXNoZXIiOjAsInZlbmRvciI6MywiZ2xDb25zZW50cyI6IiIsImN2Q29uc2VudHMiOnt9fQ.AnoAJwArAC4ANwA9AEYAUwBZAF0AbAB1AHoAfACDAIcAiACPAJAAkwCVAJ8AogCnAKsAwADEAMoA0wDaAOQA5gDvAPEBAwEKARABHgEjATcBPQFCAUMBRgFHAVIBbwFzAYEBhQGKAY0BlwGdAZ8BqAGuAbQBuAG9AcEBxQHiAeYB6wHuAe8B9QH3AfkCCgILAhwCJgIvAjACOAI-AkACSAJLAk8C3QLhAukDDAMTAyIDIwMxAzQDNQM9A0cDYANjA2oDgwOIA5oDowOqA9MD1QPZA-sEAAQDBAcECQQKBBAEFgQbBB0EKwQ9BEQERwRJBEsEUwRnBG8EdwR9BIAEigSOBKIEpASxBLUEuwS_BMoEywTOBOQE9AT2BPwFBAUGBQoFFQUbBSAFQQVMBVQFVQVfBXsFhwWIBYsFoAWiBakFrwWwBbkF1wXoBewF9QYEBgwGEwYWBhwGIgYpBisGLwYwBjcGQwZQBmYGcwZ1BoEGgwaNBpIGoQajBqcGsAa0BrkGvQbEBtEG1gblBukG9gb6BwgHEAcSByEHIwcoBy0HLgcwBzIHMwc1B0MHSgdOB1YHWAdhB2sHfQeJB5YHmAeqB6sHrAevB7AHsQe6B9MH1wfYB-sH8wf3B_wH_wgECAgIEAgUCBYIGAgaCCgIKgg3CDsIPQhDCEwIUghVCFkIXAhhCGMIZghsCHYIgQiHCIoImgidCKgIqwisCK4IsQi6CM0I2AjnCOoI9Aj7CQEJBQkICQwJEgkVCRgJGwkeCR8JIAkhCScJMgk1CTYJNwlCCUgJSQlTCVgJWglgCWMJZQlnCWsJbglwCXIJeQmICY8JmwmdCZ4JoQmkCagJrQmxCbQJtgm4CbwJvQnACcEJwgnDCcUJzgnPCdUJ3gnfCeQJ5gnnCe4J8An4CgMKBAoHCggKCQoLCgwKDwoRChcKGAokCikKLAotCjAKMQoyCjQKNgo9CkQKRQpJCkoKTApSClMKVQpWClcKWgpbClwKYAphCmIKZAplCm0Kbgp1CnkKfAp-Cn8KggqHCooKkwqZCpoKqQqzCs8K0ArSCtQK4ArjCucK6AruCvEK9Qr8Cv0LAAsBCwILBQsGCwsLDgsPCxILFAsWCxcLGAscCx4LHwshCyILJAsmCygLLAsuCy8LMQszCzULOQs6CzsLPAs-C0ALQQtCC0MLRAtGC0cLSAtJC0sLTQtOC08LUQtSC1QLVQtcC10LXwtgC2ELYgtkC2ULZgtnC2gLagtrC2wLbwtxC3ILcwt7C3wLfQt-C4MLhQuGC4wLkQuSC5MLlAuVC5YLmAuaC50LngufC6MLpAulC6cLqQuqC6sLrwuyC7MLtQu3C7gLugu7C70LwAvBC8ILxAvIC8kLygvLC9AL0QvUC9oL3QveC-ML5QvoC-wL7QvvC_IL8wv3C_kL-gv8C_4MAAwBDAIMAwwEDAUMBgwRDBIMFQwWDBcMGQwbDCAMIgwlDCgMLAwtDC4MLwwwDDQMNgw3DDgMOgw_DEAMSQxNDE4MTwxSDFMMWgxbDF8MZAxlDGwMbgxvDHAMcQxzDHQMdQx2DHoMfAx9DIkMigyLDI4MjwyRDJMMlgyXDJkMmgybDJwMngyfDKAMogyjDKQMpQymDKgMqQysDK0MsgyzDLUMuQy8DMQMxgzIDNEM2AzaDN0M3wzgDOQM6QzrDOwM8g; euconsent-v2=CPbV7RgPbV7RgDlBEAENCVCsAP_AAH_AACiQI3Nf_X__b3_n-_7___t0eY1f9_7__-0zjhfdt-8N3f_X_L8X_2M7vF36tr4KuR4ku3bBIQdtHOncTUmx6olVrzPsbk2cr7NKJ7Pkmnsbe2dYGH9_n93T_ZKZ7______7________________________-_____9________________________________wRuAJMNW4gC7EscGTaMIoUQIwrCQ6gUAFFAMLRFYQOrgp2VwE-oIWACAVARgRAgxBRgwCAAQCAJCIgJADwQCIAiAQAAgAVAIQAEbAILACwMAgAFANCxAigCECQgyICI5TAgIkSignsrEEoO9jTCEOssAKBR_RUICJQAgWBkJCwcxwBICXCyQLMUL5ACMEKAUAAA; _ga=GA1.2.1519819545.1656513682; __gads=ID=d2608ebe69ec6311-222348e1c1cd0026:T=1656513708:S=ALNI_MYSBd6zUVD7USzVjPI8EeuMmjb65g; cto_bundle=g9Ui3V9uMzVLTmo4TldDJTJGTE1HN0xLNERwQ3NNeEpUV3AwNGhuY0hXN3NTR0RSNUpYJTJCdSUyQk1uMVQ0JTJGRnI3ZGxzWjRGWSUyRlB4QiUyRnBwS0ZWMiUyQmlUek1qR0pnRTViUU5YZ0h4QlYwSHdkJTJCQnZYZzgwZEpBdUNTeHNpSTV0ZXB5YkNscTNjZHI; __gpi=UID=000006c593e7599d:T=1656964584:RT=1659183549:S=ALNI_MZm_s8pD6rMzdczO5LrC5nSZAg6Sg; usprivacy=1YNY; _gid=GA1.2.1203900387.1659183516; _gat=1"
    headers["Upgrade-Insecure-Requests"] = "1"
    headers["Sec-Fetch-Dest"] = "empty"
    headers["Sec-Fetch-Mode"] = "no-cors"
    headers["Sec-Fetch-Site"] = "same-site"
    headers["Sec-Fetch-User"] = "?1"
    headers["TE"] = "trailers"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Pragma"] = "no-cache"
    headers["Cache-Control"] = "no-cache"

    data = "code="+code


    resp = requests.post(url, headers=headers, data=data)
    content = resp.text
    content = content.split("<pre>")[1]
    content = content.split("</pre>")[0]
    code_run_output(message,content)

def php_code_run(message):
    code = str(message.text)
    from requests.structures import CaseInsensitiveDict
    code = code.replace("+","w3plussign").replace("=","w3equalsign")
    url = "https://try.w3schools.com/try_php.php?x=0.045285286835581307"
    
    headers = CaseInsensitiveDict()
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; rv:103.0) Gecko/20100101 Firefox/103.0"
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    headers["Accept-Language"] = "en-US,en;q=0.5"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Referer"] = "https://www.w3schools.com/"
    headers["Origin"] = "https://www.w3schools.com"
    headers["Connection"] = "keep-alive"
    headers["Cookie"] = "snconsent=eyJwdWJsaXNoZXIiOjAsInZlbmRvciI6MywiZ2xDb25zZW50cyI6IiIsImN2Q29uc2VudHMiOnt9fQ.AnoAJwArAC4ANwA9AEYAUwBZAF0AbAB1AHoAfACDAIcAiACPAJAAkwCVAJ8AogCnAKsAwADEAMoA0wDaAOQA5gDvAPEBAwEKARABHgEjATcBPQFCAUMBRgFHAVIBbwFzAYEBhQGKAY0BlwGdAZ8BqAGuAbQBuAG9AcEBxQHiAeYB6wHuAe8B9QH3AfkCCgILAhwCJgIvAjACOAI-AkACSAJLAk8C3QLhAukDDAMTAyIDIwMxAzQDNQM9A0cDYANjA2oDgwOIA5oDowOqA9MD1QPZA-sEAAQDBAcECQQKBBAEFgQbBB0EKwQ9BEQERwRJBEsEUwRnBG8EdwR9BIAEigSOBKIEpASxBLUEuwS_BMoEywTOBOQE9AT2BPwFBAUGBQoFFQUbBSAFQQVMBVQFVQVfBXsFhwWIBYsFoAWiBakFrwWwBbkF1wXoBewF9QYEBgwGEwYWBhwGIgYpBisGLwYwBjcGQwZQBmYGcwZ1BoEGgwaNBpIGoQajBqcGsAa0BrkGvQbEBtEG1gblBukG9gb6BwgHEAcSByEHIwcoBy0HLgcwBzIHMwc1B0MHSgdOB1YHWAdhB2sHfQeJB5YHmAeqB6sHrAevB7AHsQe6B9MH1wfYB-sH8wf3B_wH_wgECAgIEAgUCBYIGAgaCCgIKgg3CDsIPQhDCEwIUghVCFkIXAhhCGMIZghsCHYIgQiHCIoImgidCKgIqwisCK4IsQi6CM0I2AjnCOoI9Aj7CQEJBQkICQwJEgkVCRgJGwkeCR8JIAkhCScJMgk1CTYJNwlCCUgJSQlTCVgJWglgCWMJZQlnCWsJbglwCXIJeQmICY8JmwmdCZ4JoQmkCagJrQmxCbQJtgm4CbwJvQnACcEJwgnDCcUJzgnPCdUJ3gnfCeQJ5gnnCe4J8An4CgMKBAoHCggKCQoLCgwKDwoRChcKGAokCikKLAotCjAKMQoyCjQKNgo9CkQKRQpJCkoKTApSClMKVQpWClcKWgpbClwKYAphCmIKZAplCm0Kbgp1CnkKfAp-Cn8KggqHCooKkwqZCpoKqQqzCs8K0ArSCtQK4ArjCucK6AruCvEK9Qr8Cv0LAAsBCwILBQsGCwsLDgsPCxILFAsWCxcLGAscCx4LHwshCyILJAsmCygLLAsuCy8LMQszCzULOQs6CzsLPAs-C0ALQQtCC0MLRAtGC0cLSAtJC0sLTQtOC08LUQtSC1QLVQtcC10LXwtgC2ELYgtkC2ULZgtnC2gLagtrC2wLbwtxC3ILcwt7C3wLfQt-C4MLhQuGC4wLkQuSC5MLlAuVC5YLmAuaC50LngufC6MLpAulC6cLqQuqC6sLrwuyC7MLtQu3C7gLugu7C70LwAvBC8ILxAvIC8kLygvLC9AL0QvUC9oL3QveC-ML5QvoC-wL7QvvC_IL8wv3C_kL-gv8C_4MAAwBDAIMAwwEDAUMBgwRDBIMFQwWDBcMGQwbDCAMIgwlDCgMLAwtDC4MLwwwDDQMNgw3DDgMOgw_DEAMSQxNDE4MTwxSDFMMWgxbDF8MZAxlDGwMbgxvDHAMcQxzDHQMdQx2DHoMfAx9DIkMigyLDI4MjwyRDJMMlgyXDJkMmgybDJwMngyfDKAMogyjDKQMpQymDKgMqQysDK0MsgyzDLUMuQy8DMQMxgzIDNEM2AzaDN0M3wzgDOQM6QzrDOwM8g; euconsent-v2=CPbV7RgPbV7RgDlBEAENCVCsAP_AAH_AACiQI3Nf_X__b3_n-_7___t0eY1f9_7__-0zjhfdt-8N3f_X_L8X_2M7vF36tr4KuR4ku3bBIQdtHOncTUmx6olVrzPsbk2cr7NKJ7Pkmnsbe2dYGH9_n93T_ZKZ7______7________________________-_____9________________________________wRuAJMNW4gC7EscGTaMIoUQIwrCQ6gUAFFAMLRFYQOrgp2VwE-oIWACAVARgRAgxBRgwCAAQCAJCIgJADwQCIAiAQAAgAVAIQAEbAILACwMAgAFANCxAigCECQgyICI5TAgIkSignsrEEoO9jTCEOssAKBR_RUICJQAgWBkJCwcxwBICXCyQLMUL5ACMEKAUAAA; _ga=GA1.2.1519819545.1656513682; __gads=ID=d2608ebe69ec6311-222348e1c1cd0026:T=1656513708:S=ALNI_MYSBd6zUVD7USzVjPI8EeuMmjb65g; cto_bundle=g9Ui3V9uMzVLTmo4TldDJTJGTE1HN0xLNERwQ3NNeEpUV3AwNGhuY0hXN3NTR0RSNUpYJTJCdSUyQk1uMVQ0JTJGRnI3ZGxzWjRGWSUyRlB4QiUyRnBwS0ZWMiUyQmlUek1qR0pnRTViUU5YZ0h4QlYwSHdkJTJCQnZYZzgwZEpBdUNTeHNpSTV0ZXB5YkNscTNjZHI; __gpi=UID=000006c593e7599d:T=1656964584:RT=1659183549:S=ALNI_MZm_s8pD6rMzdczO5LrC5nSZAg6Sg; usprivacy=1YNY; _gid=GA1.2.1203900387.1659183516; _gat=1"
    headers["Upgrade-Insecure-Requests"] = "1"
    headers["Sec-Fetch-Dest"] = "empty"
    headers["Sec-Fetch-Mode"] = "no-cors"
    headers["Sec-Fetch-Site"] = "same-site"
    headers["Sec-Fetch-User"] = "?1"
    headers["TE"] = "trailers"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Pragma"] = "no-cache"
    headers["Cache-Control"] = "no-cache"

    data = "code=<something><?php\n"+code+"\n?></something>"


    resp = requests.post(url, headers=headers, data=data)
    content = resp.text
    content = content.split("<something>")[1]
    content = content.split("</something>")[0]
    code_run_output(message,content)

def cpp_code_run(message):
    code = str(message.text)
    from requests.structures import CaseInsensitiveDict
    code = code.replace("+","w3plussign").replace("=","w3equalsign")
    url = "https://try.w3schools.com/try_cpp.php?x=0.3710825862426206"
    
    headers = CaseInsensitiveDict()
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; rv:103.0) Gecko/20100101 Firefox/103.0"
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    headers["Accept-Language"] = "en-US,en;q=0.5"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Referer"] = "https://www.w3schools.com/"
    headers["Origin"] = "https://www.w3schools.com"
    headers["Connection"] = "keep-alive"
    headers["Cookie"] = "snconsent=eyJwdWJsaXNoZXIiOjAsInZlbmRvciI6MywiZ2xDb25zZW50cyI6IiIsImN2Q29uc2VudHMiOnt9fQ.AnoAJwArAC4ANwA9AEYAUwBZAF0AbAB1AHoAfACDAIcAiACPAJAAkwCVAJ8AogCnAKsAwADEAMoA0wDaAOQA5gDvAPEBAwEKARABHgEjATcBPQFCAUMBRgFHAVIBbwFzAYEBhQGKAY0BlwGdAZ8BqAGuAbQBuAG9AcEBxQHiAeYB6wHuAe8B9QH3AfkCCgILAhwCJgIvAjACOAI-AkACSAJLAk8C3QLhAukDDAMTAyIDIwMxAzQDNQM9A0cDYANjA2oDgwOIA5oDowOqA9MD1QPZA-sEAAQDBAcECQQKBBAEFgQbBB0EKwQ9BEQERwRJBEsEUwRnBG8EdwR9BIAEigSOBKIEpASxBLUEuwS_BMoEywTOBOQE9AT2BPwFBAUGBQoFFQUbBSAFQQVMBVQFVQVfBXsFhwWIBYsFoAWiBakFrwWwBbkF1wXoBewF9QYEBgwGEwYWBhwGIgYpBisGLwYwBjcGQwZQBmYGcwZ1BoEGgwaNBpIGoQajBqcGsAa0BrkGvQbEBtEG1gblBukG9gb6BwgHEAcSByEHIwcoBy0HLgcwBzIHMwc1B0MHSgdOB1YHWAdhB2sHfQeJB5YHmAeqB6sHrAevB7AHsQe6B9MH1wfYB-sH8wf3B_wH_wgECAgIEAgUCBYIGAgaCCgIKgg3CDsIPQhDCEwIUghVCFkIXAhhCGMIZghsCHYIgQiHCIoImgidCKgIqwisCK4IsQi6CM0I2AjnCOoI9Aj7CQEJBQkICQwJEgkVCRgJGwkeCR8JIAkhCScJMgk1CTYJNwlCCUgJSQlTCVgJWglgCWMJZQlnCWsJbglwCXIJeQmICY8JmwmdCZ4JoQmkCagJrQmxCbQJtgm4CbwJvQnACcEJwgnDCcUJzgnPCdUJ3gnfCeQJ5gnnCe4J8An4CgMKBAoHCggKCQoLCgwKDwoRChcKGAokCikKLAotCjAKMQoyCjQKNgo9CkQKRQpJCkoKTApSClMKVQpWClcKWgpbClwKYAphCmIKZAplCm0Kbgp1CnkKfAp-Cn8KggqHCooKkwqZCpoKqQqzCs8K0ArSCtQK4ArjCucK6AruCvEK9Qr8Cv0LAAsBCwILBQsGCwsLDgsPCxILFAsWCxcLGAscCx4LHwshCyILJAsmCygLLAsuCy8LMQszCzULOQs6CzsLPAs-C0ALQQtCC0MLRAtGC0cLSAtJC0sLTQtOC08LUQtSC1QLVQtcC10LXwtgC2ELYgtkC2ULZgtnC2gLagtrC2wLbwtxC3ILcwt7C3wLfQt-C4MLhQuGC4wLkQuSC5MLlAuVC5YLmAuaC50LngufC6MLpAulC6cLqQuqC6sLrwuyC7MLtQu3C7gLugu7C70LwAvBC8ILxAvIC8kLygvLC9AL0QvUC9oL3QveC-ML5QvoC-wL7QvvC_IL8wv3C_kL-gv8C_4MAAwBDAIMAwwEDAUMBgwRDBIMFQwWDBcMGQwbDCAMIgwlDCgMLAwtDC4MLwwwDDQMNgw3DDgMOgw_DEAMSQxNDE4MTwxSDFMMWgxbDF8MZAxlDGwMbgxvDHAMcQxzDHQMdQx2DHoMfAx9DIkMigyLDI4MjwyRDJMMlgyXDJkMmgybDJwMngyfDKAMogyjDKQMpQymDKgMqQysDK0MsgyzDLUMuQy8DMQMxgzIDNEM2AzaDN0M3wzgDOQM6QzrDOwM8g; euconsent-v2=CPbV7RgPbV7RgDlBEAENCVCsAP_AAH_AACiQI3Nf_X__b3_n-_7___t0eY1f9_7__-0zjhfdt-8N3f_X_L8X_2M7vF36tr4KuR4ku3bBIQdtHOncTUmx6olVrzPsbk2cr7NKJ7Pkmnsbe2dYGH9_n93T_ZKZ7______7________________________-_____9________________________________wRuAJMNW4gC7EscGTaMIoUQIwrCQ6gUAFFAMLRFYQOrgp2VwE-oIWACAVARgRAgxBRgwCAAQCAJCIgJADwQCIAiAQAAgAVAIQAEbAILACwMAgAFANCxAigCECQgyICI5TAgIkSignsrEEoO9jTCEOssAKBR_RUICJQAgWBkJCwcxwBICXCyQLMUL5ACMEKAUAAA; _ga=GA1.2.1519819545.1656513682; __gads=ID=d2608ebe69ec6311-222348e1c1cd0026:T=1656513708:S=ALNI_MYSBd6zUVD7USzVjPI8EeuMmjb65g; cto_bundle=g9Ui3V9uMzVLTmo4TldDJTJGTE1HN0xLNERwQ3NNeEpUV3AwNGhuY0hXN3NTR0RSNUpYJTJCdSUyQk1uMVQ0JTJGRnI3ZGxzWjRGWSUyRlB4QiUyRnBwS0ZWMiUyQmlUek1qR0pnRTViUU5YZ0h4QlYwSHdkJTJCQnZYZzgwZEpBdUNTeHNpSTV0ZXB5YkNscTNjZHI; __gpi=UID=000006c593e7599d:T=1656964584:RT=1659183549:S=ALNI_MZm_s8pD6rMzdczO5LrC5nSZAg6Sg; usprivacy=1YNY; _gid=GA1.2.1203900387.1659183516; _gat=1"
    headers["Upgrade-Insecure-Requests"] = "1"
    headers["Sec-Fetch-Dest"] = "empty"
    headers["Sec-Fetch-Mode"] = "no-cors"
    headers["Sec-Fetch-Site"] = "same-site"
    headers["Sec-Fetch-User"] = "?1"
    headers["TE"] = "trailers"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Pragma"] = "no-cache"
    headers["Cache-Control"] = "no-cache"

    data = "code="+code


    resp = requests.post(url, headers=headers, data=data)
    content = resp.text
    content = content.split("<pre>")[1]
    content = content.split("</pre>")[0]
    code_run_output(message,content)

def java_code_run(message):
    code = str(message.text)
    from requests.structures import CaseInsensitiveDict
    code = code.replace("+","w3plussign").replace("=","w3equalsign")
    url = "https://try.w3schools.com/try_java.php?x=0.5733571349083243"
    
    headers = CaseInsensitiveDict()
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; rv:103.0) Gecko/20100101 Firefox/103.0"
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    headers["Accept-Language"] = "en-US,en;q=0.5"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Referer"] = "https://www.w3schools.com/"
    headers["Origin"] = "https://www.w3schools.com"
    headers["Connection"] = "keep-alive"
    headers["Cookie"] = "snconsent=eyJwdWJsaXNoZXIiOjAsInZlbmRvciI6MywiZ2xDb25zZW50cyI6IiIsImN2Q29uc2VudHMiOnt9fQ.AnoAJwArAC4ANwA9AEYAUwBZAF0AbAB1AHoAfACDAIcAiACPAJAAkwCVAJ8AogCnAKsAwADEAMoA0wDaAOQA5gDvAPEBAwEKARABHgEjATcBPQFCAUMBRgFHAVIBbwFzAYEBhQGKAY0BlwGdAZ8BqAGuAbQBuAG9AcEBxQHiAeYB6wHuAe8B9QH3AfkCCgILAhwCJgIvAjACOAI-AkACSAJLAk8C3QLhAukDDAMTAyIDIwMxAzQDNQM9A0cDYANjA2oDgwOIA5oDowOqA9MD1QPZA-sEAAQDBAcECQQKBBAEFgQbBB0EKwQ9BEQERwRJBEsEUwRnBG8EdwR9BIAEigSOBKIEpASxBLUEuwS_BMoEywTOBOQE9AT2BPwFBAUGBQoFFQUbBSAFQQVMBVQFVQVfBXsFhwWIBYsFoAWiBakFrwWwBbkF1wXoBewF9QYEBgwGEwYWBhwGIgYpBisGLwYwBjcGQwZQBmYGcwZ1BoEGgwaNBpIGoQajBqcGsAa0BrkGvQbEBtEG1gblBukG9gb6BwgHEAcSByEHIwcoBy0HLgcwBzIHMwc1B0MHSgdOB1YHWAdhB2sHfQeJB5YHmAeqB6sHrAevB7AHsQe6B9MH1wfYB-sH8wf3B_wH_wgECAgIEAgUCBYIGAgaCCgIKgg3CDsIPQhDCEwIUghVCFkIXAhhCGMIZghsCHYIgQiHCIoImgidCKgIqwisCK4IsQi6CM0I2AjnCOoI9Aj7CQEJBQkICQwJEgkVCRgJGwkeCR8JIAkhCScJMgk1CTYJNwlCCUgJSQlTCVgJWglgCWMJZQlnCWsJbglwCXIJeQmICY8JmwmdCZ4JoQmkCagJrQmxCbQJtgm4CbwJvQnACcEJwgnDCcUJzgnPCdUJ3gnfCeQJ5gnnCe4J8An4CgMKBAoHCggKCQoLCgwKDwoRChcKGAokCikKLAotCjAKMQoyCjQKNgo9CkQKRQpJCkoKTApSClMKVQpWClcKWgpbClwKYAphCmIKZAplCm0Kbgp1CnkKfAp-Cn8KggqHCooKkwqZCpoKqQqzCs8K0ArSCtQK4ArjCucK6AruCvEK9Qr8Cv0LAAsBCwILBQsGCwsLDgsPCxILFAsWCxcLGAscCx4LHwshCyILJAsmCygLLAsuCy8LMQszCzULOQs6CzsLPAs-C0ALQQtCC0MLRAtGC0cLSAtJC0sLTQtOC08LUQtSC1QLVQtcC10LXwtgC2ELYgtkC2ULZgtnC2gLagtrC2wLbwtxC3ILcwt7C3wLfQt-C4MLhQuGC4wLkQuSC5MLlAuVC5YLmAuaC50LngufC6MLpAulC6cLqQuqC6sLrwuyC7MLtQu3C7gLugu7C70LwAvBC8ILxAvIC8kLygvLC9AL0QvUC9oL3QveC-ML5QvoC-wL7QvvC_IL8wv3C_kL-gv8C_4MAAwBDAIMAwwEDAUMBgwRDBIMFQwWDBcMGQwbDCAMIgwlDCgMLAwtDC4MLwwwDDQMNgw3DDgMOgw_DEAMSQxNDE4MTwxSDFMMWgxbDF8MZAxlDGwMbgxvDHAMcQxzDHQMdQx2DHoMfAx9DIkMigyLDI4MjwyRDJMMlgyXDJkMmgybDJwMngyfDKAMogyjDKQMpQymDKgMqQysDK0MsgyzDLUMuQy8DMQMxgzIDNEM2AzaDN0M3wzgDOQM6QzrDOwM8g; euconsent-v2=CPbV7RgPbV7RgDlBEAENCVCsAP_AAH_AACiQI3Nf_X__b3_n-_7___t0eY1f9_7__-0zjhfdt-8N3f_X_L8X_2M7vF36tr4KuR4ku3bBIQdtHOncTUmx6olVrzPsbk2cr7NKJ7Pkmnsbe2dYGH9_n93T_ZKZ7______7________________________-_____9________________________________wRuAJMNW4gC7EscGTaMIoUQIwrCQ6gUAFFAMLRFYQOrgp2VwE-oIWACAVARgRAgxBRgwCAAQCAJCIgJADwQCIAiAQAAgAVAIQAEbAILACwMAgAFANCxAigCECQgyICI5TAgIkSignsrEEoO9jTCEOssAKBR_RUICJQAgWBkJCwcxwBICXCyQLMUL5ACMEKAUAAA; _ga=GA1.2.1519819545.1656513682; __gads=ID=d2608ebe69ec6311-222348e1c1cd0026:T=1656513708:S=ALNI_MYSBd6zUVD7USzVjPI8EeuMmjb65g; cto_bundle=g9Ui3V9uMzVLTmo4TldDJTJGTE1HN0xLNERwQ3NNeEpUV3AwNGhuY0hXN3NTR0RSNUpYJTJCdSUyQk1uMVQ0JTJGRnI3ZGxzWjRGWSUyRlB4QiUyRnBwS0ZWMiUyQmlUek1qR0pnRTViUU5YZ0h4QlYwSHdkJTJCQnZYZzgwZEpBdUNTeHNpSTV0ZXB5YkNscTNjZHI; __gpi=UID=000006c593e7599d:T=1656964584:RT=1659183549:S=ALNI_MZm_s8pD6rMzdczO5LrC5nSZAg6Sg; usprivacy=1YNY; _gid=GA1.2.1203900387.1659183516; _gat=1"
    headers["Upgrade-Insecure-Requests"] = "1"
    headers["Sec-Fetch-Dest"] = "empty"
    headers["Sec-Fetch-Mode"] = "no-cors"
    headers["Sec-Fetch-Site"] = "same-site"
    headers["Sec-Fetch-User"] = "?1"
    headers["TE"] = "trailers"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Pragma"] = "no-cache"
    headers["Cache-Control"] = "no-cache"

    data = "code="+code


    resp = requests.post(url, headers=headers, data=data)
    content = resp.text
    content = content.split("<pre>")[1]
    content = content.split("</pre>")[0]
    code_run_output(message,content)

def html_code_run(message,driver=None):
    try:
        global current_path
        code = str(message.text)
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager
        saveAs = str(message.from_user.id)+".html"
        f = open("./"+saveAs,"w")
        f.write(code)
        f.close()
        
        # S-E-R
        options = webdriver.chrome.options.Options()
        options.add_argument("no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=800,600")
        options.add_argument("--disable-dev-shm-usage")
        options.headless = True
        driver = webdriver.Chrome(chrome_options=options)
        # S-E-R
        
        driver.get("file://"+current_path+"/"+saveAs)
        time.sleep(4)
            # Returns and base64 encoded string into image
        driver.save_screenshot('./image.png')
        f = open("image.png","rb")
        bot.send_photo(message.chat.id,f,caption="# HTML Preview")
        f.close()
        driver.quit()
    except Exception as e:
        bot.reply_to(message,str(e))
  
def escape(html):
    """Returns the given HTML with ampersands, quotes and carets encoded."""
    return html.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')  

def newCommandLang(commandID,selectedLanguage,lang="en"):
    f = open("commands.json","r")
    txt = f.read()
    txtJson = json.loads(txt)
    f.close()
    for language in txtJson["Languages"]:
        if str(language) == selectedLanguage:
            for command in txtJson["Languages"][language]["commands"]:
                if commandID == str(command):
                    
                    if lang == "ar":
                        theCommand = txtJson["Languages"][language]["commands"][command]["en"]["input"]
                        theExample = txtJson["Languages"][language]["commands"][command]["en"]["example"]
                        txtJson["Languages"][language]["commands"][command]["ar"]["input"] = theCommand
                        txtJson["Languages"][language]["commands"][command]["ar"]["example"] = theExample
                        txtJson["Languages"][language]["commands"][command]["en"]["input"] = ""
                        txtJson["Languages"][language]["commands"][command]["en"]["example"] = ""
                    else:
                        theCommand = txtJson["Languages"][language]["commands"][command]["ar"]["input"]
                        theExample = txtJson["Languages"][language]["commands"][command]["ar"]["example"]
                        txtJson["Languages"][language]["commands"][command]["en"]["input"] = theCommand
                        txtJson["Languages"][language]["commands"][command]["en"]["example"] = theExample
                        txtJson["Languages"][language]["commands"][command]["ar"]["input"] = ""
                        txtJson["Languages"][language]["commands"][command]["ar"]["example"] = ""
    f = open("commands.json","w")
    toWrite = json.dumps(txtJson)
    f.write(toWrite)
    f.close()
    return "Updated Successfully"

def AddNewCommandUser(message,commandLanguage,command,commandInput,commandExample,file_id="",lang="en",docType="document",password=None):
    f = open("usersPost.json","r")
    txtJson = json.loads(f.read())
    f.close()
    
    question = "@"+message.from_user.username+"\n"+commandInput+"\n"+commandExample
    msg = bot.send_message("-1001604626385",question)
    bot.send_poll("-1001604626385","is that's right ?\n id : #"+str(msg.id),["yes","no"],reply_to_message_id=msg.id)
    try:
        txtJson["users"][message.from_user.id]["Pending"].append({"username":message.from_user.username,"pid":msg.id,"id":command,"input":commandInput,"lan":commandLanguage,"example":commandExample,"file_id":file_id,"lang":lang,"type":docType,"password":password})
    except:
        txtJson["users"][message.from_user.id] = {"Pending":[],"Published":[]}
        txtJson["users"][message.from_user.id]["Pending"].append({"username":message.from_user.username,"pid":msg.id,"id":command,"input":commandInput,"lan":commandLanguage,"example":commandExample,"file_id":file_id,"lang":lang,"type":docType,"password":password})
     
    f = open("usersPost.json","w")
    toWrite = json.dumps(txtJson)
    f.write(toWrite)
    f.close()
    userLang = getLang(str(message.from_user.id))
    if userLang == "en":
        bot.reply_to(message,"Command is Pending Right Now You Can View Reactions in @Programmers_Code")
    else:
        bot.reply_to(message,"تم اضافة الامر وهو في لائحة التحقق قم برؤية التفاعلات هنا @Programmers_Code")

def AddNewCommand(message,commandLanguage,command,commandInput,commandExample,file_id="",lang="en",docType="document",password=None):
    f = open("commands.json","r")
    txt = str(f.read())
    txtJson = json.loads(txt)
    f.close()
    def AddCommands(commandLanguage):
        try:
            txtJson["Languages"][commandLanguage]["commands"]
        except:
            txtJson["Languages"][commandLanguage]["commands"] = {}
    def AddLanguage(commandLanguage):
            try:
                txtJson["Languages"][commandLanguage]
            except:
                txtJson["Languages"][commandLanguage] = {"commands":{}}
    def AddCommand(commandLanguage,command):
        try:
            txtJson["Languages"][commandLanguage]["commands"][command]
        except:
            txtJson["Languages"][commandLanguage]["commands"][command] = {"en":{"input":"","example":"","fileId":""},"ar":{"input":"","example":"","fileId":""}}
    
    AddLanguage(commandLanguage)
    AddCommands(commandLanguage)
    AddCommand(commandLanguage,command)
    smartExample = ""
    for lineContent in commandExample.splitlines():
        smartExample += smartCustomize(lineContent)+"\n"
    toTest = commandLanguage.replace("+","\\+")
    if not re.search('^'+toTest+'|.*'+toTest,commandInput):
        txtJson["Languages"][commandLanguage]["commands"][command][lang]["input"] = commandInput+" "+commandLanguage
    else:
        txtJson["Languages"][commandLanguage]["commands"][command][lang]["input"] = commandInput
    txtJson["Languages"][commandLanguage]["commands"][command][lang]["example"] = smartExample
    txtJson["Languages"][commandLanguage]["commands"][command][lang]["fileId"] = file_id
    txtJson["Languages"][commandLanguage]["commands"][command][lang]["type"] = docType
    if password:
        txtJson["Languages"][commandLanguage]["commands"][command][lang]["password"] = str(password)
        txtJson["Languages"][commandLanguage]["commands"][command][lang]["from_user_id"] = message.from_user.id
    jsonContent = json.dumps(txtJson)
    f = open("commands.json","w")
    f.write(jsonContent)
    f.close()
    UpdateFile()
    if str(commandLanguage) == "html":
        reply = "#"+str(commandLanguage)+"\n"
        Example = commandExample
        
        reply += Example
        bot.reply_to(message,reply)
    else:
        reply = "#"+str(commandLanguage)+"\n"
        Example = commandExample
        try:
            bot.reply_to(message,reply,parse_mode="html")
        except:
            StyledExample =styleExample(Example,True)
            reply += StyledExample
            bot.reply_to(message,reply,parse_mode="html")
    bot.reply_to(message,"New Command Added")

def getLang(id):
    try:
        f = open("users.json","r")
        txt = f.read()
        txtJson = json.loads(txt)
        f.close()
        for x in range(len(txtJson["users"])):
            if int(id) == txtJson["users"][x]["id"]:
                return str(txtJson["users"][x]["lang"])
    except:
        return "en"

def getUsers():
    f = open("users.json","r")
    txt = f.read()
    txtJson = json.loads(txt)
    f.close()
    AllUsers = ""
    for x in range(len(txtJson["users"])):
        AllUsers += str(txtJson["users"][x]["user"])+"\n"
    return AllUsers
def smartCustomize(lineContent):
    replacement = r'<b>\1</b>'
    if re.search("^::b",lineContent):
        lineContent = lineContent.replace("::b","<b>",1)+"</b>"
    lineContent = re.sub(':b(.*?):b', replacement, lineContent)
    lineContent = re.sub('^::b(.*?)',replacement,lineContent)
    lineContent = re.sub(':i(.*?):i', r'<i>\1</i>', lineContent)
    editedText = ""
    for word in lineContent.split(" "):
        editedText += re.sub(r'(.*?):href:(.*.?)',r'<a href="\2">\1</a> ',word)+" "
    return editedText
def styleExample(Example,isFailed=False):
    
    
    StyledExample = ""
    for line in Example.splitlines():
        
        tags = []
        allowedTags = ["a","b","pre","i"]
        class MyHTMLParser(HTMLParser):
            def handle_starttag(self, tag, attrs):
                tags.append(tag)
        lineContent =  str(line)
        #Customize
        lineContent = smartCustomize(lineContent)
        parser = MyHTMLParser()
        parser.feed(lineContent)
        isValid = True
        for x in range(len(tags)):
            if tags[x]:
                if not str(tags[x]) in allowedTags:
                    isValid = False
        
        if isValid and len(tags) > 0:
            StyledExample += lineContent+"\n"
        elif (re.search("^—.*—$",lineContent) or re.search("^—.*-$",lineContent) or re.search("^#",lineContent)) and isValid:
            StyledExample += lineContent+"\n"
        else:
            StyledExample += "<code>"+escape(lineContent)+"</code>\n"
    return StyledExample

def PrepareJson(message):
    f = open("commands.json")
    txt = f.read()
    txtJson = json.loads(txt)
    f.close()
    s = {
        "Languages":{
            
        }
    }
    
    #Add Languages
    for lan in txtJson["Languages"]:
        s["Languages"][lan] = {"commands":{}}
        #Add Commands
        for commandID in txtJson["Languages"][lan]["commands"]:
            s["Languages"][lan]["commands"][commandID] = {"ar":{"input":"","example":"","fileId":""},"en":{"input":"","example":"","fileId":""}}
            if len(txtJson["Languages"][lan]["commands"][commandID]["ar"]) > 1:
                uinput = txtJson["Languages"][lan]["commands"][commandID]["ar"][0]
                example = txtJson["Languages"][lan]["commands"][commandID]["ar"][1]
                s["Languages"][lan]["commands"][commandID]["ar"]["input"] = uinput
                s["Languages"][lan]["commands"][commandID]["ar"]["example"] = example
            if len(txtJson["Languages"][lan]["commands"][commandID]["en"]) > 1:
                uinput = txtJson["Languages"][lan]["commands"][commandID]["en"][0]
                example = txtJson["Languages"][lan]["commands"][commandID]["en"][1]
                s["Languages"][lan]["commands"][commandID]["en"]["input"] = uinput
                s["Languages"][lan]["commands"][commandID]["en"]["example"] = example
    f = open("commands_new.json","w")
    toWrite = json.dumps(s)
    f.write(toWrite)
    f.close()
    f = open("commands_new.json","rb")
    bot.send_document(message.chat.id,f)
    f.close()

def checkJoin(user_id):
    try:
        isInChannel = bot.get_chat_member("-1001604626385",user_id)
        return True
    except Exception as e:
        return False
def sof_direct_answer(message,link):
    from bs4 import BeautifulSoup
    try:
        r2 = requests.get(link)
        soup = BeautifulSoup(r2.text, 'html.parser')
        PostLayout = soup.find_all("div",class_="post-layout")
        QuestionTitle = soup.find("div",id="question-header").find("h1").text
        Question = "<b>Question</b>:"+QuestionTitle+"<code>"+escape(PostLayout[0].find(class_="s-prose js-post-body").text)+"</code>"
        Answers = soup.find(id="answers").find_all("div",id=re.compile('answer-[0-9]'))
        Answer = Answers[0].find("div",class_="s-prose js-post-body").text
        Answer = escape(Answer)
        Ans0 = "<b>Answer:\n</b><code>"+Answer+"</code>\n<a href='https://"+link+"'>Link</a>"
        bot.reply_to(message,str(Question),parse_mode="html")
        bot.reply_to(message,str(Ans0),parse_mode="html")
    except Exception as e:
        bot.reply_to(message,"Something Wrong Happend Try Later")
        bot.send_message(AdminID,str(e))
def sof_show_answer(message,data):
    from bs4 import BeautifulSoup
    q_id = 0
    try:
        q_id = int(message.text.split("-")[0])
    except:
        return bot.reply_to(message,"Not Valid Question")
    try:
        link = data[q_id]["link"]
        r2 = requests.get("https://"+link)
        soup = BeautifulSoup(r2.text, 'html.parser')
        PostLayout = soup.find_all("div",class_="post-layout")
        QuestionTitle = soup.find("div",id="question-header").find("h1").text
        Question = "<b>Question</b>:"+QuestionTitle+"<code>"+escape(PostLayout[0].find(class_="s-prose js-post-body").text)+"</code>"
        Answers = soup.find(id="answers").find_all("div",id=re.compile('answer-[0-9]'))
        Answer = Answers[0].find("div",class_="s-prose js-post-body").text
        Answer = escape(Answer)
        Ans0 = "<b>Answer:\n</b><code>"+Answer+"</code>\n<a href='https://"+link+"'>Link</a>"
        bot.reply_to(message,str(Question),parse_mode="html")
        bot.reply_to(message,str(Ans0),parse_mode="html")
    except Exception as e:
        bot.reply_to(message,"Something Wrong Happend Try Later")
        bot.send_message(AdminID,str(e))

def sof_do_search(message):
    from bs4 import BeautifulSoup
    import urllib.parse
    searchFor = urllib.parse.quote(str(message.text).encode('utf8'))
    r = requests.get('https://www.google.com/search?q=+'+searchFor+"+site%3Astackoverflow.com")
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all("h3")
    markup = types.ReplyKeyboardMarkup()
    data = []
    for x in range(len(results)):
        resultTitle = results[x].text
        link = ""
        try:
            link = results[x].parent.attrs['href'].split("https://")[1]
        except:
            continue
        if re.search("https://stackoverflow.com/questions/[0-9]+/","https://"+link):
            markup.add(str(x)+"-"+str(resultTitle))
            data.append({"title":resultTitle,"link":link})
    if len(data) == 0:
        return bot.reply_to(message,"No Result For This Search :(")
    msg = bot.reply_to(message,"Results Founded:"+str(len(data)),reply_markup=markup)
    bot.register_next_step_handler(msg, sof_show_answer,data)
    
def get_example(message,examples,link,lan):
    selectedExample = str(message.text)
    for x in range(len(examples)):
        if selectedExample == str(examples[x]["title"]):
            from selenium import webdriver
            options = webdriver.chrome.options.Options();
            options.add_argument("no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=800,600")
            options.add_argument("--disable-dev-shm-usage")
            options.headless = True
            driver = webdriver.Chrome(chrome_options=options)
            try:
                theLink = link+str(examples[x]["link"])
                driver.get(theLink)
                time.sleep(4)
                from selenium.webdriver.common.by import By
                Code = driver.find_element(By.CLASS_NAME,'CodeMirror-code')
                htmlCode = "<code>"+escape(str(Code.text))+"</code>"
                bot.reply_to(message,htmlCode,parse_mode="html")
                if lan == "python":
                    message.text= str(Code.text)
                    python_code_run(message)
                if lan == "php":
                    message.text= "?>"+str(Code.text)+"<?"
                    php_code_run(message)
                if lan == "cpp":
                    message.text= str(Code.text)
                    cpp_code_run(message)
                if lan == "c":
                    message.text= str(Code.text)
                    c_code_run(message)
                if lan == "java":
                    message.text= str(Code.text)
                    java_code_run(message)
                if lan == "html":
                    saveAs = str(message.from_user.id)+".html"
                    f = open(saveAs,"w")
                    f.write(str(Code.text))
                    f.close()
                    driver.get("file://"+current_path+'/'+saveAs)
                    time.sleep(4)
                        # Returns and base64 encoded string into image
                    driver.save_screenshot('./image.png')
                    f = open("/app/image.png","rb")
                    bot.send_photo(message.chat.id,f,caption="# HTML Preview")
                    f.close()
                    driver.quit()
                    return
                driver.quit()
                
            except Exception as e:
                driver.quit()
                bot.send_message(AdminID,str(e))
            break
def post_random_quiz():
    txtJson = checkLanguage("python")
    lans = []
    for language in txtJson["Languages"]:
        try:
            txtJson["Languages"][language]["Quiz"]
            lans.append(str(language))
        except:
            something = 0
    lan = random.choice(lans)
    langs = ["en","ar"]
    userLang = random.choice(langs)
    try:
        if txtJson:
            randomQuiz = random.randint(-1,len(txtJson["Languages"][lan]["Quiz"][userLang])-1)
            question = txtJson["Languages"][lan]["Quiz"][userLang][randomQuiz]["question"]
            
            options = txtJson["Languages"][lan]["Quiz"][userLang][randomQuiz]["options"]
            correct_option = txtJson["Languages"][lan]["Quiz"][userLang][randomQuiz]["correct_option"]
            file_id = txtJson["Languages"][lan]["Quiz"][userLang][randomQuiz]["file_id"]
            explain = txtJson["Languages"][lan]["Quiz"][userLang][randomQuiz]["explain"]
            if file_id:
                bot.send_photo("-1001604626385",file_id,caption=question+" #"+str(lan))
            else:
                bot.send_message("-1001604626385",question+"\n#"+str(lan))
            bot.send_poll("-1001604626385","Read Above Question & Anwer",options,explanation=explain,correct_option_id=correct_option,type="quiz")
            return
    except:
        bot.send_message(AdminID,"No Quiz For This Language")
        bot.send_message(AdminID,"Quiz "+str(lan)+" Asked")
        return
    bot.reply_to(message,"No Quiz Yet")
def get_examples(message):
    
    from bs4 import BeautifulSoup
    BASE_URL = 'https://www.w3schools.com/'
    lan = str(message.text)
    full_url = BASE_URL+lan+"/"+lan+"_examples.asp"
    r = requests.get(full_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    AllExamples = soup.find_all('a','w3-button w3-bar-item ws-grey')
    markup = types.ReplyKeyboardMarkup()
    examplesLinks = []
    for x in range(len(AllExamples)):
        markup.add(str(x)+"- "+str(AllExamples[x].text))
        examplesLinks.append({"title":str(x)+"- "+str(AllExamples[x].text),"link":AllExamples[x].attrs['href']})
    msg = bot.reply_to(message,"Choose Example:",reply_markup=markup)
    bot.register_next_step_handler(msg, get_example,examplesLinks,BASE_URL+lan+"/",lan)
def checkLanguage(lan):
    f = open("commands.json","r")
    txtJson = json.loads(f.read())
    f.close()
    for language in txtJson["Languages"]:
        if str(language) == lan:
            return txtJson
    return False
def new_quiz_done(message):
    f = open("commands.json","r")
    txtJson = json.loads(f.read())
    f.close()
    lan = userActions[message.from_user.id]["quiz"]["language"]
    question = userActions[message.from_user.id]["quiz"]["question"]
    options = userActions[message.from_user.id]["quiz"]["options"]
    correct_option = userActions[message.from_user.id]["quiz"]["correct_option"]
    file_id = userActions[message.from_user.id]["quiz"]["file_id"]
    explain = userActions[message.from_user.id]["quiz"]["explain"]
    lang = userActions[message.from_user.id]["quiz"]["lang"]
    try:
        txtJson["Languages"][lan]["Quiz"][lang].append({"question":question,"options":options,"correct_option":correct_option,"file_id":file_id,"explain":explain,"lang":lang})
    except:
        txtJson["Languages"][lan]["Quiz"] = {"en":[],"ar":[]}
        txtJson["Languages"][lan]["Quiz"][lang].append({"question":question,"options":options,"correct_option":correct_option,"file_id":file_id,"explain":explain,"lang":lang})
    f = open("commands.json","w")
    toWrite = json.dumps(txtJson)
    f.write(toWrite)
    f.close()
    UpdateFile()
    bot.reply_to(message,"Added Successfully")
def new_quiz_explain(message):
    if message.text == "/none":
        new_quiz_done(message)
    else:
        userActions[message.from_user.id]["quiz"]["explain"] = message.text
        new_quiz_done(message)
def new_quiz_correct(message):
    try:
        correct_option = int(message.text)
        if correct_option > len(userActions[message.from_user.id]["quiz"]["options"])-1 or correct_option < 0:
            return bot.reply_to(message,"Correct Answer Is Out Of Options")
        userActions[message.from_user.id]["quiz"]["correct_option"] = correct_option
        msg = bot.reply_to(message,"Enter Explaination or /none:")
        bot.register_next_step_handler(msg,new_quiz_explain)
    except:
        bot.reply_to(message,"Invalid Correct Answer ID")
def new_quiz_options(message):
    if message.text == "/done":
        allOptions = ""
        for x in range(len(userActions[message.from_user.id]["quiz"]["options"])):
            allOptions += str(x)+" "+userActions[message.from_user.id]["quiz"]["options"][x]+"\n"
        bot.reply_to(message,allOptions)
        msg = bot.reply_to(message,"Now Choose Correct Answer ID:")
        bot.register_next_step_handler(msg,new_quiz_correct)
        
        return
    if message.content_type == "poll":
        options = message.poll.options
        message.text = ""
        for x in range(len(options)):
            message.text += str(options[x].text)+"\n"
    for option in message.text.splitlines():
        userActions[message.from_user.id]["quiz"]["options"].append(str(option))
    msg = bot.reply_to(message,"Send Other Option or /done when Complete")
    bot.register_next_step_handler(msg,new_quiz_options)
def new_quiz_file(message):
    if message.text == "/none":
        if userActions[message.from_user.id]["quiz"]["question"] == "":
            return bot.reply_to(message,"There Must Be At Least A Question Or Photo \nOperation Cancelled")
        msg = bot.reply_to(message,"Now Enter Options:")
        return bot.register_next_step_handler(msg,new_quiz_options)
    if message.content_type == "photo":
        userActions[message.from_user.id]["quiz"]["file_id"] = message.photo[0].file_id
        msg = bot.reply_to(message,"Now Enter Options:")
        bot.register_next_step_handler(msg,new_quiz_options)
    else:
        msg = bot.reply_to(message,"Only Photos Allowed\nSend Photo Now:")
        bot.register_next_step_handler(msg,new_quiz_file)
def new_quiz_question(message):
    question = message.text
    if question == "null":
        msg = bot.reply_to(message,"Null Question Need to Send Photo send Any Photo Now")
        bot.register_next_step_handler(msg,new_quiz_file)
        return
    else:
        userActions[message.from_user.id]["quiz"]["question"] = question
        msg = bot.reply_to(message,"Now Send Attachment or /none To not add Attachment")
        bot.register_next_step_handler(msg,new_quiz_file)
def new_quiz_lan(message):
    language = message.text
    isExists = checkLanguage(language)
    userLang = getLang(message.from_user.id)
    if isExists:
        try:
            userActions[message.from_user.id]["quiz"] = {}
            userActions[message.from_user.id]["quiz"]["language"] = language
            userActions[message.from_user.id]["quiz"]["question"] = ""
            userActions[message.from_user.id]["quiz"]["correct_option"] = 0
            userActions[message.from_user.id]["quiz"]["file_id"] = ""
            userActions[message.from_user.id]["quiz"]["explain"] = ""
            userActions[message.from_user.id]["quiz"]["options"].clear()
            userActions[message.from_user.id]["quiz"]["lang"] = userLang
        except: 
            userActions[message.from_user.id] = {"quiz":{"language":language,"question":"","options":[],"correct_option":0,"file_id":"","explain":"","lang":userLang}}
        msg = bot.reply_to(message,"Enter Question:")
        bot.register_next_step_handler(msg,new_quiz_question)
    else:
        bot.reply_to(message,"Unsupported Language")
def quiz_random(message):
    txtJson = checkLanguage(message.text)
    userLang = getLang(message.from_user.id)
    try:
        if txtJson:
            randomQuiz = random.randint(-1,len(txtJson["Languages"][message.text]["Quiz"][userLang])-1)
            question = txtJson["Languages"][message.text]["Quiz"][userLang][randomQuiz]["question"]
            
            options = txtJson["Languages"][message.text]["Quiz"][userLang][randomQuiz]["options"]
            correct_option = txtJson["Languages"][message.text]["Quiz"][userLang][randomQuiz]["correct_option"]
            file_id = txtJson["Languages"][message.text]["Quiz"][userLang][randomQuiz]["file_id"]
            explain = txtJson["Languages"][message.text]["Quiz"][userLang][randomQuiz]["explain"]
            if file_id:
                bot.send_photo(message.chat.id,file_id,caption=question)
            else:
                bot.reply_to(message,question)
            bot.send_poll(message.chat.id,"Read Above Question & Anwer",options,explanation=explain,correct_option_id=correct_option,type="quiz")
            return
    except:
        bot.reply_to(message,"No Quiz For This Language")
        bot.send_message(AdminID,"Quiz "+str(language)+" Asked")
        return
    bot.reply_to(message,"No Quiz Yet")
def delete_quiz(message,lan):
    txtJson = checkLanguage(lan)
    userLang = getLang(message.from_user.id)
    if txtJson:
        try:
            del txtJson["Languages"][lan]["Quiz"][userLang][int(message.text)]
            f = open("commands.json","w")
            toWrite = json.dumps(txtJson)
            f.write(toWrite)
            f.close()
            UpdateFile()
            bot.reply_to(message,"Deleted Successfully")
        except Exception as e:
            bot.reply_to(message,"Somthing Happend")
            print(x)
    else:
        bot.reply_to(message,"Error")
def delete_quiz_id(message):
    lan = message.text
    txtJson = checkLanguage(lan)
    userLang = getLang(message.from_user.id)
    if txtJson:
        try:
            markup = types.ReplyKeyboardMarkup()
            for x in range(len(txtJson["Languages"][lan]["Quiz"][userLang])):
                markup.add(str(x))
            msg = bot.reply_to(message,"Choose ID:",reply_markup=markup)
            bot.register_next_step_handler(msg,delete_quiz,lan)
        except Exception as e:
            bot.reply_to(message,"Something Happend")
            print(e)
    else:
        bot.reply_to(message,"Not Supported Language")
# INSERT KEYWORD
def insert_keyword_font_color(message,newKeyword):
    color = message.text.split(" ")[0]
    newKeyword._color = color
    asList = []
    asList.append(newKeyword._language)
    asList.append(newKeyword._color)
    asList.append(newKeyword._isBold)
    txtJson = checkLanguage(newKeyword._language)
    if txtJson:
        try:
            txtJson["Languages"][newKeyword._language]["Keywords"].append({"keyword":newKeyword._keyword,"color":newKeyword._color,"isBold":newKeyword._isBold,"isRegex":newKeyword._isRegex})
        except:
            txtJson["Languages"][newKeyword._language]["Keywords"] = []
            txtJson["Languages"][newKeyword._language]["Keywords"].append({"keyword":newKeyword._keyword,"color":newKeyword._color,"isBold":newKeyword._isBold,"isRegex":newKeyword._isRegex})
        UpdateFile(txtJson)
        bot.reply_to(message,"Keyword Added Successfully")
    else:
        bot.reply_to(message,"Sorry This Language is Not Available")
def insert_keyword(message,newKeyword):
    keyword = message.text
    txtJson = checkLanguage(newKeyword._language)
    try:
        for x in range(len(txtJson["Languages"][newKeyword._language]["Keywords"])):
            key = str(txtJson["Languages"][newKeyword._language]["Keywords"][x]["keyword"])
            if str(key) == str(keyword):
                return bot.reply_to(message,"This Keyword Allready Exists")
    except Exception as e:
        print(e)
    newKeyword.setKeyword(keyword)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    lan = newKeyword._language
    markup = types.ReplyKeyboardMarkup(row_width=2)
    
    global Colors
    Colors.clear()
    for language in txtJson["Languages"]:
        try:
            for x in range(len(txtJson["Languages"][language]["Keywords"])):
                keywordColor = txtJson["Languages"][language]["Keywords"][x]["color"]
                if keywordColor not in Colors:
                    Colors.append(keywordColor)
        except:
            continue
    for color in Colors:
        markup.add(color)
    msg = bot.reply_to(message,"Now Enter Font Color",reply_markup=markup)
    bot.register_next_step_handler(msg,insert_keyword_font_color,newKeyword)
def insert_keyword_lan(message,newKeyword):
    lan = message.text
    txtJson = checkLanguage(lan)
    if txtJson:
        newKeyword._language = lan
        msg = bot.reply_to(message,"Enter Keyword:")
        bot.register_next_step_handler(msg,insert_keyword,newKeyword)
    else:
        bot.reply_to(message,"No Language Detected")
# DELETE KEYWORD
def delete_keyword_id(message,lan):
    keywordId = int(message.text.split("-")[0])
    try:
        txtJson = checkLanguage(lan)
        del txtJson["Languages"][lan]["Keywords"][keywordId]
        UpdateFile(txtJson)
        bot.reply_to(message,"Deleted Successfully")
    except:
        bot.reply_to(message,"Key Out Of Range")
def delete_keyword_lan(message):
    lan = message.text
    txtJson = checkLanguage(lan)
    if txtJson:
        try:
            keywordsLen = len(txtJson["Languages"][lan]["Keywords"])
            markup = types.ReplyKeyboardMarkup(row_width=2)
            for x in range(keywordsLen):
                markup.add(str(x)+"- "+str(txtJson["Languages"][lan]["Keywords"][x]["keyword"]))
            msg = bot.reply_to(message,"Choose Keyword:",reply_markup=markup)
            bot.register_next_step_handler(msg,delete_keyword_id,lan)
        except:
            bot.reply_to(message,"No keyowrds On This Language")
    else:
        bot.reply_to(message,"Not Supported Language")
def replyMarkupLanguages():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    txtJson = checkLanguage("python")
    for language in txtJson["Languages"]:
        markup.add(str(language))
    return markup
def preview_page(message,html,saveAs,class_=None):
    global current_path
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    f = open(saveAs,"w")
    f.write(html)
    f.close()
    options = webdriver.chrome.options.Options()
    options.add_argument("no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=800,600")
    options.add_argument("--disable-dev-shm-usage")
    options.headless = True
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("file://"+current_path+'/'+saveAs)
    time.sleep(4)
        # Returns and base64 encoded string into image
    if class_ != None:
        elem = driver.find_element(By.CLASS_NAME, class_)
        elem.screenshot('./image.png')
    else:
        driver.save_screenshot('./image.png')
    f = open("./image.png","rb")
    bot.send_photo(message.chat.id,f,caption="# HTML Preview")
    f.close()
    driver.quit()
def gen_code_code(message,lan):
    code = message.text
    code = re.sub('\b:nline\b',"\\n",code)
    code_run(message,lan)
    txtJson = checkLanguage(lan)
    # SETUP HTML CODE
    class HTML_TAGs:
        b = "<b>"
        b_e = "</b>"
        def setColor(self,code,color):
            return '<span style="color:'+color+'">'+code+"</span>"
    
    html_style = HTML_TAGs()
    specialChars = ['\/','\&',"`","!","@","#","$","%","^","*","(",")","{","}","[","]","\:","'",'"',"?",".",",","+","\=","-","_","|"]
    html_replacement= [{"name":">","value":"&gt;"},{"name":"<","value":"&lt;"}]
    code = code.replace("/","\\/").replace('&','\&')
    code= escape(code)
    styledCode = ""
    from bs4 import BeautifulSoup
    for x in range(len(html_replacement)):
        test = html_replacement[x]["value"]
        code = code.replace(html_replacement[x]["name"],test,1)
    for x in range(len(html_replacement)):
        test = "<code>"+html_replacement[x]["value"]+"</code>"
        code = code.replace(html_replacement[x]["value"],test,1)
    for specChar in specialChars:
        for x in range(len(txtJson["Languages"][lan]["Keywords"])):
            keyword = str(txtJson["Languages"][lan]["Keywords"][x]["keyword"])
            keywordColor = str(txtJson["Languages"][lan]["Keywords"][x]["color"])
            if keyword == specChar.replace("\\","",1):
                test = html_style.setColor(specChar,keywordColor)
                code = code.replace(specChar,test.replace("\\",""))
    quote = re.escape("&quot;")
    code = re.sub(quote+r'(.*?)'+quote,'<nocolor>"'+r'\1'+'"</nocolor>',code)
    line_no = 1
    for lineContent in code.splitlines():
        commentsColor = None
        for x in range(len(txtJson["Languages"][lan]["Keywords"])):
            for keyword in str(txtJson["Languages"][lan]["Keywords"][x]["keyword"]).split(" "):
                keywordColor = str(txtJson["Languages"][lan]["Keywords"][x]["color"])
                if keyword.find(":"):
                    if keyword.split(":")[0] == "comment":
                        commentChar = keyword.split(":")[1]
                        if re.search("^\s+"+re.escape(commentChar)+"|^"+re.escape(commentChar),lineContent):
                            commentsColor = keywordColor
                    if keyword.split(":")[0] == "numbers":
                        lineContent = re.sub(r'([0-9]+)',"<span style='color:"+keywordColor+"'>"+r'\1'+"</span>",lineContent)
        if commentsColor != None:
            lineContent = html_style.setColor(lineContent,commentsColor)
        else:
            for x in range(len(txtJson["Languages"][lan]["Keywords"])):
                for keyword in str(txtJson["Languages"][lan]["Keywords"][x]["keyword"]).split(" "):
                    keywordColor = str(txtJson["Languages"][lan]["Keywords"][x]["color"])
                    pattern = r'\b'+re.escape(keyword)+r'\b'
                    
                    lineContent = re.sub(pattern,html_style.setColor(keyword,keywordColor),lineContent)
                    if re.findall('<nocolor>(.*?)</nocolor>',lineContent):
                        for x2 in range(len(re.findall('<nocolor>(.*?)</nocolor>',lineContent))):
                            founeded = str(re.findall('<nocolor>(.*?)</nocolor>',lineContent)[x2])
                            soup = BeautifulSoup(lineContent, 'html.parser')
                            nocolors = soup.find_all("nocolor")
                            nocolorString = nocolors[x2].get_text()
                            lineContent = re.sub(re.escape(founeded),html_style.setColor(str(nocolorString),"grey").replace("\s","\\s").replace("\n","\\n"),lineContent)

                
        styledCode += html_style.setColor(str(line_no)+"- ","grey")+lineContent+"\n"
        line_no += 1
    styledCode = re.sub(r'editor:(.*?):hightlight:(.*?):(.*?)',r"<span style='color:\2;background-color:\3;' class='hightlight'>"+r'\1'+"</span>",styledCode)
    styledCode = re.sub(r'editor:(.*?):hightlight',"<span class='hightlight'>"+r'\1'+"</span>",styledCode)
    f = open("./quiz_html.html","r")
    quiz_html = str(f.read())
    f.close()
    styledCode = styledCode.replace("(",html_style.setColor("(","grey"))
    styledCode = styledCode.replace(")",html_style.setColor(")","grey"))
    quiz_html_1 = quiz_html.split('<pre class="codeText">')[0]+'<pre class="codeText">'+styledCode+"\n"
    quiz_html_2 = quiz_html.split('<pre class="codeText">')[1]
    quiz_html_2 = quiz_html_2.replace('<h2 id="language" style="position:relative;bottom:0px;text-align:center;color:#4c4;font-size:25px">','<h2 id="language" style="position:relative;bottom:0px;text-align:center;color:#4c4;font-size:25px">'+lan.upper())
    
    toWrite = quiz_html_1+quiz_html_2
    removeEmptyLines = ""
    for lineContent in toWrite.splitlines():
        if lineContent.strip():
            removeEmptyLines += lineContent+"\n"
    toWrite = removeEmptyLines
    path = current_path+"/"+str(message.from_user.id)+"_code_preview.html"
    f = open(path,"w")
    f.write(str(toWrite))
    f.close()
    preview_page(message,toWrite,path,class_="codePanel")
def gen_code_lan(message):
    lan = message.text
    txtJson = checkLanguage(lan)
    if txtJson:
        msg = bot.reply_to(message,"Enter Code Now:")
        bot.register_next_step_handler(msg,gen_code_code,lan)
    else:
        bot.reply_to(message,"No Supported Language")
def add_language_password(message,theLan,txtJson):
    txtJson["Languages"][theLan] = {}
    txtJson["Languages"][theLan]["commands"] = {}
    if message.text == "yes":
        txtJson["Languages"][theLan]["passwords"] = {}
    f = open("commands.json","w")
    toWrite = json.dumps(txtJson)
    f.write(toWrite)
    f.close()
    bot.reply_to(message,"Languages Updated !\n"+theLan+" New Added")
def get_protected_example(message,the_example,txtJson):
    the_password = the_example["password"]
    if message.text == the_password:
        file_id = str(the_example["fileId"])
        if file_id != "":
            documentType = "document"
            try:
                documentType = str(the_example["type"])
            except:
                something=1
            file_info = bot.get_file(file_id)
            file_path = file_info.file_path
            file_name = file_path.split("/")[len(file_path.split("/"))-1]
            download_url = bot.get_file_url(file_id)
            try:
                r = requests.get(download_url).content
                with open(file_name, 'wb') as new_file:
                    new_file.write(r)
                f = open(file_name,"rb")
                if documentType == "photo":
                    bot.send_photo(message.chat.id,file_id,caption="Photo By @PLibrary_bot")
                else:
                    bot.send_document(message.chat.id,f)
                f.close()
                os.remove(file_name)
            except Exception as e:
                bot.send_message(AdminID,e)
        if str(language) == "html":
            reply = "#"+str(language)+"\n"
            Example = str(txtJson["Languages"][language]["commands"][command][userLang]["example"])
            
            reply += Example
            bot.reply_to(message,reply,disable_web_page_preview=True)
            return
        reply = "#"+str(language)+"\n"
        Example = str(txtJson["Languages"][language]["commands"][command][userLang]["example"])
        
        # Example = escape(Example)
        StyledExample =styleExample(Example)
        reply += StyledExample
        
        try:
            bot.reply_to(message,reply,parse_mode="html",disable_web_page_preview=True)
        except:
            bot.reply_to(message,"This Example Has Error Sent To Admin Try Later")
            bot.send_message(AdminID,userMessage+"\n Example Has Error Maybe not ended tag")
        return
#BOT COMMANDS HANDLER
@bot.message_handler(commands=['html'])
def LaunchHtml(message):
    msg = bot.reply_to(message,"Now Send HTML Me Code:")
    bot.register_next_step_handler(msg, html_code_run)


@bot.message_handler(commands=['cs'])
def LaunchCs(message):
    msg = bot.reply_to(message,"Now Send C# Me Code:")
    bot.register_next_step_handler(msg, cs_code_run)


@bot.message_handler(commands=['python'])
def LaunchPython(message):
    msg = bot.reply_to(message,"Now Send Me Python Code:")
    bot.register_next_step_handler(msg, python_code_run)


@bot.message_handler(commands=['php'])
def LaunchPHP(message):
    msg = bot.reply_to(message,"Now Send Me PHP Code:")
    bot.register_next_step_handler(msg, php_code_run)


@bot.message_handler(commands=['c'])
def LaunchC(message):
    msg = bot.reply_to(message,"Now Send Me C Code:")
    bot.register_next_step_handler(msg, c_code_run)


@bot.message_handler(commands=['cpp'])
def LaunchCpp(message):
    msg = bot.reply_to(message,"Now Send Me C++ Code:")
    bot.register_next_step_handler(msg, cpp_code_run)


@bot.message_handler(commands=['java'])
def LaunchJava(message):
    msg = bot.reply_to(message,"Now Send Me Java Code:")
    bot.register_next_step_handler(msg, java_code_run)


@bot.message_handler(commands=['examples'])
def w3schools_Examples(message):
    markup = types.ReplyKeyboardMarkup()
    Languages = ["php","java","cpp","python","js","html","css","sql"]
    for x in Languages:
        markup.add(str(x))
    msg = bot.reply_to(message,"Choose Language:",reply_markup=markup)
    bot.register_next_step_handler(msg, get_examples)
@bot.poll_handler(func=lambda message: True)
def PoolHandler(obj):
    yescount = str(obj.options[0])
    yescount = json.loads(yescount.replace("'",'"'))["voter_count"]
    nocount = str(obj.options[1])
    nocount = json.loads(nocount.replace("'",'"'))["voter_count"]
    if int(yescount) > int(nocount) and int(yescount) > 20:
        postId = str(obj.question)
        postId = re.search("#[0-9]+",postId)
        postId = str(postId.group(0)).split("#")[1]
        f = open("usersPost.json","r")
        txtJson = json.loads(f.read())
        f.close()
        for userid in txtJson["users"]:
            for x in range(len(txtJson["users"][userid]["Pending"])):
                if str(txtJson["users"][userid]["Pending"][x]["pid"]) == str(postId):
                    commandID = str(txtJson["users"][userid]["Pending"][x]["id"])
                    userInput = str(txtJson["users"][userid]["Pending"][x]["input"])
                    pLan = str(txtJson["users"][userid]["Pending"][x]["lan"])
                    Example = str(txtJson["users"][userid]["Pending"][x]["example"])
                    lang = str(txtJson["users"][userid]["Pending"][x]["lang"])
                    reply1 = "#"+pLan+"\n"+Example+"\n"
                    reply2 = "User ID: "+str(userid)+"\nPost ID: "+postId+"\nCommand ID: "+commandID+"\nUser input: "+userInput+"\nExample language: "+lang
                    msg = bot.send_message("1625235944",reply1)
                    bot.reply_to(msg,reply2)

@bot.message_handler(commands=['stackoverflow'])
def sof_command(message):
    msg = bot.reply_to(message,"Send Me Something To Search:")
    bot.register_next_step_handler(msg, sof_do_search)


@bot.message_handler(user_lang="en",commands=['languages','help'])
def en_getLanguages(message):
    f = open("commands.json","r")
    txtJson = json.loads(f.read())
    f.close()
    markup = types.ReplyKeyboardMarkup(row_width=2)
    for language in txtJson["Languages"]:
        markup.add("-» "+str(language))
        
    bot.reply_to(message,"Available Languages:-",reply_markup=markup)
#BOT COMMANDS HANDLER
@bot.message_handler(user_lang="ar",commands=['languages','help'])
def ar_getLanguages(message):
    f = open("commands.json","r")
    txtJson = json.loads(f.read())
    f.close()
    markup = types.ReplyKeyboardMarkup(row_width=2)
    for language in txtJson["Languages"]:
        markup.add("عرض اوامر "+str(language))
        
    bot.reply_to(message,"اللغات المتاحة:-",reply_markup=markup)

@bot.message_handler(commands=['edit'],is_admin=True)
def edit_command(message):
    # Setup Messages Variables
    msg = bot.reply_to(message,"Enter Language:-")
    editCommandProg[message.from_user.id] = {}
    bot.register_next_step_handler(msg, edit_lan_step)

@bot.message_handler(commands=['quiz'])
def edit_command(message):
    msg = bot.reply_to(message,"Choose Language:-")
    bot.register_next_step_handler(msg, quiz_random)


@bot.message_handler(func=lambda message: True, content_types=['document'])
def command_handle_document(message):
    try:
        file_name = message.document.file_name
        if str(file_name) == "commands.json" and str(message.from_user.id) == "1625235944":
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
            
            bot.reply_to(message,str(file_name)+" Inserted")
            PostRandom()
        if str(file_name) == "usersPost.json" and str(message.from_user.id) == "1625235944":
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message,str(file_name)+" Inserted")
        if str(file_name) == "languages.json" and str(message.from_user.id) == "1625235944":
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message,str(file_name)+" Inserted")
    except:
        bot.reply_to(message,"Failed To Update")


@bot.inline_handler(lambda query: query.query != '')
def query_text(inline_query):
    try:
        if len(commands) == 0:
            f = open("commands.json","r")
            txtJson = json.loads(f.read())
            f.close()
            for lan in txtJson["Languages"]:
                for commandID in txtJson["Languages"][lan]["commands"]:
                    if txtJson["Languages"][lan]["commands"][commandID]["ar"]["input"] != "":
                        addToCommand = str(txtJson["Languages"][lan]["commands"][commandID]["ar"]["input"])
                        commands.append(addToCommand.lower())
                    if txtJson["Languages"][lan]["commands"][commandID]["en"]["input"] != "":
                        addToCommand = str(txtJson["Languages"][lan]["commands"][commandID]["en"]["input"])
                        commands.append(addToCommand)
        isFounded = False
        r_s = []
        for x in range(len(commands)):
            user_text = str(inline_query.query).lower()
            searchIn = str(commands[x]).lower()
            if re.search(user_text,searchIn):
                r = types.InlineQueryResultArticle(str(x), commands[x], types.InputTextMessageContent(commands[x]))
                r_s.append(r)
        if len(r_s) > 0:
            return bot.answer_inline_query(inline_query.id, r_s)
        r = types.InlineQueryResultArticle('1', str(inline_query.query), types.InputTextMessageContent('hi'))
        bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(str(e))



@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not os.path.exists("usersPost.json"):
        usersPost = {
            "users":{
                "user":{
                    "Pending":[
                        
                    ],
                    "Published":[
                        
                    ]
                }
            }
        }
        f = open("usersPost.json","w")
        toWrite = json.dumps(usersPost)
        f.write(toWrite)
        f.close()
    result = addUser(message.from_user)
    userLang = getLang(str(message.from_user.id))
    result = addUser(message.from_user)
    bot.send_message("1625235944",result)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    ar = types.KeyboardButton('العربية')
    en = types.KeyboardButton('English')
    markup.add(ar, en)
    msg = bot.send_message(message.from_user.id, "Choose Language:", reply_markup=markup)
    bot.register_next_step_handler(msg, lang_step)


@bot.message_handler(is_admin=True) # Check if user is admin
def admin_rep(message):
    userId = str(message.from_user.id)
    userFullName = str(message.from_user.first_name)+" "+str(message.from_user.last_name)
    userMessage = str(message.text)
    chatId = str(message.chat.id)
    userLang = getLang(message.from_user.id)
    if userMessage == "post quiz":
        post_random_quiz()
    if userMessage.lower() == "/editor delete keyword":
        msg = bot.reply_to(message,"Choose Language",reply_markup=replyMarkupLanguages())
        bot.register_next_step_handler(msg,delete_keyword_lan)
    if userMessage.lower() == "/editor code":
        msg = bot.reply_to(message,"Choose Language",reply_markup=replyMarkupLanguages())
        bot.register_next_step_handler(msg,gen_code_lan)
    if userMessage.lower() == "/editor keyword":
        newKeyword = Keywords(message.from_user.id)
        msg = bot.reply_to(message,"Choose Language:")
        bot.register_next_step_handler(msg,insert_keyword_lan,newKeyword)
    if userMessage.lower() == "delete quiz":
        msg = bot.reply_to(message,"Choose Language")
        bot.register_next_step_handler(msg,delete_quiz_id)
    if userMessage.lower() == "add quiz":
        f = open("commands.json","r")
        markup = types.ReplyKeyboardMarkup()
        txtJson = json.loads(f.read())
        for language in txtJson["Languages"]:
            markup.add(str(language))
        msg = bot.reply_to(message,"Choose Language:",reply_markup=markup)
        bot.register_next_step_handler(msg, new_quiz_lan)
    if userMessage == "PrepareJson":
        PrepareJson(message)
    if userMessage.lower() == "random post":
        f = open("commands.json","r")
        txtJson = json.loads(f.read())
        f.close()
        AllLang = ["en","ar"]
        selectedLang = random.choice(AllLang)
        AllPLan = []
        AllExamples = []
        for language in txtJson["Languages"]:
            AllPLan.append(language)
        selectedLan = random.choice(AllPLan)
        for command in txtJson["Languages"][selectedLan]["commands"]:
            for x in range(len(txtJson["Languages"][selectedLan]["commands"][command][selectedLang])):
                theTitle = str(txtJson["Languages"][selectedLan]["commands"][command][selectedLang][0])
                theExample = str(txtJson["Languages"][selectedLan]["commands"][command][selectedLang][1])
                toAppend = theTitle+"\n------\n"+styleExample(theExample)
                AllExamples.append(toAppend)
        randomPost = random.choice(AllExamples)
        bot.send_message("-1001582552996",randomPost)
    if userMessage.lower() == "try json":
        temp_def(message)
    if userMessage == "deleteCommand":
        f = open("commands.json","r")
        txtJson = json.loads(f.read())
        f.close()
        markup = types.ReplyKeyboardMarkup(row_width=2)
        for language in txtJson["Languages"]:
            markup.add(str(language))
        msg = bot.reply_to(message,"Choose Programming Language:-",reply_markup=markup)
        bot.register_next_step_handler(msg, delCommand_lan)
    if userMessage == "ar":
        commandID = str(message.reply_to_message.text.splitlines()[0].split(":")[1])
        lan = str(message.reply_to_message.text.splitlines()[2])
        lang = "ar"
        result = newCommandLang(commandID,lan,lang)
        bot.reply_to(message,result)
    if userMessage == "getUsers_":
        bot.reply_to(message,str(getUsers()))
    if userMessage == "getFile":
        try:
            f = open("commands.json","rb")
            msg = bot.send_document("-765340268",f)
            bot.pin_chat_message(msg.chat.id,msg.id)
            f.close()
            newCommandsStr = ""
            try:
                newCommandsStr = str(newCommands)
            except:
                newCommandsStr = "no "
            bot.reply_to(message,newCommandsStr+"new Command Added \nSuccessfully Sent")
            newCommands = 0
            return
        except:
            bot.reply_to(message,"Can't Find File")
            return
    if userMessage == "getCommands":
        try:
            f = open("commands.json","r")
            txt = f.read()
            f.close()
            bot.reply_to(message,"Commands :-\n"+str(txt))
            return
        except Exception:
            bot.reply_to(message,"Can't Read File ")
            return
    splitByLine = userMessage.splitlines()
    theCommand = str(str(splitByLine[0]).split(":")[0])
    if theCommand == "add language":
        theLan = str(str(splitByLine[0]).split(":")[1])
        f = open("commands.json","r")
        txtJson = json.loads(f.read())
        try:
            txtJson["Languages"][theLan]
            return bot.reply_to(message,"Language Allready Exists !")
        except:
            msg = bot.reply_to(message,"Is it containing Passwords")
            bot.register_next_step_handler(msg,add_language_password,theLan,txtJson)
            
    if theCommand == "random post":
        theLan = str(str(splitByLine[0]).split(":")[1])
        PostRandom(theLan)
    if theCommand == "push":
        postId = str(userMessage.split(":")[1])
        f = open("usersPost.json","r")
        txtJson = json.loads(f.read())
        for userid in txtJson["users"]:
            for x in range(len(txtJson["users"][userid]["Pending"])):
                if str(txtJson["users"][userid]["Pending"][x]["pid"]) == str(postId):
                    commandID = str(txtJson["users"][userid]["Pending"][x]["id"])
                    userInput = str(txtJson["users"][userid]["Pending"][x]["input"])
                    u_name = str(txtJson["users"][userid]["Pending"][x]["username"])
                    pLan = str(txtJson["users"][userid]["Pending"][x]["lan"])
                    Example = str(txtJson["users"][userid]["Pending"][x]["example"])+"\n#By: @"+u_name
                    lang = str(txtJson["users"][userid]["Pending"][x]["lang"])
                    AddNewCommand(message,pLan,commandID,userInput,Example,lang)
                    bot.send_message("-1001604626385","This Example Successfully Added\nBy: @"+u_name,reply_to_message_id=int(postId))
    if theCommand == "getPending":
        pendingID = str(str(splitByLine[0]).split(":")[1])
        f = open("usersPost.json","r")
        txtJson = json.loads(f.read())
        f.close()
        for userId in txtJson["users"]:
            for x in range(len(txtJson["users"][userId]["Pending"])):
                pendingid = txtJson["users"][userId]["Pending"][x]["pid"]
                if int(pendingID) == int(pendingid):
                    reply = str(txtJson["users"][userId]["Pending"][x]["id"])+"\n"
                    reply += str(txtJson["users"][userId]["Pending"][x]["lang"])+"\n"
                    reply += str(txtJson["users"][userId]["Pending"][x]["input"])+"\n"
                    reply += str(txtJson["users"][userId]["Pending"][x]["lan"])+"\n"
                    reply += str(txtJson["users"][userId]["Pending"][x]["example"])+"\n"
                    return bot.reply_to(message,reply)
    if theCommand == "lang":
        commandID = str(str(splitByLine[0]).split(":")[1])
        lan = str(str(splitByLine[1]))
        lang = str(str(splitByLine[2]))
        result = newCommandLang(commandID,lan,lang)
        bot.reply_to(message,result)
    if theCommand == "getFile":
        try:
            f = open(str(str(splitByLine[0]).split(":")[1]),"rb")
            bot.send_document(chatId,f)
            f.close()
            return
        except:
            bot.reply_to(message,"File Not Found")
            return
    if theCommand == "editCommand":
        # Setup Messages Variables
        msg = bot.reply_to(message,"Enter Language:-")
        bot.register_next_step_handler(msg, edit_lan_step)
    if theCommand == "newCommand":
        # Setup New Commands
        msg = bot.reply_to(message,"Enter Programming Language:")
        bot.register_next_step_handler(msg, lan_step)
    if theCommand == "deleteLanguage":
        toDelete = str(str(splitByLine[0]).split(":")[1])
        f = open("commands.json","r")
        txt = str(f.read())
        txtJson = json.loads(txt)
        f.close()
        for language in txtJson["Languages"]:
            if toDelete == str(language):
                del txtJson["Languages"][language]
                newJson = json.dumps(txtJson)
                f = open("commands.json","w")
                f.write(newJson)
                f.close()
                bot.reply_to(message,"Language Deleted Successfully")
                return
    if theCommand == "getCommand":
        commandInput = str(str(splitByLine[0]).split(":")[1])
        lang = str(str(splitByLine[0]).split(":")[2])
        f = open("commands.json","r")
        txt = str(f.read())
        txtJson = json.loads(txt)
        f.close()
        for language in txtJson["Languages"]:
            for command in txtJson["Languages"][language]["commands"]:
                if commandInput == str(txtJson["Languages"][language]["commands"][command][lang][0]):
                    commandID = str(command)
                    return bot.reply_to(message,str(command))
        bot.reply_to(message,"Command Not Found")
    if userLang == "en":
        en_user(message)
    if userLang == "ar":
        ar_user(message)


@bot.edited_message_handler(func=lambda message: True)
def editedMessages(message):
    splitByLine = str(message.text).splitlines()
    if str(message.text.split(":")[0]) == "newCommand" or str(message.text.split(":")[0]) == "editCommand":
        commandID = str(str(splitByLine[0]).split(":")[1])
        commandInput = str(splitByLine[1])
        commandLanguage = str(splitByLine[2])
        commandExample = ""
        for x in range(3,len(splitByLine)):
            commandExample += str(splitByLine[x])+"\n"
        
        f = open("commands.json","r")
        txt = str(f.read())
        txtJson = json.loads(txt)
        f.close()
        for language in txtJson["Languages"]:
            for command in txtJson["Languages"][language]["commands"]:
                if commandID == str(command):
                    txtJson["Languages"][language]["commands"][command]["0"] = commandInput
                    txtJson["Languages"][language]["commands"][command]["1"] = commandExample
                    newJson = json.dumps(txtJson)
                    f = open("commands.json","w")
                    f.write(newJson)
                    f.close()
                    bot.reply_to(message,"Updated Successfully !")
                    newCommands += 1
                    return
        bot.reply_to(message,"Command Not Found")


@bot.message_handler(func=lambda message: True,user_lang="en")
def en_user(message):
    isJoined = checkJoin(message.from_user.id)
    if not isJoined:
        return bot.reply_to(message,"To Use This Bot Join Our Channel First\n@PLibrary_channel")
    if not os.path.exists("commands.json"):
        try:
            chatInfo = bot.get_chat("-765340268")
            fileId = chatInfo.pinned_message.document.file_id
            file_name = chatInfo.pinned_message.document.file_name
            file_info = bot.get_file(fileId)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
        except Exception as e:
            something = 1
    if not os.path.exists("usersPost.json"):
        usersPost = {
            "users":{
                "user":{
                    "Pending":[
                        
                    ],
                    "Published":[
                        
                    ]
                }
            }
        }
        f = open("usersPost.json","w")
        toWrite = json.dumps(usersPost)
        f.write(toWrite)
        f.close()
    if str(message.from_user.id) != "1625235944":
        bot.send_message("1625235944",str(message.text))
    newUser = addUser(message.from_user)
    if newUser == "new User : "+str(message.from_user.id):
        bot.send_message("1625235944",newUser)
    userId = str(message.from_user.id)
    userFullName = str(message.from_user.first_name)+" "+str(message.from_user.last_name)
    userMessage = str(message.text)
    chatId = str(message.chat.id)
    userLang = getLang(message.from_user.id)
    #END
    
    
    #END
    #direct Messages
    if re.search("https://stackoverflow.com/questions/[0-9]+/",userMessage):
        link = str(re.search("https://stackoverflow.com/questions/[0-9]+/",userMessage)[0])
        sof_direct_answer(message,link)
    if userMessage == "chatId":
        bot.reply_to(message,str(message.chat.id))
        return
    if userMessage == "id":
        bot.reply_to(message,str(message.from_user.id))
        return
    if str(userMessage.splitlines()[0].split(":")[0]) == "regex":
        try:
            method = str(userMessage.splitlines()[0].split(":")[1])
            text = str(message.reply_to_message.text)
            regex = str(userMessage.splitlines()[1])
            if method == "" or method == "search":
                if re.search(regex,text):
                    output = str(re.search(regex,text)[0])
                    bot.reply_to(message,"#Output:-\n"+escape(output))
                else:
                    bot.reply_to(message,"Regex Not Found AnyThing")
            if method == "findall":
                if re.findall(regex,text):
                    output = str(re.findall(regex,text))
                    bot.reply_to(message,"#Output:-\n"+escape(output))
                else:
                    bot.reply_to(message,"Regex Not Found AnyThing")
            if method == "split":
                if re.split(regex,text):
                    output = str(re.split(regex,text))
                    bot.reply_to(message,"#Output:-\n"+escape(output))
                else:
                    bot.reply_to(message,"Regex Not Found AnyThing")
            if method == "sub":
                if re.sub(regex,text):
                    output = str(re.sub(regex,text))
                    bot.reply_to(message,"#Output:-\n"+escape(output))
                else:
                    bot.reply_to(message,"Regex Not Found AnyThing")
        except:
            something = 1
    #Check If There New Commands
    if userMessage == "new command ➕" or userMessage == "/new":
        markup = types.ReplyKeyboardMarkup(row_width=2)
        if os.path.exists("commands.json"):
            f = open("commands.json","r")
            txtJson = json.loads(f.read())
            f.close()
            for language in txtJson["Languages"]:
                markup.add(str(language))
        else:
            return bot.reply_to(message,"Languages Menu Not Ready Try Later")
        if str(message.chat.type) != "private":
            return bot.reply_to(message,"Sorry This Operation Can't be done in the group")
            
        # Setup New Commands
        newCommandProg[message.from_user.id] = {"id":"","lan":"","lang":"","input":"","example":""}
        
        msg = bot.reply_to(message,"Choose Programming Language:-\n",reply_markup=markup)
        bot.register_next_step_handler(msg, lan_step)
        
    f = open("commands.json","r")
    txt = str(f.read())
    txtJson = json.loads(txt)
    f.close()
    for language in txtJson["Languages"]:
        for command in txtJson["Languages"][language]["commands"]:
            intor = txtJson["Languages"][language]["commands"][command][userLang]["input"]
            if intor == "":
                continue
            if userMessage == intor:
                try:
                    from_user_id = txtJson["Languages"][language]["commands"][command][userLang]["from_user_id"]
                    password = txtJson["Languages"][language]["commands"][command][userLang]["password"]
                    if password and not (from_user_id == message.from_user.id or message.from_user.id == int(AdminID)):
                        the_example = txtJson["Languages"][language]["commands"][command][userLang]
                        msg = bot.reply_to(message,"Password Required Enter Password:")
                        bot.register_next_step_handler(msg,get_protected_example,the_example,txtJson)
                        return
                    else:
                        bot.reply_to(message,"Password :"+str(password))
                except:
                    something=1
                file_id = str(txtJson["Languages"][language]["commands"][command][userLang]["fileId"])
                if file_id != "":
                    documentType = "document"
                    try:
                        documentType = str(txtJson["Languages"][language]["commands"][command][userLang]["type"])
                    except:
                        something=1
                    file_info = bot.get_file(file_id)
                    file_path = file_info.file_path
                    file_name = file_path.split("/")[len(file_path.split("/"))-1]
                    download_url = bot.get_file_url(file_id)
                    try:
                        r = requests.get(download_url).content
                        with open(file_name, 'wb') as new_file:
                            new_file.write(r)
                        f = open(file_name,"rb")
                        if documentType == "photo":
                            bot.send_photo(message.chat.id,file_id,caption="Photo By @PLibrary_bot")
                        else:
                            bot.send_document(message.chat.id,f)
                        f.close()
                        os.remove(file_name)
                    except Exception as e:
                        bot.send_message(AdminID,e)
                if str(language) == "html":
                    reply = "#"+str(language)+"\n"
                    Example = str(txtJson["Languages"][language]["commands"][command][userLang]["example"])
                    
                    reply += Example
                    bot.reply_to(message,reply,disable_web_page_preview=True)
                    return
                reply = "#"+str(language)+"\n"
                Example = str(txtJson["Languages"][language]["commands"][command][userLang]["example"])
                
                # Example = escape(Example)
                StyledExample =styleExample(Example)
                reply += StyledExample
                
                try:
                    bot.reply_to(message,reply,parse_mode="html",disable_web_page_preview=True)
                except:
                    bot.reply_to(message,"This Example Has Error Sent To Admin Try Later")
                    bot.send_message(AdminID,userMessage+"\n Example Has Error Maybe not ended tag")
                return
            
    else:
        if len(userMessage.split(" ")) == 2:
            if str(userMessage.split(" ")[0]) == "translate":
                try:
                    toTranslate = str(userMessage.split(" ")[1])
                    translator = Translator()
                    translated = translator.translate(toTranslate,src='en', dest='ar')
                    bot.reply_to(message,str(translated))
                    return
                except:
                    bot.reply_to(message,"Can't Translate")
                    return
                
        if len(userMessage.split(" ")) == 2:
            theCommand = str(userMessage.split(" ")[0])
            if theCommand == "-»":
                selectedLanguage = str(userMessage.split(" ")[1])
                AllCommands = ""
                f = open("commands.json","r")
                txt = str(f.read())
                txtJson = json.loads(txt)
                f.close()
                markup = types.ReplyKeyboardMarkup()
                for language in txtJson["Languages"]:
                    if str(language) == selectedLanguage:
                        for command in txtJson["Languages"][language]["commands"]:
                            if str(txtJson["Languages"][language]["commands"][command][userLang]["input"]) == "":
                                continue
                            commandInput = str(txtJson["Languages"][language]["commands"][command][userLang]["input"])
                            markup.add(commandInput)
                markup.add("new command ➕")
                bot.reply_to(message,"Commands :-",reply_markup=markup)
                        
        
            


@bot.message_handler(func=lambda message: True,user_lang="ar")
def ar_user(message):
    isJoined = checkJoin(message.from_user.id)
    if not isJoined:
        return bot.reply_to(message,"To Use This Bot Join Our Channel First\n@PLibrary_channel")
    if not os.path.exists("commands.json"):
        try:
            chatInfo = bot.get_chat("-765340268")
            fileId = chatInfo.pinned_message.document.file_id
            file_name = chatInfo.pinned_message.document.file_name
            file_info = bot.get_file(fileId)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
        except Exception as e:
            something = 1
    if not os.path.exists("usersPost.json"):
        usersPost = {
            "users":{
                "user":{
                    "Pending":[
                        
                    ],
                    "Published":[
                        
                    ]
                }
            }
        }
        f = open("usersPost.json","w")
        toWrite = json.dumps(usersPost)
        f.write(toWrite)
        f.close()
    if str(message.from_user.id) != "1625235944":
        bot.send_message("1625235944",str(message.text))
    newUser = addUser(message.from_user)
    if newUser == "new User : "+str(message.from_user.id):
        bot.send_message("1625235944",newUser)
    userId = str(message.from_user.id)
    userFullName = str(message.from_user.first_name)+" "+str(message.from_user.last_name)
    userMessage = str(message.text)
    chatId = str(message.chat.id)
    userLang = getLang(userId)
    #END
    
    
    #END
    #direct Messages
    
    if userMessage == "chatId":
        bot.reply_to(message,str(message.chat.id))
        return
    if userMessage == "id":
        bot.reply_to(message,str(message.from_user.id))
        return
    if str(userMessage.splitlines()[0].split(":")[0]) == "regex":
        try:
            method = str(userMessage.splitlines()[0].split(":")[1])
            text = str(message.reply_to_message.text)
            regex = str(userMessage.splitlines()[1])
            if method == "" or method == "search":
                if re.search(regex,text):
                    output = str(re.search(regex,text)[0])
                    bot.reply_to(message,"#Output:-\n"+escape(output))
                else:
                    bot.reply_to(message,"Regex Not Found AnyThing")
            if method == "findall":
                if re.findall(regex,text):
                    output = str(re.findall(regex,text))
                    bot.reply_to(message,"#Output:-\n"+escape(output))
                else:
                    bot.reply_to(message,"Regex Not Found AnyThing")
            if method == "split":
                if re.split(regex,text):
                    output = str(re.split(regex,text))
                    bot.reply_to(message,"#Output:-\n"+escape(output))
                else:
                    bot.reply_to(message,"Regex Not Found AnyThing")
            if method == "sub":
                if re.sub(regex,text):
                    output = str(re.sub(regex,text))
                    bot.reply_to(message,"#Output:-\n"+escape(output))
                else:
                    bot.reply_to(message,"Regex Not Found AnyThing")
        except:
            something = 1
    #Check If There New Commands
    if userMessage == "عمل امر جديد ➕" or userMessage == "/new":
        markup = types.ReplyKeyboardMarkup(row_width=2)
        if os.path.exists("commands.json"):
            f = open("commands.json","r")
            txtJson = json.loads(f.read())
            f.close()
            for language in txtJson["Languages"]:
                markup.add(str(language))
        else:
            return bot.reply_to(message,"قائمة اللغات غير جاهزة الان حاول لاحقا")
        if str(message.chat.type) != "private":
            return bot.reply_to(message,"هذه الميزة لا تعمل في المجموعة")
        # Setup New Commands
        newCommandProg[message.from_user.id] = {"id":"","lan":"","lang":"","input":"","example":""}
        msg = bot.reply_to(message,"قم بأختيار لغة البرمجة",reply_markup=markup)
        bot.register_next_step_handler(msg, lan_step)
          
    f = open("commands.json","r")
    txt = str(f.read())
    txtJson = json.loads(txt)
    f.close()
    for language in txtJson["Languages"]:
        for command in txtJson["Languages"][language]["commands"]:
            intor = txtJson["Languages"][language]["commands"][command][userLang]["input"]
            if intor == "":
                continue
            if userMessage == intor:
                try:
                    from_user_id = txtJson["Languages"][language]["commands"][command][userLang]["from_user_id"]
                    password = txtJson["Languages"][language]["commands"][command][userLang]["password"]
                    if password and not (from_user_id == message.from_user.id or message.from_user.id == int(AdminID)):
                        the_example = txtJson["Languages"][language]["commands"][command][userLang]
                        msg = bot.reply_to(message,"هذا المثال يحتاج الي كلمة مرور ادخل كلمة المرور:")
                        bot.register_next_step_handler(msg,get_protected_example,the_example,txtJson)
                        return
                    else:
                        bot.reply_to(message,str("Password :"+password))
                except:
                    something=1
                if str(language) == "html":
                    reply = "#"+str(language)+"\n"
                    Example = str(txtJson["Languages"][language]["commands"][command][userLang]["example"])
                    
                    reply += Example
                    bot.reply_to(message,reply,disable_web_page_preview=True)
                    return
                reply = "#"+str(language)+"\n"
                Example = str(txtJson["Languages"][language]["commands"][command][userLang]["example"])
                file_id = str(txtJson["Languages"][language]["commands"][command][userLang]["fileId"])
                # Example = escape(Example)
                if file_id != "":
                    file_info = bot.get_file(file_id)
                    file_path = file_info.file_path
                    file_name = file_path.split("/")[len(file_path.split("/"))-1]
                    downloaded_file = bot.download_file(file_info.file_path)
                    with open(file_name, 'wb') as new_file:
                        new_file.write(downloaded_file)
                    f = open(file_name,"rb")
                    bot.send_document(message.chat.id,f)
                    f.close()
                    os.remove(file_name)
                StyledExample =styleExample(Example)
                reply += StyledExample
                try:
                    bot.reply_to(message,reply,parse_mode="html",disable_web_page_preview=True)
                except:
                    bot.reply_to(message,"This Example Has Error Sent To Admin Try Later")
                    bot.send_message(AdminID,userMessage+"\n Example Has Error Maybe not ended tag")
                return
            
    else:
        if len(userMessage.split(" ")) == 2:
            if str(userMessage.split(" ")[0]) == "translate":
                try:
                    toTranslate = str(userMessage.split(" ")[1])
                    translator = Translator()
                    translated = translator.translate(toTranslate,src='en', dest='ar')
                    bot.reply_to(message,str(translated))
                    return
                except:
                    bot.reply_to(message,"Can't Translate")
                    return
                
        if len(userMessage.split(" ")) == 2:
            theCommand = str(userMessage.split(" ")[0])
            if theCommand == "-»":
                selectedLanguage = str(userMessage.split(" ")[1])
                AllCommands = ""
                f = open("commands.json","r")
                txt = str(f.read())
                txtJson = json.loads(txt)
                f.close()
                markup = types.ReplyKeyboardMarkup()
                for language in txtJson["Languages"]:
                    if str(language) == selectedLanguage:
                        for command in txtJson["Languages"][language]["commands"]:
                            if str(txtJson["Languages"][language]["commands"][command][userLang]["input"]) == "":
                                continue
                            commandInput = str(txtJson["Languages"][language]["commands"][command][userLang]["input"])
                            markup.add(commandInput)
                markup.add("عمل امر جديد ➕")
                bot.reply_to(message,"الأوامر :-",reply_markup=markup)
            

bot.infinity_polling()