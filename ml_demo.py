# ml_demo.py
import random
from protocol import add_mod, mul_mod, MOD
from party0 import Party0
from party1 import Evaluator

def secure_dot_product(x_vec, w_vec):
    """
    Simulate 3PC locally without real sockets
    """
    P0 = Party0()
    P1 = Evaluator(pid=1)
    P2 = Evaluator(pid=2)

    # Input sharing
    shares1, shares2, lambdas = [], [], []
    for i, x in enumerate(x_vec):
        lam = P0.gen_mask(f"x{i}")
        m = add_mod(x, lam)
        s1 = random.randint(0, MOD-1)
        s2 = add_mod(m, -s1)
        shares1.append(s1)
        shares2.append(s2)
        lambdas.append(lam)

    # Each weight w is public -> no masking needed
    # Compute secure dot product = sum(x*w)
    result_share1, result_share2 = 0, 0
    for s1, s2, lam, w in zip(shares1, shares2, lambdas, w_vec):
        # Multiply input with weight
        # For simplicity, multiply shares separately
        result_share1 = add_mod(result_share1, mul_mod(s1, w))
        result_share2 = add_mod(result_share2, mul_mod(s2, w))
        P0.lambdas["res"] = add_mod(P0.lambdas.get("res",0), mul_mod(lam, w))

    # Reconstruction
    masked_val = add_mod(result_share1, result_share2)
    output = P0.reveal(masked_val, P0.lambdas["res"])
    return output

# Example run
x = [1,2,3]
w = [4,5,6]
print("Plaintext dot product:", sum([xi*wi for xi,wi in zip(x,w)]))
print("Secure dot product   :", secure_dot_product(x,w))
