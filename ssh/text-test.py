import paramiko
import socket
from time import sleep

ROUTER_IP='X.X.X.X'
USERNAME='username'
PASSWORD='password'


TERMINATOR = ']]>]]>'
TERMINATOR2 = b']]>]]>'

TERMINATOR = ']]>]]>'
TERMINATOR2 = b']]>]]>'

HELLO = """
<?xml version="1.0" encoding=\"UTF-8\"?>
<hello><capabilities>
     <capability>urn:ietf:params:netconf:base:1.0</capability>
     <capability>urn:ietf:params:netconf:capability:writeable-running:1.0</capability>
     <capability>urn:ietf:params:netconf:capability:startup:1.0</capability>
     <capability>urn:ietf:params:netconf:capability:url:1.0</capability>
     <capability>urn:cisco:params:netconf:capability:pi-data-model:1.0</capability>
     <capability>urn:cisco:params:netconf:capability:notification:1.0</capability>
   </capabilities>
</hello>"""


#GET RUNNING CONFIG
RUNNING = """
<?xml version="1.0" encoding=\"UTF-8\"?>
<rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:cpi="http://www.cisco.com/cpi_10/schema">
 <get-config>
  <source><running/></source>
  <filter type="cli"><config-format-xml></config-format-xml></filter>
 </get-config>
</rpc>"""

INVENTORY = """
<?xml version="1.0" encoding=\"UTF-8\"?>
<rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:cpi="http://www.cisco.com/cpi_10/schema">
 <get>
  <filter>
   <oper-data-format-xml>
    <show>inventory</show>
   </oper-data-format-xml>
  </filter>
 </get>
</rpc>"""

ARP = """
<?xml version="1.0" encoding=\"UTF-8\"?>
<rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:cpi="http://www.cisco.com/cpi_10/schema">
 <get>
  <filter>
   <oper-data-format-xml>
    <show>arp</show>
   </oper-data-format-xml>
  </filter>
 </get>
</rpc>"""

MAC_TABLE = """
<?xml version="1.0" encoding=\"UTF-8\"?>
<rpc message-id="102" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:cpi="http://www.cisco.com/cpi_10/schema">
 <get>
  <filter>
   <oper-data-format-xml>
    <show>mac address-table</show>
   </oper-data-format-xml>
  </filter>
 </get>
</rpc>"""

INT_STATUS = """
<?xml version="1.0" encoding=\"UTF-8\"?>
<rpc message-id="102" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:cpi="http://www.cisco.com/cpi_10/schema">
 <get>
  <filter>
   <oper-data-format-xml>
    <show>interfaces status</show>
   </oper-data-format-xml>
  </filter>
 </get>
</rpc>"""

CLOSE = """
<?xml version="1.0" encoding=\"UTF-8\"?>
<rpc message-id="106" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
<rpc>
  <close-session/>
</rpc>"""

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.connect((ROUTER_IP, 22))

trans = paramiko.Transport(socket)
trans.connect(username=USERNAME, password=PASSWORD)

#PROVIDES TRUE OR FALSE
trans.is_active()
#CREATE CHANNEL FOR DATA COMM
chan = trans.open_session()
name = chan.set_name('netconf')

#Invoke NETCONF
chan.invoke_subsystem('netconf')

def read(chan, responses=1):
    """Read responses."""
    while responses:
        sleep(1)
        response = chan.recv(20000)
        responses -= response.count(TERMINATOR2)
        return(response)

#SEND COMMAND
chan.send(HELLO + TERMINATOR)
#Sending a Second Hello
chan.send(HELLO + TERMINATOR)

chan.sendall(MAC_TABLE + TERMINATOR)

chan.send(CLOSE + TERMINATOR)

chan.close()
trans.close()
socket.close()
