FROM rgielen/postgresql-ubuntu

RUN apt-get update && apt-get install -y libreadline-dev bison flex git bazel

WORKDIR /tmp

RUN git clone https://github.com/google/differential-privacy.git && \
    cd differential-privacy && bazel build differential_privacy
