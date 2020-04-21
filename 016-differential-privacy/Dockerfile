FROM postgres:11.7-alpine

RUN apk add --update-cache \
    git libreadline-dev bison flex

WORKDIR /tmp
RUN git clone https://github.com/google/differential-privacy.git && \
    cd differential-privacy && bazel build differential_privacy
