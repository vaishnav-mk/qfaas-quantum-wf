# OM NAMO GANAPATHAYEN NAMAHA

import json
from qiskit_ibm_runtime import QiskitRuntimeService
from .qsserializers import program_serializers, serializers
from .python.src.utils.classes.commons.serwo_objects import SerWOObject
import logging
from qiskit.providers.job import JobStatus
# logger = logging.getLogger(__name__)
# logging.basicConfig(filename='./output/execution.log', level=logging.INFO)
# logger.info('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Poller Started::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
from datetime import datetime
import time
def est_exec_curr_time(job):
    job_metrics=job.metrics()
    created_time=datetime.strptime(job_metrics['timestamps']['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
    est_com_time=datetime.strptime(job_metrics['estimated_completion_time'], '%Y-%m-%dT%H:%M:%S.%fZ') 
    print(job.metrics())
    diff=est_com_time-created_time
    return diff


def user_function(xfaas_object) -> SerWOObject:
    try:
        input = xfaas_object.get_body()
        for key in range(0,len(input["ListResults"])):
                obj = input["ListResults"][key]
                qtoken = obj['devices']['qtoken']
                service = QiskitRuntimeService(channel="ibm_quantum", token=qtoken)
                any_failed_job = False
                
                # logging.info("We are before job load:"+str(job['id']))
                completedJob = service.job(job_id=obj["job"][0]['id'])

                logging.info("We are after job")
                
                if completedJob.status() != JobStatus.DONE:
                    completedJob = ''
                    any_failed_job = True
                if completedJob != '':
                    results = json.dumps(completedJob.result(), \
                                                    cls=program_serializers.QiskitObjectsEncoder)
                    obj["results"] = results
        
        if any_failed_job:
            # event['status'] = "AWAITED"
            input["Poll"]=True
            return SerWOObject(body=input)

        # data = {}
        # data['subobservables'] = input['data']['subobservables']
        # data['results'] = results
        # data['coefficients'] = input['data']['coefficients']
        
        input["Poll"]=False
        
        
        return SerWOObject(body=input)
    except Exception as e:
        print(e)
        logging.info(e)
        logging.info("Error in Poller function")
        raise Exception("[SerWOLite-Error]::Error at user function",e)

# if __name__ == "__main__":
#     f=open("./output/submit_out.json")
#     body=json.load(f)
#     # body=json.loads(body)
#     z=user_function(SerWOObject(body=body))
#     body=z.get_body()
#     # obj=json.dumps(body,default=str)
#     with open("./output/poller_out.json", "w") as f:
#         json.dump(body, f)
#     logging.info("Output object:"+str(body))