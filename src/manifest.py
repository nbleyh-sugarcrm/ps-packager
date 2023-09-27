from datetime import date
from datetime import datetime
import time
from typing import Dict
import os
from os import path

class Manifest():

    def __init__(self):
       date_time = datetime.fromtimestamp(int(time.time()))
       self.attributes = {'author' : "SugarCRM Projects", 'key' :  int(time.time()) , 'published_date' : date_time.strftime("%Y-%m-%d %H:%M:%S"), 'is_uninstallable' : 'false', 'type' : 'module'}
       self.manifestArray = "$manifest"
       self.installdefsArray = "$installdefs"

    def setName(self, name):
        self.attributes['name'] = name

    def setDescription(self, description):
        self.attributes['description'] = description

    def setSugarVersion(self, sugarVersion):
        v1 = {0: sugarVersion}
        versions = {'regex_matches' : v1 }
        self.attributes['acceptable_sugar_versions'] = versions

    def setVersion(self, version):
        self.attributes['version'] = version

    def createManifest(self, packagePath, copy):
        if copy:
            self.installDefs = {'id' : int(time.time()), 'copy' : {0 : {'from' : '<basepath>/files', 'to' : '.' } }}
        else:
            self.installDefs = {'id' : int(time.time())}
        self.manifest = {self.manifestArray : self.attributes, self.installdefsArray : self.installDefs}
        self.setRemoveFiles(packagePath+"/delete.txt")
        self.setPostScripts(packagePath+"/scripts/post")
        self.setPreScripts(packagePath+"/scripts/pre")
        self.ManifestFile = open(packagePath+"/manifest.php", 'a')
        self.ManifestFile.write("<?php  \n")
        self.writeManifest(self.manifest, "")
        self.ManifestFile.close()

    def setRemoveFiles(self, filepath):
        if path.exists(filepath):
            f = open(filepath)
            i = 0
            removeFiles = {}
            for line in f:
                removeFiles[i] = line.rstrip()
                i=i+1
            self.installDefs['remove_files'] = removeFiles

    def setPostScripts(self, filepath):
        if path.exists(filepath):
            scripts = os.listdir(filepath)
            i = 0
            postExecute = {}
            for script in scripts:
                postExecute[i] = "<basepath>/scripts/post/"+script
                i=i+1
            self.installDefs['post_execute'] = postExecute

    def setPreScripts(self, filepath):
        if path.exists(filepath):
            scripts = os.listdir(filepath)
            i = 0
            preExecute = {}
            for script in scripts:
                preExecute[i] = "<basepath>/scripts/pre/"+script
                i=i+1
            self.installDefs['pre_execute'] = preExecute

    def writeManifest(self, dict, tabs):
        for k, v in dict.items():
            if isinstance(v, Dict):
                if (k==self.manifestArray or k==self.installdefsArray):
                    self.ManifestFile.write(f"{tabs}{k} = array( \n")
                    self.writeManifest(v, tabs+"\t")
                    self.ManifestFile.write(tabs+"); \n")
                else:
                    self.ManifestFile.write(f"{tabs}'{k}' => array( \n")
                    self.writeManifest(v, tabs+"\t")
                    self.ManifestFile.write(tabs+"), \n")
            else:
                self.ManifestFile.write(f"{tabs}'{k}' => '{v}', \n")


