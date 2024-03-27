import os
from os import path
import tarfile
import argparse
import time
import shutil
import subprocess
import datetime
import sugarversion
import requests

# Command: python3 src/builder.py -r https://cht-dev.sugaropencloud.eu/ -i https://sugarcloud-insights-euc1.service.sugarcrm.com -u nbleyh -p *** -v 1220

# Sets up a Sugar instance based on a backup
class Builder():

    def __init__(self, version, user, pwd, sugarURL, insightsURL):
        cwd = os.getcwd()
        self.dataPath = cwd+"/data/"
        self.dbPath = cwd+"/mysql/"
        self.repairScript = cwd+"/src/php/repair.php"
        self.dbCommand = cwd+"/src/php/PruneDatabase.php"
        self.registerDbCommand = cwd+"/src/php/RegisterPuneDatabaseCommand.php"
        self.sugarVersion = sugarversion.SugarVersion(version)
        self.sugarPwd = pwd
        self.sugarUser = user
        self.sugarURL = sugarURL
        self.sugarAuthURL = sugarURL+"/rest/v11/oauth2/token"
        self.sugarInsightsURL = insightsURL+"/api/v1/backups"
        self.FQDN =  sugarURL.replace("https://", "").replace("/", "")

    def setupInstance(self):
        print("1. Cleanup...")
        self.cleanup()

        print("2. Download sources...")
        self.download()

        print("3. Configure instance...")
        self.configureInstance()
        
        print("4. Setup Sugar environment")
        os.system("sudo -S chmod -R 777 elasticsearch < /home/ansible/password.secret")
        os.system("sudo -S docker compose -f src/sugar13_stack.yml up -d < /home/ansible/password.secret")
        # Wait until containers are running
        time.sleep(60)

        print("5. Import database...")
        self.importDatabase()

        print("6. Anonymize data...")
        self.anonymize()

    def cleanup(self):
        os.system("sudo -S docker compose -f src/sugar12_stack.yml down --remove-orphans < /home/ansible/password.secret")
        if (path.exists(self.dataPath)):
            shutil.rmtree(self.dataPath)
        if (path.exists(self.dbPath)):
            shutil.rmtree(self.dbPath)
        os.mkdir(self.dataPath)

    def download(self):
        # 1. Authenticate
        data = { "grant_type":"password",
            "client_id":"sugar",
            "client_secret":"",
            "username":self.sugarUser,
            "password":self.sugarPwd,
            "platform":"base"}
        authResponse = requests.post(url = self.sugarAuthURL, data = data)
        # 2. Get backup URL
        token = authResponse.json()["access_token"]
        header = {
            "OAuth-Token" : token,
            "Content-Type" : "application/json",
            "X-Sugar-FQDN" : self.FQDN
            }
        backupResponse = requests.get(url = self.sugarInsightsURL, headers=header)
        downloadURL = backupResponse.json()["backups"][0]['download_url']
        self.backupName = downloadURL.split("/")[-1]

        print("Download backup...")
        os.system("wget -P "+os.getcwd()+" "+downloadURL)
        self.extractBackup()
        print("Download upgrader...")
        os.system("wget -P "+self.dataPath+" "+self.sugarVersion.getSilentUpgrader())
        os.system("unzip -qq "+self.dataPath+"/"+self.sugarVersion.getUpgraderFile()+" -d "+self.dataPath+"/upgrader")
        os.system("wget -P "+self.dataPath+" "+self.sugarVersion.getUpgradePackage())
        # Rename upgrade package to standard name so it can be used in Jenkins File
        os.rename(self.dataPath+"/"+self.sugarVersion.getPackageFile(), self.dataPath+"/upgrade.zip")
        print("Download tests...")
        os.system("wget -P "+self.dataPath+" "+self.sugarVersion.getPHPUnitTests())
        os.system("unzip -qq -o "+self.dataPath+"/"+self.sugarVersion.getUnitTestsFile()+" -d data/sugar")

    def extractBackup(self):
        tar = tarfile.open(os.getcwd()+"/"+self.backupName, "r:gz")
        members = []
        for member in tar.getmembers():
            if self.sugarVersion.getInstanceFolderName() in member.path and not member.name.endswith("sql") :
                members.append(member)
            if member.isfile() and member.name.endswith(self.sugarVersion.getSQLFileName()):
                members.append(member)
        tar.extractall(self.dataPath, members)
        tar.close()
        # Wait before listing new directories
        time.sleep(3)
        for item in os.listdir(self.dataPath):
            if os.path.isdir(os.path.join(self.dataPath, item)):
                shutil.move(self.dataPath+"/"+item+"/"+self.sugarVersion.getInstanceFolderName(), self.dataPath+"/sugar")
                shutil.move(self.dataPath+"/"+item+"/"+self.sugarVersion.getSQLFileName(), self.dataPath+"/"+self.sugarVersion.getSQLFileName())

    def importDatabase(self):
        # Create database
        proc = subprocess.Popen(["sudo -S docker exec sugar-mysql mysql -u root -proot -e 'create database sugar' < /home/ansible/password.secret"], stdout=subprocess.PIPE, shell=True, universal_newlines=True)
        proc.wait()
        # Import file to database
        proc = subprocess.Popen(["cat "+self.dataPath+self.sugarVersion.getSQLFileName()+" | grep -v -E '^INSERT INTO `(accounts[^ ]*|contacts[^ ]*|leads[^ ]*|opportunities[^ ]*|revenue_line_items[^ ]*|advancedreports[^ ]*|activities[^ ]*|quotes[^ ]*|products[^ ]*|product_bundle[^ ]*|purchase[^ ]*|audit_events|cj_[^ ]*|dri_[^ ]*|cases[^ ]*|calls[^ ]*|meetings[^ ]*|notes[^ ]*|tasks[^ ]*|document[^ ]*|email[^ ]*|outbound_email|eapm|job_queue|fts_queue|pmse_inbox|pmse_bpm_flow|pmse_email_message|pmse_bpm_form_action|pmse_bpm_thread|locked_field[^ ]*|hint_[^ ]*|forecast_worksheets|mobile_devices|metrics[^ ]*|metadata_cache|team_sets_modules|tag[^ ]*|subscriptions|sugarfavorites|report[^ ]*|product_templates[^ ]*|tracker[^ ]*|users_[^ ]*|user_preferences|upgrade_history|push_notifications)` VALUES ' | docker exec -i sugar-mysql mysql -u root -proot sugar"], stdout=subprocess.PIPE, shell=True, universal_newlines=True)
        proc.wait()
        # Set admin password
        proc = subprocess.Popen(["cat src/sugarconfig/admin_pwd.sql | docker exec -i sugar-mysql mysql -u root -proot sugar"], stdout=subprocess.PIPE, shell=True, universal_newlines=True)
        proc.wait()

    def configureInstance(self):
        # Set .htaccess
        shutil.copyfile("src/sugarconfig/.htaccess", self.dataPath+"/sugar/.htaccess")
        # Configuration
        config_override = open(self.dataPath+"/sugar/config_override.php", 'a')
        config_override.write("\n$sugar_config['dbconfig']['db_host_name'] = 'sugar-mysql';")
        config_override.write("\n$sugar_config['dbconfig']['db_user_name'] = 'root';")
        config_override.write("\n$sugar_config['dbconfig']['db_password'] = 'root';")
        config_override.write("\n$sugar_config['dbconfig']['db_name'] = 'sugar';")
        config_override.write("\n$sugar_config['full_text_engine']['Elastic']['host'] = 'sugar-elasticsearch';")
        config_override.write("\n$sugar_config['full_text_engine']['Elastic']['port'] = '9200';  ")
        config_override.write("\n$sugar_config['moduleInstaller']['packageScan'] = false;")
        config_override.close()
        # QRR
        shutil.copy(self.repairScript, self.dataPath+"/sugar/")
        # Copy files for anonymize function
        commandPath = self.dataPath+"sugar/custom/src/Console/Command"
        os.makedirs(commandPath)
        shutil.copy(self.dbCommand, commandPath)
        registerPath = self.dataPath+"sugar/custom/Extension/application/Ext/Console"
        os.makedirs(registerPath)
        shutil.copy(self.registerDbCommand, registerPath)

    def anonymize(self):
        # Perform QRR
        proc = subprocess.Popen(["sudo -S docker exec -t --user sugar sugar-web1 bash -c 'php /var/www/html/sugar/repair.php' < /home/ansible/password.secret"], stdout=subprocess.PIPE, shell=True, universal_newlines=True)
        proc.wait()
        # Run CLI
        proc = subprocess.Popen(["sudo -S docker exec -t --user sugar sugar-web1 bash -c 'php /var/www/html/sugar/bin/sugarcrm ps:prunedb' < /home/ansible/password.secret"], stdout=subprocess.PIPE, shell=True, universal_newlines=True)


parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version", default="1220" , help = "The Sugar Version")
parser.add_argument("-u", "--user", default="nbleyh" , help = "Admin user of the Sugar instance")
parser.add_argument("-p", "--pwd", default="Sugar123" , help = "Password of the admin user")
parser.add_argument("-r", "--url",  default="https://ewnutrition-dev.sugaropencloud.eu" , help = "URL of the Sugar instance")
parser.add_argument("-i", "--insights",  default="https://sugarcloud-insights-euc1.service.sugarcrm.com" , help = "URL of Sugar Insights")
args = parser.parse_args()

builder = Builder(args.version, args.user, args.pwd, args.url, args.insights)
builder.setupInstance()
