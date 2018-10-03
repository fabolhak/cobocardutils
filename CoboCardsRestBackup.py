# Simple backup script to save all cardsets via the REST API from CoboCards
# http://www.cobocards.com/api/pmwiki.php/Main/GetStarted

# Please be aware that the response format is HTML encoded.
# It is *not* the internal CoboCards Markup language. 
# It can *not* be re-imported into CoboCards. 

# The Backup includes:
# - Folders corresponding to CC Folders
# - Subfolders corresponding to Cardsets
# - .xml file which includes all HTML encoded cards
# - Subfolders with images (.jpg) and formulars (.gif)

# All files are packaged in a .zip file.

# An CoboCards Api Key and your credentials are required to use this script.

import requests
import os
import urllib.request
import zipfile
from datetime import date
from pathlib import Path
from xml.etree import ElementTree

# credentials
api_key = ""
mail = ""
passwd = ""

# base url (should be correct)
base_url = "https://www.cobocards.com/services/api/rest/?" 

# absolute path of the temporary backup folder (.zip file is stored in parent folder)
root_folder = "CCBackup"


# request data, check response and return response as XML object if everything is ok
def getCCData(method, args):
    response = requests.get(base_url+"api_key="+api_key+"&method="+method+args)
    tree = ElementTree.fromstring(response.content)
    status = tree.get("stat")
    if status == "fail":
        err = tree.find("err")
        err_msg = "Response Error "+err.get("code")+" using "+method+": "+err.get("msg")
        raise ValueError(err_msg)    
    return tree

# test response
def getCCTestEcho():
    return getCCData("cc.test.echo", "")

# get authentication data
def getCCUserIdentify(login, password):
    pas = "&password="+password
    log = "&login="+login
    return getCCData("cc.user.identify", pas+log)

# add authentication token to arguments
def getCCDataAuth(method, args, token):
    tok = "&auth_token="+token
    return getCCData(method, tok+args)

# get a list of all CC folder
def getCCFolderList(token):
    return getCCDataAuth("cc.folders.getList", "", token)

# get CC folder with folder_id
def getCCFolder(folder_id, token):
    fid = "&folder_id="+folder_id
    return getCCDataAuth("cc.folders.get", fid, token)

# get a list of all CC cardsets
def getCCCardSetList(token):
    return getCCDataAuth("cc.cardsets.getList", "", token)

# get CC cardset with card_set_id
def getCCCardSetGetCards(card_set_id, token):
    cid = "&set_id="+card_set_id
    full_img_p = "&img_src_urls=0"
    return getCCDataAuth("cc.cardsets.getCards", cid+full_img_p, token)


# create a new folder (if not exists already)
def createFolder(string):
    if not os.path.exists(string):
        os.makedirs(string)
    return

# create and change into folder
def createAndCdFolder(string):
    createFolder(string)
    os.chdir(string)
    return

# delete a folder
def deleteFolder(string):
    path = Path(string)
    for sub in path.iterdir():
        if sub.is_dir():
            deleteFolder(sub)
        else:
            sub.unlink()
    path.rmdir()

# save a folder as .zip file with the same name
def zipFolder(string):
    filename = date.today().__str__()+'_Backup.zip'
    ziphandle = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(string):
        for file in files:
            ziphandle.write(os.path.join(root, file))
    ziphandle.close()


# go into correct folder
createAndCdFolder(root_folder)

# get token
log_data = getCCUserIdentify(mail, passwd)
token = log_data.find("token").text

# get folders and cardsets
folders = getCCFolderList(token).find("folders")
cardsets = getCCCardSetList(token).find("cardsets")

# insert root folder with id=0 to folder list
no_folder = ElementTree.Element("folder", {"id":"0", "title":"Root"})
folders.insert(0, no_folder)

# iterate over all folders, cardsets and images and store everything
for folder in folders.iterfind("folder"):
    fid = folder.get("id")
    ftitle = folder.get("title").replace('/','-')
    createAndCdFolder(ftitle)
    print("process folder: " + ftitle)
    for cardset in cardsets.iterfind("set"):
        if cardset.get("folder_id") == fid and cardset.get("size") != "0":
            cid = cardset.get("id")
            ctitle = cardset.get("title").replace('/','-')
            createAndCdFolder(ctitle)
            print("    process cardset: " + ctitle)
            
            # write cardset .xml
            filename = cid+'.xml'
            carddata = getCCCardSetGetCards(cid, token).find("cards")
            root = ElementTree.ElementTree(carddata)
            root.write(filename)
            
            # save images
            for card in carddata.iterfind("card"):
                for im in card.find("images"):
                    im_url = im.get("url")
                    im_path_file = im.get("path")
                    im_path, im_file = os.path.split(im_path_file)
                    createFolder(im_path)
                    # try to get images -> sometimes urls do not work properly!
                    req = urllib.request.Request(im_url)
                    try: urllib.request.urlopen(req)
                    except urllib.error.URLError as e:
                        print("Could not fetch", im_url, ": ", e.reason)
                    else:
                        urllib.request.urlretrieve(im_url, im_path_file)
            os.chdir("..")
    os.chdir("..")

# create .zip file and delete folder
os.chdir("..")
print("zip folder...")
zipFolder(root_folder)
print("delete folder...")
deleteFolder(root_folder)
print("exit...")



