import os
from os import path
import shutil
import argparse
import manifest
import time

# Command: python3 src/packager.py -t zhinst_1120_phase1_S27 -b zhinst_1120_phase1_S26 -r git@github.com:sugarcrm-ps/ps-dev-zhinst.git -u "11.*" -a "ZHINST Phase 1 S27"

class Packager():

    def __init__(self):
        cwd = os.getcwd()
        self.repoPath = cwd+"/../repo"
        self.deltaPath=cwd+"/../delta"
        self.packagePath = cwd+"/package"
        self.removeLegacyFilesScript = cwd+"/removeLegacyFiles.php"
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
        #self.cleanup()

        print("2. Get sources...")
        #self.performGitCheckout()

        print("3. Perform delta...")
        #self.performDelta()

        print("4. Copy files...")
        #self.copyFiles()

        print("5. Create manifest...")
        #self.man.createManifest(self.packagePath)

        print("6. Zip package...")
        shutil.make_archive(os.getcwd()+"/"+time.strftime("%Y%m%d")+"_"+self.name.replace(" ", "_"), 'zip', self.packagePath)

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
        os.system("rsync -R $(git diff --diff-filter=ACMR "+self.base+" "+self.target+" --name-only) "+self.deltaPath)
        os.system("git diff "+self.base+"..."+self.target+" --name-only --diff-filter=D | cut -c10-99 | > "+self.packagePath+"/delete.txt")
        # Are there files to be deleted
        count = len(open(self.packagePath+"/delete.txt").readlines(  ))
        if (count > 0):
            self.deleteFiles = True

    def copyFiles(self):
        # Application files
        shutil.copytree(self.deltaPath+"/sugarcrm", self.packagePath+"/files")
        # Script files
        postScriptsPath = self.packagePath+"/customer/upgrade/"+self.target+"/scripts/php/post/"
        preScriptsPath = self.packagePath+"/customer/upgrade/"+self.target+"/scripts/php/pre/"
        if (path.exists(postScriptsPath)):
            shutil.copytree(self.deltaPath+"/scripts/post", postScriptsPath)
        if (path.exists(preScriptsPath)):
            shutil.copytree(self.deltaPath+"/scripts/pre", preScriptsPath)
        # removeLegacyFiles script
        if (self.deleteFiles):
            if (not path.exists(preScriptsPath)):
                os.mkdir(preScriptsPath)
            shutil.copyfile(self.removeLegacyFilesScript, preScriptsPath)

    def cleanup(self):
        if (path.exists(self.repoPath)):
            shutil.rmtree(self.repoPath)
        if (path.exists(self.packagePath)):
            shutil.rmtree(self.packagePath)
        if (path.exists(self.deltaPath)):
            shutil.rmtree(self.deltaPath)

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


