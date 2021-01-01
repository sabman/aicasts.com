

## Concepts


- Tokenizing
- Text preprocessing
- Hyperparameter Optimization
- Lemmatizing
- Pattern Matching

## Courses

- Natural Language Processing course by Dan Jurafsky and Christopher Manning https://www.youtube.com/playlist?list=PLQiyVNMpDLKnZYBTUOlSI9mi9wAErFtFm
- https://web.stanford.edu/~jurafsky/NLPCourseraSlides.html

- https://www.coursera.org/specializations/natural-language-processing

ref https://github.com/sabman/aicasts.com/issues/18


Quick start:
```sh
pip install transformers
pip install -U tqdm
```

```python
import torch
from transformers import BertTokenizer, BertModel, BertForMaskedLM

# OPTIONAL: if you want to have more information on what's happening under the hood, activate the logger as follows
import logging
logging.basicConfig(level=logging.INFO)

# Load pre-trained model tokenizer (vocabulary)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenize input
text = "[CLS] Who was Jim Henson ? [SEP] Jim Henson was a puppeteer [SEP]"
tokenized_text = tokenizer.tokenize(text)

# Mask a token that we will try to predict back with `BertForMaskedLM`
masked_index = 8
tokenized_text[masked_index] = '[MASK]'
assert tokenized_text == ['[CLS]', 'who', 'was', 'jim', 'henson', '?',
                          '[SEP]', 'jim', '[MASK]', 'was', 'a', 'puppet', '##eer', '[SEP]']

# Convert token to vocabulary indices
indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
# Define sentence A and B indices associated to 1st and 2nd sentences (see paper)
segments_ids = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]

# Convert inputs to PyTorch tensors
tokens_tensor = torch.tensor([indexed_tokens])
segments_tensors = torch.tensor([segments_ids])

# Load pre-trained model (weights)
model = BertModel.from_pretrained('bert-base-uncased')

# Set the model in evaluation mode to deactivate the DropOut modules
# This is IMPORTANT to have reproducible results during evaluation!
model.eval()

# If you have a GPU, put everything on cuda
tokens_tensor = tokens_tensor.to('cuda') # change to cpu if no gpu
segments_tensors = segments_tensors.to('cuda') # change to cpu if no gpu
model.to('cuda') # change to cpu if no gpu

# Predict hidden states features for each layer
with torch.no_grad():
    # See the models docstrings for the detail of the inputs
    outputs = model(tokens_tensor, token_type_ids=segments_tensors)
    # Transformers models always output tuples.
    # See the models docstrings for the detail of all the outputs
    # In our case, the first element is the hidden state of the last layer of the Bert model
    encoded_layers = outputs[0]
# We have encoded our input sequence in a FloatTensor of shape (batch size, sequence length, model hidden dimension)
assert tuple(encoded_layers.shape) == (
    1, len(indexed_tokens), model.config.hidden_size)

# Load pre-trained model (weights)
model = BertForMaskedLM.from_pretrained('bert-base-uncased')
model.eval()

# If you have a GPU, put everything on cuda
tokens_tensor = tokens_tensor.to('cuda') # change to cpu if no gpu
segments_tensors = segments_tensors.to('cuda') # change to cpu if no gpu
model.to('cuda') # change to cpu if no gpu

# Predict all tokens
with torch.no_grad():
    outputs = model(tokens_tensor, token_type_ids=segments_tensors)
    predictions = outputs[0]

# confirm we were able to predict 'henson'
predicted_index = torch.argmax(predictions[0, masked_index]).item()
predicted_token = tokenizer.convert_ids_to_tokens([predicted_index])[0]
assert predicted_token == 'henson'
```

```
python bret_example.py
```

TODO:
* examples: https://github.com/huggingface/transformers#run-the-examples
  * https://github.com/huggingface/transformers/blob/master/examples/README.md


```
git clone https://github.com/huggingface/transformers
cd transformers
pip install .
pip install -r ./examples/requirements.txt
```

- https://huggingface.co/datasets/style_change_detection
- https://github.com/jabraunlin/reddit-user-id
- https://medium.com/data-science-bootcamp/getting-started-with-natural-language-processing-nlp-for-beginners-64a699cc60c3
- https://dev.to/nicfoxds/getting-started-in-nlp-b0e
- https://github.com/graykode/nlp-roadmap
- https://www.kaggle.com/matleonard/intro-to-nlp


```python

corpus = ["You are reading a tutorial by Uniqtech. We are talking about Natural Language Processing aka NLP. Would you like to learn more? Learn more about Machine Learning today!"]
# if use corpus = "..."
# receive error
# ValueError: Iterable over raw text documents expected, string object received.

from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
bow = count_vect.fit_transform(corpus)
bow.shape #(1,22)
count_vect.get_feature_names()
#[u'about', u'aka', u'are', u'by', u'language', u'learn', u'learning', u'like', u'machine', u'more', u'natural', u'nlp', u'processing', u'reading', u'talking', u'to', u'today', u'tutorial', u'uniqtech', u'we', u'would', u'you']
bow.toarray()
#array([[2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]])
```

```python
#import regex
import re
corpus = "You are reading a tutorial by Uniqtech. We are talking about Natural Language Processing aka NLP. Would you like to learn more? Learn more about Machine Learning today!"
corpus = re.sub("[^a-zA-Z0-9]+", "",corpus)
corpus
# 'YouarereadingatutorialbyUniqtechWearetalkingaboutNaturalLanguageProcessingakaNLPWouldyouliketolearnmoreLearnmoreaboutMachineLearningtoday'
#note space is also removed
# ^\s means DO NOT MATCH SPACE
corpus = re.sub("[^a-zA-Z0-9\s]+", "",corpus)
corpus
#returns 'You are reading a tutorial by Uniqtech We are talking about Natural Language Processing aka NLP Would you like to learn more Learn more about Machine Learning today'
```

German and spaCy

- https://www.kaggle.com/saburq/intro-to-nlp/

Full Course on Kaggle:
- https://www.kaggle.com/learn/natural-language-processing


## Text Classification with SpaCy

A common task in NLP is text classification. This is "classification" in the conventional machine learning sense, and it is applied to text. Examples include spam detection, sentiment analysis, and tagging customer queries.

In this tutorial, you'll learn text classification with spaCy. The classifier will detect spam messages, a common functionality in most email clients. Here is an overview of the data you'll use:

exe 1 https://www.kaggle.com/saburq/exercise-intro-to-nlp/edit

---

exe 2 https://www.kaggle.com/saburq/exercise-text-classification/edit

u did a great such a great job for DeFalco's restaurant in the **previous** exercise that the chef has hired you for a new project.

The restaurant's menu includes an email address where visitors can give feedback about their food.

The manager wants you to create a tool that automatically sends him all the negative reviews so he can fix them, while automatically sending all the positive reviews to the owner, so the manager can ask for a raise.

You will first build a model to distinguish positive reviews from negative reviews using Yelp reviews because these reviews include a rating with each review. Your data consists of the text body of each review along with the star rating. Ratings with 1-2 stars count as "negative", and ratings with 4-5 stars are "positive". Ratings with 3 stars are "neutral" and have been dropped from the data.

Let's get started. First, run the next code cell.


exe 3 https://www.kaggle.com/saburq/word-vectors/edit

You know at this point that machine learning on text requires that you first represent the text numerically. So far, you've done this with bag of words representations. But you can usually do better with word embeddings.

**Word embeddings** (also called word vectors) represent each word numerically in such a way that the vector corresponds to how that word is used or what it means. Vector encodings are learned by considering the context in which the words appear. Words that appear in similar contexts will have similar vectors. For example, vectors for "leopard", "lion", and "tiger" will be close together, while they'll be far away from "planet" and "castle".

Even cooler, relations between words can be examined with mathematical operations. Subtracting the vectors for "man" and "woman" will return another vector. If you add that to the vector for "king" the result is close to the vector for "queen."

![Word vector examples](https://www.tensorflow.org/images/linear-relationships.png)

These vectors can be used as features for machine learning models. Word vectors will typically improve the performance of your models above bag of words encoding. spaCy provides embeddings learned from a model called Word2Vec. You can access them by loading a large language model like `en_core_web_lg`. Then they will be available on tokens from the `.vector` attribute.


```py
import numpy as np
import spacy

# Need to load the large model to get the vectors
nlp = spacy.load('en_core_web_lg')
```

```py
# Disabling other pipes because we don't need them and it'll speed up this part a bit
text = "These vectors can be used as features for machine learning models."
with nlp.disable_pipes():
    vectors = np.array([token.vector for token in  nlp(text)])
```

```py
vectors.shape
# (12, 300)
```

These are 300-dimensional vectors, with one vector for each word. However, we only have document-level labels and our models won't be able to use the word-level embeddings. So, you need a vector representation for the entire document. 

There are many ways to combine all the word vectors into a single document vector we can use for model training. A simple and surprisingly effective approach is simply averaging the vectors for each word in the document. Then, you can use these document vectors for modeling.

spaCy calculates the average document vector which you can get with `doc.vector`. Here is an example loading the spam data and converting it to document vectors.
These are 300-dimensional vectors, with one vector for each word. However, we only have document-level labels and our models won't be able to use the word-level embeddings. So, you need a vector representation for the entire document. 
​
There are many ways to combine all the word vectors into a single document vector we can use for model training. A simple and surprisingly effective approach is simply averaging the vectors for each word in the document. Then, you can use these document vectors for modeling.
​
spaCy calculates the average document vector which you can get with `doc.vector`. Here is an example loading the spam data and converting it to document vectors.

```py
import pandas as pd

# Loading the spam data
# ham is the label for non-spam messages
spam = pd.read_csv('../input/nlp-course/spam.csv')

with nlp.disable_pipes():
    doc_vectors = np.array([nlp(text).vector for text in spam.text])
    
doc_vectors.shape
```


```py
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(doc_vectors, spam.label,
                                                    test_size=0.1, random_state=1)
```

exe 4 https://www.kaggle.com/saburq/exercise-word-vectors/edit word vectors

Vectorizing Language

Embeddings are both conceptually clever and practically effective.

So let's try them for the sentiment analysis model you built for the restaurant. Then you can find the most similar review in the data set given some example text. It's a task where you can easily judge for yourself how well the embeddings work

```py
%matplotlib inline

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import spacy

# Set up code checking
from learntools.core import binder
binder.bind(globals())
from learntools.nlp.ex3 import *
print("\nSetup complete")
```

## Stanford cs224n deep learning and nlp

http://web.stanford.edu/class/cs224n/

## Transformer Architecture

https://en.wikipedia.org/wiki/Transformer_(machine_learning_model)

## References

- https://www.kaggle.com/abhishek/approaching-almost-any-nlp-problem-on-kaggle/
- https://www.kaggle.com/c/spooky-author-identification/discussion/42220
- Feature Engineering https://www.kaggle.com/c/spooky-author-identification/discussion/42242

## Topics

- tfidf 
- count features
- logistic regression
- naive bayes
- svm
- xgboost
- grid search
- word vectors
- LSTM
- GRU
- Ensembling
