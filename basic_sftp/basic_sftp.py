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

    def transferPDF(self, fname):
        '''This method downloads a pdf, opens the file, saves the buffer info, and
        transfers the contents to a server (printer in the future)'''
        # ****** TO DO figure out what is supposed to go in and out
        # and if they are downloading the pdf from a url or a file
        # then figure out the format of the json so that I can better
        # write that part

        # Makes sure there is a connection
        if self.sftpConnect is None:
            self.sftp()

        # Encodes the pdf
        encoded_pdf = self.get_pdf_data_from_file(fname)
        data = {}
        data['encoded_pdf'] = encoded_pdf
        logging.info('The pdf has been encoded.')

        # Dumps the json data to a file that can be transferred to the remote server
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
        logging.info('The encoded pdf has been put into a json file.')

        # Transfers the json file to the remote server
        self.sftpConnect.put('data.json', self.remotePath + 'data.json')
        logging.info('The JSON file has been moved to the remote server.')

        # Transfers the pdf to the remote server
        filename = fname.split('/')[-1]
        self.sftpConnect.put(fname, self.remotePath + filename)
        logging.info('The pdf file has been moved to the remote server.')

        return self.sftpConnect.exists(self.remotePath)

    def encode(self, data):
        '''Returns a base64 encode value of binary data'''
        return base64.b64encode(data)

    def decode(self, data):
        '''Returns the decoded value of a base-64 encoded string'''
        return base64.b64decode(data.encode())

    def get_pdf_data_from_file(self, filename):
        ''' Open a pdf file in binary mode and returns a string encoded in base-64'''
        with open(filename, 'rb') as myFile:
            return self.encode(myFile.read())

    def get_pdf_data_from_url(self, url):
        '''Downloads and opens a pdf in binary mode and returns a string encoded in base-64'''
        myfile = requests.get(url)
        return self.encode(myfile.content)

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
