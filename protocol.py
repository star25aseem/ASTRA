import random

MOD = 2**64   # Ring Z_(2^64)

def add_mod(x, y): 
    return (x + y) % MOD

def mul_mod(x, y): 
    return (x * y) % MOD

# Message send/recv stubs (replace with sockets later)
def send(to, msg): 
    pass

def recv(): 
    pass
