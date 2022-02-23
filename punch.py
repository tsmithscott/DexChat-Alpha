import miniupnpc

upnp = miniupnpc.UPnP()

upnp.discoverdelay = 10
upnp.discover()

upnp.selectigd()

port = 25000

# addportmapping(external-port, protocol, internal-host, internal-port, description, remote-host)
upnp.addportmapping(port, 'UDP', upnp.lanaddr, port, 'testing', '')
