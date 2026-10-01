#!/usr/bin/env python3

import logging

import common

if __name__ == "__main__":

    # setup args and logging
    args = common.setup_args(domain=common.ArgMod.REQUIRED, llist=common.ArgMod.REQUIRED, memail=common.ArgMod.REQUIRED)
    common.setup_logging(args.verbose)

    fqdn_listname = "{}@{}".format(args.llist, args.domain)
    logging.info("unsubscribe: {} from list: {} ...".format(args.memail, fqdn_listname))

    # setup client
    client = common.new_client()

    # The admin is removing this address, so treat it as confirmed and
    # approved; otherwise it could wait for the member or a moderator,
    # depending on the list's unsubscription policy.
    llist = common.fetch_list(client, fqdn_listname)
    llist.unsubscribe(args.memail, pre_confirmed=True, pre_approved=True)
