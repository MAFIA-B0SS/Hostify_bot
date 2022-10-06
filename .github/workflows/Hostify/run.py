import telebot
import socket,sys,os,requests
import re,time
from telebot import util
import json
inDevolop = False
AdminID = 1625235944
BOT_TOKEN = os.environ.get("HOSTIFY_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
@bot.message_handler(commands=['start', 'help']) 
if not os.path.exists("hosts.json"):
    try:
        chatInfo = bot.get_chat(-1001764050546)
        fileId = chatInfo.pinned_message.document.file_id
        file_name = chatInfo.pinned_message.document.file_name
        file_info = bot.get_file(fileId)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
    except Exception as e:
        bot.send_message(AdminID,str(e))

def send_welcome(message):
    
    bot.reply_to(message, "Welcome to hosts scanning bot Join Our @Hostify Channel To Know How's works")
@bot.message_handler(func=lambda message: True, content_types=['document'])
def command_handle_document(message):
    try:
        if message.from_user.id != AdminID:
            return
        file_name = message.document.file_name
        if str(file_name) == "hosts.json" or str(file_name) == "hostsScans.txt" and str(message.from_user.id) == "1625235944":
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message,str(file_name)+" Inserted")
            
    except:
        bot.reply_to(message,"Failed To Update")
def checkIp (text):
    splitbydot = text.split(".")
    for ipSub in splitbydot:
        if  re.findall("\D", ipSub):
            return False
        if int(ipSub) > 255 or int(ipSub) < 0 or ipSub == "":
            return False
    return True
def getIpInfo(ip):
    url = "https://ipinfo.io/account/search?query="+ip

    headers = requests.structures.CaseInsensitiveDict()
    headers["Host"] = "ipinfo.io"
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; rv:102.0) Gecko/20100101 Firefox/102.0"
    headers["Accept"] = "*/*"
    headers["Accept-Language"] = "en-US,en;q=0.5"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Referer"] = "https://ipinfo.io/account/search"
    headers["Content-Type"] = "application/json"
    headers["Connection"] = "keep-alive"
    headers["Cookie"] = "_ga_RWP85XL4SC=GS1.1.1658463840.3.1.1658465711.42; _ga=GA1.1.1785554479.1657459179; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%2288ddd990-8696-48f9-9749-c290b47d44c2%22; flash=; amp_bc6a9b=4d166a41-68a6-4aae-bf64-b96f50283598R.NzM3MTUx..1g8i2bojf.1g8i47hnt.1c.1.1d; G_ENABLED_IDPS=google; jwt-express=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3MzcxNTEsImVtYWlsIjoiYm90bWFrZXJAdGVtbC5uZXQiLCJjcmVhdGVkIjoiYSBmZXcgc2Vjb25kcyBhZ28oMjAyMi0wNy0yMlQwNDozNzo0Ni41NTBaKSIsInN0cmlwZV9pZCI6bnVsbCwiaWF0IjoxNjU4NDY0NjY2fQ.XRbQQY6JhrAHcbqYIKQOe4gjajkkbAW8lAugzHuXT4I; new_trial=%7B%22trials%22%3A%5B%5D%2C%22user_id%22%3A737151%7D; onboarding=0"
    headers["Sec-Fetch-Dest"] = "empty"
    headers["Sec-Fetch-Mode"] = "cors"
    headers["Sec-Fetch-Site"] = "same-origin"


    resp = requests.get(url, headers=headers)
    result = json.loads(resp.content)
    return result
def convertToHost(text):
    try:
        theHost = str(socket.gethostbyaddr(text)[0])
        return theHost
    except Exception:
        return "Can't Find Host With This Ip"

def revHostsCheck(ip):
    f = open("hosts.json","r")
    txt = str(f.read())
    txtJson = json.loads(txt)
    f.close()
    ipLastDigit = int(ip.split(".")[3])
    for ip2 in txtJson["revHosts"]:
        ip3_1 = ip.split(".")[0]+"."+ip.split(".")[1]+"."+ip.split(".")[2]
        ip3_2 = str(ip2).split(".")[0]+"."+str(ip2).split(".")[1]+"."+str(ip2).split(".")[2]
        if ip3_1 == ip3_2:
            if ipLastDigit >= int(str(ip2).split(".")[3]):
                AllHosts = ""
                if len(txtJson["revHosts"][ip2]) == 0:
                    return "0 Hosts Founded"
                for x in range(0,len(txtJson["revHosts"][ip2])):
                    rHost = str(txtJson["revHosts"][ip2][x]["domain"])
                    rIp = str(txtJson["revHosts"][ip2][x]["ip"])
                    if rHost == "":
                        continue
                    AllHosts += rHost+" | "+rIp + "\n"
                
                return AllHosts
    return ""
def prepareJson(message):
    f = open("hosts.json","r")
    txt = f.read()
    txtJson = json.loads(txt)
    f.close()
    newStructure = {
        "hosts":[
        
        ],
        "revHosts":{
            
        },
        "scannedHosts":{
            "host":{
                "headers":[
                    
                ]
            }
        }
    }
    for ip in txtJson["revHosts"]:
        theip = str(ip)
        for x in range(0,len(txtJson["revHosts"][ip])):
            scannedIp = str(str(txtJson["revHosts"][ip][x]).split(":")[1])
            scannedDomain = str(str(txtJson["revHosts"][ip][x]).split(":")[0])
            if scannedDomain == "-----------" or scannedDomain == "":
                continue
            try:
                newStructure["revHosts"][theip].append({"domain":scannedDomain,"ip":scannedIp})
            except:
                newStructure["revHosts"][theip] = []
                newStructure["revHosts"][theip].append({"domain":scannedDomain,"ip":scannedIp})
    f = open("hosts_new.json","w")
    toWrite = json.dumps(newStructure)
    f.write(toWrite)
    f.close()
    bot.reply_to(message,"Done :)")
def convertToIp(text):
    try:
        ipbyhost = str(socket.getaddrinfo(text,80)[2][4][0])
        return ipbyhost
    except Exception:
        return "Can't reolve Host"
def getLatestUpdate(message):
    f = open("updates.txt","r")
    txt = str(f.read())
    hostsFileId = ""
    hostsScanedFileId = ""
    for line in txt.splitlines():
        if str(line) == "":
            continue
        if str(line.split(":")[0]) == "hosts":
            hostsFileId = str(line)
        if str(line.split(":")[0]) == "hostsScan":
            hostsScanedFileId = str(line)
    if hostsFileId != "":
        file_info = bot.get_file(hostsFileId)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("hosts.txt", 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message,"Hosts Inserted")
    if hostsScanedFileId != "":
        file_info = bot.get_file(hostsScanedFileId)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("hostsScans.txt", 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message,"Hosts Scan Inserted")
def filterHostsScan(text):
    toFilter = text
    # Open File
    f = open("hosts.json","r")
    txt = str(f.read())
    txtJson = json.loads(txt)
    f.close()
    #
    result = ""
    u_headerName = str(text.split(":")[0]).lower()
    u_headerValue = str(text.split(":")[1]).lower()
    for host in txtJson["scannedHosts"]:
        for x in range(0,len(txtJson["scannedHosts"][host]["headers"])):
            headerName = str(txtJson["scannedHosts"][host]["headers"][x]["name"]).lower()
            headerValue = str(txtJson["scannedHosts"][host]["headers"][x]["value"]).lower()
            if re.search(u_headerName,headerName) and re.search(u_headerValue,headerValue):
                result += str(host)+"\n"
                break
    return result 
def filterHosts(text):
    toFilter = str(text.split(":")[1])
    command = str(text.split(":")[0])
    # Open File
    f = open("hosts.json","r")
    txt = str(f.read())
    txtJson = json.loads(txt)
    f.close()
    #
    result = ""
    for ip in txtJson["revHosts"]:
        for x in range(0,len(txtJson["revHosts"][ip])):
            rHost = str(txtJson["revHosts"][ip][x]["domain"])
            rIp = str(txtJson["revHosts"][ip][x]["ip"])
            if command == "end":
                if re.search(toFilter+"$", rHost):
                    result += rHost+" | "+rIp+"\n"
            if command == "in":
                if re.search(toFilter, rHost):
                    result += rHost+" | "+rIp+"\n"
            if command == "start":
                if re.search("^"+toFilter, rHost):
                    result += rHost+" | "+rIp+"\n"
    return result
def removeEmptyLines(txt):
    result = ""
    for line in txt.splitlines():
        if str(line) == "":
            continue
        result+= str(line)+"\n"
    return result
def UpdateHosts():
    try:
        f = open("hosts.json","rb")
        msg = bot.send_document("-1001764050546",f)
        bot.pin_chat_message("-1001764050546",msg.id)
        f.close()
    except:
        something = 0
def scanHost(text,message):
    #Check if Founded
    f = open("hosts.json","r")
    txt = str(f.read())
    txtJson = json.loads(txt)
    f.close()
    limitSearch = 0
    
    finishMsg = ""
    nextMessage = int(message.id)+1
    successScan = 0
    failedScan = 0
    
    for line in text.splitlines():
        isExists = False
        for scannedHost in txtJson["scannedHosts"]:
            theHost = str(scannedHost)
            if theHost == str(line):
                reply = "Host :"+theHost+"\n"
                AllHeaders = ""
                for x in range(0,len(txtJson["scannedHosts"][theHost]["headers"])):
                    headerName = str(txtJson["scannedHosts"][theHost]["headers"][x]["name"])
                    headerValue = str(txtJson["scannedHosts"][theHost]["headers"][x]["value"])
                    AllHeaders += headerName + " : " + headerValue+"\n"
                reply += AllHeaders
                bot.reply_to(message,reply)
                isExists = True
                break
        if isExists:
            continue
        try:
            bot.reply_to(message,"Scanning Host : "+str(line))
            r = requests.get("http://"+str(line),timeout=5.0)
            
            finishMsg = "Host : "+str(line)+"\n"
            finishMsg += "Status Code : "+str(r.status_code)+"\n"
            txtJson["scannedHosts"][str(line)] = {"headers":[]}
            for header in r.headers:
                finishMsg += header + " : "+ r.headers[header]+"\n"
                txtJson["scannedHosts"][str(line)]["headers"].append({"name":str(header),"value":str(r.headers[header])})
            
            bot.edit_message_text(finishMsg, str(message.chat.id), str(nextMessage))
            successScan+=1
        except Exception as e:
            failedScan+=1
            bot.edit_message_text("Host : "+str(line)+"\nScan Failed\n"+str(e), str(message.chat.id), str(nextMessage))
        nextMessage+=1
        limitSearch +=1
        if limitSearch == 4:
            break
    f = open("hosts.json","w")
    toWrite = json.dumps(txtJson)
    f.write(toWrite)
    f.close()
    UpdateHosts()
    bot.reply_to(message,"Scan Finished\n"+str(successScan)+" Host Scanned\n"+str(failedScan)+" Failed Scan\n*Note 4 scan allowed per request")
def getServer(text):
    f = open("hosts.json","r")
    txt = f.read()
    txtJson = json.loads(txt)
    f.close()
    result = ""
    for line in text.splitlines():
        lineContent = str(line)
        try:
            r = requests.get("http://"+lineContent)
            result += lineContent+" "+r.headers['Server']+"\n"
        except Exception:
            result = lineContent+" Failed"
    return result
def goClean(text):
    result = ""
    splitbyLines = text.splitlines()
    for line in splitbyLines:
        if line == "-----------":
            continue
        removeIp = line.split("|")[0]
        removeEffect = removeIp.split("->")[1]
        result = result + str(removeEffect)+"\n"
    return result
  
def hostOptions(message,host):
    result = ""
    try:
        r = requests.options("http://"+host,timeout=5.0)
        result = "-> Host : "+host+"\nStatus Code : "+str(r.status_code)+"\n"
        for header in r.headers:
            if str(header).lower() == "allow":
                result += " -> "+header + " : "+ r.headers[header]+"\n"
    except:
        result = "Can't Resovle Host : "+host
    bot.reply_to(message,result)
def getHostsCount(message):
    f = open("hosts.json","r")
    txt = str(f.read())
    txtJson = json.loads(txt)
    f.close()
    AllHostsCount = 0
    for ip in txtJson["revHosts"]:
        for x in range(0,len(txtJson["revHosts"][ip])):
            AllHostsCount+=1
    bot.reply_to(message,str(AllHostsCount))
def getHostsTxt(message):
    f = open("hosts.txt","r")
    txt = str(f.read())
    f.close()
    result = ""
    for line in txt.splitlines():
        if str(line) == "":
            continue
        hosts = line.split(":")[1].split(" ")
        for host in hosts:
            result += str(host.split("|")[0]).replace("->","\n")
    f = open("temp.txt","w")
    f.write(result)
    f = open("temp.txt","rb")
    bot.send_document(str(message.chat.id),f)
    f.close()
def checkIfExist(ip):
    f = open("hosts.txt","r")
    txt = str(f.read())
    f.close()
    for line in txt.splitlines():
        if str(line) == "":
            continue
        if str(line.split(":")[0]) == ip:
            return str(line.split(":")[1])
    else:
        return ""
def ipList(message):
    msgTx = str(message.text)
    chatId = str(message.chat.id)
    Splitbylines = str(msgTx.split(":")[1]).splitlines()
    FoundedHosts = ""
    numberOfIps = ""
    Progress = int(message.id)+1
    bot.reply_to(message,"Getting Hosts....")
    newHosts = ""
    f = open("hosts.json","r")
    txt = str(f.read())
    txtJson = json.loads(txt)
    f.close()
    for ip in Splitbylines:
        if str(ip) == "":
            continue
        if not checkIp(str(ip)):
            continue
        # Check if Ip Is Exist
        
        
        splitbydot = ip.split(".")
        ip1 = splitbydot[0]
        ip2 = splitbydot[1]
        ip3 = splitbydot[2]
        ip4 = splitbydot[3]
        ip_3 = ip1+"."+ip2+"."+ip3+"."
        numberOfIps += "\n"+ip+ " To "+ip_3+"255"
        isExists =revHostsCheck(str(ip))
        if isExists != "":
            FoundedHosts += "\n"+isExists
            continue
        txtJson["revHosts"][ip] = []
        
        if ip1 == "127" and ip2 == "0" and ip3 == "0" and ip4 == "1":
            bot.reply_to(message,"Sorry This Ip Is Blocked Try Other One")
            return
        for x in range(int(ip4),256):
            
            if x == 100 or x==150 or x==200 or x>250:
                try:
                    bot.edit_message_text(ip_3+str(x), chatId, str(Progress))
                except Exception:
                    something=1
            foundedHost = convertToHost(ip_3+str(x))
            if foundedHost == "Can't Find Host With This Ip":
                continue
            try:
                newHosts += "\n ->  "+foundedHost+ " | " + ip_3+str(x)
                FoundedHosts = "\n"+FoundedHosts+"\n ->  "+foundedHost+ " | " + ip_3+str(x)
                txtJson["revHosts"][ip].append({"domain":foundedHost,"ip":ip_3+str(x)})
                newHosts += foundedHost+"\n"
            except Exception:
                continue
        
        FoundedHosts = FoundedHosts+"\n-----------"
        
        
    # Done From Searching ..
    try:
        f = open("hosts.json","w")
        toWrite = json.dumps(txtJson)
        f.write(toWrite)
        f.close()
        f = open("hosts.json","rb")
        msg = bot.send_document("-1001764050546",f)
        bot.pin_chat_message("-1001764050546",msg.id)
        f.close()
    except:
        something = 0
    bot.edit_message_text("Done :\nIP List:\n"+numberOfIps, chatId, str(Progress))
    isFromGroup = False
    if str(message.chat.id) == "-1001764050546":
        isFromGroup = True
    splitted_text = util.split_string(newHosts, 3000)
    for text in splitted_text:
        bot.reply_to(message, text)
    bot.send_message(chatId,"Done :\nIP List:\n"+numberOfIps)
    f.close()
@bot.message_handler(func=lambda message: True)
def test(message):
    
    isIp = checkIp(str(message.text))
    isScan = False
    toIp = False
    toHost = False
    isList = False
    isGo = False
    getPorts = False
    isFromGroup = False
    #Setup Message Variables
    message_text = str(message.text)
    message_id = str(message.id)
    #Setup User Information
    user_name = str(message.from_user.first_name)+" "+str(message.from_user.last_name)
    user_id = str(message.from_user.id)
    #Setup Chat Information
    chat_id = str(message.chat.id)
    bot.send_message("1625235944",user_name+"\n"+message_text)
    #Functions
    def isiPFunc(message,ip):
        # All Hosts For Print Result
        AllHosts = ""
        #Read Hosts File
        f = open("hosts.json", "r")
        txt = str(f.read())
        txtJson = json.loads(txt)
        f.close()
        #READ END
        #Prepare For Scan
        txtJson["revHosts"][ip] = []
        splitbydot = ip.split(".")
        ip1 = splitbydot[0]
        ip2 = splitbydot[1]
        ip3 = splitbydot[2]
        ip4 = splitbydot[3]
        ip_3 = ip1+"."+ip2+"."+ip3+"."
        if ip1 == "127" and ip2 == "0" and ip3 == "0" and ip4 == "1":
            bot.reply_to(message,"Sorry This Ip Is Blocked Try Other One")
            return
        FoundedHosts = ""
        Progress = int(message.id)+1
        bot.reply_to(message,"Getting Hosts....")
        startFrom = 0
        if isGo:
            startFrom = 0
        else:
            startFrom = int(ip4)
        
        for x in range(startFrom,256):
            if x == 100 or x==150 or x==200 or x>250:
                try:
                    bot.edit_message_text(ip_3+str(x), chat_id, str(Progress))
                    
                except Exception:
                    something=1
            foundedHost = convertToHost(ip_3+str(x))
            if foundedHost == "Can't Find Host With This Ip":
                continue
            try:
                FoundedHosts = "\n"+FoundedHosts+"\n ->  "+foundedHost+ " | " + ip_3+str(x)
                txtJson["revHosts"][ip].append({"domain":foundedHost,"ip":ip_3+str(x)})
                
            except Exception:
                continue
        try:
            #Prepare File For Write
            f = open("hosts.json","w")
            toWrite = json.dumps(txtJson)
            f.write(toWrite)
            f.close()
        except:
            something = 0
        
        bot.edit_message_text("Done :\n"+str(ip_3)+str(startFrom)+" To "+str(ip_3)+"255", chat_id, str(Progress))
        splitted_text = util.split_string(FoundedHosts, 3000)
        
        for text in splitted_text:
            bot.reply_to(message, text)
        bot.send_message(chat_id,"Done :\n"+ip+" To "+ip_3+"255")
        time.sleep(0.7)
    
    
    #Check If It's Admin
    isAdmin = False
    if chat_id == "1625235944" or chat_id == "1087968824":
        isAdmin = True
    #END
    
    if chat_id == "-1001764050546":
        isFromGroup = True
    if not isAdmin:
        notmember = 1
    else:
        
        if str(message_text.split(":")[0]) == "getFile":
            f = open(str(message_text.split(":")[1]),"rb")
            bot.send_document(chat_id,f)
            f.close()
        if message_text == "Prepare Json":
            prepareJson(message)
        if message_text == "insertFiles":
            getLatestUpdate(message)
        if len(message_text.split(" ")) == 2:
            theCommand = str(message_text.split(" ")[0])
            param = str(message_text.split(" ")[1])
            if theCommand == "AddMember":
                for member in usersReadList:
                    if str(member) == param:
                        bot.reply_to(message,"Allready a Member")
                        return
                # Add New Member
                try:
                    usersFile = open("users.txt","a")
                    usersFile.write("\n"+param)
                    bot.reply_to(message,"Now Member "+param+" Can Use This Bot")
                    return
                except Exception:
                    bot.reply_to(message,"Sorry Admin Try Again")
                    return
        if str(message.text) == "clear members":
            try:
                usersFile = open("users.txt","w")
                usersFile.write("No Users")
                usersFile.close()
                bot.reply_to(message,"Successfully Removed Users")
                return
            except Exception:
                bot.reply_to(message,"Something Happend Try Again")
                return
        if str(message.text) == "member":
            memberId = str(message.reply_to_message.from_user.id)
            memberName = str(message.reply_to_message.from_user.first_name)
            for member in usersReadList:
                if str(member) == memberId:
                    bot.reply_to(message,"Allready a Member")
                    return
            # Add New Member
            try:
                usersFile = open("users.txt","a")
                usersFile.write("\n"+memberId)
                bot.reply_to(message,"Now Member "+ memberName +" Can Use This Bot")
                return
            except Exception:
                bot.reply_to(message,"Sorry Admin Try Again")
                return
    #Direct Reply Message
    if message_text.lower() == "filter ips":
        searchIn = str(message.reply_to_message.text)
        AllIps = re.findall("\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",searchIn)
        bot.reply_to(message,str(AllIps))
    if message_text.lower() == "getInfo":
        p = str(message.reply_to_message.text)
        for line in p.splitlines():
            user_ip = str(line)
            searchType = ""
            reply = ""
            if re.search("as(\d)+",user_ip):
                searchType = "asn"
            
            result = getIpInfo(user_ip)
            if searchType == "asn":
                #Variables
                CompanyName = "Company : "+str(result["asn"]["name"])+"\n"
                num_ips = "Number Of Ips : "+str(result["asn"]["num_ips"])+"\n"
                ip_ranges = "Ip Ranges :-\n"
                xip_ranges = result["asn"]["prefixes"]
                for x in range(0,len(xip_ranges)):
                    ip_ranges += "  "+str(xip_ranges[x]["netblock"])+"\n"
                reply = CompanyName+num_ips+ip_ranges
            else:
                Company = "Company : "+str(result["company"]["name"])+"\n"
                Company_Domains = "Company Domain : "+str(result["asn"]["domain"])+"\n"
                hostname = "Host : "+str(result["hostname"])+"\n"
                inRange = "Route : "+str(result["asn"]["route"])+"\n"
                reply = Company+Company_Domains+hostname+inRange
            bot.reply_to(message,reply)
    if message_text.lower() == "all hosts count":
        getHostsCount(message)
    if message_text.lower() == "get hosts txt":
        getHostsTxt(message)
    if len(message_text.split(" ")) == 3:
        if len(message_text.split(" ")[2].split(":")):
            if str(message_text.split(" ")[0]) == "get" and str(message_text.split(" ")[1]) == "hosts":
                filterHost = str(message_text.split(" ")[2])
                findEnd = filterHosts(filterHost)
                splitted_text = util.split_string(findEnd, 3000)
                for text in splitted_text:
                    bot.reply_to(message, text)
                return
    if len(message_text.split(" ")) == 4:
        theCommand = str(message_text.split(" ")[2])
        if theCommand == "header":
            if str(message_text.split(" ")[0]) == "get" and str(message_text.split(" ")[1]) == "hosts":
                filterHost = str(message_text.split(" ")[3])
                findEnd = filterHostsScan(filterHost)
                splitted_text = util.split_string(findEnd, 3000)
                for text in splitted_text:
                    bot.reply_to(message, text)
                return
    if message_text.lower() == "bug" or message_text == "bugs":
        bot.reply_to(message,"@MAFIA_B0SS There is some bugs")
        return
    if message_text.lower() == "id":
        bot.reply_to(message,user_id)
        return
    if message_text.lower() == "chatid":
        bot.reply_to(message,chat_id)
        return
    if message_text.lower() == "founded hosts":
        if isAdmin:
            f = open("hosts.txt", "rb")
            bot.send_document(chat_id,f)
            f.close()
            f = open("hostsScans.txt", "rb")
            bot.send_document(chat_id,f)
            f.close()
            return
    if message_text.lower() == "indevolop":
        if inDevolop:
            bot.reply_to(message,"Yes , some fixed is very important for me :)")
        else:
            bot.reply_to(message,"No , You Can Use Me Now type SD_HOSTS_COMMANDS to see what i can do")
        return
    if message_text.upper() == "SD_HOSTS_COMMANDS":
        reply = "@Hostify"
        bot.reply_to(message,reply)
        return
    if message_text.lower() == "toip":
        message_text = "ip:"+str(message.reply_to_message_text)
        toIp = True
    elif message_text.lower() == "scan":
        message_text = "ip:"+str(message.reply_to_message_text)
        isScan = True
    elif message_text.lower() == "go":
        message_text = str(message.reply_to_message_text)
        isIp = checkIp(message_text)
    elif message_text.lower() == "toHost":
        message_text = "ip:"+str(message.reply_to_message_text)
        toHost = True
    elif message_text.lower() == "clean":
        message_text = str(message.reply_to_message_text)
        result = goClean(message_text)
        bot.reply_to(message,result)
    elif message_text.lower() == "server":
        message_text = "ip:"+str(message.reply_to_message.text)
        theServer = getServer(str(message_text.split(":")[1]))
        bot.reply_to(message,"Servers: \n"+theServer)
        
    elif str(message_text.split(":")[0]) != "":
        theCommand = str(message_text.split(":")[0])
        if theCommand == "getInfo":
            try:
                user_ip = str(message_text.split(":")[1])
                searchType = ""
                reply = ""
                if re.search("as(\d)+",user_ip):
                    searchType = "asn"
                
                result = getIpInfo(user_ip)
                if searchType == "asn":
                    #Variables
                    CompanyName = "Company : "+str(result["asn"]["name"])+"\n"
                    num_ips = "Number Of Ips : "+str(result["asn"]["num_ips"])+"\n"
                    ip_ranges = "Ip Ranges :-\n"
                    xip_ranges = result["asn"]["prefixes"]
                    for x in range(0,len(xip_ranges)):
                        ip_ranges += "  "+str(xip_ranges[x]["netblock"])+"\n"
                    reply = CompanyName+num_ips+ip_ranges
                else:
                    Company = "Company : "+str(result["company"]["name"])+"\n"
                    Company_Domains = "Company Domain : "+str(result["asn"]["domain"])+"\n"
                    hostname = "Host : "+str(result["hostname"])+"\n"
                    inRange = "Route : "+str(result["asn"]["route"])+"\n"
                    reply = Company+Company_Domains+hostname+inRange
                bot.reply_to(message,reply)
            except Exception as e:
                bot.reply_to(message,str(e))
        if theCommand == "options":
            hostOptions(message,str(message_text.split(":")[1]))
        if theCommand == "toIp":
            toIp = True
        if theCommand == "scan":
            isScan = True
        if theCommand == "toHost":
            toHost = True
        if theCommand == "server":
            theServer = getServer(str(message_text.split(":")[1]))
            bot.reply_to(message,"Server: "+theServer)
        if theCommand == "payload":
            payload = GeneratePayload(str(message_text))
            bot.reply_to(message,payload)
        if theCommand == "list":
            isList = True
        if theCommand == "ports":
            getPorts = True
    if len(message_text.split(" ")) == 2:
        theCommand = message_text.split(" ")[0]
        param = message_text.split(" ")[1]
        if theCommand == "go":
            message_text = str(message.reply_to_message.text)
            isIp = checkIp(message_text)
            if isIp:
                ip3 = str(message_text.split(".")[0])+"."+str(message_text.split(".")[1])+"."+str(message_text.split(".")[2])+"."
                message_text = str(ip3)+str(param)
                
    
    if inDevolop:
        if isIp or isScan or toIp or toHost:
            if not isAdmin:
                bot.reply_to(message,"Devolopment Mode Activated Please Try Again Later")
                return
    
    
    #END
    if toIp:
        result = convertToIp(str(message_text.split(":")[1]))
        bot.reply_to(message,result)
    if isScan:
        
        result = scanHost(str(message_text.split(":")[1]),message)
    if isIp:
        result = revHostsCheck(message_text)
        if result == "":
            isiPFunc(message,message_text)
        else:
            splitted_text = util.split_string(result, 3000)
            for text in splitted_text:
                bot.reply_to(message, text)
            ip_3 = str(message_text.split(".")[0])+"."+str(message_text.split(".")[1])+"."+str(message_text.split(".")[2])+"."
            bot.send_message(chat_id,"Done :\n"+message_text+" To "+ip_3+"255")
    if toHost:
        result = convertToHost(str(message_text.split(":")[1]))
        bot.reply_to(message,result)
                
    #Check if it's Ip
    if isList:
        ipList(message)
bot.infinity_polling()
