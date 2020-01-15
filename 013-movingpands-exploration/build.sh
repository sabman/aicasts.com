#!/bin/bash

docker build -t movingpandas \
  --build-arg USER_ID=$(id -u) \
  --build-arg GROUP_ID=$(id -g) .
