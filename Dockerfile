FROM public.ecr.aws/lambda/python:3.9

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

COPY *.py ${LAMBDA_TASK_ROOT}

CMD ["lambda_function.handler"]