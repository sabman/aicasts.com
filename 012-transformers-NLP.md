## Concepts

- Tokenizing
- Text preprocessing
- Hyperparameter Optimization
- Lemmatizing
- Pattern Matching

## Courses

- Natural Language Processing course by Dan Jurafsky and Christopher Manning https://www.youtube.com/playlist?list=PLQiyVNMpDLKnZYBTUOlSI9mi9wAErFtFm
- https://web.stanford.edu/~jurafsky/NLPCourseraSlides.html


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