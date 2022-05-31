import os
from os import path
import tarfile
import argparse
import time
import shutil
import subprocess
import boto3
import datetime

# Command: python3 src/builder.py -b cht-dev.sugaropencloud.tar.gz


# wget https://bootstrap.pypa.io/get-pip.py
# python3 get-pip.py
# pip install boto3

# Sets up a Sugar instance based on a backup
class Builder():

    def __init__(self):
        cwd = os.getcwd()
        self.dataPath = cwd+"/data/"

    def setBackupName(self, backupName):
        self.backupName = backupName

    def setSQLFileName(self, sqlFileName):
        self.sqlFileName = sqlFileName

    def setInstanceFolderName(self, instanceFolderName):
        self.instanceFolderName = instanceFolderName

    def setupInstance(self):
        print("1. Cleanup...")
        #self.cleanup()

        print("2. Download backup...")
        #self.downloadBackup()

        print("3. Unzip backup...")
        #self.extractBackup()

        print("4. Setup Sugar environment")
        os.system("docker-compose -f src/sugar12_stack.yml up -d")
        # Wait until containers are running
        time.sleep(60)

        print("5. Import database...")
        #self.importDatabase()

        print("6. Configure instance...")
        #self.configureInstance()

    def cleanup(self):
        os.system("docker-compose -f src/sugar12_stack.yml down")
        if (path.exists(self.dataPath)):
            shutil.rmtree(self.dataPath)
        os.mkdir(self.dataPath)

    def downloadBackup(self):
        client = boto3.client(
            's3',
            aws_access_key_id = '',
            aws_secret_access_key = '',
            region_name = 'eu-central-1'
        )
        client.download_file('sugar-ps-backups', self.backupName, self.dataPath+"/"+self.backupName)

    def extractBackup(self):
        tar = tarfile.open(self.dataPath+self.backupName, "r:gz")
        members = []
        for member in tar.getmembers():
            if self.instanceFolderName in member.path and not member.name.endswith("sql") :
                members.append(member)
            if member.isfile() and member.name.endswith(self.sqlFileName):
                members.append(member)
        tar.extractall(self.dataPath, members)
        tar.close()
        # Wait before listing new directories
        time.sleep(3)
        for item in os.listdir(self.dataPath):
            if os.path.isdir(os.path.join(self.dataPath, item)):
                shutil.move(self.dataPath+"/"+item+"/"+self.instanceFolderName, self.dataPath+"/sugar")
                shutil.move(self.dataPath+"/"+item+"/"+self.sqlFileName, self.dataPath+"/"+self.sqlFileName)

    def importDatabase(self):
        # Create database
        proc = subprocess.Popen(["docker exec sugar-mysql mysql -u root -proot -e 'create database sugar'"], stdout=subprocess.PIPE, shell=True, universal_newlines=True)
        proc.wait()
        # Import file to database
        proc = subprocess.Popen(["cat "+self.dataPath+self.sqlFileName+" | docker exec -i sugar-mysql mysql -u root -proot sugar"], stdout=subprocess.PIPE, shell=True, universal_newlines=True)
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
        config_override.close()

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--backup",  required=True , help = "Name of the backup file")
parser.add_argument("-i", "--instance", default="sugar1130ent" , help = "Name of the instance folder in the backup")
parser.add_argument("-s", "--sql", default="sugar1130ent.sql" , help = "Name of the sql file in the backup")
args = parser.parse_args()

builder = Builder()
builder.setBackupName(args.backup)
builder.setInstanceFolderName(args.instance)
builder.setSQLFileName(args.sql)
builder.setupInstance()
