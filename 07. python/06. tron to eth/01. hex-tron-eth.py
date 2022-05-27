from tronapi import Tron
from tronapi import HttpProvider

full_node = HttpProvider('https://api.trongrid.io')
solidity_node = HttpProvider('https://api.trongrid.io')
event_server = HttpProvider('https://api.trongrid.io')
tron = Tron(full_node=full_node,
            solidity_node=solidity_node,
            event_server=event_server)

print("-----------------------------测试-------------------------------")
result1 = tron.address.to_hex('TT67rPNwgmpeimvHUMVzFfKsjL9GZ1wGw8')
print(result1.replace("41","0x").lower())
# result: 41BBC8C05F1B09839E72DB044A6AA57E2A5D414A10

print("-----------------------------address-------------------------------")
result1 = tron.address.to_hex('TT67rPNwgmpeimvHUMVzFfKsjL9GZ1wGw8')
print(result1.replace("41","0x").lower())



'''
tron.address.from_hex('41BBC8C05F1B09839E72DB044A6AA57E2A5D414A10')
# result: TT67rPNwgmpeimvHUMVzFfKsjL9GZ1wGw8
'''
