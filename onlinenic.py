# -*- coding: utf-8 -*-

import hashlib
import telnetlib
import uuid

from BeautifulSoup import BeautifulStoneSoup


"""
ONLINENIC COMMANDS
------------------

The following dict defines all the commands supported by the OnlineNIC API.
"""

ONLINENIC_COMMANDS = {
    'login': {
        'category': 'client',
        'action': 'Login',
        'checksum': {
            'name': 'login'
        }
    },
    'logout': {
        'category': 'client',
        'action': 'Logout',
        'checksum': {
            'name': 'logout'
        }
    },
    'create_contact': {
        'category': 'domain',
        'action': 'CreateContact',
        'checksum': {
            'name': 'crtcontact',
            'extra': ['name', 'org', 'email']
        }
    },
    'check_contact': {
        'category': 'domain',
        'action': 'CheckContact',
        'checksum': {
            'name': 'checkcontact',
            'extra': ['domaintype', 'contactid']
        }
    },
    'update_contact': {
        'category': 'domain',
        'action': 'UpdateContact',
        'checksum': {
            'name': 'updatecontact',
            'extra': ['domaintype', 'domain', 'contacttype']
        }
    },
    'change_registrant': {
        'category': 'domain',
        'action': 'ChangeRegistrant',
        'checksum': {
            'name': 'chgregistrant',
            'extra': ['domaintype', 'domain', 'name', 'org', 'email']
        }
    },
    'query_eu_trade': {
        'category': 'domain',
        'action': 'QueryEuTrade',
        'checksum': {
            'name': 'queryeutrade',
            'extra': ['domain']
        }
    },
    'check_domain': {
        'category': 'domain',
        'action': 'CheckDomain',
        'checksum': {
            'name': 'checkdomain',
            'extra': ['domaintype', 'domain']
        }
    },
    'info_domain': {
        'category': 'domain',
        'action': 'InfoDomain',
        'checksum': {
            'name': 'infodomain',
            'extra': ['domaintype', 'domain']
        }
    },
    'create_domain': {
        'category': 'domain',
        'action': 'CreateDomain',
        'checksum': {
            'name': 'createdomain',
            'extra': ['domaintype', 'domain', 'period', 'dns', 'registrant',
                     'admin', 'tech', 'billing', 'password']
        }
    },
    'renew_domain': {
        'category': 'domain',
        'action': 'RenewDomain',
        'checksum': {
            'name': 'renewdomain',
            'extra': ['domaintype', 'domain', 'period']
        }
    },
    'delete_domain': {
        'category': 'domain',
        'action': 'DeleteDomain',
        'checksum': {
            'name': 'deldomain',
            'extra': ['domaintype', 'domain']
        }
    },
    'update_domain_status': {
        'category': 'domain',
        'action': 'UpdateDomainStatus',
        'checksum': {
            'name': 'updatedomainstatus',
            'extra': ['domaintype', 'domain']
        }
    },
    'update_domain_extra': {
        'category': 'domain',
        'action': 'UpdateDomainExtra',
        'checksum': {
            'name': 'updatedomainextra',
            'extra': ['domaintype', 'domain']
        }
    },
    'update_domain_dns': {
        'category': 'domain',
        'action': 'UpdateDomainDns',
        'checksum': {
            'name': 'updatedomaindns',
            'extra': ['domaintype', 'domain']
        }
    },
    'update_domain_pwd': {
        'category': 'domain',
        'action': 'UpdateDomainPwd',
        'checksum': {
            'name': 'updatedomainpwd',
            'extra': ['domaintype', 'domain', 'password']
        }
    },
    'info_domain_extra': {
        'category': 'domain',
        'action': 'InfoDomainExtra',
        'checksum': {
            'name': 'infodomainextra',
            'extra': ['domaintype', 'domain']
        }
    },
    'get_auth_code': {
        'category': 'domain',
        'action': 'GetAuthcode',
        'checksum': {
            'name': 'getauthcode',
            'extra': ['domaintype', 'domain']
        }
    },
    'check_host': {
        'category': 'domain',
        'action': 'CheckHost',
        'checksum': {
            'name': 'checkhost',
            'extra': ['domaintype', 'hostname']
        }
    },
    'info_host': {
        'category': 'domain',
        'action': 'InfoHost',
        'checksum': {
            'name': 'infohost',
            'extra': ['domaintype', 'hostname']
        }
    },
    'create_host': {
        'category': 'domain',
        'action': 'CreateHost',
        'checksum': {
            'name': 'createhost',
            'extra': ['domaintype', 'hostname', 'addr']
        }
    },
    'update_host': {
        'category': 'domain',
        'action': 'UpdateHost',
        'checksum': {
            'name': 'updatehost',
            'extra': ['domaintype', 'hostname', 'addaddr', 'remaddr']
        }
    },
    'delete_host': {
        'category': 'domain',
        'action': 'DeleteHost',
        'checksum': {
            'name': 'deletehost',
            'extra': ['domaintype', 'hostname', 'addaddr', 'remaddr']
        }
    },
    'query_cust_transfer': {
        'category': 'domain',
        'action': 'QueryCustTransfer',
        'checksum': {
            'name': 'querycusttransfer',
            'extra': ['domaintype', 'domain', 'op']
        }
    },
    'request_cust_transfer': {
        'category': 'domain',
        'action': 'RequestCustTransfer',
        'checksum': {
            'name': 'requestcusttransfer',
            'extra': ['domaintype', 'domain', 'password', 'curID']
        }
    },
    'cust_transfer_set_pwd': {
        'category': 'domain',
        'action': 'CustTransferSetPwd',
        'checksum': {
            'name': 'custtransfersetpwd',
            'extra': ['domaintype', 'domain', 'password']
        }
    },
    'query_reg_transfer': {
        'category': 'domain',
        'action': 'QueryRegTransfer',
        'checksum': {
            'name': 'queryregtransfer',
            'extra': ['domaintype', 'domain']
        }
    },
    'request_reg_transfer': {
        'category': 'domain',
        'action': 'RequestRegTransfer',
        'checksum': {
            'name': 'requestregtransfer',
            'extra': ['domaintype', 'domain']
        }
    },
    'cancel_reg_transfer': {
        'category': 'domain',
        'action': 'CancelRegTransfer',
        'checksum': {
            'name': 'cancelregtransfer',
            'extra': ['domaintype', 'domain']
        }
    },
    'get_account_balance': {
        'category': 'account',
        'action': 'GetAccountBalance',
        'checksum': {
            'name': 'getaccountbalance'
        }
    },
    'get_customer_info': {
        'category': 'account',
        'action': 'GetCustomerInfo',
        'checksum': {
            'name': 'getcustomerinfo'
        }
    },
    'modify_customer_info': {
        'category': 'account',
        'action': 'ModCustomerInfo',
        'checksum': {
            'name': 'modcustomerinfo'
        }
    },
    'order_ssl': {
        'category': 'ssl',
        'action': 'Order',
        'checksum': {
            'name': 'Order'
        }
    },
    'get_approver_email_list': {
        'category': 'ssl',
        'action': 'GetApproverEmailList',
        'checksum': {
            'name': 'GetApproverEmailList'
        }
    },
    'cancel_ssl': {
        'category': 'ssl',
        'action': 'Cancel',
        'checksum': {
            'name': 'Cancel',
            'extra': ['orderId']
        }
    },
    'info_ssl': {
        'category': 'ssl',
        'action': 'Info',
        'checksum': {
            'name': 'Info',
            'extra': ['orderId']
        }
    },
    'resend_approver_email': {
        'category': 'ssl',
        'action': 'ResendApproverEmail',
        'checksum': {
            'name': 'ResendApproverEmail',
            'extra': ['orderId']
        }
    },
    'change_approver_email': {
        'category': 'ssl',
        'action': 'ChangeApproverEmail',
        'checksum': {
            'name': 'ChangeApproverEmail',
            'extra': ['orderId']
        }
    },
    'get_certs': {
        'category': 'ssl',
        'action': 'GetCerts',
        'checksum': {
            'name': 'GetCerts'
        }
    },
    'reissue_ssl': {
        'category': 'ssl',
        'action': 'Reissue',
        'checksum': {
            'name': 'Reissue',
            'extra': ['orderId']
        }
    },
    'resend_fulfillment_email': {
        'category': 'ssl',
        'action': 'ResendFulfillmentEmail',
        'checksum': {
            'name': 'ResendFulfillmentEmail',
            'extra': ['orderId']
        }
    },
    'parse_csr': {
        'category': 'ssl',
        'action': 'ParseCSR',
        'checksum': {
            'name': 'ParseCSR',
            'extra': ['orderId']
        }
    }
}


"""
ONLINENIC DOMAIN TYPES
----------------------

OnlineNIC assigns codes to each domain name extension they support. The codes
below are for non-IDN domains.
"""

ONLINENIC_DOMAIN_TYPES = {
    '.com': '0',
    '.net': '0',
    '.org': '807',
    '.cn': '220',
    '.biz': '800',
    '.info': '805',
    '.us': '806',
    '.in': '808',
    '.mobi': '903',
    '.eu': '902',
    '.asia': '905',
    '.me': '906',
    '.name': '804',
    '.tel': '907',
    '.cc': '600',
    # Chinese IDN
    #'.cc': '610',
    '.tv': '400',
    '.tw': '302',
    '.uk': '901',
    '.co': '908',
}


"""
ONLINENIC IDN CODES
-------------------

If you're working with an IDN domain name, you will need to identify the ISO
using one of the codes below. These codes are grouped by
ONLINENIC_DOMAIN_TYPES.
"""

ONLINENIC_IDN_CODES = {
    '0': {
        '0': 'English',
        '1': 'Chinese(simplified)-gb2312',
        '10101': 'Danish-1',
        '10102': 'Dutch-1',
        '10103': 'Faeroese-1',
        '10104': 'Finnish-1',
        '10105': 'Flemish-1',
        '10106': 'German-1',
        '10107': 'Icelandic-1',
        '10108': 'Irish-1',
        '10109': 'Italian-1',
        '10110': 'Norwegian-1',
        '10111': 'Portuguese-1',
        '10112': 'Spanish-1',
        '10113': 'Swedish-1',
        '10201': 'Croatian-2',
        '10202': 'Czech-2',
        '10203': 'Hungarian-2',
        '10204': 'Polish-2',
        '10205': 'Romanian-2',
        '10206': 'Slovak-2',
        '10207': 'Slovenian-2',
        '10208': 'Serbian-2',
        '10301': 'Afrikaans-3',
        '10302': 'Catalan-3',
        '10303': 'Esperanto-3',
        '10304': 'Maltese-3',
        '10401': 'Estonian-4',
        '10402': 'Greenlandic-4',
        '10403': 'Latvian-4',
        '10404': 'Lithuanian-4',
        '10501': 'Cyrillic-5',
        '10701': 'Greek-7',
        '10901': 'French-9',
        '10902': 'Turkish-9',
        '11001': 'Sami-11',
        '11401': 'Welsh-14',
        '11501': 'Vietnamese',
        '151': 'Thai-windows-874',
        '152': 'Devanagari-utf8',
        '153': 'Gurmukhi-utf8',
        '154': 'Gujarati-utf8',
        '155': 'Oriya-utf8',
        '156': 'Tamil-utf8',
        '157': 'Telugu-utf8',
        '158': 'Kannada-utf8',
        '159': 'Malayalam-utf8',
        '160': 'Sinhala-utf8',
        '161': 'Lao-utf8',
        '162': 'Tibetan-utf8',
        '163': 'Myanmar-utf8',
        '164': 'Kmer-utf8',
        '180': 'Hebrew-utf8',
        '181': 'Arabic-utf8',
        '182': 'Syriac-utf8',
        '183': 'Thaana-utf8',
        '184': 'Ethiopic-utf8',
        '185': 'Cherokee-utf8',
        '186': 'Canadian Aboriginal Symbols-utf8',
        '187': 'Mongolian-utf8',
        '2': 'Chinese(traditional)-big5',
        '3': 'Japanese-shift-jis',
        '4': 'Korean-euc-kr'
    },
    '800': {
        '800': 'English (en)',
        '810': 'Chinese (zh)- gb2312',
        '811': 'Danish (da)',
        '812': 'German (de)',
        '813': 'Icelandic (is)',
        '814': 'Japanese (jp)',
        '815': 'Norwegian (no)',
        '816': 'Spanish (es)',
        '817': 'Swedish (sv)',
        '818': 'Korean (ko)',
    }
}


"""
ONLINENIC SERVERS
-----------------

OnlineNIC offers a test server for testing purposes. Only use the live server
when you're ready to start being billed.

When using the test server use the following client_id and password:

        client_id: 135610
        password: 654123
"""

ONLINENIC_SERVERS = {
    'test': ('ote.onlinenic.com', 30009),
    'live': ('www.onlinenic.com', 30009)
}


"""
ONLINENIC ERRORS
----------------

Exceptions that represent errors that OnlineNIC's API can return.
"""


class OnlineNICError(Exception):
    """A base class for OnlineNIC API errors."""
    pass


class InvalidResponseError(OnlineNICError):
    """Raised when the response received cannot be parsed."""
    pass


class UnknownCommandError(OnlineNICError):
    """Raised when an unknown command is used."""
    pass


class CommandSyntaxError(OnlineNICError):
    """Raised when the syntax of a command is invalid."""
    pass


class RequiredParameterError(OnlineNICError):
    """Raised when a required parameter is missing."""
    pass


class ParameterRangeError(OnlineNICError):
    """Raised when a pamater value is outside the expected range."""
    pass


class ParameterSyntaxError(OnlineNICError):
    """Raised when the syntax of a parameter value is invalid."""
    pass


class BillingError(OnlineNICError):
    """Raised when there is a billing issue with OnlineNIC."""
    pass


class ObjectRenewalError(OnlineNICError):
    """Raised when an object cannot be renewed."""
    pass


class ObjectTransferError(OnlineNICError):
    """Raised when an object cannot be transferred."""
    pass


class AuthorizationError(OnlineNICError):
    """Raised when there is an authorization error."""
    pass


class InvalidAuthorizationError(AuthorizationError):
    """Raised whent he authorization is invalid."""
    pass


class ObjectPendingTransferError(OnlineNICError):
    """Raised when an object is pending a transfer."""
    pass


class ObjectExistsError(OnlineNICError):
    """Raised when the object already exists."""
    pass


class ObjectDoesNotExistError(OnlineNICError):
    """Raised when the object does not exist."""
    pass


class ObjectStatusError(OnlineNICError):
    """Raised when the object status is in conflict with the operation."""
    pass


class ObjectAssociationError(OnlineNICError):
    """Raised when the object association is in conflict with the operation."""
    pass


class ParameterValuePolicyError(OnlineNICError):
    """Raised when a parameter value is in conflict with policy."""
    pass


class ObjectIDSheildError(OnlineNICError):
    """Raised when an object cannot have ID Shield applied to it."""
    pass


class CommandFailureError(OnlineNICError):
    """Raised when a command fails, general failure."""
    pass


class SessionEndedError(OnlineNICError):
    """Raised when a session is ended by the server."""
    pass


class SessionTimeoutError(OnlineNICError):
    """Raised when session timed out."""
    pass


class NetworkError(OnlineNICError):
    """Raised when OnlineNIC is experiencing a network issue."""
    pass


class DidNotLoginError(OnlineNICError):
    """Raised when the client attempts an operation before logging in."""
    pass


class ChecksumError(OnlineNICError):
    """Raised when the checksum that is provided is invalid."""
    pass


class InternalDatabaseError(OnlineNICError):
    """Raised when OnlineNIC is experiencing a database issue."""
    pass


"""
ONLINENIC ERROR CODES
---------------------

This dict maps OnlineNIC error codes to the exceptions defined above.
"""

ONLINENIC_ERRORS = {
    '2000': UnknownCommandError,
    '2001': CommandSyntaxError,
    '2003': RequiredParameterError,
    '2004': ParameterRangeError,
    '2005': ParameterSyntaxError,
    '2104': BillingError,
    '2105': ObjectRenewalError,
    '2106': ObjectTransferError,
    '2201': AuthorizationError,
    '2202': InvalidAuthorizationError,
    '2300': ObjectPendingTransferError,
    '2302': ObjectExistsError,
    '2303': ObjectDoesNotExistError,
    '2304': ObjectStatusError,
    '2305': ObjectAssociationError,
    '2306': ParameterValuePolicyError,
    '2307': ObjectIDSheildError,
    '2400': CommandFailureError,
    '2500': SessionEndedError,
    '2501': SessionTimeoutError,
    '5000': NetworkError,
    '5500': DidNotLoginError,
    '6000': ChecksumError,
    '60001': InternalDatabaseError
}


class OnlineNIC(object):
    """OnlineNIC API wrapper class."""

    def __init__(self, client_id, password, live=False):
        self.client_id = client_id
        self.password = password
        self.set_server(live)
        self.socket = telnetlib.Telnet(self.server[0], self.server[1])
        self.login()

    def __del__(self):
        self.logout()
        self.socket.close()

    def set_server(self, live=False):
        self.server = ONLINENIC_SERVERS['live' if live is True else 'test']

    def __getattr__(self, name):
        if name in ONLINENIC_COMMANDS:
            def request_handler(**kwargs):
                return self.request(name, **kwargs)
            return request_handler
        return super(OnlineNIC, self).__getattr__(name)

    def read(self):
        msg = self.socket.read_until('</response>')
        return msg.strip()

    def write(self, xml):
        self.socket.write(xml + "\n")

    def request(self, cmd, **params):
        """Handles the API request."""
        if cmd not in ONLINENIC_COMMANDS:
            raise UnknownCommandError('Unrecognized command: {}'.format(cmd))

        # OnlineNIC sends a greeting after loggin.
        if cmd == 'login':
            greeting = self.read()

        if cmd in ['login', 'logout']:
            params['clid'] = self.client_id

        if 'domain' in params and 'domaintype' not in params:
            params['domaintype'] = self.determine_domaintype(params['domain'])

        request = [
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
            '<request>',
            '\t<category>{}</category>'.format(ONLINENIC_COMMANDS[cmd]['category']),
            '\t<action>{}</action>'.format(ONLINENIC_COMMANDS[cmd]['action']),
            '\t<params>'
        ]

        for key, value in params.iteritems():
            if isinstance(value, (list, tuple)):
                for v in value:
                    request.append('\t\t<param name="{}">{}</param>'.format(key, v))
            else:
                request.append('\t\t<param name="{}">{}</param>'.format(key, value))

        # If cltrid is provided, use it. Otherwise generate one.
        if 'cltrid' in params:
            cltrid = params.pop('cltrid')
        else:
            cltrid = self.generate_cltrid()
        request.append('\t<cltrid>{}</cltrid>'.format(cltrid))

        request.append('\t<chksum>{}</chksum>'.format(
            self.checksum(cmd, cltrid, **params)))
        request.append('</request>')
        request = '\n'.join(request)
        self.write(request)

        return self.response()

    def response(self):
        """Handle/parse the OnlineNIC API response."""
        soup = BeautifulStoneSoup(self.read())

        response = soup.find('response')
        if response is None:
            raise InvalidResponseError('No <response> container found.')

        contents = {}
        for key in ['code', 'msg', 'value', 'category', 'action']:
            value = response.find(key)
            if value is None:
                raise InvalidResponseError(
                        'No {} found in response.'.format(key)
                )
            contents[key] = value.string.strip()

        for key in ['cltrid', 'svtrid', 'checksum']:
            value = response.find(key)
            contents[key] = value.string.strip() if value else None


        if contents['code'] in ONLINENIC_ERRORS:
            raise ONLINENIC_ERRORS[contents['code']](
                    '{} [{}]'.format(contents['msg'], contents['value'])
            )

        resdata = response.find('resdata')
        if resdata is not None:
            contents['data'] = {}
            for d in resdata.contents:
                if d is not None and d.string.strip():
                    contents['data'][d.get('name')] = d.string.strip()

        return contents

    def checksum(self, cmd, cltrid, **params):
        """Generate the checksum for a command."""
        password = hashlib.md5(self.password).hexdigest()
        checksum = [self.client_id, password, cltrid,
                    ONLINENIC_COMMANDS[cmd]['checksum']['name']]
        if 'extra' in ONLINENIC_COMMANDS[cmd]['checksum']:
            for k in ONLINENIC_COMMANDS[cmd]['checksum']['extra']:
                if k in params:
                    if isinstance(params[k], (list, tuple)):
                        for p in params[k]:
                            checksum.append(p)
                    else:
                        checksum.append(params[k])
        return hashlib.md5(''.join(checksum)).hexdigest()

    def generate_cltrid(self, length=32):
        """Generate a random cltrid."""
        return hashlib.sha512(uuid.uuid4().hex).hexdigest()[0:length]

    def determine_domaintype(self, domain):
        """Return the ONLINE_DOMAIN_TYPE for a domain."""
        for ext, code in ONLINE_DOMAIN_TYPES.iteritems():
            if domain.endswith(ext):
                return code
        return None
