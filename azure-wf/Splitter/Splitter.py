import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import PauliList
from circuit_knitting.cutting import (
    OptimizationParameters,
    DeviceConstraints,
    find_cuts,
    cut_wires,
    expand_observables,
    partition_problem,
    generate_cutting_experiments
)
from .qutils import marshaller, serializers
from .python.src.utils.classes.commons.serwo_objects import SerWOObject
import logging
# logger = logging.getLogger(__name__)
# logging.basicConfig(filename='./output/execution.log', level=logging.INFO)
# logger.info('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Splitter Started::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')

def create_observables(qc: QuantumCircuit) -> list:
    observables = []
    for i in range(qc.num_qubits):
        obs = 'I'*(i)+'Z'+'I'*(qc.num_qubits-i-1)
        observables.append(obs)
    return observables

def user_function(xfaas_object) -> SerWOObject:
    try:
        input = xfaas_object.get_body()
            # The cut points are assumed to be marked already
        circuit = serializers.circuit_deserializer(input['data']['circuit'])
        observables = PauliList(input['data']['observables'])

        # Specify settings for the cut-finding optimizer
        optimization_settings = OptimizationParameters(seed=111)

        # Specify the size of the QPUs available
        device_constraints = DeviceConstraints(qubits_per_subcircuit=10)

        cut_circuit, metadata = find_cuts(circuit, optimization_settings, device_constraints)

        qc_w_ancilla = cut_wires(cut_circuit)
        observables_expanded = expand_observables(observables, circuit, qc_w_ancilla)
        partitioned_problem = partition_problem(circuit=qc_w_ancilla, observables=observables_expanded)
        subobservables = partitioned_problem.subobservables
        subexperiments, coefficients = generate_cutting_experiments(
                                        circuits=partitioned_problem.subcircuits,
                                        observables=subobservables,
                                        num_samples=np.inf
                                        )
        logging.info(subexperiments.keys())
        data = {}

        List= []
        keys = subexperiments.keys()
        print(keys)

        for key in keys:
            # print(subexperiments[key])
            subex = []
            for item in subexperiments[key]:
                subex.append(serializers.circuit_serializer(item))
            print("subex", subex)
            print("devices", input["devices"])
            List.append({
                'subexperiments': subex,
                'devices': input['devices'][key]
            })


        data['subexperiments'] = marshaller.jsonifyCuts(subexperiments=subexperiments)
        data['subobservables'] = marshaller.sub_observables_to_dict(subobservables)
        data['coefficients'] = marshaller.coefficients_to_list(coeffcients=coefficients)

        returnbody = {
                "data": data, \
                "credentials": input['credentials'], \
                "devices": input['devices'], \
                "List": List
            }
        return SerWOObject(body=returnbody)
    except Exception as e:
        print(e)
        logging.info(e)
        logging.info("Error in Invoke function")
        raise Exception("[SerWOLite-Error]::Error at user function",e)


# if __name__ == "__main__":
#     f=open("./output/input.json")
#     body=json.load(f)
#     # body=json.loads(body)
#     z=user_function(SerWOObject(body=body))
#     body=z.get_body()
#     # obj=json.dumps(body)
#     with open("./output/splitter_out.json", "w") as f:
#         json.dump(body, f)
#     logging.info("Output object:"+str(body))