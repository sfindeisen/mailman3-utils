#!/usr/bin/env python3

import logging

import common

if __name__ == "__main__":

    # setup args and logging
    args = common.setup_args(domain=common.ArgMod.REQUIRED, llist=common.ArgMod.REQUIRED)
    common.setup_logging(args.verbose)

    fqdn_listname = "{}@{}".format(args.llist, args.domain)
    logging.info("searching for list: {} ...".format(fqdn_listname))

    # setup client
    client = common.new_client()

    # fetch list
    llist  = common.fetch_list(client, fqdn_listname)
    for attr in sorted(llist.settings):
        print("{}: {}".format(attr, llist.settings[attr]))
