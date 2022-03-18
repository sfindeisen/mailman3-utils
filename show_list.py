#!/usr/bin/env python3

import logging

import common

if __name__ == "__main__":

    args = common.setup_args(domain=common.ArgMod.REQUIRED, llist=common.ArgMod.REQUIRED)
    common.setup_logging(args.verbose)

    fqdn_listname = "{}@{}".format(args.llist, args.domain)
    logging.info("searching for list: {} ...".format(fqdn_listname))

    client = common.new_client()
    lists  = client.lists
    lists  = list(filter(lambda x : (fqdn_listname == x.fqdn_listname), lists))

    if lists:
        llist = lists[0]
    else:
        raise Exception("List not found: {}".format(fqdn_listname))

    for attr in sorted(llist.settings):
        print("{}: {}".format(attr, llist.settings[attr]))
