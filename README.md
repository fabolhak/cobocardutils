# cobocardutils
Some utility tools for the flashcard learning tool CoboCards.com

## Rest API Backuper

Simple backup script to save all cardsets via the REST API from CoboCards: http://www.cobocards.com/api/pmwiki.php/Main/GetStarted

Please be aware that the response format is HTML encoded. It is *not* the internal CoboCards Markup language.  It can *not* be re-imported into CoboCards. 

The Backup includes:
* Folders corresponding to CC Folders
* Subfolders corresponding to Cardsets
* .xml file which includes all HTML encoded cards
* Subfolders with images (.jpg) and formulars (.gif)

All files are packaged in a .zip file.

### Credentials

An CoboCards Api Key and your credentials are required to use this script (see script source code).

### Usage

`python3 CoboCardsRestBackup.py`

## Export Backuper

Simple backup script ([Jupyter Notebook](https://jupyter.org/)) to save all cardsets using the export function of Cobocards.

The exported XML files are encoded in the internal CoboCards Markup languange and can be reimported. They also include images. Latex formulars are included as source code in the card content.

### Dependencies

The script uses [Selenium](https://selenium-python.readthedocs.io/) and a [Chrome driver](https://chromedriver.storage.googleapis.com/index.html) to crawl through all cardsets and export them automatically.

### Credentials

A CoboCards username and password is required.

### Usage

Open it as a [jupyter notebook](https://jupyter.org/) and execute all fields.

##  One Note Importer

Simple importer script for Cobocard Backups to OneNote using the Microsoft [Graph API](http://graph.microsoft.com/). Data from both backup sources (see above) is required in order to preserve Latex formulars as source.

### Dependencies

You have to register an app in order to be able to use the script. The app must be able to access the following scopes: 

* `Notes.ReadWrite.All`
* `Notes.Read.All`
* `Notes.Create`
* `Notes.ReadWrite`
* `Notes.ReadWrite.CreatedByApp`

After registering, insert the cliend id and secret in the `./microsoft_graph_authenticator/config.py` file. 

### Usage

Open it as a [jupyter notebook](https://jupyter.org/) and execute all fields.
