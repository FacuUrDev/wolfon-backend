FROM public.ecr.aws/lambda/python:3.12
LABEL authors="wolfon"
EXPOSE 80
COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt
RUN pip install fastapi[all]
# RUN pip install mangum

COPY app.py ${LAMBDA_TASK_ROOT}
COPY src ${LAMBDA_TASK_ROOT}/src/

ENTRYPOINT ["fastapi", "run", "app.py", "--proxy-headers", "--port", "80"]

#docker build -f Dockerfile -t wolfon-bakcend . && docker run -p 80:80 -v ./src:/var/task/src --env DATABASE_NAME=wolfon_test --env-file .env --name wolfon-backend wolfon-bakcend