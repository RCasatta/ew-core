from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import config

conf = config.read_default_config();

# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%( conf['rpcuser'] , conf['rpcpassword'] ) )
best_block_hash = rpc_connection.getbestblockhash()
print(rpc_connection.getblock(best_block_hash))

# batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
last = 392147
blockof = 100
iteration = last/blockof
for iternow in range(iteration) :
  commands = [ [ "getblockhash", iternow * blockof + height] for height in range(100) ]
  block_hashes = rpc_connection.batch_(commands)
  blocks = rpc_connection.batch_([ [ "getblock", h ] for h in block_hashes ])
  block_times = [ block["time"] for block in blocks ]
  print( str(iternow) + " of " + str(iteration) + " time:" + str(block_times[0]) )

