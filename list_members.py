#!/usr/bin/env python3

import logging

import mailmanclient

import common

# One line per member: the email address, then labeled properties so the
# output stays grep-friendly. The display name goes last because it may
# contain spaces.
def describe(member):
    # Mailman resolves a member's effective preferences (member, address,
    # user, site default) only in this resource, and mailmanclient has no
    # accessor for it.
    prefs = mailmanclient.Preferences(member._connection, "{}/all/preferences".format(member.self_link))
    return "{} delivery_mode={} delivery_status={} moderation_action={} verified={} bounce_score={} display_name={}".format(
        member.email,
        prefs['delivery_mode'],
        prefs['delivery_status'],
        member.moderation_action or "default",
        "yes" if member.address.verified else "no",
        member.bounce_score,
        member.display_name or "")

if __name__ == "__main__":

    # setup args and logging
    args = common.setup_args(domain=common.ArgMod.REQUIRED, llist=common.ArgMod.REQUIRED, wide=common.ArgMod.OPTIONAL)
    common.setup_logging(args.verbose)

    fqdn_listname = "{}@{}".format(args.llist, args.domain)
    logging.info("searching for list: {} ...".format(fqdn_listname))

    # setup client
    client = common.new_client()

    # fetch list and print its subscribers (owners, moderators and
    # nonmembers have their own rosters and are not included)
    llist = common.fetch_list(client, fqdn_listname)
    for member in sorted(llist.members, key=lambda m: m.email):
        print(describe(member) if args.wide else member.email)
