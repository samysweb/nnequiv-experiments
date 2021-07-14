import numpy as np
import sys

import gurobipy as grb

from properties import PROPERTY
from performance import Encoder
from analysis import get_grb_inputs, compare_outputs
from analysis import get_grb_inputs, calculate_violation

bounds=PROPERTY[sys.argv[3]]

reference=sys.argv[1]
test=sys.argv[2]

epsilon = None
if sys.argv[4]=="top":
	mode = 'one_hot_partial_top_1'
else:
	print("EPSILON")
	epsilon = float(sys.argv[4])
	mode = 'optimize_diff_chebyshev'

optimize_constraints = True
if len(sys.argv)>5 and sys.argv[5]=="noop":
	optimize_constraints = False

enc=Encoder()
enc.encode_equiv(reference, test, bounds[1], bounds[0], mode)
#print(enc.input_layer.invars)

center = (np.array(bounds[0])+np.array(bounds[1]))/2.0
radius = abs((bounds[1][0]-bounds[0][0])/2) # Assuming box which is same everywhere for now...
enc.add_input_radius(center,radius,metric='chebyshev')
#print("[PRETTY_PRINT]")
#enc.pretty_print()
if optimize_constraints:
	print("[OPTIMIZE_CONSTRAINTS]")
	enc.optimize_constraints()
model = enc.create_gurobi_model()

print("[SOLVE]")
eps=1e-12
if epsilon is None:
	# Maximize
	#model.setAttribute('ModelSense',-1)
	# Maximize
	model.setParam('BestObjStop',eps)
else:
	print(f"Setting BestObjStop to {epsilon+eps}")
	# Maximize
	#model.setAttribute('ModelSense',-1)
	model.setParam('BestObjStop',epsilon+eps)
model.optimize()
print("[RESULTS]")
ins = get_grb_inputs(model, len(enc.input_layer.invars))
print(ins)
#print(calculate_violation(ins, reference, test, top_k=1))
ins = get_grb_inputs(model, len(enc.input_layer.invars))
print(ins)
print(compare_outputs(reference, test,ins, sort=True))

