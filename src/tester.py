import argparse
import os


# wget https://honeycomb.sugarcrm.io/download/release/12.0.0/265/silentUpgrade-PRO-12.0.0.zip
# unzip silentUpgrade-PRO-12.0.0.zip -d ./upgrader
# wget https://honeycomb.sugarcrm.io/download/release/12.0.0/265/SugarEnt-Upgrade-11.3.0-to-12.0.0.zip
# php upgrader/CliUpgrader.php -z /var/www/html/SugarEnt-Upgrade-11.3.0-to-12.0.0.zip -l upgrade.log -s /var/www/html/cht-sugarcrm/ -u nbleyh -S healthcheck

# Command: python3 src/tester.py -u https://honeycomb.sugarcrm.io/download/release/12.0.0/265/silentUpgrade-PRO-12.0.0.zip -p https://honeycomb.sugarcrm.io/download/release/12.0.0/265/SugarEnt-Upgrade-11.3.0-to-12.0.0.zip
class Tester():

    def __init__(self):
        cwd = os.getcwd()
        self.dataPath = cwd+"/data/"

    def setSilentUpgrader(self, silentUpgrader):
        self.silentUpgrader = silentUpgrader

    def setUpgradePackage(self, upgradePackage):
        self.upgradePackage=upgradePackage

    def setDockerContainer(self, dockerContainer):
        self.dockerContainer = dockerContainer

    def runHealthcheck(self):
        upgraderFile = self.silentUpgrader.split("/")[-1]
        packageFile = self.upgradePackage.split("/")[-1]
        os.system("wget -P "+self.dataPath+" "+self.silentUpgrader)
        os.system("unzip "+self.dataPath+"/"+upgraderFile+" -d "+self.dataPath+"/upgrader")
        os.system("wget -P "+self.dataPath+" "+self.upgradePackage)
        os.system("docker exec "+self.dockerContainer+" php /var/www/html/upgrader/CliUpgrader.php -z /var/www/html/"+packageFile+" -l /var/www/html/upgrader/health.log -s /var/www/html/sugar/ -u admin -S healthcheck")

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--upgrader",  required=True , help = "URL of the Silent Upgrader zip")
parser.add_argument("-p", "--package", required=True , help = "URL of the Upgrade Package zip")
parser.add_argument("-d", "--docker", default="sugar-web1" , help = "Docker container where to run the tests")
args = parser.parse_args()

tester = Tester()
tester.setUpgradePackage(args.package)
tester.setSilentUpgrader(args.upgrader)
tester.setDockerContainer(args.docker)
tester.runHealthcheck()