#!/usr/bin/env python3

import logging

import common

def show_attr(domain, attr):
    val = getattr(domain, attr, None)
    print("{:<20}: {}".format(attr, val))

if __name__ == "__main__":

    # setup args and logging
    args = common.setup_args(domain=common.ArgMod.REQUIRED)
    common.setup_logging(args.verbose)

    # setup client
    client = common.new_client()

    # fetch domain
    domain = common.fetch_domain(client, args.domain)

    # print domain attributes
    attrs = set(vars(domain).keys())
    # TODO: web_host is already deprecated; but what is now the right way to fetch it?
    attrs.update(['description', 'mail_host', 'alias_domain', 'web_host', 'self_link'])

    for x in sorted(attrs):
        show_attr(domain, x)
