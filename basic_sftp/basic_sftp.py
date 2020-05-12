"""Main module."""
import pysftp
import logging
import time
import os

logging.basicConfig(level=logging.INFO)
remotepath = '/home/brian/files/'


def basic_sftp(fname, direct):
    '''This method creates a connection to the host server and puts a file
    in that location and gets back the succcess file'''
    try:
        startTime = time.perf_counter()
        s = pysftp.Connection(
            '64.227.11.42', username='guest', password='password')

        if direct:
            # This allows you to move the entire contents of a folder to your remote
            # server rather than just one file
            fileNum = len([f for f in os.listdir(fname)
                           if os.path.isfile(os.path.join(fname, f))])
            foldername = fname.split('/')[-2]
            newfolder = remotepath + foldername
            # Creates a new folder, places the items in the folder, gives privileges to the admin
            s.mkdir(newfolder)
            s.put_r(fname, newfolder)
            s.chmod(newfolder, mode=777)
        else:
            # This will just move one specific file to the remote server
            fileNum = 1
            filename = fname.split('/')[-1]
            s.put(fname, remotepath + filename)

        endTime = time.perf_counter() - startTime
        logging.info('A total of %d file(s) were added in %2.4f seconds.' %
                     (fileNum, endTime))
        return s.exists(remotepath)

    except Exception as e:
        logging.error(str(e))
        return(False)
