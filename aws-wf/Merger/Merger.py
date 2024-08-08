from python.src.utils.classes.commons.serwo_objects import SerWOObject
import logging
# logger = logging.getLogger(__name__)
# logging.basicConfig(filename='./output/execution.log', level=logging.INFO)
# logger.info('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::Poller Started::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')

def user_function(xfaas_object) -> SerWOObject:
    try:
        body = xfaas_object.get_body()

        print(body)
        logging.info(str(body))
               
        return xfaas_object
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