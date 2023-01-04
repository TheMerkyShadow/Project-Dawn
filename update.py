import os
import sys

import json
import time
import datetime
import traceback
import subprocess

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

import urllib
from urllib.request import urlopen
from urllib.request import urlretrieve

from pathlib import Path

import shutil
import platform
 
import os
import sys

import json

from pathlib import Path

class JsonConfig:
    def __init__(self, dir='config.json'):
        self.Path = Path(dir)
        self.Read() 
    def Read(self):
        self.Table = json.loads(self.Path.read_text())
    def Encode(self):
        return json.dumps(self.Table, indent=4)
    def __getitem__(self, item):
        return self.Table.get(item, None)
    def __setitem__(self, item, value):
        self.Table[item] = value
    def __delitem__(self, item):
         if item in self.Table:
              del self.Table[item]        
    def Write(self):
        self.Path.write_text(self.Encode())
    def __repr__(self):
        return repr(self.Table)
    
def Minecraft():
    return JsonConfig("manifest.json")["minecraft"]        

class GitManager:
    def __init__(self, repo='TheMerkyShadow/Project-Dawn'):
        self.Repo = repo
        self.Config = JsonConfig("manifest.json")
    def APIGateway(self, api):
        url = ( 'https://api.github.com/repos/' )
        url += ( self.Repo +api )
        try:              
            return json.load(urlopen(url))
        except urllib.error.URLError as e:
            print( traceback.format_exc() )
    def Latest(self):
        return self.APIGateway('/branches/main')['commit']['sha']
    def Diff(self):
        self.Old = self.Config['commit']        
        self.New = self.Latest()
        if not self.Old.isalnum():
            self.Old = self.New        
        if self.Old == self.New:
            return None
        return self.APIGateway('/compare/' + self.Old + '...' + self.New)['files']
    def Sync(self):
        print( "[Verification Started]" )
        diff = self.Diff()
        if diff:
            for info in diff:
                path = Path( info["filename"] )
                url = info["raw_url"]
                
                parent = path.parent
                parent.mkdir(parents=True, exist_ok=True)

                status = info["status"]
                try:
                    if status == "added" or status == "modified":
                        urlretrieve(url,path)
                    elif status == "renamed":
                        previous = Path( info["previous_filename"] )
                        if previous.is_file():
                            previous.rename(path)                        
                    elif status == "removed":
                        if path.is_file():    
                            path.unlink()
                        if parent.is_dir():
                            empty = list(os.scandir(parent)) == 0
                            if empty:                                 
                                parent.rmdir()
                                
                except Exception as e:
                    print( "ASSET ERROR:", status, path )
                    print( traceback.format_exc() )
                    return
                    
                print( status, path )
                
        self.Config.Read()
        self.Config["commit"] = self.New
        self.Config.Write()
        print( self.Old, "=>", self.New )
        print( "[Verification Complete]" )
        return
