FROM kennethreitz/pipenv as build
ADD . /app
WORKDIR /app
RUN pipenv install --dev \
 && pipenv lock -r > requirements.txt \
 && pipenv run python setup.py bdist_wheel

FROM ubuntu:bionic
COPY --from=build /app/dist/*.whl .
ARG DEBIAN_FRONTEND=noninteractive
RUN set -xe \
 && apt-get update -q \
 && apt-get install -y -q \
        python3-wheel \
        python3-pip \
 && python3 -m pip install *.whl \
 && apt-get remove -y python3-pip python3-wheel \
 && apt-get autoremove -y \
 && apt-get clean -y \
 && rm -f *.whl \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /app \
 && useradd warmane --no-create-home --user-group
USER warmane
CMD ["pipenv run python3 warmane.py"]
