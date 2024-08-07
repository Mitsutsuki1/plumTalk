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


def htmlCreater(textOriginalList,titleName,creatorName,plumtalk_rabelCheck):
    iconFileLocation = ""
    displayName = ""
    iconFileName = ""
    npcObjectIconFileName = ""
    talkAreaType = "normal"
    talkAreaMargin = "left"
    
    
    startFlg = 0
    repeatFlg = 0
    tagElementFirstFlg = 0
    tagElementCounter = 0
    displayNameCounter = 0
    iconFileCounter = 0
    imageAreaCounter = 0
    plumContainerCounter = 1
    
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
    textOriginalList = textOriginalList.replace("@@@ゲヘナ生徒1@@@","@@@ゲヘナ生徒１@@@").replace("@@@ゲヘナ生徒2@@@","@@@ゲヘナ生徒２@@@").replace("@@@ゲヘナ生徒3@@@","@@@ゲヘナ生徒３@@@").replace("@@@ゲヘナ生徒4@@@","@@@ゲヘナ生徒４@@@").replace("@@@ゲヘナ生徒5@@@","@@@ゲヘナ生徒５@@@").replace("@@@トリニティ生徒1@@@","@@@トリニティ生徒１@@@").replace("@@@トリニティ生徒2@@@","@@@トリニティ生徒２@@@").replace("@@@トリニティ生徒3@@@","@@@トリニティ生徒３@@@").replace("@@@トリニティ生徒4@@@","@@@トリニティ生徒４@@@").replace("@@@トリニティ生徒5@@@","@@@トリニティ生徒５@@@").replace("@@@ミレニアム生徒1@@@","@@@ミレニアム生徒１@@@").replace("@@@ミレニアム生徒2@@@","@@@ミレニアム生徒２@@@").replace("@@@レッドウィンター生徒1@@@","@@@レッドウィンター生徒１@@@").replace("@@@レッドウィンター生徒2@@@","@@@レッドウィンター生徒２@@@").replace("@@@山海経生徒1@@@","@@@山海経生徒１@@@").replace("@@@山海経生徒2@@@","@@@山海経生徒２@@@").replace("@@@乗務員1@@@","@@@乗務員１@@@").replace("@@@乗務員2@@@","@@@乗務員２@@@").replace("@@@乗務員3@@@","@@@乗務員３@@@").replace("@@@スケバン1@@@","@@@スケバン１@@@").replace("@@@スケバン2@@@","@@@スケバン２@@@").replace("@@@スケバン3@@@","@@@スケバン３@@@").replace("<強調>","<b>").replace("</強調>","</b>").replace("<照れ>","<font class=\"blush\">").replace("</照れ>","</font>").replace("<blush>","<font class=\"blush\">").replace("</blush>","</font>")
    textOriginalList = textOriginalList.splitlines()
    textOriginalList.append("")
    
    try:
        with open('./charactorList.dat','r',encoding="UTF-8") as f:
            charactorListDat = f.readlines()
    except:
        print("ERROR:エラーが発生しました。charactorList.datが見つからない。あるいはUTF-8ではない文字コードになっている可能性があります。プログラムを終了します。")
        time.sleep(1)
        sys.exit()
    
    
    for charactorLineDat in charactorListDat:
        if startFlg == 1:
            if re.search("No[\d]{3}_[\d]{3}_tagElement:", charactorLineDat):
                if displayNameCounter < tagElementCounter:
                    while tagElementCounter > displayNameCounter:
                        displayNameList.append(None)
                        displayNameCounter += 1
                
                if iconFileCounter < tagElementCounter:
                    while tagElementCounter > iconFileCounter:
                        iconFileList.append(None)
                        iconFileCounter += 1
                
                charactorId = re.search("No[\d]{3}_[\d]{3}", charactorLineDat)
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
        print("ERROR:返信窓用画像のbase64化に失敗しました。設定ファイル上で誤ったファイルが指定されている可能性があります。プログラムを終了します。")
        time.sleep(1)
        sys.exit()
    
    replyWindow_backgroundName = "		background: #dce6e9 url(data:image/" + ext.replace(".","") + ";base64," + src + ") no-repeat right top;\n" 
    
    try:            
        root, ext = os.path.splitext("./images/" + favorStory_backgroundName)
        with open("./images/" + favorStory_backgroundName, mode='rb') as f:
            src = base64.b64encode(f.read()).decode('utf-8')
    except:
        print("ERROR:絆ストーリー用画像のbase64化に失敗しました。設定ファイル上で誤ったファイルが指定されている可能性があります。プログラムを終了します。")
        time.sleep(1)
        sys.exit()
    
    favorStory_backgroundName = "		background: #f4d6de url(data:image/" + ext.replace(".","") + ";base64," + src + ") no-repeat right top;\n"

    try:
        with open('./scriptAndCSSList.dat','r',encoding="UTF-8") as f:
            scriptAndCSSList = f.readlines()
    except:
        print("ERROR:scriptAndCSSList.datが見つからない。あるいはファイルが破損している可能性があります。プログラムを終了します。")
        time.sleep(1)
        sys.exit()
    
    if plumtalk_rabelCheck == False:
        try:
            with open("./images/plum.webp", mode='rb') as f:
                plumSrc = base64.b64encode(f.read()).decode('utf-8')
        except:
            print("ERROR:ヘッダー用画像のbase64化に失敗しました。ファイルが破損している可能性があります。プログラムを終了します。")
            time.sleep(1)
            sys.exit()
    
    startFlg = 0
    tagElementCounter = 0
    replyContinueFlg = 0
    displayName = ""
    iconFileName = ""
    displayNameBefore = ""
    talkAreaTypeBefore = ""
    talkAreaMarginBefore = ""
    iconInsert = False
            
    if not creatorName == "":
            creatorName = "作者:" + creatorName
            
    newCreateList.append("<html lang=\"ja\">\n")
    newCreateList.append("	<head>\n")
    newCreateList.append("		<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\n")
    newCreateList.append("		<meta http-equiv=\"Content-Style-Type\" content=\"text/css\">\n")
    newCreateList.append("		<title>PlumTalk</title>\n")
    
    for text in scriptAndCSSList:
        if re.search("background: #dce6e9 url",text) and re.search("no-repeat right top",text):
            newCreateList.append(replyWindow_backgroundName) 
        elif re.search("background: #f4d6de url",text) and re.search("no-repeat right top",text):
            newCreateList.append(favorStory_backgroundName) 
        else:
            newCreateList.append(text)
    
    newCreateList.append("	</head>\n")
    newCreateList.append("	<body>\n")
    newCreateList.append("		<div name=\"pngDounload_Area\">\n")
    newCreateList.append("			<p style=\"background-color:4d5b70;\"><a class=\"btn_main\" onclick=\"pngDounload(" + str(plumContainerCounter) + ")\"><font size=\"1\"><b>▼PNGダウンロード</b></font></a></p>\n")
    newCreateList.append("		</div>\n")
    newCreateList.append("		<div class=\"plumContainer\" id=\"plumContainer" + str(plumContainerCounter) +"\" >\n")
    if plumtalk_rabelCheck == False:
        newCreateList.append("			<div class=\"header\">\n")
        newCreateList.append("              <img src=\"data:image/webp;base64," + plumSrc + "\" alt=\"プラム\" width=6% />PlumTalk</font>\n")
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
                        newCreateList.append("					<hidden_solid>\n")
                        newCreateList.append("					</hidden_solid>\n")
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

                        if iconInsert == False:
                            if repeatFlg == 0:
                                try:            
                                    root, ext = os.path.splitext("./" + iconFileLocation + iconFileName)
                                    with open("./" + iconFileLocation + iconFileName, mode='rb') as f:
                                        src = base64.b64encode(f.read()).decode('utf-8')
                                except:
                                    iconFileName = npcObjectIconFileName
                                    root, ext = os.path.splitext("./" + iconFileLocation + iconFileName)
                                    with open("./" + iconFileLocation + iconFileName, mode='rb') as f:
                                        src = base64.b64encode(f.read()).decode('utf-8')
    
                            newCreateList.append("						<img src=\"data:image/" + ext.replace(".","") + ";base64," + src + "\" />\n")
                        else:
                            imageAreaCounterStr = "<div id=" + "\"imageArea" + str(imageAreaCounter) + "\" >\n"
                            newCreateList.append("								" + imageAreaCounterStr)
                            newCreateList.append("									<p><label for=\"file_upload(" + str(imageAreaCounter) + ")\">▼画像<br>　選択<input type=\"file\" accept=\"image/*\" id=\"file_upload(" + str(imageAreaCounter) + ")\"  onchange=\"insertIcon( this ," + str(imageAreaCounter) + ");\"/></label></p>\n")
                            newCreateList.append("								</div>\n")
                            imageAreaCounter += 1
                            
                            
                        newCreateList.append("					</figure>\n")
                        newCreateList.append("					<solid>\n")
                        newCreateList.append("					</solid>\n")

                        newCreateList.append("					<div class=\"textfield1\">\n")
                        newCreateList.append("						<div class=\"name\">\n")
                        newCreateList.append("							<p>" + displayName + "</p>\n")
                        newCreateList.append("						</div>\n")


                    newCreateList.append("						<div class=\"text\">\n")
                    
                    if talkAreaMargin == "leftAndPicture" or talkAreaMargin == "rightAndPicture" or talkAreaMargin == "rightAndHiddenAndPicture":
                        newCreateList.append("							<div>\n")
                        imageAreaCounterStr = "<div id=" + "\"imageArea" + str(imageAreaCounter) + "\" >\n"
                        newCreateList.append("								" + imageAreaCounterStr)
                        newCreateList.append("									<p><label for=\"file_upload(" + str(imageAreaCounter) + ")\">▼画像選択<input type=\"file\" accept=\"image/*\" id=\"file_upload(" + str(imageAreaCounter) + ")\"  onchange=\"insertImage( this ," + str(imageAreaCounter) + ");\"/></label></p>\n")
                        newCreateList.append("								</div>\n")                        
                        newCreateList.append("							</div>\n")
                        imageAreaCounter += 1
                    else:
                        if newCreateTextLine == []:
                            newCreateList.append("							<p><br></p>\n")
                        else:
                            for text in newCreateTextLine:
                                if not text == "":
                                    newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                                else:
                                    newCreateList.append("							<p><br></p>\n")
                        
                        newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                        if re.search("<div class=\"text\">\n",newCreateList[-2]) and newCreateList[-1] == "":
                            newCreateList[-1] = "							<p><br></p>\n"

                    newCreateList.append("						</div>\n")
                    newCreateList.append("					</div>\n")
                    newCreateList.append("				</div>\n")
                    
                    
                elif talkAreaType == "replyContinue":
                    if replyContinueFlg == 0:
                        if re.search("@@@返信@@@",textOriginalLine) or re.search("@@@リピート@@@",textOriginalLine):
                            newCreateList.append("				<div class=\"rightTable\">\n")
                            newCreateList.append("					<div class=\"textfield3\">\n")
                            newCreateList.append("                      <p><font color=#84c4f4>|</font> 返信する</p>\n")
                            newCreateList.append("                      <p><hr></p>\n")
                            newCreateList.append("						<div class=\"text\">\n")
   
                            if newCreateTextLine == []:
                                newCreateList.append("							<p><br></p>\n")
                            else:
                                for text in newCreateTextLine:
                                    if not text == "":
                                        newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                                    else:
                                        newCreateList.append("							<p><br></p>\n")
                            
                            newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                            if re.search("<div class=\"text\">\n",newCreateList[-2]) and newCreateList[-1] == "":
                                newCreateList[-1] = "							<p><br></p>\n"
                            
                            newCreateList.append("						</div>\n")
                            replyContinueFlg = 1
                            if not re.search("@@@追加@@@",textOriginalLine) and not re.search("@@@リピート@@@",textOriginalLine):
                                newCreateList.append("					</div>\n")
                                newCreateList.append("				</div>\n")
                                replyContinueFlg = 0
                        else:
                            newCreateList.append("				<div class=\"rightTable\">\n")
                            newCreateList.append("					<div class=\"textfield3\">\n")
                            newCreateList.append("                      <p><font color=#84c4f4>|</font> 返信する</p>\n")
                            newCreateList.append("                      <p><hr></p>\n")
                            newCreateList.append("						<div class=\"text\">\n")
   
                            if newCreateTextLine == []:
                                newCreateList.append("							<p><br></p>\n")
                            else:
                                for text in newCreateTextLine:
                                    if not text == "":
                                        newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                                    else:
                                        newCreateList.append("							<p><br></p>\n")
                            
                            newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                            if re.search("<div class=\"text\">\n",newCreateList[-2]) and newCreateList[-1] == "":
                                newCreateList[-1] = "							<p><br></p>\n"
                            
                            newCreateList.append("						</div>\n")
                            newCreateList.append("					</div>\n")
                            newCreateList.append("				</div>\n")
                            
                                
                    elif replyContinueFlg == 1:
                        if re.search("@@@返信@@@",textOriginalLine) or re.search("@@@リピート@@@",textOriginalLine):
                            newCreateList.append("						<div class=\"text\">\n")

                            if newCreateTextLine == []:
                                newCreateList.append("							<p><br></p>\n")
                            else:
                                for text in newCreateTextLine:
                                    if not text == "":
                                        newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                                    else:
                                        newCreateList.append("							<p><br></p>\n")
                            
                            newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                            if re.search("<div class=\"text\">\n",newCreateList[-2]) and newCreateList[-1] == "":
                                newCreateList[-1] = "							<p><br></p>\n"
                            
                            newCreateList.append("						</div>\n")
                            replyContinueFlg = 1
                            if not re.search("@@@追加@@@",textOriginalLine) and not re.search("@@@リピート@@@",textOriginalLine):
                                newCreateList.append("					</div>\n")
                                newCreateList.append("				</div>\n")
                                replyContinueFlg = 0
                        else:
                            newCreateList.append("						<div class=\"text\">\n")

                            if newCreateTextLine == []:
                                newCreateList.append("							<p><br></p>\n")
                            else:
                                for text in newCreateTextLine:
                                    if not text == "":
                                        newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                                    else:
                                        newCreateList.append("							<p><br></p>\n")
                            
                            newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                            if re.search("<div class=\"text\">\n",newCreateList[-2]) and newCreateList[-1] == "":
                                newCreateList[-1] = "							<p><br></p>\n"
                            
                            newCreateList.append("						</div>\n")
                            newCreateList.append("					</div>\n")
                            newCreateList.append("				</div>\n")
                            replyContinueFlg = 0


                elif talkAreaType == "reply":
                    newCreateList.append("				<div class=\"rightTable\">\n")
                    newCreateList.append("					<div class=\"textfield3\">\n")
                    newCreateList.append("                      <p><font color=#84c4f4>|</font> 返信する</p>\n")
                    newCreateList.append("                      <p><hr></p>\n")
                    newCreateList.append("						<div class=\"text\">\n")

   
                    if newCreateTextLine == []:
                        newCreateList.append("							<p><br></p>\n")
                    else:
                        for text in newCreateTextLine:
                            if not text == "":
                                newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                            else:
                                newCreateList.append("							<p><br></p>\n")
                    
                    newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                    if re.search("<div class=\"text\">\n",newCreateList[-2]) and newCreateList[-1] == "":
                        newCreateList[-1] = "							<p><br></p>\n"
                    
                    newCreateList.append("						</div>\n")
                    newCreateList.append("					</div>\n")
                    newCreateList.append("				</div>\n")
                elif talkAreaType == "label":
                    newCreateList.append("				<div class=\"centerTable\">\n")
                    newCreateList.append("					<div class=\"textfield\">\n")
                    newCreateList.append("						<div class=\"text\">\n")

                    if newCreateTextLine == []:
                        newCreateList.append("							<p><br></p>\n")
                    else:
                        for text in newCreateTextLine:
                            if not text == "":
                                newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                            else:
                                newCreateList.append("							<p><br></p>\n")
                    
                    newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                    if re.search("<div class=\"text\">\n",newCreateList[-2]) and newCreateList[-1] == "":
                        newCreateList[-1] = "							<p><br></p>\n"

                    newCreateList.append("						</div>\n")
                    newCreateList.append("					</div>\n")
                    newCreateList.append("				</div>\n")
                elif talkAreaType == "love":
                    newCreateList.append("				<div class=\"rightTable\">\n")
                    newCreateList.append("					<div class=\"textfield4\">\n")
                    newCreateList.append("                      <p><font color=#FF5192>|</font>絆イベント</p>\n")
                    newCreateList.append("                      <p><hr></p>\n")
                    newCreateList.append("						<div class=\"text\">\n")
                    newCreateList.append(                           "<p>" + displayName + "の絆ストーリーへ</p>\n")
                    newCreateList.append("						</div>\n")
                    newCreateList.append("					</div>\n")
                    newCreateList.append("				</div>\n")
                elif talkAreaType == "pictureTable":
                    newCreateList.append("				<div class=\"imageArea\">\n")
                    imageAreaCounterStr = "<div id=" + "\"imageArea" + str(imageAreaCounter) + "\" >\n"
                    newCreateList.append("					" + imageAreaCounterStr)
                    newCreateList.append("						<div id=\"img\">\n")
                    newCreateList.append("							<p><label for=\"file_upload(" + str(imageAreaCounter) + ")\">▼画像選択<input type=\"file\" accept=\"image/*\" id=\"file_upload(" + str(imageAreaCounter) + ")\"  onchange=\"insertImage( this ," + str(imageAreaCounter) + ");\"/></label></p>\n")
                    newCreateList.append("						</div>\n")
                    newCreateList.append("					</div>\n")                                            
                    newCreateList.append("				</div>\n")
                    imageAreaCounter += 1
                elif talkAreaType == "space":
                    newCreateList.append("				<div class=\"centerTable\">\n")
                    newCreateList.append("				    <p><br></p>\n")
                    newCreateList.append("				</div>\n")
                    displayName = displayNameBefore
                    talkAreaType = talkAreaTypeBefore
                    talkAreaMargin = talkAreaMarginBefore
                elif talkAreaType == "cut" and not talkAreaTypeBefore == "cut":
                    newCreateList.append("				<div class=\"centerTable\">\n")
                    newCreateList.append("				    <p><br></p>\n")
                    newCreateList.append("				</div>\n")
                    newCreateList.append("			</div>\n")
                    newCreateList.append("		</div>\n")
                    plumContainerCounter += 1
                    newCreateList.append("		<div name=\"pngDownload_Area\">\n")
                    newCreateList.append("			<p style=\"background-color:#4d5b70;\"><a class=\"btn_main\" onclick=\"pngDounload(" + str(plumContainerCounter) + ")\"><font size=\"1\"><b>▼PNGダウンロード(" + str(plumContainerCounter) + ")</b></font></a></p>\n")
                    newCreateList.append("		</div>\n")
                    newCreateList.append("		<div class=\"plumContainer\" id=\"plumContainer" + str(plumContainerCounter) +"\" >\n")
                    newCreateList.append("			<div class=\"lineElements\">\n")
                    
                
                repeatFlg = 0
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
            iconInsert = False
            
            if re.search("@@@カット@@@",textOriginalLine):
                talkAreaType = "cut"
            if re.search("@@@スペース@@@",textOriginalLine) and not re.search("@@@アイコン@@@",textOriginalLine) and elementExist == False:
                talkAreaType = "space"
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
            if re.search("@@@リピート@@@",textOriginalLine):
                displayName = displayNameBefore
                talkAreaType = talkAreaTypeBefore
                talkAreaMargin = talkAreaMarginBefore
                repeatFlg = 1
            if re.search("@@@アイコン表示@@@",textOriginalLine):
                displayNameBefore = ""
                talkAreaTypeBefore = ""
                talkAreaMarginBefore = ""
            if re.search("@@@アイコン変更@@@",textOriginalLine):
                displayNameBefore = ""
                talkAreaTypeBefore = ""
                talkAreaMarginBefore = ""
                iconInsert = True
            
            if displayName == "":
                displayName = re.sub("@@@左左左*","",textOriginalLine)
                displayName = re.sub("@@@右右右*","",displayName)
                displayName = displayName.replace("@@@画像","").replace("@@@左","").replace("@@@右","").replace("@@@返信","").replace("@@@追加","").replace("@@@ラベル","").replace("@@@絆ストーリー","").replace("@@@リピート","").replace("@@@カット","").replace("@@@スペース","").replace("@@@アイコン表示","").replace("@@@アイコン変更","").replace("@@@","").replace("　","").replace(" ","").replace("\n","")

            if displayName == "":
                displayName = "？"
            elif talkAreaType == "pictureTable":
                talkAreaType = "normal"
                talkAreaMargin = "leftAndPicture"
            elif talkAreaType == "space":
                talkAreaType = "normal"
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
                newCreateList.append("					<hidden_solid>\n")
                newCreateList.append("					</hidden_solid>\n")
                newCreateList.append("					<div class=\"textfield1_hidden\">\n")
            elif displayNameBefore == displayName and talkAreaTypeBefore == talkAreaType and talkAreaMarginBefore == talkAreaMargin:
                newCreateList.append("					<div class=\"textfield2\">\n")
            elif displayNameBefore == displayName and talkAreaTypeBefore == talkAreaType and talkAreaMarginBefore == "right" and talkAreaMargin == "rightAndPicture" and not talkAreaTypeBefore == "cut":
                newCreateList.append("					<div class=\"textfield2\">\n")
            elif displayNameBefore == displayName and talkAreaTypeBefore == talkAreaType and talkAreaMarginBefore == "rightAndPicture" and talkAreaMargin == "right" and not talkAreaTypeBefore == "cut":
                newCreateList.append("					<div class=\"textfield2\">\n")
            elif displayNameBefore == displayName and talkAreaTypeBefore == talkAreaType and talkAreaMarginBefore == "left" and talkAreaMargin == "leftAndPicture" and not talkAreaTypeBefore == "cut":
                newCreateList.append("					<div class=\"textfield2\">\n")
            elif displayNameBefore == displayName and talkAreaTypeBefore == talkAreaType and talkAreaMarginBefore == "leftAndPicture" and talkAreaMargin == "left" and not talkAreaTypeBefore == "cut":
                newCreateList.append("					<div class=\"textfield2\">\n")
            else:
                newCreateList.append("					<figure>\n")
                if iconInsert == False:
                    if repeatFlg == 0:
                        try:            
                            root, ext = os.path.splitext("./" + iconFileLocation + iconFileName)
                            with open("./" + iconFileLocation + iconFileName, mode='rb') as f:
                                src = base64.b64encode(f.read()).decode('utf-8')
                        except:
                            iconFileName = npcObjectIconFileName
                            root, ext = os.path.splitext("./" + iconFileLocation + iconFileName)
                            with open("./" + iconFileLocation + iconFileName, mode='rb') as f:
                                src = base64.b64encode(f.read()).decode('utf-8')

                    newCreateList.append("						<img src=\"data:image/" + ext.replace(".","") + ";base64," + src + "\" />\n")
                else:
                    imageAreaCounterStr = "<div id=" + "\"imageArea" + str(imageAreaCounter) + "\" >\n"
                    newCreateList.append("								" + imageAreaCounterStr)
                    newCreateList.append("									<p><label for=\"file_upload(" + str(imageAreaCounter) + ")\">▼画像<br>　選択<input type=\"file\" accept=\"image/*\" id=\"file_upload(" + str(imageAreaCounter) + ")\"  onchange=\"insertIcon( this ," + str(imageAreaCounter) + ");\"/></label></p>\n")
                    newCreateList.append("								</div>\n")
                    imageAreaCounter += 1

                newCreateList.append("					</figure>\n")
                newCreateList.append("					<solid>\n")
                newCreateList.append("					</solid>\n")
                newCreateList.append("					<div class=\"textfield1\">\n")
                newCreateList.append("						<div class=\"name\">\n")
                newCreateList.append("							<p>" + displayName + "</p>\n")
                newCreateList.append("						</div>\n")


            newCreateList.append("						<div class=\"text\">\n")

            if talkAreaMargin == "leftAndPicture" or talkAreaMargin == "rightAndPicture" or talkAreaMargin == "rightAndHiddenAndPicture":
                newCreateList.append("							<div>\n")
                imageAreaCounterStr = "<div id=" + "\"imageArea" + str(imageAreaCounter) + "\" >\n"
                newCreateList.append("								" + imageAreaCounterStr)
                newCreateList.append("									<p><label for=\"file_upload(" + str(imageAreaCounter) + ")\">▼画像選択<input type=\"file\" accept=\"image/*\" id=\"file_upload(" + str(imageAreaCounter) + ")\"  onchange=\"insertImage( this ," + str(imageAreaCounter) + ");\"/></label></p>\n")
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
                if re.search("<div class=\"text\">\n",newCreateList[-2]) and newCreateList[-1] == "":
                    newCreateList[-1] = "							<p><br></p>\n"

            newCreateList.append("						</div>\n")
            newCreateList.append("					</div>\n")
            newCreateList.append("				</div>\n")

        elif talkAreaType == "replyContinue":
            if replyContinueFlg == 0:
                if re.search("@@@返信@@@",textOriginalLine) or re.search("@@@リピート@@@",textOriginalLine):
                    newCreateList.append("				<div class=\"rightTable\">\n")
                    newCreateList.append("					<div class=\"textfield3\">\n")
                    newCreateList.append("                      <p><font color=#84c4f4>|</font> 返信する</p>\n")
                    newCreateList.append("                      <p><hr></p>\n")
                    newCreateList.append("						<div class=\"text\">\n")

                    for text in newCreateTextLine:
                        if not text == "":
                            newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                        else:
                            newCreateList.append("							<p><br></p>\n")
                    
                    newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                    if re.search("<div class=\"text\">\n",newCreateList[-2]) and newCreateList[-1] == "":
                        newCreateList[-1] = "							<p><br></p>\n"
                    
                    newCreateList.append("						</div>\n")
                    replyContinueFlg = 1
                    if not re.search("@@@追加@@@",textOriginalLine) and not re.search("@@@リピート@@@",textOriginalLine):
                        newCreateList.append("					</div>\n")
                        newCreateList.append("				</div>\n")
                        replyContinueFlg = 0
                else:
                    newCreateList.append("				<div class=\"rightTable\">\n")
                    newCreateList.append("					<div class=\"textfield3\">\n")
                    newCreateList.append("                      <p><font color=#84c4f4>|</font> 返信する</p>\n")
                    newCreateList.append("                      <p><hr></p>\n")
                    newCreateList.append("						<div class=\"text\">\n")

                    for text in newCreateTextLine:
                        if not text == "":
                            newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                        else:
                            newCreateList.append("							<p><br></p>\n")
                    
                    newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                    if re.search("<div class=\"text\">\n",newCreateList[-2]) and newCreateList[-1] == "":
                        newCreateList[-1] = "							<p><br></p>\n"
                    
                    newCreateList.append("						</div>\n")
                    newCreateList.append("					</div>\n")
                    newCreateList.append("				</div>\n")
                    
                        
            elif replyContinueFlg == 1:
                if re.search("@@@返信@@@",textOriginalLine) or re.search("@@@リピート@@@",textOriginalLine):
                    newCreateList.append("						<div class=\"text\">\n")

                    for text in newCreateTextLine:
                        if not text == "":
                            newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                        else:
                            newCreateList.append("							<p><br></p>\n")
                    
                    newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
                    if re.search("<div class=\"text\">\n",newCreateList[-2]) and newCreateList[-1] == "":
                        newCreateList[-1] = "							<p><br></p>\n"
                    
                    newCreateList.append("						</div>\n")
                    replyContinueFlg = 1
                    if not re.search("@@@追加@@@",textOriginalLine) and not re.search("@@@リピート@@@",textOriginalLine):
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
                    if re.search("<div class=\"text\">\n",newCreateList[-2]) and newCreateList[-1] == "":
                        newCreateList[-1] = "							<p><br></p>\n"
                    
                    newCreateList.append("						</div>\n")
                    newCreateList.append("					</div>\n")
                    newCreateList.append("				</div>\n")
                    replyContinueFlg = 0


        elif talkAreaType == "reply":
            newCreateList.append("				<div class=\"rightTable\">\n")
            newCreateList.append("					<div class=\"textfield3\">\n")
            newCreateList.append("                      <p><font color=#84c4f4>|</font> 返信する</p>\n")
            newCreateList.append("                      <p><hr></p>\n")
            newCreateList.append("						<div class=\"text\">\n")

   
            for text in newCreateTextLine:
                if not text == "" :
                    newCreateList.append("							<p>" + text.replace("\n","") + "</p>\n")
                else:
                    newCreateList.append("							<p><br></p>\n")
            
            newCreateList[-1] = newCreateList[-1].replace("							<p><br></p>\n","")
            if re.search("<div class=\"text\">\n",newCreateList[-2]) and newCreateList[-1] == "":
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
            if re.search("<div class=\"text\">\n",newCreateList[-2]) and newCreateList[-1] == "":
                newCreateList[-1] = "							<p><br></p>\n"

            newCreateList.append("						</div>\n")
            newCreateList.append("					</div>\n")
            newCreateList.append("				</div>\n")
        elif talkAreaType == "love":
            newCreateList.append("				<div class=\"rightTable\">\n")
            newCreateList.append("					<div class=\"textfield4\">\n")
            newCreateList.append("                      <p><font color=#FF5192>|</font>絆イベント</p>\n")
            newCreateList.append("                      <p><hr></p>\n")
            newCreateList.append("						<div class=\"text\">\n")
            newCreateList.append("							<p>" + displayName + "の絆ストーリーへ</p>\n")
            newCreateList.append("						</div>\n")
            newCreateList.append("					</div>\n")
            newCreateList.append("				</div>\n")
        elif talkAreaType == "pictureTable":
            newCreateList.append("				<div class=\"imageArea\">\n")
            imageAreaCounterStr = "<div id=" + "\"imageArea" + str(imageAreaCounter) + "\" >\n"
            newCreateList.append("					" + imageAreaCounterStr)
            newCreateList.append("						<div id=\"img\">\n")
            newCreateList.append("							<p><label for=\"file_upload(" + str(imageAreaCounter) + ")\">▼画像選択<input type=\"file\" accept=\"image/*\" id=\"file_upload(" + str(imageAreaCounter) + ")\"  onchange=\"insertImage( this ," + str(imageAreaCounter) + ");\"/></label></p>\n")
            newCreateList.append("						</div>\n")
            newCreateList.append("					</div>\n")                                            
            newCreateList.append("				</div>\n")
            imageAreaCounter += 1
        elif talkAreaType == "space":
            newCreateList.append("				<div class=\"centerTable\">\n")
            newCreateList.append("				    <p><br></p>\n")
            newCreateList.append("				</div>\n")
        elif talkAreaType == "cut":
            pass
    else:
        newCreateList.append("				<div class=\"centerTable\">\n")
        newCreateList.append("					<div class=\"textfield\">\n")
        newCreateList.append("						<div class=\"text\">\n")
        newCreateList.append("							<p>エラー:テキストエリアが空欄、あるいは有効なタグが存在しません。</p>\n")
        newCreateList.append("						</div>\n")
        newCreateList.append("					</div>\n")
        newCreateList.append("				</div>\n")

    newCreateTextLine = []


    if plumtalk_rabelCheck == False:
        newCreateList.append("			</div>\n")
        newCreateList.append("			<div class=\"footer\">\n")
        newCreateList.append("				<img src=\"data:image/webp;base64," + plumSrc + "\" alt=\"プラム\" width=3% />PlumTalk for WEB\n")
        newCreateList.append("			</div>\n")
    else:
        newCreateList.append("				<div class=\"centerTable\">\n")
        newCreateList.append("				    <p><br></p>\n")
        newCreateList.append("				</div>\n")
        newCreateList.append("			</div>\n")
    
    newCreateList.append("		</div>\n")
    newCreateList.append("	</body>\n")
    newCreateList.append("</html>")

    return newCreateList



@app.route("/")
def hello():
   input_from_python = []
   textLineOriginal = []
   plumtalk_rabelCheck = []
   titleName = []
   creatorName = []
   return render_template('index.html',input_from_python=input_from_python,textLineOriginal=textLineOriginal,plumtalk_rabelCheck=plumtalk_rabelCheck,titleName=titleName,creatorName=creatorName)

@app.route('/convertHtml', methods=['POST'])
def convertHtml():
    titleName = request.form['titleName']
    creatorName = request.form['creatorName']
    plumtalk_rabelCheck = True
#    plumtalk_rabelCheck = request.form.get('plumtalk_rabelCheck')
#    if plumtalk_rabelCheck == None:
#        plumtalk_rabelCheck = False
#    elif plumtalk_rabelCheck == "on":
#        plumtalk_rabelCheck = True

    textLineOriginal = request.form['createTalk']
    textLineOriginal = textLineOriginal.replace("\n","").replace("\r","\n")
    
    newHtmlLine = htmlCreater(textLineOriginal,titleName,creatorName,plumtalk_rabelCheck)
    newHtmlLine = ''.join(newHtmlLine)

#    with open("./templates/" + "newCreate_sumple.html",'w', encoding="utf-8") as f:
#        for newHtmlSentence in newHtmlLine:
#            f.write(newHtmlSentence)
    
    return render_template('index.html',input_from_python=newHtmlLine,textLineOriginal=textLineOriginal,plumtalk_rabelCheck=request.form.get('plumtalk_rabelCheck'),titleName=titleName,creatorName=creatorName)

    
@app.route('/convertHtml_sumple1', methods=['POST'])
def convertHtml_sumple1():
    titleName = ""
    creatorName = ""
    plumtalk_rabelCheck = True
#    plumtalk_rabelCheck = request.form.get('plumtalk_rabelCheck')
#    if plumtalk_rabelCheck == None:
#        plumtalk_rabelCheck = False
#    elif plumtalk_rabelCheck == "on":
#        plumtalk_rabelCheck = True
    textLineOriginal = request.form['sumpleTalk1']
    textLineOriginal = textLineOriginal.replace("\n","").replace("\r","\n")
    
    newHtmlLine = htmlCreater(textLineOriginal,titleName,creatorName,plumtalk_rabelCheck)
    newHtmlLine = ''.join(newHtmlLine)
    
    return render_template('index.html',input_from_python=newHtmlLine,textLineOriginal=textLineOriginal,plumtalk_rabelCheck=request.form.get('plumtalk_rabelCheck'),titleName=titleName,creatorName=creatorName)

@app.route('/convertHtml_sumple2', methods=['POST'])
def convertHtml_sumple2():
    titleName = ""
    creatorName = ""
    plumtalk_rabelCheck = True
#    plumtalk_rabelCheck = request.form.get('plumtalk_rabelCheck')
#    if plumtalk_rabelCheck == None:
#        plumtalk_rabelCheck = False
#    elif plumtalk_rabelCheck == "on":
#        plumtalk_rabelCheck = True
    textLineOriginal = request.form['sumpleTalk2']
    textLineOriginal = textLineOriginal.replace("\n","").replace("\r","\n")
    
    newHtmlLine = htmlCreater(textLineOriginal,titleName,creatorName,plumtalk_rabelCheck)
    newHtmlLine = ''.join(newHtmlLine)
    
    return render_template('index.html',input_from_python=newHtmlLine,textLineOriginal=textLineOriginal,plumtalk_rabelCheck=request.form.get('plumtalk_rabelCheck'),titleName=titleName,creatorName=creatorName)

@app.route('/convertHtml_sumple3', methods=['POST'])
def convertHtml_sumple3():
    titleName = ""
    creatorName = ""
    plumtalk_rabelCheck = True
#    plumtalk_rabelCheck = request.form.get('plumtalk_rabelCheck')
#    if plumtalk_rabelCheck == None:
#        plumtalk_rabelCheck = False
#    elif plumtalk_rabelCheck == "on":
#        plumtalk_rabelCheck = True
    textLineOriginal = request.form['sumpleTalk3']
    textLineOriginal = textLineOriginal.replace("\n","").replace("\r","\n")
    
    newHtmlLine = htmlCreater(textLineOriginal,titleName,creatorName,plumtalk_rabelCheck)
    newHtmlLine = ''.join(newHtmlLine)
    
    return render_template('index.html',input_from_python=newHtmlLine,textLineOriginal=textLineOriginal,plumtalk_rabelCheck=request.form.get('plumtalk_rabelCheck'),titleName=titleName,creatorName=creatorName)

@app.route('/convertHtml_sumple4', methods=['POST'])
def convertHtml_sumple4():
    titleName = ""
    creatorName = ""
    plumtalk_rabelCheck = True
#    plumtalk_rabelCheck = request.form.get('plumtalk_rabelCheck')
#    if plumtalk_rabelCheck == None:
#        plumtalk_rabelCheck = False
#    elif plumtalk_rabelCheck == "on":
#        plumtalk_rabelCheck = True
    textLineOriginal = request.form['sumpleTalk4']
    textLineOriginal = textLineOriginal.replace("\n","").replace("\r","\n")
    
    newHtmlLine = htmlCreater(textLineOriginal,titleName,creatorName,plumtalk_rabelCheck)
    newHtmlLine = ''.join(newHtmlLine)
    
    return render_template('index.html',input_from_python=newHtmlLine,textLineOriginal=textLineOriginal,plumtalk_rabelCheck=request.form.get('plumtalk_rabelCheck'),titleName=titleName,creatorName=creatorName)

@app.route('/convertHtml_sumple5', methods=['POST'])
def convertHtml_sumple5():
    titleName = ""
    creatorName = ""
    plumtalk_rabelCheck = True
#    plumtalk_rabelCheck = request.form.get('plumtalk_rabelCheck')
#    if plumtalk_rabelCheck == None:
#        plumtalk_rabelCheck = False
#    elif plumtalk_rabelCheck == "on":
#        plumtalk_rabelCheck = True
    textLineOriginal = request.form['sumpleTalk5']
    textLineOriginal = textLineOriginal.replace("\n","").replace("\r","\n")
    
    newHtmlLine = htmlCreater(textLineOriginal,titleName,creatorName,plumtalk_rabelCheck)
    newHtmlLine = ''.join(newHtmlLine)
    
    return render_template('index.html',input_from_python=newHtmlLine,textLineOriginal=textLineOriginal,plumtalk_rabelCheck=request.form.get('plumtalk_rabelCheck'),titleName=titleName,creatorName=creatorName)

@app.route('/convertHtml_sumple6', methods=['POST'])
def convertHtml_sumple6():
    titleName = ""
    creatorName = ""
    plumtalk_rabelCheck = True
#    plumtalk_rabelCheck = request.form.get('plumtalk_rabelCheck')
#    if plumtalk_rabelCheck == None:
#        plumtalk_rabelCheck = False
#    elif plumtalk_rabelCheck == "on":
#        plumtalk_rabelCheck = True
    textLineOriginal = request.form['sumpleTalk6']
    textLineOriginal = textLineOriginal.replace("\n","").replace("\r","\n")
    
    newHtmlLine = htmlCreater(textLineOriginal,titleName,creatorName,plumtalk_rabelCheck)
    newHtmlLine = ''.join(newHtmlLine)
    
    return render_template('index.html',input_from_python=newHtmlLine,textLineOriginal=textLineOriginal,plumtalk_rabelCheck=request.form.get('plumtalk_rabelCheck'),titleName=titleName,creatorName=creatorName)

@app.route('/convertHtml_sumple7', methods=['POST'])
def convertHtml_sumple7():
    titleName = ""
    creatorName = ""
    plumtalk_rabelCheck = True
#    plumtalk_rabelCheck = request.form.get('plumtalk_rabelCheck')
#    if plumtalk_rabelCheck == None:
#        plumtalk_rabelCheck = False
#    elif plumtalk_rabelCheck == "on":
#        plumtalk_rabelCheck = True
    textLineOriginal = request.form['sumpleTalk7']
    textLineOriginal = textLineOriginal.replace("\n","").replace("\r","\n")
    
    newHtmlLine = htmlCreater(textLineOriginal,titleName,creatorName,plumtalk_rabelCheck)
    newHtmlLine = ''.join(newHtmlLine)
    
    return render_template('index.html',input_from_python=newHtmlLine,textLineOriginal=textLineOriginal,plumtalk_rabelCheck=request.form.get('plumtalk_rabelCheck'),titleName=titleName,creatorName=creatorName)

if __name__ == '__main__':
   app.run(debug=True, threaded=False, host='0.0.0.0', port=80)
#   app.run(debug=True, threaded=False, host='localhost', port=5000)
