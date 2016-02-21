__author__ = 'catatonic'

import os
from wp_plugin import *
from wp_scan import *
from wp_downloader import *
from wp_datastore import *
import argparse

parser = argparse.ArgumentParser(description="Scan directories using a scanner")
parser.add_argument('-s', '--src', help='Source of locations to scan', required=False)
parser.add_argument('-t', '--datastore', help='Plugins database (default: ./datastore.db', required=False)

args = vars(parser.parse_args())

source = "/var/www/wordpress/wp-content/plugins/"
if args['src'] is not None:
    source = args['src']
print ("Processing data from: " + source)

for filename in os.listdir(source):
    fullpath = str.format("{0}/{1}", source, filename)
    plugin = WPPlugin(dataStore=NoDataStore(), downloader=NopDownloader(fullpath))
    plugin.Name = filename
    plugin.UnzippedPath = fullpath
    scanner = RipsScanner()
    plugin.ProcessPlugin(scanner)