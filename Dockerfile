FROM continuumio/miniconda3
LABEL org.bokeh.demo.maintainer="Bokeh <info@bokeh.org>"

ENV BK_VERSION=3.4.3
ENV PY_VERSION=3.10
ENV NP_VERSION=2.1.0
ENV BOKEH_RESOURCES=cdn
ENV BOKEH_LOG_LEVEL=debug

RUN apt-get install git bash

RUN conda install -n base python=${PY_VERSION} conda-libmamba-solver
RUN conda config --set solver libmamba
#RUN conda install -c bokeh --yes --quiet python=${PY_VERSION} pyyaml jinja2 bokeh=${BK_VERSION} numpy "nodejs>=14" pandas scipy
RUN conda install -c bokeh -c conda-forge --yes --quiet python=${PY_VERSION} pyyaml jinja2 numpy=${NP_VERSION} "nodejs>=14" pandas scipy git pip
RUN pip install git+https://github.com/mkellom/bokeh.git@0a6241cb7a783642d61207a46a96b3c949ff8fe1
RUN pip install matplotlib
RUN conda clean -ay

RUN python -c 'import bokeh;'

EXPOSE 5006

RUN mkdir -p /myapp && mkdir -p /myapp/data && mkdir -p /myapp/templates && mkdir -p /myapp/images && mkdir -p /myapp/static
VOLUME /myapp/data

COPY myapp/__init__.py myapp/__init__.py
COPY myapp/app_hooks.py myapp/app_hooks.py
COPY myapp/data_load.py myapp/data_load.py
COPY myapp/main.py myapp/main.py
COPY myapp/download.js myapp/download.js
COPY myapp/index.html myapp/templates/index.html

RUN chmod -R 555 myapp/templates

CMD bokeh serve --show myapp --session-token-expiration=3600 --allow-websocket-origin=microbiomes.microbiomes.development.svc.spin.nersc.org --allow-websocket-origin=microbiomes-dev.jgi.doe.gov
#CMD bokeh serve --show myapp --session-token-expiration=3600 --allow-websocket-origin=microbiomes.microbiomes.production.svc.spin.nersc.org --allow-websocket-origin=microbiomes.jgi.doe.gov