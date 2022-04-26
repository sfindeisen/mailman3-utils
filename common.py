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
def apply_list_settings(llist, llang=None, ldesc=None):
    llist.settings['accept_these_nonmembers']    = []
    llist.settings['acceptable_aliases']         = []
    llist.settings['admin_immed_notify']         = True
    llist.settings['admin_notify_mchanges']      = True
    llist.settings['administrivia']              = True
    llist.settings['advertised']                 = True
    llist.settings['allow_list_posts']           = True
    llist.settings['anonymous_list']             = False
    llist.settings['archive_policy']             = 'private'
    llist.settings['archive_rendering_mode']     = 'text'

    llist.settings['autorespond_owner']          = 'none'
    llist.settings['autorespond_postings']       = 'none'
    llist.settings['autorespond_requests']       = 'none'
    llist.settings['autoresponse_grace_period']  = '90d'
    llist.settings['autoresponse_owner_text']    = ''
    llist.settings['autoresponse_postings_text'] = ''
    llist.settings['autoresponse_request_text']  = ''

    llist.settings['bounce_info_stale_after']                   = '7d'
    llist.settings['bounce_notify_owner_on_disable']            = True
    llist.settings['bounce_notify_owner_on_removal']            = True
    llist.settings['bounce_score_threshold']                    = 5
    llist.settings['bounce_you_are_disabled_warnings']          = 3
    llist.settings['bounce_you_are_disabled_warnings_interval'] = '7d'
    # bounces_address

    llist.settings['collapse_alternatives']      = False
    llist.settings['convert_html_to_plaintext']  = False
    llist.settings['default_member_action']      = 'defer'
    llist.settings['default_nonmember_action']   = 'reject'
    llist.settings['description']                = llist.list_name

    llist.settings['digest_send_periodic']     = True
    llist.settings['digest_size_threshold']    = 100
    llist.settings['digest_volume_frequency']  = 'monthly'
    llist.settings['digests_enabled']          = True

    llist.settings['discard_these_nonmembers']        = []
    llist.settings['display_name']                    = llist.list_name
    llist.settings['dmarc_mitigate_action']           = 'munge_from'
    llist.settings['dmarc_mitigate_unconditionally']  = False
    # dmarc_moderation_notice
    # dmarc_wrapped_message_text
    llist.settings['emergency']                       = False
    llist.settings['filter_action']                   = 'reject'
    llist.settings['filter_content']                  = False
    llist.settings['filter_extensions']               = []
    llist.settings['filter_types']                    = []
    llist.settings['first_strip_reply_to']            = False    # TODO : check how it works
    llist.settings['forward_unrecognized_bounces_to'] = 'administrators'
    llist.settings['gateway_to_mail']                 = False
    llist.settings['gateway_to_news']                 = False
    # hold_these_nonmembers
    llist.settings['include_rfc2369_headers']         = True

    if ldesc:
        llist.settings['info'] = ldesc

    # join_address
    # last_post_at
    # leave_address
    llist.settings['linked_newsgroup']                = ''
    # list_name
    # mail_host
    llist.settings['max_days_to_hold']                =  0
    llist.settings['max_message_size']                = 100
    llist.settings['max_num_recipients']              = 10
    llist.settings['member_roster_visibility']        = 'moderators'
    # moderator_password
    llist.settings['newsgroup_moderation']            = 'none'
    # next_digest_number
    llist.settings['nntp_prefix_subject_too']         = False
    # no_reply_address
    # owner_address
    llist.settings['pass_extensions']                 = []
    llist.settings['pass_types']                      = []
    llist.settings['personalize']                     = 'none'
    # post_id
    # posting_address
    # posting_pipeline

    if llang:
        llist.settings['preferred_language'] = llang

    llist.settings['process_bounces']                 = True
    llist.settings['reject_these_nonmembers']         = []
    llist.settings['reply_goes_to_list']              = 'point_to_list'
    llist.settings['reply_to_address']                = None
    # request_address
    llist.settings['require_explicit_destination']    = True
    llist.settings['respond_to_post_requests']        = False
    llist.settings['send_goodbye_message']            = True
    llist.settings['send_welcome_message']            = True
    llist.settings['subject_prefix']                  = '[{}]'.format(llist.list_name)
    llist.settings['subscription_policy']             = 'confirm_then_moderate'
    llist.settings['unsubscription_policy']           = 'confirm'
    # usenet_watermark
    # volume

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

def setup_args(domain=ArgMod.UNKNOWN, llist=ArgMod.UNKNOWN, lstyle=ArgMod.UNKNOWN, llang=ArgMod.UNKNOWN, ldesc=ArgMod.UNKNOWN):
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
    if llang:
        parser.add_argument("--lang",
                            required=llang.is_required(),
                            dest="llang",
                            help="list's preferred language")
    if ldesc:
        parser.add_argument("--desc",
                            required=ldesc.is_required(),
                            dest="ldesc",
                            help="list's description")

    parser.add_argument("--verbose",
                        required=False,
                        action="store_true",
                        default=False,
                        help="verbose processing")

    # Parse command line arguments
    args = parser.parse_args()
    return args
