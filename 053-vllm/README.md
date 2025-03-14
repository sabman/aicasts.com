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


vLLM is fast with:

- State-of-the-art serving throughput
- Efficient management of attention key and value memory with PagedAttention
- Continuous batching of incoming requests
- Fast model execution with CUDA/HIP graph
- Quantization: GPTQ, AWQ, INT4, INT8, and FP8
- Optimized CUDA kernels, including integration with FlashAttention and FlashInfer.
- Speculative decoding
- Chunked prefill

vLLM is flexible and easy to use with:
- Seamless integration with popular HuggingFace models
- High-throughput serving with various decoding algorithms, including parallel sampling, beam search, and more
- Tensor parallelism and pipeline parallelism support for distributed inference
- Streaming outputs
- OpenAI-compatible API server
- Support NVIDIA GPUs, AMD CPUs and GPUs, Intel CPUs, Gaudi® accelerators and GPUs, PowerPC CPUs, TPU, and AWS Trainium and Inferentia Accelerators.
- Prefix caching support
- Multi-lora support
