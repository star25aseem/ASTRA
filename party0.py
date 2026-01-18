# party0.py
import random
from protocol import add_mod, mul_mod, MOD, send, recv

class Party0:
    def __init__(self):
        self.lambdas = {}    # wire_id -> lambda mask
        self.triples = {}    # gate_id -> (d,e,f) triple

    def gen_mask(self, wire_id):
        lam = random.randint(0, MOD-1)
        self.lambdas[wire_id] = lam
        return lam

    def gen_mult_triple(self, gate_id):
        d = random.randint(0, MOD-1)
        e = random.randint(0, MOD-1)
        f = mul_mod(d, e)
        self.triples[gate_id] = (d, e, f)
        return (d, e, f)

    def reveal(self, masked_val, lam):
        # Final step: remove mask and give result to client
        return add_mod(masked_val, -lam)
