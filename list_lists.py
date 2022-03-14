#!/usr/bin/env python3

import common

if __name__ == "__main__":

    client = common.program_start()

    lists = client.lists
    for lx in lists:
        print(lx.fqdn_listname)
