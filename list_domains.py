#!/usr/bin/env python3

import logging

import common

if __name__ == "__main__":

    common.program_start()

    client  = common.new_client()
    domains = client.domains
    for d in domains:
        print(d)
