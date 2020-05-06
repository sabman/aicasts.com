
https://www.pythonforengineers.com/natural-language-processing-and-sentiment-analysis-with-python/
https://github.com/huggingface/transformers
https://huggingface.co/transformers/installation.html

```
pip install transformers
```

```python
from transformers import pipeline

# Allocate a pipeline for sentiment-analysis
nlp = pipeline('sentiment-analysis')
nlp('We are very happy to include pipeline into the transformers repository.')
>>> {'label': 'POSITIVE', 'score': 0.99893874}

# Allocate a pipeline for question-answering
nlp = pipeline('question-answering')
nlp({
    'question': 'What is the name of the repository ?',
    'context': 'Pipeline have been included in the huggingface/transformers repository'
})
>>> {'score': 0.28756016668193496, 'start': 35, 'end': 59, 'answer': 'huggingface/transformers'}
```



> In this tutorial I’ll show you how to use BERT with the huggingface PyTorch library to quickly and efficiently fine-tune a model to get near state of the art performance in sentence classification. More broadly, I describe the practical application of transfer learning in NLP to create high performance models with minimal effort on a range of NLP tasks.

- [ ] https://mccormickml.com/2019/07/22/BERT-fine-tuning/


> This is Part 3 of a series on fine-grained sentiment analysis in Python. Parts 1 and 2 covered the analysis and explanation of six different classification methods on the Stanford Sentiment Treebank fine-grained (SST-5) dataset. In this post, we’ll look at how to improve on past results by building a transformer-based model and applying transfer learning, a powerful method that has been dominating NLP task leaderboards lately.

- [ ] https://towardsdatascience.com/fine-grained-sentiment-analysis-part-3-fine-tuning-transformers-1ae6574f25a6