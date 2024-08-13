

class SugarVersion():

    def __init__(self, version):
        self.version = version

    def getSilentUpgrader(self):
        if (self.version == '1130'):
            return "https://honeycomb.sugarcrm.io/download/release/12.0.0/265/silentUpgrade-PRO-12.0.0.zip"
        if (self.version == '1200'):
            return "https://honeycomb.sugarcrm.io/download/train/12.1.0/134/silentUpgrade-PRO-12.1.0.zip"
        if (self.version == '1210'):
            return "https://honeycomb.sugarcrm.io/download/train/12.2.0/125/silentUpgrade-PRO-12.2.0.zip"
        if (self.version == '1220'):
            return "https://honeycomb.sugarcrm.io/download/train/12.3.0/207/silentUpgrade-PRO-12.3.0.zip"
        if (self.version == '1230'):
            return "https://honeycomb.sugarcrm.io/download/train/13.0.0/167/silentUpgrade-PRO-13.0.0.zip"
        if (self.version == '1300'):
            return "https://honeycomb.sugarcrm.io/download/train/13.1.0/75/silentUpgrade-PRO-13.1.0.zip"
        if (self.version == '1310'):
            return "https://honeycomb.sugarcrm.io/download/train/13.2.0/49/silentUpgrade-PRO-13.2.0.zip"
        if (self.version == '1320'):
            return "https://honeycomb.sugarcrm.io/download/release/13.2.0/205/silentUpgrade-PRO-13.2.0.zip"
        if (self.version == '1330'):
            return "https://honeycomb.service.sugarcrm.com/download/build/13.3.0/297/silentUpgrade-PRO-13.3.0.zip"
        if (self.version == '1400'):
            return "https://honeycomb.service.sugarcrm.com/download/build/14.0.0/233/silentUpgrade-PRO-14.0.0.zip"
        if (self.version == '1410'):
            return "https://honeycomb.service.sugarcrm.com/download/release/14.1.0/latest/silentUpgrade-PRO-14.1.0.zip"
        else:
            print(self.version+" is not a supported Sugar Version!")

    def getUpgradePackage(self):
        if (self.version == '1130'):
            return "https://honeycomb.sugarcrm.io/download/release/12.0.0/265/SugarEnt-Upgrade-11.3.0-to-12.0.0.zip"
        if (self.version == '1200'):
            return "https://honeycomb.sugarcrm.io/download/train/12.1.0/134/SugarEnt-Upgrade-12.0.0-to-12.1.0.zip"
        if (self.version == '1210'):
            return "https://honeycomb.sugarcrm.io/download/train/12.2.0/125/SugarEnt-Upgrade-12.1.0-to-12.2.0.zip"
        if (self.version == '1220'):
            return "https://honeycomb.sugarcrm.io/download/train/12.3.0/207/SugarEnt-Upgrade-12.2.0-to-12.3.0.zip"
        if (self.version == '1230'):
            return "https://honeycomb.sugarcrm.io/download/release/13.0.0/167/SugarEnt-Upgrade-12.3.0-to-13.0.0.zip"
        if (self.version == '1300'):
            return "https://honeycomb.sugarcrm.io/download/train/13.1.0/75/SugarEnt-Upgrade-13.0.0-to-13.1.0.zip"
        if (self.version == '1310'):
            return "https://honeycomb.sugarcrm.io/download/train/13.2.0/49/SugarEnt-Upgrade-13.1.0-to-13.2.0.zip"
        if (self.version == '1320'):
            return "https://honeycomb.sugarcrm.io/download/train/13.3.0/103/SugarEnt-Upgrade-13.2.0-to-13.3.0.zip"
        if (self.version == '1330'):
            return "https://honeycomb.service.sugarcrm.com/download/build/14.0.0/140/SugarEnt-Upgrade-13.3.0-to-14.0.0.zip"
        if (self.version == '1400'):
            return "https://honeycomb.service.sugarcrm.com/download/build/14.1.0/69/SugarEnt-Upgrade-14.0.0-to-14.1.0.zip"
        if (self.version == '1410'):
            return "https://honeycomb.service.sugarcrm.com/download/release/14.1.0/latest/SugarEnt-Upgrade-14.0.0-to-14.1.0.zip"
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
        if (self.version == '1210'):
            return "https://honeycomb.sugarcrm.io/download/release/12.1.0/200/SugarEnt-12.1.0-tests.zip"
        if (self.version == '1220'):
            return "https://honeycomb.sugarcrm.io/download/release/12.2.0/200/SugarEnt-12.2.0-tests.zip"
        if (self.version == '1230'):
            return "https://honeycomb.sugarcrm.io/download/release/12.3.0/316/SugarEnt-12.3.0-tests.zip"
        if (self.version == '1300'):
            return "https://honeycomb.sugarcrm.io/download/release/13.0.0/216/SugarEnt-13.0.0-tests.zip"
        if (self.version == '1310'):
            return "https://honeycomb.sugarcrm.io/download/release/13.1.0/251/SugarUlt-13.1.0-tests.zip"
        if (self.version == '1320'):
            return "https://honeycomb.sugarcrm.io/download/release/13.2.0/205/SugarEnt-13.2.0-tests.zip"
        if (self.version == '1330'):
            return "https://honeycomb.service.sugarcrm.com/download/build/13.3.0/297/SugarEnt-13.3.0-tests.zip"
        if (self.version == '1400'):
            return "https://honeycomb.service.sugarcrm.com/download/build/14.0.0/233/SugarEnt-14.0.0-tests.zip"
        if (self.version == '1410'):
            return "https://honeycomb.service.sugarcrm.com/download/release/14.1.0/latest/SugarEnt-14.1.0-tests.zip"
        else:
            print(self.version+" is not a supported Sugar Version!")

    def getUnitTestsFile(self):
        return self.getPHPUnitTests().split("/")[-1]

    def getInstanceFolderName(self):
        return "sugar"+self.version+"ent"

    def getSQLFileName(self):
        return self.getInstanceFolderName()+".sql"