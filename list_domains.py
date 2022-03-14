#!/usr/bin/env python3

import common

if __name__ == "__main__":

    client = common.program_start()

    domains = client.domains
    for d in domains:
        print(d)
