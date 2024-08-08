# OM NAMO GANAPATHAYEN NAMAHA
from circuit_knitting.cutting import reconstruct_expectation_values
from qutils import marshaller, program_serializers
import json
from python.src.utils.classes.commons.serwo_objects import SerWOObject
import logging
# logger = logging.getLogger(__name__)
# logging.basicConfig(filename='./output/execution.log', level=logging.INFO)
# logger.info('Started')

def user_function(xfaas_object) -> SerWOObject:
    try:
        input = xfaas_object.get_body()
        subobservables = marshaller.dict_to_sub_observables(input['data']['subobservables'])
        coefficients = json.loads(input['data']['coefficients'])
        corrected_coefficients = []
        for c in coefficients:
            corrected_coefficients.append(tuple(c))

        res = {}
        for i, obj in enumerate(input["ListResult"]):
            res[str(i)] = obj['body']['results']


        results = marshaller.decode_results(res)
        reconstructed_expvals = reconstruct_expectation_values(
            results,
            corrected_coefficients,
            subobservables,
        )
        print(reconstructed_expvals)

        returnbody = {
                "data": {'result': reconstructed_expvals}, \
                "devices": input['devices']
            }
        return SerWOObject(body=returnbody)
    except Exception as e:
        print(e)
        logging.info(e)
        logging.info("Error in Invoke function")
        raise Exception("[SerWOLite-Error]::Error at user function",e)


# if __name__ == "__main__":
#     f=open("./output/poller_out.json")
#     body=json.load(f)
#     # body=json.loads(body)
#     z=user_function(SerWOObject(body=body))
#     body=z.get_body()
#     # obj=json.dumps(body,default=str)
#     with open("./output/reconstructor_out.json", "w") as f:
#         json.dump(body, f)
#     logging.info("Output object:"+str(body))