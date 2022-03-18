#!/usr/bin/env python3

import common

if __name__ == "__main__":

    # setup args and logging
    args = common.setup_args()
    common.setup_logging(args.verbose)

    # setup client
    client = common.new_client()

    domains = client.domains
    for d in domains:
        print(d)
