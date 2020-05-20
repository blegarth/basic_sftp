"""Main module."""
import pysftp
import logging
import time
import os

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

######### OTher changes that need to be done to the program ###############
# * Have a set method for the sftp connect that allows you to change the settings of the current connection
# * Make it so that the ssh key is required for the click method
# * Fix the sftp method so that you can create a new connection if one already exists
#   or just set all of the variables and start one if none exists
# *
