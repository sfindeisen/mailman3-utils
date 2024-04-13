#!/usr/bin/env python3

import common
import logging

if __name__ == "__main__":

    # setup args and logging
    args = common.setup_args(domain=common.ArgMod.REQUIRED)
    common.setup_logging(args.verbose)

    logging.info("create domain: {} ...".format(args.domain))

    # setup client
    client = common.new_client()

    # create domain
    client.create_domain(args.domain)
    logging.warning("Remember to (create and) link the Web Host aka Django site! In your web browser login to Postorius and then go to: /admin/sites/site/ . Then remember to configure the new Web Host in /etc/mailman3/nginx.conf (or similar).")
