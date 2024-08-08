from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from .qutils import marshaller,serializers
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from .python.src.utils.classes.commons.serwo_objects import SerWOObject
import logging
# logger = logging.getLogger(__name__)
# logging.basicConfig(filename='./output/execution.log', level=logging.INFO)
# logger.info('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Transpiler Started::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')

def user_function(xfaas_object) -> SerWOObject:
    try:
        input = xfaas_object.get_body()
        # print(input)
        qtoken = input['devices']['qtoken']
        service = QiskitRuntimeService('ibm_quantum', token=qtoken)
        device = input['devices']
        # print("devices",devices)
        # num_devices = len(devices)
        # subexperiments = marshaller.objectifyCuts(input['subexperiments'])
        subexperiments= [serializers.circuit_deserializer(item) for item in input['subexperiments']]
        batched_subexperiments = subexperiments
        # batched_subexperiments = [list(b) for b in divide(num_devices, subexperiments.keys())]
        subexperiments_transpiled = {}
        backend = None
        # for i in range(num_devices):
            # print(devices)
            # device = devices[i]
        skip_transpilation = False
        if device['device'] == 'aer':
            if 'backend' in device:
                real_backend = service.backend(device['backend'])
                backend = AerSimulator.from_backend(real_backend)
            elif 'noise-model' in device:
                noise_model = NoiseModel.from_dict(device['noise-model'])
                backend = AerSimulator(noise_model=noise_model)
            elif 'backend' not in device:
                skip_transpilation = True
        elif device['device'] == 'ibmq_qasm_simulator':
            skip_transpilation = True
        else:
            backend = service.backend(device['device'])
        if not skip_transpilation:
            pm = generate_preset_pass_manager(2, backend)
            l = []
            for subcircuit in subexperiments:
                l.append(pm.run(subcircuit))
            subexperiments_transpiled = l
        if len(subexperiments_transpiled) == 0:
            subexperiments_transpiled = subexperiments
        # data = input['data']
        # input['subexperiments'] = marshaller.jsonifyCuts(subexperiments=subexperiments_transpiled)
        input['subexperiments'] = [serializers.circuit_serializer(item) for item in subexperiments_transpiled]
        
        return SerWOObject(body=input)
    except Exception as e:
        print(e)
        logging.info(e)
        logging.info("Error in Invoke function")
        raise Exception("[SerWOLite-Error]::Error at user function",e)

# if __name__ == "__main__":
#     f=open("./output/splitter_out.json")
#     body=json.load(f)
#     # body=json.loads(body)
#     js=[]
#     for obj in body["List"]:
#         print(obj)
#         z=user_function(SerWOObject(body=obj))
#         body=z.get_body()
#         js.append(body)
#         # obj=json.dumps(body)
#     with open("./output/transpile_out.json", "w") as f:
#         json.dump(js, f)
#     logging.info("Output object:"+str(body))