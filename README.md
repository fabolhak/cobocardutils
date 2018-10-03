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
