__author__ = 'catatonic'
__version__ = "0.1"
__license__ = "over 9000% free"
from BeautifulSoup import *

import httplib2


class WPPlugin:
    """Word Press Plugin Class, contains information like: # of downloads, Rating, etc."""

    def __init__(self, dataStore, downloader):
        self.Name = ""
        self.Description = ""
        self.Version = ""
        self.Updated = ""
        self.Downloads = 0
        self.Rating = ""
        self.Page = ""
        self.DownloadLink = ""
        self.DataStore = dataStore
        self.Downloader = downloader
        self.Limit = 0
        self.UnzippedPath = ""
        return

    def SetLimit(self, limit):
        self.Limit = limit

    def GetDownloadUrl(self):
        #Check that the plugin we're looking for actually has a download page.
        if self.Page is None:
            print ("Plugin download page is NULL!")
            exit(-1)

        if self.DownloadLink != "":
            return self.DownloadLink

        http = httplib2.Http('.cache')
        resp, content = http.request(self.Page, "GET")
        if resp['status'] != '200':
            print (str.format("Retrieving data from {0} failed", self.Page))
            exit(-1)
        soup = BeautifulSoup(content)
        pageSoup = soup.find('a', attrs={'itemprop': 'downloadUrl'})
        if pageSoup['href'] is None:
            print (str.format("Could not locate download URL for {0}", self.Name))
            exit(-1)
        self.DownloadLink = pageSoup['href']
        return pageSoup['href']

    def ProcessPlugin(self, scanner):
	if self.Downloads < self.Limit:
            print('Limit not reached, skipping ' + self.Name)
            return
        previousPlugin = self.DataStore.GetPreviousPlugin(self)
        #compare the retrieved row to the plugin in order to determine if we already have an entry for it.
        if previousPlugin is None:
            #insert new record for plugin
            print ('Inserting new record for: ' + self.Name)
            self.DataStore.InsertPlugin(self)
        else:
            #do a comparison of the existing record, if it's changed update the record (insert new record with today's date)
            if self.Version != previousPlugin[2]:
                #Inform the user if a new version has appeared.
                print (str.format("New version for {0} available!", self.Name))
                self.DataStore.InsertPlugin(self)

        #Check if we need to download and update the source.
        previousDownload = self.DataStore.GetPreviousDownload(self)
        if previousDownload is not None and previousDownload == self.Version:
            print (str.format("Plugin {0} is up-to-date.", self.Name))
        else:
            self.Downloader.DownloadPlugin(self)
            self.Downloader.UnpackPlugin(self)

        scanner.Scan(self)
        scanner.GenerateReport(self)


class WPPluginFactory:
    """Word Press Plugin Factor, generates WPPlugin Objects from html."""

    def __init__(self, dataStore, downloader):
        self.DataStore = dataStore
        self.Downloader = downloader
        return

    def ParseSinglePluginHtml(self, pluginSoup):
        plugin = WPPlugin(self.DataStore, self.Downloader)
        #The basics
        plugin.Name = str(pluginSoup.find('div', attrs={'class': 'name column-name'}).text)
        plugin.Page = pluginSoup.find('div', attrs={'class': 'name column-name'}).a['href']
        plugin.Description = pluginSoup.find('div', attrs={'class': 'desc column-description'}).text
        #The harder stuff.
        plugin.Updated = pluginSoup.find('div', attrs={'class': 'column-updated'}).span['title']
        plugin.Downloads = int(pluginSoup.find('div', attrs={'class': 'column-installs'}).text.split('+')[0].replace(',',''))
        plugin.Rating = pluginSoup.find('div', attrs={'class': 'wporg-ratings'})['title'].split(' ')[0]
        return plugin

    def ParseAllPluginsHtml(self, htmlBlock):
        """

        :param htmlBlock: the block of HTML containing multiple plugin-blocks
        :return: an array of WPPlugin objects
        """
        soup = BeautifulSoup(htmlBlock)
        pluginSoups = soup.findAll('div', attrs={'class': 'plugin-card'})
        plugins = []
        for pluginSoup in pluginSoups:
            try:
                plugin = self.ParseSinglePluginHtml(pluginSoup)
                plugins.append(plugin)
            except UnicodeEncodeError:
                print (str.format("Could not process plugin because of unicode error... skipping!"))
        return plugins
