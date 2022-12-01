FROM abelsiqueira/python-and-julia:py3.10-jl1.7


COPY . /app

WORKDIR /app

RUN --mount=type=cache,target=/var/julia julia script/setup/setup.jl  \
    && pip install -r requirements.txt  \
    && python script/setup/setup.py && rm -rf ./script

EXPOSE 5000
CMD gunicorn wsgi:app