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

    # fetch list and print its subscribers (owners, moderators and
    # nonmembers have their own rosters and are not included)
    llist = common.fetch_list(client, fqdn_listname)
    for email in sorted(m.email for m in llist.members):
        print(email)
