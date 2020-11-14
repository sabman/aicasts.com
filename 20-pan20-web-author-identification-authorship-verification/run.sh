#!/bin/bash

# baseline script is representing documents using bag-of-character-ngrams model that is TFIDF weighted, cosine similarity between each document pair in the calibration data set is  calculated.

python pan20-verif-baseline.py \
    -input_pairs="datasets/pan20-authorship-verification-training-small/pairs.jsonl" \
    -input_truth="datasets/pan20-authorship-verification-training-small/truth.jsonl" \
    -test_pairs="datasets/pan20-authorship-verification-test/pairs.jsonl" \
    -num_iterations=0 \
    -output="out"

