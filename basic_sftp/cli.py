"""Console script for basic_sftp."""
import sys
import click
import os
import logging
from basic_sftp import basic_sftp


@click.command()
@click.option('--d/--f', default=False, help='Whether it is a directory or file')
@click.argument('fname', metavar="filename")
def main(d, fname):
    """This is the basic command line script for an SFTP transfer. You can select
    to transfer either a specific file or an entire directory."""

    if os.path.exists(fname):
        logging.info('Moving %s to the remote server...' % fname)
        success = basic_sftp.basic_sftp(fname, d)

        # Printe the success message
        if success:
            logging.info("Success moving the file over.")
        else:
            logging.info("Some problem has occured. Unable to move file over")
        return 0
    else:
        logging.error('File not found')
        return 1


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
