__author__ = 'catatonic'

import sqlite3


class WPDataStore:
    def TouchDatabase(self):
        """
        Creates the datastore if it does not exist.
        :raise: Not implemented
        """
        raise 'Method not implemented'

    def GetPreviousPlugin(self):
        raise 'Method not implemented'
    def InsertPlugin(self):
        """
        Inserts plugin information given a plugin.
        :param plugin: Plugin with the information to store.
        :raise: Not implemented
        """
        raise 'Method not implemented'

    def GetPreviousDownload(self):
        raise 'Method not implemented'

    def InsertDownload(self):
        """
        Inserts download information given a plugin
        :param plugin: Plugin which is assessed for downloads
        :raise: Not implemented
        """
        raise 'Method not implemented'


class NoDataStore(WPDataStore):
    def TouchDatabase(self):
        return
    def GetPreviousPlugin(self,plugin):
        return None
    def InsertPlugin(self, plugin):
        return
    def GetPreviousDownload(self, plugin):
        return None
    def InsertDownload(self, plugin):
        return


class Sqlite3DataStore (WPDataStore):
    """ Word Press Data Store """
    def __init__(self, path):
        self.path = path
        self.connection = None
        self.TouchDatabase()
        return

    def connect(self):
        self.connection = sqlite3.connect(self.path)

    def commit(self):
        self.connection.commit();

    def close(self):
        self.connection.close()

    def TouchDatabase(self):
        """
        Creates the database and tables if they do not exist.
        """
        self.connect()
        try:
            cursor = self.connection.cursor()
            # Create table
            cursor.execute(
                'CREATE TABLE plugins (name text, description text, version text, updated datetime, integer downloads, rating downloads, page text, entryDate datetime)')
            cursor.execute('CREATE TABLE downloads (name text, version text, entryDate datetime)')
            self.commit()
        except sqlite3.Error:
            #seriously, we don't care.
            pass
        self.close()

    def GetPreviousPlugin(self, plugin):
        self.connect()
        cursor = self.connection.cursor()
        #Get the max effective dated row from plugins where the key for name matches.
        cursor.execute(
            'select * from plugins where name=? and entryDate = (select max(entryDate) from plugins where name = ?)',
            (plugin.Name,
             plugin.Name)
        )
        previousPlugin = cursor.fetchone()
        self.close()
        return previousPlugin

    def InsertPlugin(self, plugin):
        """
        :param plugin: plugin to update the database info with.
        :return: No value is returned, but the database will have the most recent new information
        """
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute('insert into plugins values (?, ?, ?, ?, ?, ?, ?, datetime())',
                   (plugin.Name,
                    plugin.Description,
                    plugin.Version,
                    plugin.Updated,
                    plugin.Downloads,
                    plugin.Rating,
                    plugin.Page))
        self.commit()
        self.close()
        return

    def GetPreviousDownload(self, plugin):
        self.connect()
        cursor = self.connection.cursor()
        #Get the max effective dated row from downloads where the key for name matches.
        cursor.execute(
            'select * from downloads where name=? and entryDate = (select max(entryDate) from downloads where name = ?)',
            (plugin.Name,
             plugin.Name)
        )
        previousDownload = cursor.fetchone()
        self.close()
        if previousDownload is None:
            return None
        return previousDownload[1]

    def InsertDownload(self, plugin):
        """

        :param plugin: the plugin to download
        :return: True - the plugin needs to be downloaded
                 False - the plugin does not need to be downloaded.
        """
        self.connect()
        cursor = self.connection.cursor()
        #Insert new download record
        print ("Inserting new download record.")
        cursor.execute('insert into downloads values (?, ?, datetime())',
                       (plugin.Name,
                        plugin.Version))
        self.commit()
        self.close()
        return True