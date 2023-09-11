# -*- coding: utf-8 -*-
"""
Created by ミツツキ

"""
#app.py
from flask import Flask, render_template, request
import sys
import re
import os
import time
import base64
import html

app = Flask(__name__)

# http://127.0.0.1:5000をルートとして、("")の中でアクセスポイント指定
# @app.route("hoge")などで指定すると、http://127.0.0.1:5000/hogeでの動作を記述できる。

def htmlCreater(textOriginalList,titleName,creatorName):
    iconFileLocation = ""
    displayName = ""
    iconFileName = ""
    npcObjectIconFileName = ""
    talkAreaType = "normal"
    talkAreaMargin = "left"
    
    
    startFlg = 0
    tagElementFirstFlg = 0
    tagElementCounter = 0
    displayNameCounter = 0
    iconFileCounter = 0
    imageAreaCounter = 0
    
    newCreateList = []
    newCreateTextLine = []
    charactorListDat = []
    elementExist = False
    charactorId = ""
    tagElementList = []
    displayNameList = []
    iconFileList = []
    
    #-- 処理開始 --
    
    textOriginalList = html.unescape(textOriginalList)
    textOriginalList = re.sub("[@＠][@＠][@＠]","@@@",textOriginalList)
#   textOriginalList = textOriginalList.replace("（水着）","(水着)").replace("（正月）","(正月)").replace("（体操服）","(体操服)").replace("（応援団）","(応援団)").replace("（幼女）","(幼女)").replace("（温泉）","(温泉)").replace("（バニーガール）","(バニー)").replace("（バニー）","(バニー)").replace("（ライディング）","(ライディング)").replace("（私服）","(私服)").replace("（クリスマス）","(クリスマス)")
    textOriginalList = textOriginalList.replace("@@@スケバン1@@@","@@@スケバン１@@@").replace("@@@スケバン2@@@","@@@スケバン２@@@").replace("@@@スケバン3@@@","@@@スケバン３@@@").replace("<強調>","<b>").replace("</強調>","</b>").replace("<照れ>","<font class=\"blush\">").replace("</照れ>","</font>").replace("<blush>","<font class=\"blush\">").replace("</blush>","</font>")
    textOriginalList = textOriginalList.splitlines(True)
    
    try:
        with open('./charactorList.dat','r',encoding="UTF-8") as f:
            charactorListDat = f.readlines()
    except:
        print("ERROR:エラーが発生しました。charactorList.datが見つからない。あるいはUTF-8ではない文字コードになっている可能性があります。プログラムを終了します。")
        time.sleep(1)
        sys.exit()
    
    
    for charactorLineDat in charactorListDat:
        if startFlg == 1:
            if re.search("No[\d]{3}_[\d]{1}_tagElement:", charactorLineDat):
                if displayNameCounter < tagElementCounter:
                    while tagElementCounter > displayNameCounter:
                        displayNameList.append(None)
                        displayNameCounter += 1
                
                if iconFileCounter < tagElementCounter:
                    while tagElementCounter > iconFileCounter:
                        iconFileList.append(None)
                        iconFileCounter += 1
                
                charactorId = re.search("No[\d]{3}_[\d]{1}", charactorLineDat)
                charactorId = charactorId.group()
                tagElement = re.sub("[@＠][@＠][@＠]","@@@",charactorLineDat)
                tagElement = charactorLineDat.replace(charactorId +"_tagElement:","").replace("\n","")
                tagElementList.append(tagElement)
                tagElementCounter += 1      
            
            elif re.search(charactorId + "_displayName:", charactorLineDat) and not charactorId == "":
                displayName = charactorLineDat.replace(charactorId +"_displayName:","").replace("\n","")
                if displayName == "":
                    displayNameList.append(None)
                else:
                    displayNameList.append(displayName)
                    
                displayNameCounter += 1
                
            
            elif re.search(charactorId + "_iconFile:", charactorLineDat) and not charactorId == "":
                iconFile = charactorLineDat.replace(charactorId +"_iconFile:","").replace("\n","")
                if iconFile == "":
                    iconFileList.append(None)
                else:
                    iconFileList.append(iconFile)
            
                iconFileCounter += 1
            
            elif re.search("iconFileLocation:", charactorLineDat):
                iconFileLocation = charactorLineDat.replace("iconFileLocation:","").replace("\n","") + "/"
            elif re.search("npcObjectIconFileName:", charactorLineDat):
                npcObjectIconFileName = charactorLineDat.replace("npcObjectIconFileName:","").replace("\n","")
            elif re.search("replyWindow_backgroundName:", charactorLineDat):
                replyWindow_backgroundName = charactorLineDat.replace("replyWindow_backgroundName:","").replace("\n","")
            elif re.search("favorStory_backgroundName:", charactorLineDat):
                favorStory_backgroundName = charactorLineDat.replace("favorStory_backgroundName:","").replace("\n","")                
        elif re.match("\[\[##プログラム読み取りエリア##\]\]", charactorLineDat):
            startFlg = 1
    
    try:            
        root, ext = os.path.splitext("./images/" + replyWindow_backgroundName)
        with open("./images/" + replyWindow_backgroundName, mode='rb') as f:
            src = base64.b64encode(f.read()).decode('utf-8')
    except:
        print("ERROR:画像のbase64化に失敗しました。設定ファイル上で誤ったファイルが指定されている可能性があります。プログラムを終了します。")
        time.sleep(1)
        sys.exit()
    
    replyWindow_backgroundName = "		background: #dce6e9 url(data:image/" + ext.replace(".","") + ";base64," + src + ") no-repeat right top;\n" 
    
    try:            
        root, ext = os.path.splitext("./images/" + favorStory_backgroundName)
        with open("./images/" + favorStory_backgroundName, mode='rb') as f:
            src = base64.b64encode(f.read()).decode('utf-8')
    except:
        print("ERROR:画像のbase64化に失敗しました。設定ファイル上で誤ったファイルが指定されている可能性があります。プログラムを終了します。")
        time.sleep(1)
        sys.exit()
    
    favorStory_backgroundName = "		background: #f4d6de url(data:image/" + ext.replace(".","") + ";base64," + src + ") no-repeat right top;\n"
    
    startFlg = 0
    tagElementCounter = 0
    replyContinueFlg = 0
    displayName = ""
    iconFileName = ""
    displayNameBefore = ""
    talkAreaTypeBefore = ""
    talkAreaMarginBefore = ""
            
    if not creatorName == "":
            creatorName = "作者:" + creatorName
            
   
    newCreateList.append("<html lang=\"ja\">\n")
    newCreateList.append("	<head>\n")
    newCreateList.append("		<meta charset=\"UTF-8\"/>\n")
    newCreateList.append("		<title>PlumTalk</title>\n")
    newCreateList.append("	</head>\n")
    newCreateList.append("	<body>\n")
    newCreateList.append("		<div class=\"plumContainer\">\n")
    newCreateList.append("			<div class=\"header\">\n")

    try:
        with open("./images/plum.webp", mode='rb') as f:
            plumSrc = base64.b64encode(f.read()).decode('utf-8')
    except:
        print("ERROR:画像のbase64化に失敗しました。ヘッダー用の画像が破損している可能性があります。プログラムを終了します。")
        time.sleep(1)
        sys.exit()

    newCreateList.append("              <img src=data:image/webp;base64," + plumSrc + " alt=\"プラム\" width=6% />PlumTalk</font>\n")

    newCreateList.append("			</div>\n")
    newCreateList.append("			<div class=\"subtitle\">\n")
    
    newCreateList.append("				" + titleName + "<br>" + creatorName + "\n")
    newCreateList.append("			</div>\n")
    newCreateList.append("			<div class=\"lineElements\">\n")


    for textOriginalLine in textOriginalList:
        if re.search("@@@",textOriginalLine):
            if tagElementFirstFlg == 1:
                if talkAreaType == "normal":

                    if talkAreaMargin == "left" or talkAreaMargin == "leftAndPicture":
                        newCreateList.append("				<div class=\"leftTable\">\n")                            
                    elif talkAreaMargin == "right" or talkAreaMargin == "rightAndHidden" or talkAreaMargin == "rightAndPicture" or talkAreaMargin == "rightAndHiddenAndPicture":
                        newCreateList.append("				<div class=\"rightTable\">\n")
                        
                    if talkAreaMargin == "rightAndHidden" or talkAreaMargin == "rightAndHiddenAndPicture":
                        newCreateList.append("					<div class=\"textfield1_hidden\">\n")
                    elif displayNameBefore == displayName and talkAreaTypeBefore == talkAreaType and talkAreaMarginBefore == talkAreaMargin:
                        newCreateList.append("					<div class=\"textfield2\">\n")
                    elif displayNameBefore == displayName and talkAreaTypeBefore == talkAreaType and talkAreaMarginBefore == "right" and talkAreaMargin == "rightAndPicture":
                        newCreateList.append("					<div class=\"textfield2\">\n")
                    elif displayNameBefore == displayName and talkAreaTypeBefore == talkAreaType and talkAreaMarginBefore == "rightAndPicture" and talkAreaMargin == "right":
                        newCreateList.append("					<div class=\"textfield2\">\n")
                    elif displayNameBefore == displayName and talkAreaTypeBefore == talkAreaType and talkAreaMarginBefore == "left" and talkAreaMargin == "leftAndPicture":
                        newCreateList.append("					<div class=\"textfield2\">\n")
                    elif displayNameBefore == displayName and talkAreaTypeBefore == talkAreaType and talkAreaMarginBefore == "leftAndPicture" and talkAreaMargin == "left":
                        newCreateList.append("					<div class=\"textfield2\">\n")
                    else:
                        newCreateList.append("					<figure>\n")
                        try:            
                            root, ext = os.path.splitext("./" + iconFileLocation + iconFileName)
                            with open("./" + iconFileLocation + iconFileName, mode='rb') as f:
                                src = base64.b64encode(f.read()).decode('utf-8')
                        except:
                            iconFileName = npcObjectIconFileName
                            root, ext = os.path.splitext("./" + iconFileLocation + iconFileName)
                            with open("./" + iconFileLocation + iconFileName, mode='rb') as f:
                                src = base64.b64encode(f.read()).decode('utf-8')

                        newCreateList.append("						<img src=data:image/" + ext.replace(".","") + ";base64," + src + " />\n")
                        newCreateList.append("					</figure>\n")
                        newCreateList.append("					<div class=\"textfield1\">\n")
                        newCreateList.append("						<div class=\"name\">\n")
                        newCreateList.append("							<p>" + displayName + "</p>\n")
                        newCreateList.append("						</div>\n")


                    newCreateList.append("						<div class=\"text\">\n")
                    
                    if talkAreaMargin == "leftAndPicture" or talkAreaMargin == "rightAndPicture" or talkAreaMargin == "rightAndHiddenAndPicture":
                        newCreateList.append("							<div>\n")
                        imageAreaCounterStr = "<div id=" + "\"imageArea" + str(imageAreaCounter) + "\" >\n"
                        newCreateList.append("									" + imageAreaCounterStr)
                        newCreateList.append("									<p><input type=\"file\" class=\"form-control me-2\" id=\"uploadImage\" /></p>\n")
                        newCreateList.append("									<p><br></p>\n")
                        newCreateList.append("									<p><button type=\"button\" class=\"btn btn-primary form-control w-25\" onclick=\"insertImage(" + str(imageAreaCounter) + ")\" >画像を挿入</button></p>\n")
                        newCreateList.append("								</div>\n")                        
                        newCreateList.append("							</div>\n")
                        imageAreaCounter += 1
                    else:
                        for text in newCreateTextLine:
                            if not text == "":
                                newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                            else:
                                newCreateList.append("							<p><br></p>\n")
                        
                        newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                        if re.search("<div class=\"text\">\n",newCreateList[-2]) and not text == "":
                            newCreateList[-1] = "							<p><br></p>\n"

                    newCreateList.append("						</div>\n")
                    newCreateList.append("					</div>\n")
                    newCreateList.append("				</div>\n")
                    
                    
                elif talkAreaType == "replyContinue":
                    if replyContinueFlg == 0:
                        if re.search("@@@返信@@@",textOriginalLine) or re.search("@@@連続@@@",textOriginalLine):
                            newCreateList.append("				<div class=\"rightTable\">\n")
                            newCreateList.append("					<div class=\"textfield3\">\n")
                            newCreateList.append("                      <p><font color=#84c4f4>|</font> 返信する</p>\n")
                            newCreateList.append("                      <p><u>　　　　　　　　　　　　　　　　　　　　　</u></p>\n")
                            newCreateList.append("						<div class=\"text\">\n")
   
                            for text in newCreateTextLine:
                                if not text == "":
                                    newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                                else:
                                    newCreateList.append("							<p><br></p>\n")
                            
                            newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                            if re.search("<div class=\"text\">\n",newCreateList[-2]) and not text == "":
                                newCreateList[-1] = "							<p><br></p>\n"
                            
                            newCreateList.append("						</div>\n")
                            replyContinueFlg = 1
                            if not re.search("@@@追加@@@",textOriginalLine) and not re.search("@@@連続@@@",textOriginalLine):
                                newCreateList.append("					</div>\n")
                                newCreateList.append("				</div>\n")
                                replyContinueFlg = 0
                        else:
                            newCreateList.append("				<div class=\"rightTable\">\n")
                            newCreateList.append("					<div class=\"textfield3\">\n")
                            newCreateList.append("                      <p><font color=#84c4f4>|</font> 返信する</p>\n")
                            newCreateList.append("                      <p><u>　　　　　　　　　　　　　　　　　　　　　</u></p>\n")
                            newCreateList.append("						<div class=\"text\">\n")
   
                            for text in newCreateTextLine:
                                if not text == "":
                                    newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                                else:
                                    newCreateList.append("							<p><br></p>\n")
                            
                            newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                            if re.search("<div class=\"text\">\n",newCreateList[-2]) and not text == "":
                                newCreateList[-1] = "							<p><br></p>\n"
                            
                            newCreateList.append("						</div>\n")
                            newCreateList.append("					</div>\n")
                            newCreateList.append("				</div>\n")
                            
                                
                    elif replyContinueFlg == 1:
                        if re.search("@@@返信@@@",textOriginalLine) or re.search("@@@連続@@@",textOriginalLine):
                            newCreateList.append("						<div class=\"text\">\n")

                            for text in newCreateTextLine:
                                if not text == "":
                                    newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                                else:
                                    newCreateList.append("							<p><br></p>\n")
                            
                            newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                            if re.search("<div class=\"text\">\n",newCreateList[-2]) and not text == "":
                                newCreateList[-1] = "							<p><br></p>\n"
                            
                            newCreateList.append("						</div>\n")
                            replyContinueFlg = 1
                            if not re.search("@@@追加@@@",textOriginalLine) and not re.search("@@@連続@@@",textOriginalLine):
                                newCreateList.append("					</div>\n")
                                newCreateList.append("				</div>\n")
                                replyContinueFlg = 0
                        else:
                            newCreateList.append("						<div class=\"text\">\n")

                            for text in newCreateTextLine:
                                if not text == "":
                                    newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                                else:
                                    newCreateList.append("							<p><br></p>\n")
                            
                            newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                            if re.search("<div class=\"text\">\n",newCreateList[-2]) and not text == "":
                                newCreateList[-1] = "							<p><br></p>\n"
                            
                            newCreateList.append("						</div>\n")
                            newCreateList.append("					</div>\n")
                            newCreateList.append("				</div>\n")
                            replyContinueFlg = 0


                elif talkAreaType == "reply":
                    newCreateList.append("				<div class=\"rightTable\">\n")
                    newCreateList.append("					<div class=\"textfield3\">\n")
                    newCreateList.append("                      <p><font color=#84c4f4>|</font> 返信する</p>\n")
                    newCreateList.append("                      <p><u>　　　　　　　　　　　　　　　　　　　　　</u></p>\n")
                    newCreateList.append("						<div class=\"text\">\n")

   
                    for text in newCreateTextLine:
                        if not text == "":
                            newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                        else:
                            newCreateList.append("							<p><br></p>\n")
                    
                    newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                    if re.search("<div class=\"text\">\n",newCreateList[-2]) and not text == "":
                        newCreateList[-1] = "							<p><br></p>\n"
                    
                    newCreateList.append("						</div>\n")
                    newCreateList.append("					</div>\n")
                    newCreateList.append("				</div>\n")
                elif talkAreaType == "label":
                    newCreateList.append("				<div class=\"centerTable\">\n")
                    newCreateList.append("					<div class=\"textfield\">\n")
                    newCreateList.append("						<div class=\"text\">\n")

                    for text in newCreateTextLine:
                        if not text == "":
                            newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                        else:
                            newCreateList.append("							<p><br></p>\n")
                    
                    newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                    if re.search("<div class=\"text\">\n",newCreateList[-2]) and not text == "":
                        newCreateList[-1] = "							<p><br></p>\n"

                    newCreateList.append("						</div>\n")
                    newCreateList.append("					</div>\n")
                    newCreateList.append("				</div>\n")
                elif talkAreaType == "love":
                    newCreateList.append("				<div class=\"rightTable\">\n")
                    newCreateList.append("					<div class=\"textfield4\">\n")
                    newCreateList.append("                      <p><font color=#FF5192>|</font>絆イベント</p>\n")
                    newCreateList.append("                      <p><u>　　　　　　　　　　　　　　　　　　　　　</u></p>\n")
                    newCreateList.append("						<div class=\"text\">\n")
                    newCreateList.append(                           "<p>" + displayName + "の絆ストーリーへ</p>\n")
                    newCreateList.append("						</div>\n")
                    newCreateList.append("					</div>\n")
                    newCreateList.append("				</div>\n")
                elif talkAreaType == "pictureTable":
                    newCreateList.append("				<div class=\"imageArea\">\n")
                    imageAreaCounterStr = "<div id=" + "\"imageArea" + str(imageAreaCounter) + "\" >\n"
                    newCreateList.append("									" + imageAreaCounterStr)
                    newCreateList.append("						<p><input type=\"file\" class=\"form-control me-2\" id=\"uploadImage\" /></p>\n")
                    newCreateList.append("						<p><br></p>\n")
                    newCreateList.append("						<p><button type=\"button\" class=\"btn btn-primary form-control w-25\" onclick=\"insertImage(" + str(imageAreaCounter) + ")\" >画像を挿入</button></p>\n")
                    newCreateList.append("					</div>\n")                                            
                    newCreateList.append("				</div>\n")
                    imageAreaCounter += 1
                elif talkAreaType == "cut" and not talkAreaTypeBefore == "cut":
                    pass
#                   newCreateList.append("[[##cut##]]\n")
                    
                
                
                displayNameBefore = displayName
                talkAreaTypeBefore = talkAreaType
                talkAreaMarginBefore = talkAreaMargin       
                newCreateTextLine = []
                
            
            tagElementFirstFlg = 1
            displayName = ""
            iconFileName = ""
            
            for tagElement in tagElementList:
                if re.search(tagElement.replace("(","\(").replace(")","\)"),textOriginalLine):
                    elementExist = True
                    for index, display in enumerate(displayNameList):
                        if index == tagElementCounter:
                            displayName = display
                            if displayName is None:
                                displayName = tagElement.replace("@@@","")
                            break
                    
                    for index, iconFile in enumerate(iconFileList):
                        if index == tagElementCounter:
                            iconFileName = iconFile
                            if iconFileName is None:
                                iconFileName = npcObjectIconFileName
                            break
                        
                
                if elementExist == True:
                    elementExist = False
                    tagElementCounter = 0
                    break
            
            
                    
                
                tagElementCounter += 1
            
            talkAreaType = "normal"
            talkAreaMargin = "left"
            
            if re.search("@@@画像@@@",textOriginalLine):
                talkAreaType = "pictureTable"
            if re.search("@@@左@@@",textOriginalLine) or re.search("@@@左左@@@",textOriginalLine) or re.search("@@@左左左@@@",textOriginalLine) or re.search("@@@左左左左[^@]*@@@",textOriginalLine):
                talkAreaType = "normal"
                talkAreaMargin = "left"
                if re.search("@@@画像@@@",textOriginalLine):
                    talkAreaMargin = "leftAndPicture"
            if re.search("@@@右@@@",textOriginalLine):
                talkAreaType = "normal"
                talkAreaMargin = "right"
                if re.search("@@@画像@@@",textOriginalLine):
                    talkAreaMargin = "rightAndPicture"
            if re.search("@@@右右@@@",textOriginalLine) or re.search("@@@右右右@@@",textOriginalLine) or re.search("@@@右右右右[^@]*@@@",textOriginalLine):
                talkAreaType = "normal"
                talkAreaMargin = "rightAndHidden"
                if re.search("@@@画像@@@",textOriginalLine):
                    talkAreaMargin = "rightAndHiddenAndPicture"
            if re.search("@@@返信@@@",textOriginalLine):
                if re.search("@@@追加@@@",textOriginalLine):
                    talkAreaType = "replyContinue"
                else:
                    talkAreaType = "reply"
            if re.search("@@@ラベル@@@",textOriginalLine):    
                talkAreaType = "label"
            if re.search("@@@絆ストーリー@@@",textOriginalLine):
                talkAreaType = "love"
            if re.search("@@@連続@@@",textOriginalLine):
                displayName = displayNameBefore
                talkAreaType = talkAreaTypeBefore
                talkAreaMargin = talkAreaMarginBefore
            if re.search("@@@アイコン@@@",textOriginalLine):
                displayNameBefore = ""
                talkAreaTypeBefore = ""
                talkAreaMarginBefore = ""

            if re.search("@@@カット@@@",textOriginalLine):
                talkAreaType = "cut"
                    
            
            if displayName == "":
                displayName = re.sub("@@@左左左*","",textOriginalLine)
                displayName = re.sub("@@@右右右*","",displayName)
                displayName = displayName.replace("@@@画像","").replace("@@@左","").replace("@@@右","").replace("@@@返信","").replace("@@@追加","").replace("@@@ラベル","").replace("@@@絆ストーリー","").replace("@@@連続","").replace("@@@カット","").replace("@@@","").replace("　","").replace(" ","").replace("\n","")
            if displayName == "":
                displayName = "？"
            elif talkAreaType == "pictureTable":
                talkAreaType = "normal"
                talkAreaMargin = "leftAndPicture"
            if iconFileName == "":
                iconFileName = npcObjectIconFileName

            
            tagElementCounter = 0
            
        elif tagElementFirstFlg == 1:
            if talkAreaMargin == "left":
                newCreateTextLine.append(textOriginalLine.replace("<赤字>","<font class=\"textRed_left\">").replace("</赤字>","</font>").replace("<red>","<font class=\"textRed_left\">").replace("</red>","</font>"))                    
            else:
                newCreateTextLine.append(textOriginalLine.replace("<赤字>","<font class=\"textRed_right\">").replace("</赤字>","</font>").replace("<red>","<font class=\"textRed_right\">").replace("</red>","</font>"))                    
        else:
            pass
                        
    
    if tagElementFirstFlg == 1:
        if talkAreaType == "normal":
    
            if talkAreaMargin == "left" or talkAreaMargin == "leftAndPicture":
                newCreateList.append("				<div class=\"leftTable\">\n")                            
            elif talkAreaMargin == "right" or talkAreaMargin == "rightAndHidden" or talkAreaMargin == "rightAndPicture" or talkAreaMargin == "rightAndHiddenAndPicture":
                newCreateList.append("				<div class=\"rightTable\">\n")
                
            if talkAreaMargin == "rightAndHidden" or talkAreaMargin == "rightAndHiddenAndPicture":
                newCreateList.append("					<div class=\"textfield1_hidden\">\n")
            elif displayNameBefore == displayName and talkAreaTypeBefore == talkAreaType and talkAreaMarginBefore == talkAreaMargin:
                newCreateList.append("					<div class=\"textfield2\">\n")
            elif displayNameBefore == displayName and talkAreaTypeBefore == talkAreaType and talkAreaMarginBefore == "right" and talkAreaMargin == "rightAndPicture":
                newCreateList.append("					<div class=\"textfield2\">\n")
            elif displayNameBefore == displayName and talkAreaTypeBefore == talkAreaType and talkAreaMarginBefore == "rightAndPicture" and talkAreaMargin == "right":
                newCreateList.append("					<div class=\"textfield2\">\n")
            elif displayNameBefore == displayName and talkAreaTypeBefore == talkAreaType and talkAreaMarginBefore == "left" and talkAreaMargin == "leftAndPicture":
                newCreateList.append("					<div class=\"textfield2\">\n")
            elif displayNameBefore == displayName and talkAreaTypeBefore == talkAreaType and talkAreaMarginBefore == "leftAndPicture" and talkAreaMargin == "left":
                newCreateList.append("					<div class=\"textfield2\">\n")
            else:
                newCreateList.append("					<figure>\n")
                try:            
                    root, ext = os.path.splitext("./" + iconFileLocation + iconFileName)
                    with open("./" + iconFileLocation + iconFileName, mode='rb') as f:
                        src = base64.b64encode(f.read()).decode('utf-8')
                except:
                    iconFileName = npcObjectIconFileName
                    root, ext = os.path.splitext("./" + iconFileLocation + iconFileName)
                    with open("./" + iconFileLocation + iconFileName, mode='rb') as f:
                        src = base64.b64encode(f.read()).decode('utf-8')

                newCreateList.append("						<img src=data:image/" + ext.replace(".","") + ";base64," + src + " />\n")
                newCreateList.append("					</figure>\n")
                newCreateList.append("					<div class=\"textfield1\">\n")
                newCreateList.append("						<div class=\"name\">\n")
                newCreateList.append("							<p>" + displayName + "</p>\n")
                newCreateList.append("						</div>\n")


            newCreateList.append("						<div class=\"text\">\n")
            
            if talkAreaMargin == "leftAndPicture" or talkAreaMargin == "rightAndPicture" or talkAreaMargin == "rightAndHiddenAndPicture":
                newCreateList.append("							<div>\n")
                imageAreaCounterStr = "<div id=" + "\"imageArea" + str(imageAreaCounter) + "\" >\n"
                newCreateList.append("									" + imageAreaCounterStr)
                newCreateList.append("									<p><input type=\"file\" class=\"form-control me-2\" id=\"uploadImage\" /></p>\n")
                newCreateList.append("									<p><br></p>\n")
                newCreateList.append("									<p><button type=\"button\" class=\"btn btn-primary form-control w-25\" onclick=\"insertImage(" + str(imageAreaCounter) + ")\" >画像を挿入</button></p>\n")
                newCreateList.append("								</div>\n")                        
                newCreateList.append("							</div>\n")
                imageAreaCounter += 1
            else:
                for text in newCreateTextLine:
                    if not text == "":
                        newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                    else:
                        newCreateList.append("							<p><br></p>\n")
                
                newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                if re.search("<div class=\"text\">\n",newCreateList[-2]) and not text == "":
                    newCreateList[-1] = "							<p><br></p>\n"
            newCreateList.append("						</div>\n")
            newCreateList.append("					</div>\n")
            newCreateList.append("				</div>\n")
            
            
        elif talkAreaType == "replyContinue":
            if replyContinueFlg == 0:
                if re.search("@@@返信@@@",textOriginalLine) or re.search("@@@連続@@@",textOriginalLine):
                    newCreateList.append("				<div class=\"rightTable\">\n")
                    newCreateList.append("					<div class=\"textfield3\">\n")
                    newCreateList.append("                      <p><font color=#84c4f4>|</font> 返信する</p>\n")
                    newCreateList.append("                      <p><u>　　　　　　　　　　　　　　　　　　　　　</u></p>\n")
                    newCreateList.append("						<div class=\"text\">\n")
   
                    for text in newCreateTextLine:
                        if not text == "":
                            newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                        else:
                            newCreateList.append("							<p><br></p>\n")
                    
                    newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                    if re.search("<div class=\"text\">\n",newCreateList[-2]) and not text == "":
                        newCreateList[-1] = "							<p><br></p>\n"
                    
                    newCreateList.append("						</div>\n")
                    replyContinueFlg = 1
                    if not re.search("@@@追加@@@",textOriginalLine) and not re.search("@@@連続@@@",textOriginalLine):
                        newCreateList.append("					</div>\n")
                        newCreateList.append("				</div>\n")
                        replyContinueFlg = 0
                else:
                    newCreateList.append("				<div class=\"rightTable\">\n")
                    newCreateList.append("					<div class=\"textfield3\">\n")
                    newCreateList.append("                      <p><font color=#84c4f4>|</font> 返信する</p>\n")
                    newCreateList.append("                      <p><u>　　　　　　　　　　　　　　　　　　　　　</u></p>\n")
                    newCreateList.append("						<div class=\"text\">\n")
   
                    for text in newCreateTextLine:
                        if not text == "":
                            newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                        else:
                            newCreateList.append("							<p><br></p>\n")
                    
                    newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                    if re.search("<div class=\"text\">\n",newCreateList[-2]) and not text == "":
                        newCreateList[-1] = "							<p><br></p>\n"
                    
                    newCreateList.append("						</div>\n")
                    newCreateList.append("					</div>\n")
                    newCreateList.append("				</div>\n")
                    
                        
            elif replyContinueFlg == 1:
                if re.search("@@@返信@@@",textOriginalLine) or re.search("@@@連続@@@",textOriginalLine):
                    newCreateList.append("						<div class=\"text\">\n")

                    for text in newCreateTextLine:
                        if not text == "":
                            newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                        else:
                            newCreateList.append("							<p><br></p>\n")
                    
                    newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                    if re.search("<div class=\"text\">\n",newCreateList[-2]) and not text == "":
                        newCreateList[-1] = "							<p><br></p>\n"
                    
                    newCreateList.append("						</div>\n")
                    replyContinueFlg = 1
                    if not re.search("@@@追加@@@",textOriginalLine) and not re.search("@@@連続@@@",textOriginalLine):
                        newCreateList.append("					</div>\n")
                        newCreateList.append("				</div>\n")
                        replyContinueFlg = 0
                else:
                    newCreateList.append("						<div class=\"text\">\n")

                    for text in newCreateTextLine:
                        if not text == "":
                            newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                        else:
                            newCreateList.append("							<p><br></p>\n")
                    
                    newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                    if re.search("<div class=\"text\">\n",newCreateList[-2]) and not text == "":
                        newCreateList[-1] = "							<p><br></p>\n"
                    
                    newCreateList.append("						</div>\n")
                    newCreateList.append("					</div>\n")
                    newCreateList.append("				</div>\n")
                    replyContinueFlg = 0


        elif talkAreaType == "reply":
            newCreateList.append("				<div class=\"rightTable\">\n")
            newCreateList.append("					<div class=\"textfield3\">\n")
            newCreateList.append("                      <p><font color=#84c4f4>|</font> 返信する</p>\n")
            newCreateList.append("                      <p><u>　　　　　　　　　　　　　　　　　　　　　</u></p>\n")
            newCreateList.append("						<div class=\"text\">\n")

   
            for text in newCreateTextLine:
                if not text == "" :
                    newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                else:
                    newCreateList.append("							<p><br></p>\n")
            
            newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
            if re.search("<div class=\"text\">\n",newCreateList[-2]) and not text == "":
                newCreateList[-1] = "							<p><br></p>\n"
            
            newCreateList.append("						</div>\n")
            newCreateList.append("					</div>\n")
            newCreateList.append("				</div>\n")
        elif talkAreaType == "label":
            newCreateList.append("				<div class=\"centerTable\">\n")
            newCreateList.append("					<div class=\"textfield\">\n")
            newCreateList.append("						<div class=\"text\">\n")

            for text in newCreateTextLine:
                if not text == "":
                    newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                else:
                    newCreateList.append("							<p><br></p>\n")
            
            newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
            if re.search("<div class=\"text\">\n",newCreateList[-2]) and not text == "":
                newCreateList[-1] = "							<p><br></p>\n"

            newCreateList.append("						</div>\n")
            newCreateList.append("					</div>\n")
            newCreateList.append("				</div>\n")
        elif talkAreaType == "love":
            newCreateList.append("				<div class=\"rightTable\">\n")
            newCreateList.append("					<div class=\"textfield4\">\n")
            newCreateList.append("                      <p><font color=#FF5192>|</font>絆イベント</p>\n")
            newCreateList.append("                      <p><u>　　　　　　　　　　　　　　　　　　　　　</u></p>\n")
            newCreateList.append("						<div class=\"text\">\n")
            newCreateList.append("							<p>" + displayName + "の絆ストーリーへ</p>\n")
            newCreateList.append("						</div>\n")
            newCreateList.append("					</div>\n")
            newCreateList.append("				</div>\n")
        elif talkAreaType == "pictureTable":
            newCreateList.append("				<div class=\"imageArea\">\n")
            imageAreaCounterStr = "<div id=" + "\"imageArea" + str(imageAreaCounter) + "\" >\n"
            newCreateList.append("									" + imageAreaCounterStr)
            newCreateList.append("						<p><input type=\"file\" class=\"form-control me-2\" id=\"uploadImage\" /></p>\n")
            newCreateList.append("						<p><br></p>\n")
            newCreateList.append("						<p><button type=\"button\" class=\"btn btn-primary form-control w-25\" onclick=\"insertImage(" + str(imageAreaCounter) + ")\" >画像を挿入</button></p>\n")
            newCreateList.append("					</div>\n")                                            
            newCreateList.append("				</div>\n")
            imageAreaCounter += 1
        elif talkAreaType == "cut" and not talkAreaTypeBefore == "cut":
            pass
#       newCreateList.append("[[##cut##]]\n")            
    else:
        newCreateList.append("				<div class=\"centerTable\">\n")
        newCreateList.append("					<div class=\"textfield\">\n")
        newCreateList.append("						<div class=\"text\">\n")
        newCreateList.append("							<p>エラー:テキストエリアが空欄、あるいは有効なタグが存在しません。</p>\n")
        newCreateList.append("						</div>\n")
        newCreateList.append("					</div>\n")
        newCreateList.append("				</div>\n")

    newCreateTextLine = []


    newCreateList.append("			</div>\n")
    newCreateList.append("			<div class=\"footer\">\n")
    newCreateList.append("              <img src=data:image/webp;base64," + plumSrc + " alt=\"プラム\" width=3% />PlumTalk for WEB\n")
    newCreateList.append("			</div>\n")
    newCreateList.append("		</div>\n")

    try:
        with open('./scriptAndCSSList.dat','r',encoding="UTF-8") as f:
            scriptAndCSSList = f.readlines()
    except:
        print("ERROR:エラーが発生しました。scriptAndCSSList.datが見つからない。あるいはファイルが破損している可能性があります。プログラムを終了します。")
        time.sleep(1)
        sys.exit()
    
    for line in scriptAndCSSList:
        if re.search("background: #dce6e9 url",line) and re.search("no-repeat right top",line):
            newCreateList.append(replyWindow_backgroundName) 
        elif re.search("background: #f4d6de url",line) and re.search("no-repeat right top",line):
            newCreateList.append(favorStory_backgroundName) 
        else:
            newCreateList.append(line)    
    
    return newCreateList



@app.route("/")
def hello():
   input_from_python = []
   return render_template('index.html',input_from_python=input_from_python)

@app.route('/convertHtml', methods=['POST'])
def convertHtml():
    titleName = request.form['titleName']
    createrName = request.form['creatorName']
#    titleName = ""
#    createrName = ""
    textLineOriginal = request.form['createTalk']
    textLineOriginal = textLineOriginal.replace("\n","").replace("\r","\n")
    
    newHtmlLine = htmlCreater(textLineOriginal,titleName,createrName)
    newHtmlLine = ''.join(newHtmlLine)
    
#    with open("./templates/" + "newCreate_sumple.html",'w', encoding="utf-8") as f:
#        for newHtmlSentence in newHtmlLine:
#            f.write(newHtmlSentence)
    
    return render_template('index.html',input_from_python=newHtmlLine)



@app.route('/convertHtml_sumple1', methods=['POST'])
def convertHtml_sumple1():
    titleName = ""
    createrName = ""
    textLineOriginal = request.form['sumpleTalk1']
    textLineOriginal = textLineOriginal.replace("\n","").replace("\r","\n")
    
    newHtmlLine = htmlCreater(textLineOriginal,titleName,createrName)
    newHtmlLine = ''.join(newHtmlLine)
    
#    with open("./templates/" + "newCreate_sumple.html",'w', encoding="utf-8") as f:
#        for newHtmlSentence in newHtmlLine:
#            f.write(newHtmlSentence)
    
    return render_template('index.html',input_from_python=newHtmlLine)

@app.route('/convertHtml_sumple2', methods=['POST'])
def convertHtml_sumple2():
    titleName = ""
    createrName = ""
    textLineOriginal = request.form['sumpleTalk2']
    textLineOriginal = textLineOriginal.replace("\n","").replace("\r","\n")
    
    newHtmlLine = htmlCreater(textLineOriginal,titleName,createrName)
    newHtmlLine = ''.join(newHtmlLine)
    
#    with open("./templates/" + "newCreate_sumple.html",'w', encoding="utf-8") as f:
#        for newHtmlSentence in newHtmlLine:
#            f.write(newHtmlSentence)
    
    return render_template('index.html',input_from_python=newHtmlLine)

@app.route('/convertHtml_sumple3', methods=['POST'])
def convertHtml_sumple3():
    titleName = ""
    createrName = ""
    textLineOriginal = request.form['sumpleTalk3']
    textLineOriginal = textLineOriginal.replace("\n","").replace("\r","\n")
    
    newHtmlLine = htmlCreater(textLineOriginal,titleName,createrName)
    newHtmlLine = ''.join(newHtmlLine)
    
#    with open("./templates/" + "newCreate_sumple.html",'w', encoding="utf-8") as f:
#        for newHtmlSentence in newHtmlLine:
#            f.write(newHtmlSentence)
    
    return render_template('index.html',input_from_python=newHtmlLine)

@app.route('/convertHtml_sumple4', methods=['POST'])
def convertHtml_sumple4():
    titleName = ""
    createrName = ""
    textLineOriginal = request.form['sumpleTalk4']
    textLineOriginal = textLineOriginal.replace("\n","").replace("\r","\n")
    
    newHtmlLine = htmlCreater(textLineOriginal,titleName,createrName)
    newHtmlLine = ''.join(newHtmlLine)
    
#    with open("./templates/" + "newCreate_sumple.html",'w', encoding="utf-8") as f:
#        for newHtmlSentence in newHtmlLine:
#            f.write(newHtmlSentence)
    
    return render_template('index.html',input_from_python=newHtmlLine)

@app.route('/convertHtml_sumple5', methods=['POST'])
def convertHtml_sumple5():
    titleName = ""
    createrName = ""
    textLineOriginal = request.form['sumpleTalk5']
    textLineOriginal = textLineOriginal.replace("\n","").replace("\r","\n")
    
    newHtmlLine = htmlCreater(textLineOriginal,titleName,createrName)
    newHtmlLine = ''.join(newHtmlLine)
    
#    with open("./templates/" + "newCreate_sumple.html",'w', encoding="utf-8") as f:
#        for newHtmlSentence in newHtmlLine:
#            f.write(newHtmlSentence)
    
    return render_template('index.html',input_from_python=newHtmlLine)

@app.route('/convertHtml_sumple6', methods=['POST'])
def convertHtml_sumple6():
    titleName = ""
    createrName = ""
    textLineOriginal = request.form['sumpleTalk6']
    textLineOriginal = textLineOriginal.replace("\n","").replace("\r","\n")
    
    newHtmlLine = htmlCreater(textLineOriginal,titleName,createrName)
    newHtmlLine = ''.join(newHtmlLine)
    
#    with open("./templates/" + "newCreate_sumple.html",'w', encoding="utf-8") as f:
#        for newHtmlSentence in newHtmlLine:
#            f.write(newHtmlSentence)
    
    return render_template('index.html',input_from_python=newHtmlLine)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=80)