# syntax=docker/dockerfile:1

# A Dockerfile for stitiching together the different AlphaX packages with a defined version.

# https://github.com/michaelosthege/pythonnet-docker
FROM --platform=linux/amd64 mosthege/pythonnet:python3.10.10-mono6.12-pythonnet3.0.1

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY get_ref.sh .
COPY replace_alphax.sh .
COPY pip.conf /etc/pip.conf

RUN pip freeze > /app/requirements_0.txt

############################################################################
ARG ALPHABASE_REF="main"
RUN if [ "$ALPHABASE_REF" != "skip" ]; then \
      git clone https://github.com/MannLabs/alphabase.git; \
      cd alphabase; \
      git checkout $(../get_ref.sh $ALPHABASE_REF); \
      git status; \
    fi

RUN --mount=type=cache,target=/root/.cache/pip \
    if [ "$ALPHABASE_REF" != "skip" ]; then \
    cd alphabase && pip install "."; \
    pip freeze > /app/requirements_1_alphabase.txt; \
    fi

############################################################################
ARG ALPHATIMS_REF="main"
RUN if [ "$ALPHATIMS_REF" != "skip" ]; then \
      git clone https://github.com/MannLabs/alphatims.git; \
      cd alphatims; \
      git checkout $(../get_ref.sh $ALPHATIMS_REF); \
      git status; \
    fi

RUN --mount=type=cache,target=/root/.cache/pip \
    if [ "$ALPHATIMS_REF" != "skip" ]; then \
    cd alphatims && pip install "."; \
    pip freeze > /app/requirements_2_alphatims.txt; \
    fi

############################################################################
ARG ALPHARAW_REF="main"
RUN if [ "$ALPHARAW_REF" != "skip" ]; then \
      git clone https://github.com/MannLabs/alpharaw.git; \
      cd alpharaw; \
      git checkout $(../get_ref.sh $ALPHARAW_REF); \
      ../replace_alphax.sh; \
      git status; \
    fi

RUN --mount=type=cache,target=/root/.cache/pip \
    if [ "$ALPHARAW_REF" != "skip" ]; then \
    cd alpharaw && pip install ".[viz]"; \
    pip freeze > /app/requirements_3_alpharaw.txt; \
    fi

############################################################################
ARG ALPHAVIZ_REF="skip"
RUN if [ "$ALPHAVIZ_REF" != "skip" ]; then \
      git clone https://github.com/MannLabs/alphaviz.git; \
      cd alphaviz; \
      git checkout $(../get_ref.sh $ALPHAVIZ_REF); \
      ../replace_alphax.sh; \
      git status; \
    fi

RUN --mount=type=cache,target=/root/.cache/pip \
    if [ "$ALPHAVIZ_REF" != "skip" ]; then  \
    cd alphaviz && pip install "."; \
    pip freeze > /app/requirements_4_alphaviz.txt; \
    fi

############################################################################
ARG ALPHAMAP_REF="skip"
RUN if [ "$ALPHAMAP_REF" != "skip" ]; then \
      git clone https://github.com/MannLabs/alphamap.git; \
      cd alphamap; \
      git checkout $(../get_ref.sh $ALPHAMAP_REF); \
      ../replace_alphax.sh; \
      git status; \
    fi

RUN --mount=type=cache,target=/root/.cache/pip \
    if [ "$ALPHAMAP_REF" != "skip" ]; then \
    cd alphamap && pip install "."; \
    pip freeze > /app/requirements_4b_alphamap.txt; \
    fi

############################################################################
ARG ALPHAPEPTDEEP_REF="main"
RUN if [ "$ALPHAPEPTDEEP_REF" != "skip" ]; then \
      git clone https://github.com/MannLabs/alphapeptdeep.git; \
      cd alphapeptdeep; \
      git checkout $(../get_ref.sh $ALPHAPEPTDEEP_REF); \
      ../replace_alphax.sh; \
      git status; \
    fi

RUN --mount=type=cache,target=/root/.cache/pip \
    if [ "$ALPHAPEPTDEEP_REF" != "skip" ]; then \
    cd alphapeptdeep && pip install "."; \
    pip freeze > /app/requirements_5_alphapeptdeep.txt; \
    fi

############################################################################
ARG ALPHAPEPTTOOLS_REF="skip"
RUN if [ "$ALPHAPEPTTOOLS_REF" != "skip" ]; then \
      git clone https://github.com/MannLabs/alphapepttools.git; \
      cd alphapepttools; \
      git checkout $(../get_ref.sh $ALPHAPEPTTOOLS_REF); \
      ../replace_alphax.sh; \
      git status; \
    fi

RUN --mount=type=cache,target=/root/.cache/pip \
    if [ "$ALPHAPEPTTOOLS_REF" != "skip" ]; then \
    cd alphapepttools && pip install "."; \
    pip freeze > /app/requirements_5b_alphapepttools.txt; \
    fi

############################################################################
ARG DIRECTLFQ_REF="main"
RUN if [ "$DIRECTLFQ_REF" != "skip" ]; then \
      git clone https://github.com/MannLabs/directlfq.git; \
      cd directlfq; \
      git checkout $(../get_ref.sh $DIRECTLFQ_REF); \
      git status; \
    fi

RUN --mount=type=cache,target=/root/.cache/pip \
    if [ "$DIRECTLFQ_REF" != "skip" ]; then \
    cd directlfq && pip install "."; \
    pip freeze > /app/requirements_6_directlfq.txt; \
    fi
############################################################################
ARG ALPHADIA_REF="main"
RUN if [ "$ALPHADIA_REF" != "skip" ]; then \
      git clone https://github.com/MannLabs/alphadia.git; \
      cd alphadia; \
      git checkout $(../get_ref.sh $ALPHADIA_REF); \
      ../replace_alphax.sh; \
      git status; \
    fi

RUN --mount=type=cache,target=/root/.cache/pip \
    if [ "$ALPHADIA_REF" != "skip" ]; then \
    cd alphadia && pip install ".[stable]"; \
    pip freeze > /app/requirements_7_alphadia.txt; \
    fi

############################################################################
# additional dependencies for testing
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install pytest nbmake neptune

RUN pip freeze > /app/requirements_8_final.txt

## TODO remove this once https://github.com/MannLabs/alphabase/pull/288 is released
#RUN --mount=type=cache,target=/root/.cache/pip \
#    pip uninstall progressbar -y

# build:
# docker build -f Dockerfile  --build-arg="ALPHABASE_REF=latest" --build-arg="ALPHATIMS_REF=latest" --build-arg="ALPHARAW_REF=f8a355a" --build-arg="ALPHAPEPTDEEP_REF=latest" --build-arg="DIRECTLFQ_REF=latest" -t alphax_e2e .

# run bash:
# DATA_FOLDER=.
# docker run -v $DATA_FOLDER:/app/data/ -it alphax_e2e bash
