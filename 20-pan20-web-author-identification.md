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

```python
def main():
    parser = argparse.ArgumentParser(description='Distance-based verification: PAN20 baseline')
    # data settings:
    parser.add_argument('-input_pairs', type=str, required=True,
                        help='Path to the jsonl-file with the input pairs')
    parser.add_argument('-input_truth', type=str, required=True,
                        help='Path to the ground truth-file for the input pairs')
    parser.add_argument('-test_pairs', type=str, required=True,
                        help='Path to the jsonl-file with the test pairs')
    parser.add_argument('-output', type=str, required=True,
                        help='Path to the output folder for the predictions.\
                             (Will be overwritten if it exist already.)')
    # algorithmic settings:
    parser.add_argument('-seed', default=2020, type=int,
                        help='Random seed')
    parser.add_argument('-vocab_size', default=3000, type=int,
                        help='Maximum number of vocabulary items in feature space')
    parser.add_argument('-ngram_size', default=4, type=int,
                        help='Size of the ngrams')
    parser.add_argument('-num_iterations', default=0, type=int,
                        help='Number of iterations (`k`); zero by default')
    parser.add_argument('-dropout', default=.5, type=float,
                        help='Proportion of features to keep in each iteration')
    # run
    args = parser.parse_args()
    print(args)

    np.random.seed(args.seed)
    random.seed(args.seed)

    try:
        shutil.rmtree(args.output)
    except FileNotFoundError:
        pass
    os.mkdir(args.output)

    gold = {}
    for line in open(args.input_truth):
        d = json.loads(line.strip())
        gold[d['id']] = int(d['same'])
    
    # truncation for development purposes
    cutoff = 0
    if cutoff:
        gold = dict(random.sample(gold.items(), cutoff))
        print(len(gold))

    texts = []
    for line in tqdm(open(args.input_pairs)):
        d = json.loads(line.strip())
        if d['id'] in gold:
            texts.extend(d['pair'])

    print('-> constructing vectorizer')
    vectorizer = TfidfVectorizer(max_features=args.vocab_size, analyzer='char',
                                 ngram_range=(args.ngram_size, args.ngram_size))
    vectorizer.fit(texts)

```