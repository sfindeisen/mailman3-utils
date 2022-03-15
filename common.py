import argparse
import logging
import os
import sys

import mailmanclient

# Creates and returns new Mailman3 REST client.
def new_client():
    client_pass = os.getenv('MAILMAN_REST_API_PASS')
    if client_pass:
        client = mailmanclient.Client('http://localhost:8001/3.1', 'restadmin', client_pass)
        logging.debug('Mailman client: {}'.format(client))
        return client
    else:
        raise Exception("Environment variable MAILMAN_REST_API_PASS not set!")

# Configures the logging subsystem.
def setup_logging(verbose=False):
    log_format = '[{asctime}] {levelname:8} {threadName:<14} {message}'
    logging.basicConfig(stream=sys.stderr, level=(logging.DEBUG if verbose else logging.INFO), format=log_format, style='{')

def setup_args():
    parser = argparse.ArgumentParser(
        add_help=True, allow_abbrev=False, epilog="""This program comes with ABSOLUTELY NO WARRANTY.""")

    parser.add_argument("--verbose",
                        required=False,
                        action="store_true",
                        default=False,
                        help="verbose processing")

    # Parse command line arguments
    args = parser.parse_args()
    return args

# Program start for the simple case.
def program_start():
    args = setup_args()
    setup_logging(args.verbose)
    return new_client()
