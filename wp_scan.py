__author__ = 'catatonic'

import requests
from BeautifulSoup import *


class WPScanner:
    name = ""

    def Scan(self, plugin):
        """
        Performs a scan of the plugin
        :param plugin: plugin to scan, must have a location set
        :raise: Not implemented
        """
        raise 'Method not implemented'

    def GenerateReport(self, plugin):
        """
        Take results of the scan and generate a report, maybe insert the results into the database?
        Contains various business logic to help reduce the false positives from a scan.l
        :param plugin: plugin to generate a scan report for
        :raise: Not implemented
        """
        raise 'Method not implemented'

class SkipScanner(WPScanner):
    def Scan(self, plugin):
        return
    def GenerateReport(self, plugin):
	print ('Name: ', plugin.Name)
        return


class RipsScanner(WPScanner):
    def __init__(self):
        self.name = "Rips Scanner v. 0.54"
        self.scanResults = ""
        return

    def Scan(self, plugin):
        print ('Scanning plugin (' + plugin.Name + ')')
        ripsopts = {'loc':plugin.UnzippedPath,
                    'subdirs':'1',
                    'verbosity':'1',
                    'vector':'all',
                    'treestyle':'1',
                    'stylesheet':'ayti'
        }
        r = requests.post(url="http://localhost/rips-0.55/main.php", data=ripsopts)
        self.scanResults = r.text
        return

    def GenerateReport(self, plugin):
        print ('Generating report from scan')
        soup = BeautifulSoup(self.scanResults)
        statSoup = soup.find('div', attrs={'class': 'stats', 'id' : 'stats'})
        if statSoup is None:
            print ("Failed to scan " + plugin.Name)
            return
        if statSoup('table')[1]('tr') != 'No vulnerabilities found.':
            print ('\033[93m')
        print (statSoup('table')[0].text + ':')
        for row in statSoup('table')[1]('tr'):
            print ('\t' + row.text)
	print ('\033[0m')
        print ('-------------------------------')
        for row in statSoup('table')[2]('tr'):
            print ('\t' + row.text)
        print ('-------------------------------')
        print (statSoup('table')[3].text)
        return
