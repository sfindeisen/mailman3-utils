#!/usr/bin/env python3

import common

def fetch_lists(client, domain):
    if domain:
        return common.fetch_domain(client, domain).lists
    else:
        return client.lists

if __name__ == "__main__":

    # setup args and logging
    args = common.setup_args(domain=common.ArgMod.OPTIONAL)
    common.setup_logging(args.verbose)

    # setup client
    client = common.new_client()

    # print lists
    lists = fetch_lists(client, args.domain)
    for lx in lists:
        print(lx.fqdn_listname)
