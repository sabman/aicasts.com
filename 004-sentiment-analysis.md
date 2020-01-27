
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