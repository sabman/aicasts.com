# VLLM

## Installation

```bash
pip install vllm
```

## What is VLLM?

VLLM is a fast and efficient LLM inference engine that supports both single-GPU and multi-GPU inference. It is designed to be used with the VLLM API, which is a Python API for the VLLM engine.

## How to use VLLM?

```python
from vllm import LLM

llm = LLM(model="meta-llama/Meta-Llama-3-8B-Instruct")

llm.generate("Hello, world!")
```