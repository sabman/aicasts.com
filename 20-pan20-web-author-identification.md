# Authorship Verification 2020

- Source: https://pan.webis.de/clef20/pan20-web/author-identification.html
- Code: https://github.com/pan-webis-de/pan-code/tree/master/clef20/authorship-verification


In this challenge, given two pieces of texts, we have to determine if they were written by the same author or two different authors based on the writing "style".

To test the quality of the model there are three distinct verification tasks, each task is to be released every year starting in 2020 and ending 2022.

Year 1 (PAN 2020): Closed-set verification.


https://github.com/pan-webis-de/pan-code/blob/master/clef20/authorship-verification/README.md

This folder contains all code, data and images used in preparing the extended lab overview paper for the authorship verification task at PAN 2020. The relevant files are the following:

## Data

**submissions**: the folder containing the unaltered predictions by each submitted system for the test set.
**datasets/pan20-authorship-verification-test/truth.jsonl**: the ground ground for the test problems.
**img/*.svg**: SVG-files for the images used in the extended lab overview paper.

## Spreadsheets
**metrics.xlsx**: the final performance of each system in a tabular format.
**predictions.xlsx**: a tabular overview of all predictions for all submissions per text pair.
**predictions_topic.xlsx**: same as predictions.xlsx, but with a column for the topical dissimilarity for each text pair, as measured by a simple NMF-based topic model.

TODO: 
- try training
- check this issue https://github.com/pan-webis-de/pan-code/issues/1

This baseline offers a naive, yet fast solution to the  PAN2020 track on authorship verification. All documents are represented using a **bag-of-character-ngrams** model, that is **TFIDF weighted**. The **cosine similarity** between each document pair in the calibration data set is calculated. Finally, the resulting similarities are optimized, and projected through a simple **rescaling operation**, so that they can function as **pseudo-probabilities**, indiciating the likelihood that a document-pair is a same-author pair. Via a grid search, the optimal verification threshold is determined, taking into account that some difficult problems can be left unanswered.
