# evaluator.py
import random
from protocol import add_mod, mul_mod, MOD, send, recv

class Evaluator:
    def __init__(self, pid):
        self.pid = pid   # 1 or 2
        self.masked_vals = {}  # wire_id -> masked share

    def input_share(self, x, lam):
        # Client input x, mask λ from P0
        m = add_mod(x, lam)     # masked value
        # Split m into additive shares for P1 and P2
        share1 = random.randint(0, MOD-1)
        share2 = add_mod(m, -share1)
        if self.pid == 1:
            return share1
        else:
            return share2

    def add(self, m1, m2):
        return add_mod(m1, m2)

    def mul(self, x_share, y_share, triple):
        """
        Semi-honest ASTRA Π^s_Mul:
        - P0 gave triple (d,e,f) offline
        - Online: P1,P2 locally compute deltas, exchange 2 values
        """
        d, e, f = triple
        # Each evaluator has masked shares: (x+λx), (y+λy)
        # Protocol simplified here: just multiply shares
        partial = mul_mod(x_share, y_share)
        # Exchange partials
        other_partial = recv()
        send("other", partial)
        full = add_mod(partial, other_partial)
        return full
