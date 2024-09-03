import os
from os import path
import shutil
from shutil import ignore_patterns
import argparse
import manifest
import time
import glob
import subprocess
from pathlib import Path

# Command: python3 src/packager.py -t zhinst_1120_phase1_S28 -b zhinst_1120_phase1_S27 -r git@github.com:sugarcrm-ps/ps-dev-zhinst.git -u "1.0" -a "ZHINST Phase 1 S27"

class Packager():

    def __init__(self):
        cwd = os.getcwd()
        self.repoPath = cwd+"/repo"
        self.deltaPath=cwd+"/delta"
        self.packagePath = cwd+"/package"
        self.removeLegacyFilesScript = cwd+"/src/removeLegacyFiles.php"
        self.deleteFiles = False
        self.man = manifest.Manifest()

    def setTarget(self, target):
        self.target = target

    def setBase(self, base):
        self.base = base

    def setRepository(self, repo):
        self.repo = repo

    def setSugarVersion(self, sugarVersion):
        self.man.setSugarVersion(sugarVersion)

    def setVersion(self, version):
        self.man.setVersion(version)

    def setName(self, name):
        self.name = name
        self.man.setName(name)

    def setDescription(self, description):
        self.man.setDescription(description)

    def createPackage(self):
        print("1. Cleanup...")
        self.cleanup()

        print("2. Get sources...")
        self.performGitCheckout()

        print("3. Perform delta...")
        self.performDelta()

        print("4. Check deleted files...")
        self.processDeletedFiles()

        print("5. Copy files...")
        self.copyFiles()

        print("6. Create manifest...")
        self.man.createManifest(self.packagePath)

        print("7. Zip package...")
        shutil.make_archive(self.packagePath+"/../"+time.strftime("%Y%m%d")+"_"+self.name.replace(" ", "_"), 'zip', self.packagePath)

    def performGitCheckout(self):
        os.system("git clone -b "+self.base+" "+self.repo+" "+self.repoPath)
        os.chdir(self.repoPath)
        os.system("git checkout "+self.target)

    def performDelta(self):
        if not path.exists(self.deltaPath):
            os.mkdir(self.deltaPath)
        if (not path.exists(self.packagePath)):
            os.mkdir(self.packagePath)
        os.chdir(self.repoPath)
        os.system("rsync -R -s -v \"$(git diff --diff-filter=ACMR "+self.base+".."+self.target+" --name-only)\" "+self.deltaPath)

    def processDeletedFiles(self):
        # Are there files to be deleted
        os.chdir(self.repoPath)
        proc = subprocess.Popen(["git diff "+self.base+".."+self.target+" --name-only --diff-filter=D | cut -c10-199"], stdout=subprocess.PIPE, shell=True, universal_newlines=True)
        deleteFile = open(self.packagePath+"/delete.txt", 'a')
        for line in proc.stdout:
            deleteFile.write(line)
            self.deleteFiles = True
        proc.wait()

    def copyFiles(self):
        # Application files
        shutil.copytree(self.deltaPath+"/sugarcrm", self.packagePath+"/files")
        # Script files
        postScriptsPathSource = self.deltaPath+"/customer/upgrade/"+self.target+"/scripts/php/post/"
        preScriptsPathSource = self.deltaPath+"/customer/upgrade/"+self.target+"/scripts/php/pre/"
        postScriptsPathTarget = self.packagePath+"/scripts/post/"
        preScriptsPathTarget = self.packagePath+"/scripts/pre/"
        if (path.exists(postScriptsPathSource)):
            shutil.copytree(postScriptsPathSource, postScriptsPathTarget, ignore=ignore_patterns('.*'))
        else :
            print("No post script files found")
        if (path.exists(preScriptsPathSource)):
            shutil.copytree(preScriptsPathSource, preScriptsPathTarget, ignore=ignore_patterns('.*'))
        else :
            print("No pre script files found")
        # removeLegacyFiles script
        if (self.deleteFiles):
            preScripts = Path(preScriptsPathTarget)
            preScripts.mkdir(parents=True, exist_ok=True)
            shutil.copy(self.removeLegacyFilesScript, preScriptsPathTarget)

    def cleanup(self):
        if (path.exists(self.repoPath)):
            shutil.rmtree(self.repoPath)
        if (path.exists(self.packagePath)):
            shutil.rmtree(self.packagePath)
        if (path.exists(self.deltaPath)):
            shutil.rmtree(self.deltaPath)
        for f in os.listdir(os.getcwd()):
            if f.endswith(".zip"):
                os.remove(os.path.join(os.getcwd(), f))

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version", default="11.2" , help = "Sugar Version")
parser.add_argument("-t", "--target", required=True , help = "Name of the Target Branch")
parser.add_argument("-b", "--base", required=True , help = "Name of the Base Branch")
parser.add_argument("-r", "--repo", required=True , help = "Git Repository")
parser.add_argument("-u", "--buildnum", default="1.0" , help = "Build Number")
parser.add_argument("-a", "--name",  required=True , help = "Name of the package")
parser.add_argument("-d", "--description", default="" , help = "Description of the package")
args = parser.parse_args()

packager = Packager()
packager.setBase(args.base)
packager.setTarget(args.target)
packager.setRepository(args.repo)
packager.setSugarVersion(args.version)
packager.setVersion(args.buildnum)
packager.setName(args.name)
packager.setDescription(args.description)
packager.createPackage()


