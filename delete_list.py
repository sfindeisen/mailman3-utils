#!/usr/bin/env python3

import common
import logging

if __name__ == "__main__":

    # setup args and logging
    args = common.setup_args(domain=common.ArgMod.REQUIRED, llist=common.ArgMod.REQUIRED)
    common.setup_logging(args.verbose)

    fqdn_listname = "{}@{}".format(args.llist, args.domain)
    logging.info("delete list: {} ...".format(fqdn_listname))

    # setup client
    client = common.new_client()
    client.delete_list(fqdn_listname)
