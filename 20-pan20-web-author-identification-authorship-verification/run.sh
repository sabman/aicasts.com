#!/bin/bash

# baseline script is representing documents using bag-of-character-ngrams model that is TFIDF weighted, cosine similarity between each document pair in the calibration data set is  calculated.

# resulting similarities are optimized, and projected through a simple rescaling operation, so that they can function as pseudo-probabilities, indiciating the likelihood that a document-pair is a same-author pair

# Input Pairs path: 
# datasets/pan20-authorship-verification-training-small/pan20-authorship-verification-training-small.jsonl

# Input Truth path:
# datasets/pan20-authorship-verification-training-small/pan20-authorship-verification-training-small-truth.jsonl

# Test Pairs Path:
# datasets/pan20-authorship-verification-test/truth.jsonl

python pan20-verif-baseline.py \
    -input_pairs="datasets/pan20-authorship-verification-training-small/pairs.jsonl" \
    -input_truth="datasets/pan20-authorship-verification-training-small/truth.jsonl" \
    -test_pairs="datasets/pan20-authorship-verification-test/pairs.jsonl" \
    -num_iterations=0 \
    -output="out"

