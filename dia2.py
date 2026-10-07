from spinqit import Circuit, X, H, CX, Z, draw 
from spinqit import get_compiler, BasicSimulatorBackend, BasicSimulatorConfig 
from spinqit import NMRConfig, get_nmr  

circ=Circuit()
q = circ.allocateQubits(2)
#circ << (H,q[1])
#circ << (X,q[1])

#circ << (CX,(q[0],q[1]))
circ << (H,q[0])
circ << (CX,(q[0],q[1]))
circ << (Z,q[0])

compilador = get_compiler("native")
r=compilador.compile(circ, 0)
draw(r, "reto_bell.png")

engine=BasicSimulatorBackend()
config=BasicSimulatorConfig()

result = engine.execute(r, config)
print(result.counts)
print(result.states)



identificador="UlisesElRapa"
nombre_tarea = "Entrelazamiento_"+identificador

config=NMRConfig()
config.configure_ip("")
config.configure_port()
config.configure_account("", "")
config.configure_task(nombre_tarea,"Prueba estado bell fisico")
config.configure_shots(1000)
config.configure_measure_qubits(q)
engine=get_nmr()
print("enviando tarea")

resultado = engine.execute(r,config) 
print(resultado.counts)
print(resultado.probabilities)