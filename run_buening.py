import numpy as np
import sys

from properties import PROPERTY
from performance import Encoder
from analysis import get_grb_inputs, compare_outputs
from analysis import get_grb_inputs, calculate_violation

bounds=PROPERTY[sys.argv[3]]

reference=sys.argv[1]
test=sys.argv[2]

assert sys.argv[4]=="top"
mode = 'one_hot_partial_top_1'

enc=Encoder()
enc.encode_equiv(reference, test, bounds[1], bounds[0], mode)

center = (np.array(bounds[0])+np.array(bounds[1]))/2.0
radius = abs((bounds[1][0]-bounds[0][0])/2) # Assuming box which is same everywhere for now...
enc.add_input_radius(center,radius,metric='chebyshev')
print("[PRETTY_PRINT]")
enc.pretty_print()
print("[OPTIMIZE_CONSTRAINTS]")
enc.optimize_constraints()
model = enc.create_gurobi_model()
print("[SOLVE]")
model.optimize()
print("[RESULTS]")
ins = get_grb_inputs(model, 64)
print(ins)
print(calculate_violation(ins, reference, test, top_k=1))
ins = get_grb_inputs(model, 10)
print(ins)
print(compare_outputs(reference, test,ins))