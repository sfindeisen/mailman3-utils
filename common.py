import argparse
import enum
import logging
import os
import sys

import mailmanclient

# Command line argument modifiers
@enum.unique
class ArgMod(enum.Enum):
    UNKNOWN  = 0
    OPTIONAL = 1
    REQUIRED = 2

    def is_unknown(self):
        return (self is self.UNKNOWN)
    def is_optional(self):
        return (self is self.OPTIONAL)
    def is_required(self):
        return (self is self.REQUIRED)

    def __str__(self):
        return ("{}/{}".format(self.name, self.value))
    def __bool__(self):
        return (not self.is_unknown())

# Given a Mailman3 list object, tweaks its settings in an opinionated way!
def apply_list_settings(llist):
    llist.settings['accept_these_nonmembers']    = []
    llist.settings['acceptable_aliases']         = []
    llist.settings['admin_immed_notify']         = True
    llist.settings['admin_notify_mchanges']      = True
    llist.settings['administrivia']              = True
    llist.settings['advertised']                 = True
    llist.settings['allow_list_posts']           = True
    llist.settings['anonymous_list']             = False
    llist.settings['archive_policy']             = 'private'
    llist.settings['collapse_alternatives']      = True
    llist.settings['archive_rendering_mode']     = 'text'
    llist.settings['autorespond_owner']          = 'none'
    llist.settings['autorespond_postings']       = 'none'
    llist.settings['autorespond_requests']       = 'none'
    llist.settings['autoresponse_grace_period']  = '90d'
    llist.settings['autoresponse_owner_text']    = ''
    llist.settings['autoresponse_postings_text'] = ''
    llist.settings['autoresponse_request_text']  = ''

    # save the new settings
    llist.settings.save()

def fetch_domain(client, domain):
    doms = client.domains
    doms = list(filter(lambda x: (domain == x.mail_host), doms))

    if doms:
        domc = len(doms)
        if (2 <= domc):
            raise Exception("Multiple matches for domain: {}, bailing out".format(domain))
        else:
                return doms[0]
    else:
        raise Exception("Domain not found: {}".format(domain))

def fetch_list(client, fqdn_listname):
    lists  = client.lists
    lists  = list(filter(lambda x : (fqdn_listname == x.fqdn_listname), lists))

    if lists:
        return lists[0]
    else:
        raise Exception("List not found: {}".format(fqdn_listname))

def fetch_styles(client):
    return set(client.styles['style_names'])

# Creates and returns new Mailman3 REST client.
def new_client():
    client_pass = os.getenv('MAILMAN_REST_API_PASS')
    if client_pass:
        client = mailmanclient.Client('http://localhost:8001/3.1', 'restadmin', client_pass)
        logging.debug('Mailman client: {}'.format(client))
        return client
    else:
        raise Exception("Environment variable MAILMAN_REST_API_PASS not set!")

# Configures the logging subsystem.
def setup_logging(verbose=False):
    log_format = '[{asctime}] {levelname:8} {threadName:<14} {message}'
    logging.basicConfig(stream=sys.stderr, level=(logging.DEBUG if verbose else logging.INFO), format=log_format, style='{')

def setup_args(domain=ArgMod.UNKNOWN, llist=ArgMod.UNKNOWN, lstyle=ArgMod.UNKNOWN):
    parser = argparse.ArgumentParser(
        add_help=True, allow_abbrev=False, epilog="""This program comes with ABSOLUTELY NO WARRANTY.""")

    # print("domain: {} => {},{},{}".format(domain, domain.is_unknown(), domain.is_optional(), domain.is_required()))
    # print("llist : {} => {},{},{}".format(llist,   llist.is_unknown(),  llist.is_optional(),  llist.is_required()))

    if domain:
        parser.add_argument("-d", "--domain",
                            required=domain.is_required())
    if llist:
        parser.add_argument("-l", "--list",
                            required=llist.is_required(),
                            dest="llist",
                            help="list name (without the domain)")
    if lstyle:
        parser.add_argument("-s", "--style",
                            required=lstyle.is_required(),
                            default="private-default",
                            dest="lstyle",
                            help="list style name")

    parser.add_argument("--verbose",
                        required=False,
                        action="store_true",
                        default=False,
                        help="verbose processing")

    # Parse command line arguments
    args = parser.parse_args()
    return args
