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


############### I was struggling to get the context stuff to work for this ###############
############### the functionality of the file transfer works now so it would #############
############### creating different click commands in the future to get more ##############
# functionality.

# @click.argument('ssh_key', metavar='ssh_key', help='The SSH Key to access the remote server')
# add this back into the arguments and parameters for the actual method

# pass_obj = click.make_pass_decorator(basic_sftp.BasicSftp, ensure=True)


# @click.group()
# @pass_context
# def main(ctx):
#     '''Groups together the commands'''
#     pass


# @click.group(invoke_without_command=True)
# @click.argument('remotepath', metavar='remotepath', required=False)
# @click.argument('ip', metavar='ip', required=False)
# @click.argument('username', metavar='username', default='guest', required=False)
# @click.argument('password', metavar='password', default='password', required=False)
# @click.argument('port', metavar='port', default='22', required=False)
# @click.pass_context
# def main(ctx, remotepath, ip, username, password, port):
#     '''This instansiates the BasicSftp object to be able to transfer files in the future'''
#     if ctx.invoked_subcommand is None:
#         logging.info('remotepath %s ip %s username %s password %s port %s' %
#                      (remotepath, ip, username, password, port))
#         ctx.obj = basic_sftp.BasicSftp()
#         ctx.obj.setup(remotepath, ip, username, password, int(port))


# @main.command()
# @click.argument('remotepath', metavar='remotepath')
# @click.argument('ip', metavar='ip')
# @click.argument('username', metavar='username', default='guest', required=False)
# @click.argument('password', metavar='password', default='password', required=False)
# @click.argument('port', metavar='port', default='22', required=False)
# @click.pass_context
# def setup(ctx, remotepath, ip, username, password, port):
#     '''This instansiates the BasicSftp object to be able to transfer files in the future'''
#     logging.info('remotepath %s ip %s username %s password %s port %s' %
#                  (remotepath, ip, username, password, port))
#     ctx = basic_sftp.BasicSftp()
#     ctx.setup(remotepath, ip, username, password, int(port))


# @main.command()
# @click.option('--d/--f', default=False, help='Whether it is a directory or file')
# @click.argument('fname', metavar="filename")
# @pass_obj
# def transfer(obj, d, fname):
#     """This is the basic command line script for an SFTP transfer. You can select
#     to transfer either a specific file or an entire directory."""
#     logging.info('I made it to this part with the wrong stuff %s' % (str(obj)))

#     if obj:
#         logging.info('Connecting to remote server @%s . . .' % (obj.getip()))
#         obj.sftp()  # add ssh_key in later
#         logging.info('Connected to remote server @%s' % (obj.getip()))

#         if os.path.exists(fname):
#             logging.info('Moving %s to the remote server...' % fname)
#             success = obj.transferContents(fname, d)

#             # Print the success message
#             if success:
#                 logging.info("Success moving the file over.")
#             else:
#                 logging.info(
#                     "Some problem has occured. Unable to move file over")
#             return 0
#         else:
#             logging.error('File not found')
#             return 1
#     else:
#         logging.error('The SFTP Client has not been properly set up')
#         return 1


# @main.command()
# @pass_obj
# def close(ctx):
#     '''Closes the current connection for the SFTP Client'''
#     ctx.obj['sftp'].close()
#     logging.info('The connection to the remote server has been closed.')

if __name__ == "__main__":
    main()  # pragma: no cover
