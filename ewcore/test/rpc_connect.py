import bitcoinrpc


user = 'xenoky'
password = 'asf4tw5yhub3r9gjdrrmprg99627o98Gnfjgtyfgi74dE'
port = '8332'
host='192.168.1.233'

access = bitcoinrpc.connect_to_remote(user, password, host, port)

print(access.getinfo())