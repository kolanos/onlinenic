import onlinenic


class MockOnlineNIC(onlinenic.OnlineNIC):
    read_data = None
    write_data = None

    def __init__(self, client_id, password, live=False):
        self.client_id = client_id
        self.password = password
        self.set_server(live)

    def prime_read(self, expected):
        self.read_data = expected

    def read(self):
        return self.read_data

    def write(self, xml):
        self.write_data = xml

    def __del__(self):
        pass


def test_init():
    on = MockOnlineNIC('135610', '654123')

    assert on.client_id == '135610'
    assert on.password == '654123'
    assert on.server[0] == 'ote.onlinenic.com'
    assert on.server[1] == 30009

    on = MockOnlineNIC('135610', '654123', True)

    assert on.server[0] == 'www.onlinenic.com'
    assert on.server[1] == 30009


def test_login():
    on = MockOnlineNIC('135610', '654123')
    on.prime_read("""<?xml version="1.0"?>
<response>
	<category>client</category>
	<action>Login</action>
	<code>1000</code>
	<msg>Command completed successfully</msg>
	<value>L115:no value</value>
	<resData>
	</resData>
	<cltrid>cf65f78fbf2970eee91b3673f88f1de3</cltrid>
	<svtrid>cf65f78fbf2970eee91b3673f88f1de3-API-SRV</svtrid>
	<chksum>10c73f315a9968862da695e8bb85ff64</chksum>
</response>""")

    result = on.login()

    assert result['category'] == 'client'
    assert result['action'] == 'Login'
    assert result['code'] == '1000'
    assert result['msg'] == 'Command completed successfully'
    assert result['value'] == 'L115:no value'
    assert result['data'] == {}
    assert result['cltrid'] == 'cf65f78fbf2970eee91b3673f88f1de3'
    assert result['svtrid'] == 'cf65f78fbf2970eee91b3673f88f1de3-API-SRV'
    assert result['chksum'] == '10c73f315a9968862da695e8bb85ff64'
    assert on.write_data == """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<request>
	<category>client</category>
	<action>Login</action>
	<params>
		<param name="clid">135610</param>
	<cltrid>cf65f78fbf2970eee91b3673f88f1de3</cltrid>
	<chksum>59b66730de0ab32189a93f2b53a3e5b8</chksum>
</request>"""
