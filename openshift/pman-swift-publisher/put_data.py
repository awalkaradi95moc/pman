#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Takes the output data in the share directory and pushes it into Swift
SWIFT_KEY enviornment variable to be passed by the template
"""

import os
import zipfile
import configparser
from keystoneauth1.identity import v3
from keystoneauth1 import session
from swiftclient import client as swift_client
from swift_handler import SwiftHandler


class SwiftStore():

    swiftConnection = None        

    def _putObject(self, containerName, key, value):
        """
        Creates an object with the given key and value and puts the object in the specified container
        """

        self.swiftConnection.put_object(containerName, key , contents=value, content_type='text/plain')
        print('Object added with key %s' %key)


    def zipdir(self, path, ziph, **kwargs):
        """
        Zip up a directory.

        :param path:
        :param ziph:
        :param kwargs:
        :return:
        """
        str_arcroot = ""
        for k, v in kwargs.items():
            if k == 'arcroot':  str_arcroot = v
        for root, dirs, files in os.walk(path):
            for file in files:
                str_arcfile = os.path.join(root, file)
                if len(str_arcroot):
                    str_arcname = str_arcroot.split('/')[-1] + str_arcfile.split(str_arcroot)[1]
                else:
                    str_arcname = str_arcfile
                try:
                    ziph.write(str_arcfile, arcname = str_arcname)
                except:
                    print("Skipping %s" % str_arcfile)


    def storeData(self, **kwargs):
        """
        Creates an object of the file and stores it into the container as key-value object 
        """

        key = ''
        for k,v in kwargs.items():
            if k == 'path': 	      key         = v

        fileName      = '/tmp/share/'
        ziphandler    = zipfile.ZipFile('/tmp/share/ziparchive.zip', 'w', zipfile.ZIP_DEFLATED)
    
        self.zipdir(fileName, ziphandler, arcroot = fileName)

        with open('/tmp/share/ziparchive.zip','rb') as f:
            zippedFileContent = f.read()
        os.remove('/tmp/share/ziparchive.zip')

        swiftHandler = SwiftHandler()
        self.swiftConnection = swiftHandler._initiateSwiftConnection()            
       
        containerName = key
        key = os.path.join('output','data') 
        self._putObject(containerName, key, zippedFileContent)
        
        #Delete temporary empty directory created by Swift
        swiftHandler._deleteEmptyDirectory(key)


if __name__ == "__main__":

    obj = SwiftStore()
    obj.storeData(path = os.environ.get('SWIFT_KEY'))
