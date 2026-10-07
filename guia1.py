from spinqit import Circuit, X, H, Z, draw
from spinqit import get_compiler, get_basic_simulator, BasicSimulatorConfig     

circ=Circuit()
q = circ.allocateQubits(1)
circ << (H,q[0])
circ << (Z,q[0])
circ << (H,q[0])

compilador = get_compiler("native") #

ir = compilador.compile(circ, 0)
draw(ir, "Circuito_HZH.png") 

engine = get_basic_simulator()
config = BasicSimulatorConfig()

config.configure_shots(1000)
config.configure_measure_qubits([q[0]])

result=engine.execute(ir, config)

print(result.counts)
print(result.probabilities)
print(result.states)