#!/usr/bin/env python3

import logging

import common

if __name__ == "__main__":

    # setup args and logging
    args = common.setup_args(
        domain=common.ArgMod.REQUIRED,
        llist=common.ArgMod.REQUIRED,
        memail=common.ArgMod.REQUIRED,
        mname=common.ArgMod.OPTIONAL,
        mdelivery=common.ArgMod.OPTIONAL,
        minvite=common.ArgMod.OPTIONAL,
        mwelcome=common.ArgMod.OPTIONAL
    )
    common.setup_logging(args.verbose)

    fqdn_listname = "{}@{}".format(args.llist, args.domain)
    logging.info("subscribe: {} to list: {} ...".format(args.memail, fqdn_listname))

    # setup client
    client = common.new_client()

    # The admin is adding this address, so treat it as verified, confirmed
    # and approved; otherwise it could wait for the member or a moderator,
    # depending on the list's subscription policy. --invite lets the
    # member opt in by email instead.
    llist = common.fetch_list(client, fqdn_listname)
    result = llist.subscribe(args.memail,
                             display_name=args.mname,
                             pre_verified=True,
                             pre_confirmed=True,
                             pre_approved=True,
                             invitation=args.minvite,
                             send_welcome_message=args.mwelcome,
                             delivery_mode=args.mdelivery)

    # a subscription that is not complete yet comes back as a pending token
    if isinstance(result, dict):
        logging.info("subscription pending, waiting for: {}".format(result['token_owner']))
