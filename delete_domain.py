#!/usr/bin/env python3

import common
import logging

if __name__ == "__main__":

    # setup args and logging
    args = common.setup_args(domain=common.ArgMod.REQUIRED)
    common.setup_logging(args.verbose)

    # setup client
    client = common.new_client()

    # delete domain
    domain = common.fetch_domain(client, args.domain)
    domain.delete()
