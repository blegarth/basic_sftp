"""Console script for basic_sftp."""
import sys
import click
import os
import logging
from basic_sftp import basic_sftp


@click.command()
@click.argument('remotepath', metavar='remotepath')
@click.argument('ip', metavar='ip')
@click.option('--ssh', metavar='ssh', is_flag=True)
def main(remotepath, ip, ssh):
    '''This instansiates the BasicSftp object to be able to transfer files in the future'''
    username = click.prompt('Username ', type=str, default='guest')
    password = click.prompt('Password ', hide_input=True, default='password')

    # If the user designated that he wanted to include the ssh key then it will be prompted
    if ssh:
        ssh_key = click.prompt('SSH Key file location ')
    else:
        ssh_key = None

    port = click.prompt('Port ', type=int, default=22)

    logging.debug('remotepath %s ip %s username %s password %s port %s' %
                  (remotepath, ip, username, password, port))
    bsftp = basic_sftp.BasicSftp(
        remotepath, ip, username, password, ssh_key, port)

    if bsftp:
        logging.info('Connecting to remote server @%s . . .' % (bsftp.getip()))
        bsftp.sftp()
        logging.info('Connected to remote server @%s' % (bsftp.getip()))

        fname = click.prompt('Filename/folder name you would like to transfer')
        if os.path.exists(fname):
            logging.info('Moving %s to the remote server...' % fname)
            d = (fname[-1] == '/')
            success = bsftp.transferContents(fname, d)

            # Print the success message
            if success:
                logging.info("Success moving the file over.")
            else:
                logging.info(
                    "Some problem has occured. Unable to move file over")
            return 0
        else:
            logging.error('File not found')
            return 1
    else:
        logging.error('The SFTP Client has not been properly set up')
        return 1


if __name__ == "__main__":
    main()  # pragma: no cover
