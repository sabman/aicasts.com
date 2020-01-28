
https://www.pythonforengineers.com/natural-language-processing-and-sentiment-analysis-with-python/
https://github.com/huggingface/transformers

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
