"""Main module."""
import pysftp
import logging
import time
import os
import io
import requests
import json
import base64

logging.basicConfig(level=logging.INFO)
remotepath = '/home/brian/files/'


class BasicSftp():
    def __init__(self, remotepath, ip, username, password, ssh_key, port):
        self.sftpConnect = None
        self.remotePath = remotepath
        self.ip = ip
        self.username = username
        self.password = password
        self.ssh_key = ssh_key
        self.port = port

    def setVariables(self, remotepath=None, ip=None, username=None, password=None, ssh_key=None, port=None):
        '''Sets the variables if you want to change them after instansiating a BasicSftp'''
        if self.sftpConnect:
            self.close()
        if remotepath:
            self.remotePath = remotepath
        if ip:
            self.ip = ip
        if username:
            self.username = username
        if password:
            self.password = password
        if ssh_key:
            self.ssh_key = ssh_key
        if port:
            self.port = port

    def sftp(self):
        '''This method creates a sftp connection to a remote server allowing you
        to transfer files later'''
        try:
            if self.ssh_key:
                self.sftpConnect = pysftp.Connection(
                    self.ip, username=self.username, password=self.password, private_key=self.ssh_key, port=self.port)
            else:
                self.sftpConnect = pysftp.Connection(
                    self.ip, username=self.username, password=self.password, port=self.port)

            return self.sftpConnect.exists(self.remotePath)

        except Exception as e:
            logging.error(e)
            return(False)

    def transferContents(self, fname, direct):
        '''This method transfers the contents of a local folder to the remote
        server'''
        try:
            # startTime = time.perf_counter()
            if direct:
                # This allows you to move the entire contents of a folder to your remote
                # server rather than just one file
                fileNum = len([f for f in os.listdir(fname)
                               if os.path.isfile(os.path.join(fname, f))])
                foldername = fname.split('/')[-2]
                newfolder = self.remotePath + foldername
                # Creates a new folder, places the items in the folder, gives privileges to the admin
                self.sftpConnect.mkdir(newfolder)
                self.sftpConnect.put_r(fname, newfolder)
                self.sftpConnect.chmod(newfolder, mode=777)
            else:
                # This will just move one specific file to the remote server
                fileNum = 1
                filename = fname.split('/')[-1]
                self.sftpConnect.put(fname, self.remotePath + filename)
            # endTime = time.perf_counter() - startTime
            logging.info('A total of %d file(s) were added in %2.4f seconds.' %
                         (fileNum, 1))
            return self.sftpConnect.exists(self.remotePath)

        except Exception as e:
            logging.error(str(e))
            return False

    def transfer_json(self, jsonObj):
        '''This method transfers the JSON object that is being passed
        to the server'''
        # Makes sure there is a connection
        if self.sftpConnect is None:
            self.sftp()

        tempfile = 'data.json'
        # Dumps the json data to a file that can be transferred to the remote server
        with open(tempfile, 'w') as outfile:
            json.dump(jsonObj, outfile)
        logging.info('The encoded pdf has been put into a json file.')

        # Transfers the json file to the remote server
        self.sftpConnect.put(tempfile, self.remotePath + 'data.json')
        logging.info('The JSON file has been moved to the remote server.')

        os.remove(tempfile)

        return self.sftpConnect.exists(self.remotePath)

    def transfer_pdf_stream(self, bites):
        '''This method takes in an opened PDF stream then converts it to a pdf
        and save it to the remote server'''
        # Makes sure there is a connection
        if self.sftpConnect is None:
            self.sftp()

        tempfile = 'data.pdf'
        # Writes the pdfstream data to the outfile
        with open(tempfile, 'wb') as outfile:
            outfile.write(bites.read())
        logging.info('The pdf stream has been converted to a pdf')

        # Transfers the pdf file to the remote server
        self.sftpConnect.put(tempfile, self.remotePath + 'data.pdf')
        logging.info('The PDF file has been moved to the remote server.')

        os.remove(tempfile)

        return self.sftpConnect.exists(self.remotePath)

    def check_open(self):
        '''Checks to see if the connection is open and returns the object'''
        return str(self.sftpConnect)

    def close(self):
        '''Closes the connection if there is one'''
        if self.sftpConnect:
            self.sftpConnect.close()

    def getip(self):
        '''Returns the IP address'''
        return self.ip

    def __str__(self):
        return('%s /n %s /n %s /n %s /n %d' % (self.remotePath, self.ip, self.username, self.password, self.port))
