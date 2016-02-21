__author__ = 'catatonic'

import os
import zipfile
from urllib2 import urlopen, URLError, HTTPError


class WPDownloader:
    def __init__(self, path):
        self.path = path
        return
    def TouchDownloads(self):
        raise 'Method not implemented'
    def DownloadPlugin(self, plugin):
        raise 'Method not implemented'
    def UnpackPlugin(self, plugin):
        raise 'Method not implemented'

class NopDownloader(WPDownloader):
    def __init__(self, path):
        self.path = path
        return
    def DownloadPlugin(self, plugin):
        return
    def UnpackPlugin(self, plugin):
        return

class WebDownloader(WPDownloader):
    """ Word Press Plugin File Store """
    def __init__(self, path):
        self.path = path
        self.TouchDownloads()
        return

    def TouchDownloads(self):
        """
        Creates the downloads directory if it does not exist.
        """
        if not os.path.isdir(self.path):
            os.mkdir(self.path)

    def DownloadPlugin(self, plugin):
        print ("Updating plugin source")
        href = plugin.GetDownloadUrl()
        if href is None:
            print ("Could not get Download URL")
            exit(-1)
        print (str.format("Downloading: {0}", href))
        try:
            handle = urlopen(href)
            with open(str.format("{0}/{1}", self.path, os.path.basename(href)), "wb") as local_file:
                local_file.write(handle.read())
        #handle errors
        except HTTPError, e:
            print ("HTTP Error:", e.code, href)
        except URLError, e:
            print ("URL Error:", e.reason, href)
        return

    def UnpackPlugin(self, plugin):
        """
        :param plugin: the plugin to download
        :return: No value is returned, however the .zip file is extracted and then removed
        """
        print ("Unpacking the downloaded plugin")
        href = plugin.GetDownloadUrl()
        filePath = str.format("{0}/{1}", self.path, os.path.basename(href))
        with zipfile.ZipFile(filePath) as zf:
            zf.extractall(str.format('{0}/', self.path))
            plugin.UnzippedPath = str.format("{0}{1}", self.path, zf.namelist()[0])
            print ("Setting UnzippedPath to " + plugin.UnzippedPath)
        os.remove(filePath)
        return