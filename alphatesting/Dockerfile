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
ARG ALPHABASE_REF="latest"
RUN git clone https://github.com/MannLabs/alphabase.git \
    && cd alphabase \
    && git checkout $(../get_ref.sh $ALPHABASE_REF) \
    && git status

RUN --mount=type=cache,target=/root/.cache/pip \
    cd alphabase && pip install "."

RUN pip freeze > /app/requirements_1_alphabase.txt

############################################################################
ARG ALPHATIMS_REF="latest"
RUN git clone https://github.com/MannLabs/alphatims.git \
    && cd alphatims \
    && git checkout $(../get_ref.sh $ALPHATIMS_REF) \
    && git status

RUN --mount=type=cache,target=/root/.cache/pip \
    cd alphatims && pip install "."

RUN pip freeze > /app/requirements_2_alphatims.txt

############################################################################
ARG ALPHARAW_REF="latest"
RUN git clone https://github.com/MannLabs/alpharaw.git \
    && cd alpharaw \
    && git checkout $(../get_ref.sh $ALPHARAW_REF) \
    && ../replace_alphax.sh \
    && git status

RUN --mount=type=cache,target=/root/.cache/pip \
    cd alpharaw && pip install "."

RUN pip freeze > /app/requirements_3_alpharaw.txt

############################################################################
ARG ALPHAVIZ_REF="skip"
RUN if [ "$ALPHAVIZ_REF" != "skip" ]; then \
      && git clone https://github.com/MannLabs/alphaviz.git \
      && cd alphaviz \
      && git checkout $(../get_ref.sh $ALPHAVIZ_REF) \
      && ../replace_alphax.sh \
      && git status \
    && fi

RUN --mount=type=cache,target=/root/.cache/pip \
    && if [ "$ALPHAVIZ_REF" != "skip" ]; then \
      && cd alphaviz && pip install "." \
      && pip freeze > /app/requirements_4_alphaviz.txt \
    && fi

############################################################################
ARG ALPHAMAP_REF="skip"
RUN if [ "$ALPHAMAP_REF" != "skip" ]; then \
      && git clone https://github.com/MannLabs/alphamap.git \
      && cd alphamap \
      && git checkout $(../get_ref.sh $ALPHAVIZ_REF) \
      && ../replace_alphax.sh \
      && git status \
    && fi

RUN --mount=type=cache,target=/root/.cache/pip \
    if [ "$ALPHAMAP_REF" != "skip" ]; then \
      && cd alphamap && pip install "." \
      && pip freeze > /app/requirements_4b_alphamap.txt \
    fi

############################################################################
ARG ALPHAPEPTDEEP_REF="latest"
RUN git clone https://github.com/MannLabs/alphapeptdeep.git \
    && cd alphapeptdeep \
    && git checkout $(../get_ref.sh $ALPHAPEPTDEEP_REF) \
    && ../replace_alphax.sh \
    && git status

RUN --mount=type=cache,target=/root/.cache/pip \
    cd alphapeptdeep && pip install "."

RUN pip freeze > /app/requirements_5_alphapeptdeep.txt

############################################################################
ARG DIRECTLFQ_REF="latest"
RUN git clone https://github.com/MannLabs/directlfq.git \
    && cd directlfq \
    && git checkout $(../get_ref.sh $DIRECTLFQ_REF) \
    && git status

RUN --mount=type=cache,target=/root/.cache/pip \
    cd directlfq && pip install "."

RUN pip freeze > /app/requirements_6_directlfq.txt
############################################################################
ARG ALPHADIA_REF="latest"
RUN git clone https://github.com/MannLabs/alphadia.git \
    && cd alphadia \
    && git checkout $(../get_ref.sh $ALPHADIA_REF) \
    && ../replace_alphax.sh \
    && git status

RUN --mount=type=cache,target=/root/.cache/pip \
    cd alphadia && pip install ".[stable]"

RUN pip freeze > /app/requirements_7_alphadia.txt

############################################################################
# additional dependencies for testing
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install pytest nbmake

RUN pip freeze > /app/requirements_8_final.txt

## TODO remove this once https://github.com/MannLabs/alphabase/pull/288 is released
#RUN --mount=type=cache,target=/root/.cache/pip \
#    pip uninstall progressbar -y

# build:
# docker build -f Dockerfile  --build-arg="ALPHABASE_REF=latest" --build-arg="ALPHATIMS_REF=latest" --build-arg="ALPHARAW_REF=f8a355a" --build-arg="ALPHAPEPTDEEP_REF=latest" --build-arg="DIRECTLFQ_REF=latest" -t alphax_e2e .

# run bash:
# DATA_FOLDER=.
# docker run -v $DATA_FOLDER:/app/data/ -it alphax_e2e bash
