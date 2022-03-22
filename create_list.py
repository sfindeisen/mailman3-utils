#!/usr/bin/env python3

import common
import logging

if __name__ == "__main__":

    # setup args and logging
    args = common.setup_args(domain=common.ArgMod.REQUIRED, llist=common.ArgMod.REQUIRED, lstyle=common.ArgMod.OPTIONAL, llang=common.ArgMod.OPTIONAL)
    common.setup_logging(args.verbose)

    fqdn_listname = "{}@{}".format(args.llist, args.domain)
    logging.info("create list: {} using style: {} ...".format(fqdn_listname, args.lstyle))

    # setup client
    client = common.new_client()

    if args.lstyle not in common.fetch_styles(client):
        # if the style name is wrong, list creation succeeds, but then later
        # fetching the list properties results in error 500.
        raise Exception("Unknown style name: {}".format(args.lstyle))

    domain = common.fetch_domain(client, args.domain)
    llist = domain.create_list(args.llist, style_name=args.lstyle)
    common.apply_list_settings(llist, llang=(args.llang or 'en'))
