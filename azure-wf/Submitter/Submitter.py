from qiskit_ibm_runtime import QiskitRuntimeService, Sampler, Session, Options
from .qutils import serializers
from .python.src.utils.classes.commons.serwo_objects import SerWOObject
import logging
# logger = logging.getLogger(__name__)
# logging.basicConfig(filename='./output/execution.log', level=logging.INFO)
# logger.info('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Submitter Started::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    

def user_function(xfaas_object) -> SerWOObject:
    try:
        input = xfaas_object.get_body()
        # subexperiments = marshaller.objectifyCuts(input['subexperiments'])
        subexperiments = [serializers.circuit_deserializer(item) for item in input['subexperiments']]
        qtoken = input['devices']['qtoken']
        service = QiskitRuntimeService(channel="ibm_quantum", token=qtoken)
        devices = input['devices']
        num_devices = 1
        # batched_subexperiments = [list(b) for b in divide(num_devices, subexperiments.keys())]
        batched_subexperiments = subexperiments
        options = Options()
        options.execution.shots = 1000 # {{ shots }}
        options.transpilation.skip_transpilation = True
        options.resilience_level = 1 # {{ resilience_level }} # set to 1 if you need measurement error mitigation
        jobs = []
        
        session = Session(service=service, backend=devices['device'])
        sampler = Sampler(session=session, options=options)
        # for key in batched_subexperiments:
        job = sampler.run(subexperiments)
        jobs.append({'id': job.job_id(),  'device': devices['device']})

        data = {}
        data["job"] = jobs
        # data["data"] = input["data"]
        # data["credentials"] = input["credentials"]    
        data["devices"]=devices
        
        returnbody=data
        return SerWOObject(body=returnbody)
    except Exception as e:
        print(e)
        logging.info(e)
        logging.info("Error in Submitter function")
        raise Exception("[SerWOLite-Error]::Error at user function",e)


# if __name__ == "__main__":
#     f=open("./output/transpile_out.json")
#     body=json.load(f)
#     output = []
#     # body=json.loads(body)
#     for obj in body:
#         z=user_function(SerWOObject(body=obj))
#         body=z.get_body()
#         output.append(body)
#     # obj=json.dumps(body,default=str)
#     with open("./output/submit_out.json", "w") as f:
#         json.dump(output, f)
#     # logging.info("Output object:"+str(body))