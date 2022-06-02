import argparse
import os


# wget https://honeycomb.sugarcrm.io/download/release/12.0.0/265/silentUpgrade-PRO-12.0.0.zip
# unzip silentUpgrade-PRO-12.0.0.zip -d ./upgrader
# wget https://honeycomb.sugarcrm.io/download/release/12.0.0/265/SugarEnt-Upgrade-11.3.0-to-12.0.0.zip
# php upgrader/CliUpgrader.php -z /var/www/html/SugarEnt-Upgrade-11.3.0-to-12.0.0.zip -l upgrade.log -s /var/www/html/cht-sugarcrm/ -u nbleyh -S healthcheck

#  sudo wget https://honeycomb.sugarcrm.io/download/release/11.3.0/236/SugarEnt-11.3.0-tests.zip
#  sudo unzip -o SugarEnt-11.3.0-tests.zip -d sugar
#  docker exec -it sugar-web1 /bin/sh -c "composer install && cd tests/unit-php && ../../vendor/bin/phpunit --log-junit results.xml"

# Command: python3 src/tester.py -m unit -u https://honeycomb.sugarcrm.io/download/release/12.0.0/265/silentUpgrade-PRO-12.0.0.zip -p https://honeycomb.sugarcrm.io/download/release/12.0.0/265/SugarEnt-Upgrade-11.3.0-to-12.0.0.zip -t https://honeycomb.sugarcrm.io/download/release/11.3.0/236/SugarEnt-11.3.0-tests.zip
class Tester():

    def __init__(self):
        cwd = os.getcwd()
        self.dataPath = cwd+"/data/"

    def setSilentUpgrader(self, silentUpgrader):
        self.silentUpgrader = silentUpgrader

    def setUpgradePackage(self, upgradePackage):
        self.upgradePackage=upgradePackage

    def setPHPUnitTests(self, phpUnitTests):
        self.phpUnitTests = phpUnitTests

    def setDockerContainer(self, dockerContainer):
        self.dockerContainer = dockerContainer

    def run(self, mode):
        if (mode == "health"):
            self.runHealthcheck()
        elif(mode == "unit"):
            self.runPHPUnitTests()
        else:
            self.runHealthcheck()
            self.runPHPUnitTests()

    def runHealthcheck(self):
        print("Run Healthcheck...")
        upgraderFile = self.silentUpgrader.split("/")[-1]
        packageFile = self.upgradePackage.split("/")[-1]
        os.system("sudo wget -P "+self.dataPath+" "+self.silentUpgrader)
        os.system("sudo unzip "+self.dataPath+"/"+upgraderFile+" -d "+self.dataPath+"/upgrader")
        os.system("sudo wget -P "+self.dataPath+" "+self.upgradePackage)
        os.system("docker exec "+self.dockerContainer+" php /var/www/html/upgrader/CliUpgrader.php -z /var/www/html/"+packageFile+" -l /var/www/html/upgrader/health.log -s /var/www/html/sugar/ -u admin -S healthcheck")

    def runPHPUnitTests(self):
        print("Run PHPUnit Tests...")
        testsFile = self.phpUnitTests.split("/")[-1]
        os.system("sudo wget -P "+self.dataPath+" "+self.phpUnitTests)
        os.system("sudo unzip -o "+self.dataPath+"/"+testsFile+" -d data/sugar")
        os.system("docker exec -it sugar-web1 /bin/sh -c 'composer install && cd tests/unit-php && ../../vendor/bin/phpunit --log-junit results.xml'")

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--upgrader",  required=True , help = "URL of the Silent Upgrader zip")
parser.add_argument("-p", "--package", required=True , help = "URL of the Upgrade Package zip")
parser.add_argument("-t", "--unittests", required=True , help = "URL of the PHPUnit Tests zip")
parser.add_argument("-d", "--docker", default="sugar-web1" , help = "Docker container where to run the tests")
parser.add_argument("-m", "--mode", default="all" , help = "Run Healtheck (health), PHPUnit Tests (unit) or both (all)")
args = parser.parse_args()

tester = Tester()
tester.setUpgradePackage(args.package)
tester.setSilentUpgrader(args.upgrader)
tester.setDockerContainer(args.docker)
tester.setPHPUnitTests(args.unittests)
tester.run(args.mode)