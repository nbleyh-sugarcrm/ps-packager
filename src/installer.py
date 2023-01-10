import requests
import json
import os.path
import os
import argparse
import time
import shutil
import subprocess


# Command: python3 src/installer.py -a "ZHINST Phase 1 S27"
class Installer():

    def __init__(self):
        cwd = os.getcwd()
        self.sugarPath = cwd+"/data/sugar"

    def setSugarURL(self, sugarURL):
        self.sugarAuthURL = sugarURL+"/rest/v11/oauth2/token"
        self.sugarPackagesURL = sugarURL+"/rest/v11/Administration/packages"

    def setPackageName(self, packageName):
        generatedPackage = time.strftime("%Y%m%d")+"_"+packageName.replace(" ", "_")+".zip"
        if (os.path.exists(os.getcwd()+"/"+generatedPackage)):
            self.package = os.getcwd()+"/"+generatedPackage
        else:
            self.package = os.getcwd()+"/"+packageName

    def setUserName(self, username):
        self.username = username

    def setPwd(self, pwd):
        self.pwd = pwd

    def run(self):
        print("Installing package "+self.package)
        # 1. Authenticate
        data = { "grant_type":"password",
                "client_id":"sugar",
                "client_secret":"",
                "username":self.username,
                "password":self.pwd,
                "platform":"base"}
        authResponse = requests.post(url = self.sugarAuthURL, data = data)
        # 2. Upload package
        token = authResponse.json()["access_token"]
        header = {"oauth-token" : token}
        files = {"upgrade_zip": open(self.package,'rb')}
        uploadResponse = requests.post(url = self.sugarPackagesURL, headers=header, files=files)
        if (uploadResponse.json().get("error")=="upload_package_error"):
            print("Package could not be uploaded")
            print(uploadResponse.json())
        # 3. Install package
        packageID = uploadResponse.json()["file_install"]
        installResponse = requests.get(url = self.sugarPackagesURL+"/"+packageID+"/install", headers=header)
        if (installResponse.json()["status"]!="installed"):
            raise Exception("Package installation failed: "+installResponse.json())
        print("Installation status: "+installResponse.json()["status"])
        # 4. Perform QRR
        print("Run QRR")
        proc = subprocess.Popen(["docker exec -t --user sugar sugar-web1 bash -c 'php /var/www/html/sugar/repair.php'"], stdout=subprocess.PIPE, shell=True, universal_newlines=True)
        proc.wait()
        print("QRR Finished")

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--url",  default="http://localhost/sugar/" , help = "URL of the Sugar instance")
parser.add_argument("-a", "--name",  required=True , help = "Name of the package")
parser.add_argument("-u", "--user", default="admin" , help = "Admin user of the Sugar instance")
parser.add_argument("-p", "--pwd", default="Password123" , help = "Password of the admin user")
args = parser.parse_args()

installer = Installer()
installer.setSugarURL(args.url)
installer.setPackageName(args.name)
installer.setUserName(args.user)
installer.setPwd(args.pwd)
installer.run()
