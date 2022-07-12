

class SugarVersion():

    def __init__(self, version):
        self.version = version

    def getSilentUpgrader(self):
        if (self.version == '1130'):
            return "https://honeycomb.sugarcrm.io/download/release/12.0.0/265/silentUpgrade-PRO-12.0.0.zip"
        if (self.version == '1200'):
            return "https://honeycomb.sugarcrm.io/download/train/12.1.0/134/silentUpgrade-PRO-12.1.0.zip"
        else:
            print(self.version+" is not a supported Sugar Version!")

    def getUpgradePackage(self):
        if (self.version == '1130'):
            return "https://honeycomb.sugarcrm.io/download/release/12.0.0/265/SugarEnt-Upgrade-11.3.0-to-12.0.0.zip"
        if (self.version == '1200'):
            return "https://honeycomb.sugarcrm.io/download/train/12.1.0/134/SugarEnt-Upgrade-12.0.0-to-12.1.0.zip"
        else:
            print(self.version+" is not a supported Sugar Version!")

    def getUpgraderFile(self):
        return self.getSilentUpgrader().split("/")[-1]

    def getPackageFile(self):
        return self.getUpgradePackage().split("/")[-1]

    def getPHPUnitTests(self):
        if (self.version == '1130'):
            return "https://honeycomb.sugarcrm.io/download/release/11.3.0/236/SugarEnt-11.3.0-tests.zip"
        if (self.version == '1200'):
            return "https://honeycomb.sugarcrm.io/download/release/12.0.0/265/SugarUlt-12.0.0-tests.zip"

        else:
            print(self.version+" is not a supported Sugar Version!")

    def getUnitTestsFile(self):
        return self.getPHPUnitTests().split("/")[-1]

    def getInstanceFolderName(self):
        return "sugar"+self.version+"ent"

    def getSQLFileName(self):
        return self.getInstanceFolderName()+".sql"