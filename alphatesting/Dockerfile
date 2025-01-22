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

############################################################################
ARG ALPHABASE_REF="development"
RUN git clone https://github.com/MannLabs/alphabase.git \
    && cd alphabase \
    && git checkout $(../get_ref.sh $ALPHABASE_REF) \
    && git status

RUN --mount=type=cache,target=/root/.cache/pip \
    cd alphabase && pip install "."


############################################################################
ARG ALPHATIMS_REF="develop"
RUN git clone https://github.com/MannLabs/alphatims.git \
    && cd alphatims \
    && git checkout $(../get_ref.sh $ALPHATIMS_REF) \
    && git status

RUN --mount=type=cache,target=/root/.cache/pip \
    cd alphatims && pip install "."


############################################################################
ARG ALPHARAW_REF="development"
RUN git clone https://github.com/MannLabs/alpharaw.git \
    && cd alpharaw \
    && git checkout $(../get_ref.sh $ALPHARAW_REF) \
    && ../replace_alphax.sh \
    && git status

RUN --mount=type=cache,target=/root/.cache/pip \
    cd alpharaw && pip install "."


############################################################################
ARG ALPHAVIZ_REF="development"
RUN git clone https://github.com/MannLabs/alphaviz.git \
    && cd alphaviz \
    && git checkout $(../get_ref.sh $ALPHAVIZ_REF) \
    && ../replace_alphax.sh \
    && git status

RUN --mount=type=cache,target=/root/.cache/pip \
    cd alphaviz && pip install "."



############################################################################
ARG ALPHAPEPTDEEP_REF="development"
RUN git clone https://github.com/MannLabs/alphapeptdeep.git \
    && cd alphapeptdeep \
    && git checkout $(../get_ref.sh $ALPHAPEPTDEEP_REF) \
    && ../replace_alphax.sh \
    && git status

RUN --mount=type=cache,target=/root/.cache/pip \
    cd alphapeptdeep && pip install "."


############################################################################
ARG DIRECTLFQ_REF="development"
RUN git clone https://github.com/MannLabs/directlfq.git \
    && cd directlfq \
    && git checkout $(../get_ref.sh $DIRECTLFQ_REF) \
    && git status

RUN --mount=type=cache,target=/root/.cache/pip \
    cd directlfq && pip install "."

############################################################################
ARG ALPHADIA_REF="main"
RUN git clone https://github.com/MannLabs/alphadia.git \
    && cd alphadia \
    && git checkout $(../get_ref.sh $ALPHADIA_REF) \
    && git status

# need to delete requirements in two files, otherwise the test comparing them will fail
RUN cd alphadia \
    && ../replace_alphax.sh ./requirements/requirements.txt \
    && ../replace_alphax.sh ./requirements/requirements_loose.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    cd alphadia && pip install ".[stable]"


############################################################################
# additional dependencies for testing
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install pytest nbmake

# TODO remove this once https://github.com/MannLabs/alphabase/pull/288 is released
RUN --mount=type=cache,target=/root/.cache/pip \
    pip uninstall progressbar


# build:
# docker build -f Dockerfile.e2e  --build-arg="ALPHABASE_REF=latest" --build-arg="ALPHATIMS_REF=latest" --build-arg="ALPHARAW_REF=f8a355a" --build-arg="ALPHAPEPTDEEP_REF=latest" --build-arg="DIRECTLFQ_REF=latest" -t alphax_e2e .

# run bash:
# docker run -v $DATA_FOLDER:/app/data/ -it alphax_e2e bashx
