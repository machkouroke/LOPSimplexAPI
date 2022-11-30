FROM abelsiqueira/python-and-julia:py3.10-jl1.7

EXPOSE 5000/tcp
COPY . /app

WORKDIR /app

RUN --mount=type=cache,target=/var/julia julia script/setup/setup.jl && pip install -r requirements.txt && python script/setup/setup.py && rm -rf /app/script


CMD gunicorn wsgi:app