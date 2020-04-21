FROM postgres:11.7-alpine

RUN apt-get update && apt-get install -y git libreadline-dev bison flex

WORKDIR /tmp
RUN git clone https://github.com/google/differential-privacy.git && \
    cd differential-privacy && bazel build differential_privacy
