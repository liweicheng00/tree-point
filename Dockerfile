FROM python:3.8
RUN useradd user


WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

USER user
CMD ["bash", "run.sh"]