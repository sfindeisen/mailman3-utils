#!/usr/bin/env python3

import common

def fetch_lists(client, domain):
    if domain:
        doms = client.domains
        doms = list(filter(lambda x: (domain == x.mail_host), doms))

        if doms:
            domc = len(doms)
            if (2 <= domc):
                raise Exception("Multiple matches for domain: {}, bailing out".format(domain))
            else:
                return doms[0].lists
        else:
            raise Exception("Domain not found: {}".format(domain))
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
