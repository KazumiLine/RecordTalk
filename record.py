from linepy import *
from datetime import datetime
import time, random, sys, json, codecs, threading, string, os, requests, timeit, _thread
token = input("login token :")
cl = LINE(token)
print(cl.authToken)
wait = {"chatroom":"u992a6e77041a772b8abd613ea64d4623"}
def detectchat():      #--------talk record will be saved in www folder and save as a txt, and pictures will be saved in tmp folder
    while True:
        try:
            ops = cl.poll.fetchOperations(cl.revision, 50)
            if ops is not None:
                for op in ops:
                    if op.type in [25,26]:
                        if op.message.toType == 0:
                            if "{}.txt".format(op.message._from)  not in os.listdir("www") and "{}.txt".format(op.message.to)  not in os.listdir("www"):
                                rever = []
                                if op.message._from == cl.profile.mid:
                                    talks = cl.getRecentMessagesV2(op.message.to)[1:]
                                    user = op.message.to
                                    talkto = cl.getContact(op.message.to).displayName
                                else:
                                    talks = cl.getRecentMessagesV2(op.message._from)[1:]
                                    user = op.message._from
                                    talkto = cl.getContact(op.message._from).displayName
                                for mess in talks:
                                   if mess.contentType == 0 and mess.text != None:
                                       if mess._from == cl.profile.mid:
                                           rever.append("\nsend text:{}".format(mess.text))
                                       else:
                                           rever.append("\nrecieve text:{}".format(mess.text))
                                   elif mess.contentType == 1:
                                       rever.append("\n[{}] PICTURE".format(datetime.strftime(datetime.now(),"%H:%M")))
                                       cl.downloadObjectMsg(mess.id, saveAs="tmp/{}.png".format(mess.id))
                                   elif mess.contentType == 7:
                                       rever.append("\n[{}] STICKER".format(datetime.strftime(datetime.now(),"%H:%M")))
                                rever.reverse()
                                for x in rever:
                                    talkto += x
                                with open("www/{}.txt".format(user),"a") as talk:
                                    talk.write(talkto)
                            if op.message.contentType == 0:
                                if op.message._from == cl.profile.mid:
                                    print("self: place:{} text:{}".format(cl.getContact(op.message.to).displayName,op.message.text))
                                    wait["chatroom"] = op.message.to
                                    with open("www/{}.txt".format(op.message.to),"a") as talk:
                                        talk.write("\n[{}] send text:{}".format(datetime.strftime(datetime.now(),"%H:%M"),op.message.text))
                                else:
                                    print("{}: self text:{}".format(cl.getContact(op.message._from).displayName,op.message.text))
                                    wait["chatroom"] = op.message._from
                                    with open("www/{}.txt".format(op.message._from),"a") as talk:
                                        talk.write("\n[{}] recieve text:{}".format(datetime.strftime(datetime.now(),"%H:%M"),op.message.text))
                            elif op.message.contentType == 1:
                                print("\n[{}] PICTURE".format(datetime.strftime(datetime.now(),"%H:%M")))
                                cl.downloadObjectMsg(op.message.id, saveAs="tmp/{}_{}.png".format(datetime.strftime(datetime.now(),"%H:%M"),op.message.id))
                            elif op.message.contentType == 7:
                                print("\n[{}] STICKER".format(datetime.strftime(datetime.now(),"%H:%M")))
                        if op.message.toType == 2 and op.message.contentType == 0:
                            if "{}.txt".format(op.message.to) not in os.listdir("www"):
                                with open("www/{}.txt".format(op.message.to),"a") as talk:
                                    talk.write(cl.getGroup(op.message.to).name)
                            with open("www/{}.txt".format(op.message.to),"a") as talk:
                                talk.write("\n[{}] sender:{} text:{}".format(datetime.strftime(datetime.now(),"%H:%M"),cl.getContact(op.message._from).displayName,op.message.text))
                    cl.revision = max(op.revision, cl.revision)
        except Exception as e:
            print(e)
def control():     #---------you can send message to any one who is talking to the target~
    while 1:
        text = input()
        if text.lower() == 'clear':
            os.system("clear")
            return
        elif text.lower().startswith("send "):
            wait["chatroom"] = text[5:].split(' ',2)[0]
            text = text[5:].split(' ',2)[1]
        elif text.lower().startswith("unsend "):
            talks = cl.getRecentMessagesV2(wait["chatroom"])
            times = 0
            print(talks)            
            for mess in talks:
                if mess._from == cl.profile.mid: 
                    try:
                        cl.unsendMessage(mess.id)
                        times += 1
                    except Exception as error: print(error)
                    if times == int(text[7:]):
                        break
            return
        try:
            cl.sendMessage(wait["chatroom"],text)
            cl.reversion = cl.poll.getLastOpRevision()
        except Exception as e:
            print(e)
            
            
def checkroom():     #-------using mid to search someone's talk record
    target = input("mid :")
    talks = cl.getRecentMessagesV2(target)
    talks.reverse()
    for mess in talks:
        if mess.contentType == 0 and mess.text != None:
            if mess._from == cl.profile.mid:
                print("send text:{}".format(mess.text))
            else:
                print("recieve text:{}".format(mess.text))
        if mess.contentType == 1:
            cl.downloadObjectMsg(mess.id, saveAs="tmp/{}.png".format(mess.id))
           
threading.Thread(target=control).start()
threading.Thread(target=detectchat).start()
#threading.Thread(target=checkroom).start()


