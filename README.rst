=========
OnlineNIC
=========

A simple wrapper for the `OnlineNIC`<http://www.onlinenic.com> API.

Usage
-----

Registering a domain name::

    import onlinenic

    on = onlinenic.OnlineNIC('135610', '654123')

    result = on.create_contact(domaintype='0',
                               name='John Doe',
                               org='Widgets 'R Us, Inc.',
                               street='123 Main St',
                               city='Plainsville',
                               province='PA',
                               postalcode='12345',
                               country='US',
                               voice='+1.1234567890',
                               fax='+1.1234567890',
                               email='johndoe@whocares.com',
                               password='abc123')

    contactid = result['data']['contactid']

    result = on.create_domain(domain='somedomain.com',
                              period='1',
                              registrant=contactid,
                              admin=contactid,
                              tech=contactid,
                              billing=contactid,
                              password='abc123',
                              dns=['ns1.dnsprovider.com',
                                   'ns2.dnsprovider.com'])
