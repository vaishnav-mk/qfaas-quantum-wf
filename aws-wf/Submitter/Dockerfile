# FROM ubuntu:22.04
# RUN apt-get update && apt-get install -y python3
# FROM seshapad/aws-lambda-qiskit:base
# FROM seshapad/qxfaas-qiskit-1.0:base
FROM public.ecr.aws/lambda/python:3.8
# RUN pip install --upgrade pip
COPY . .
ADD python ./python
RUN pip install -r requirements.txt
# Command can be overwritten by providing a different command in the template directly.
# ENTRYPOINT ["python","./Submitter.py"]
CMD ["standalone_app_runner.lambda_handler"] 
# CMD [ "Submitter.exec" ]
