__author__ = 'catatonic'
__author__ = 'catatonic'
__version__ = "0.2.0"
__license__ = "over 9000% free"

import argparse
from wp_plugin import *
from wp_scan import *
from wp_datastore import *
from wp_downloader import *

parser = argparse.ArgumentParser(description="Collect information on Wordpress Plugins")
parser.add_argument('-s', '--src', help='Source of plugin data', required=True)
parser.add_argument('-d', '--dest', help='Destination folder (default: ./downloads)', required=False)
parser.add_argument('-k', '--skipscan', help='Set this flag to skip scanning', action="store_true")
parser.add_argument('-t', '--datastore', help='Plugins database (default: ./datastore.db', required=False)
parser.add_argument('-l', '--limit', help='Limit for number of downloads before getting package, default is 500k',
                    required=False)
args = vars(parser.parse_args())

limit = 500000
if args['limit'] is not None:
    limit = int(args['limit'])
    print (str.format("Setting downloads limit to: {0}", limit))

downloaddir = "downloads"
if args['dest'] is not None:
    downloaddir = args['dest']

datastore = "datastore.db"
if args['datastore'] is not None:
    datastore = args['datastore']

print ("Processing data from: " + args['src'])

#todo: refactor the data retrieval to the wp_plugin file.
http = httplib2.Http('.cache')
resp, content = http.request(args['src'], "GET")
if resp['status'] != '200':
    print (resp['status'])
    print (str.format("Retrieving data from {0} failed", args['src']))
    exit(-1)

factory = WPPluginFactory(dataStore=Sqlite3DataStore(datastore), downloader=WebDownloader(downloaddir))
plugins = factory.ParseAllPluginsHtml(content)

for plugin in plugins:
    plugin.SetLimit(limit)
    scanner = SkipScanner()
    if not args['skipscan']:
        scanner = RipsScanner()
    plugin.ProcessPlugin(scanner)

exit(0)