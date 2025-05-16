import urllib.request
import re
from models.simple_tokenizer_v2 import SimpleTokenizerV2

url = (
    "https://raw.githubusercontent.com/rasbt/"
    "LLMs-from-scratch/main/ch02/01_main-chapter-code/"
    "the-verdict.txt"
)

file_path = "data/the-verdict.txt"

urllib.request.urlretrieve(url, file_path)

with open(file_path, "r", encoding="utf-8") as f:
    raw_text = f.read()

print("Total number of character:", len(raw_text))

print(raw_text[:99])

preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text)

preprocessed = [item.strip() for item in preprocessed if item.strip()]

print(len(preprocessed))
print(preprocessed[:30])

all_words = sorted(set(preprocessed))

vocab_size = len(all_words)

all_tokens = sorted(list(set(preprocessed)))
all_tokens.extend(["<|endoftext|>", "<|unk|>"])
vocab = {token: integer for integer, token in enumerate(all_tokens)}
print(len(vocab.items()))

for i, item in reversed(list(enumerate(vocab.items()))):
    print(item)
    print(i)
    if i < 1000:
        break

# =============== Try Tokenizer ================
tokenizer = SimpleTokenizerV2(vocab)
text = """"It's the last he painted, you know,"
       Mrs. Gisburn said with pardonable pride."""
ids = tokenizer.encode(text)

print(ids)
print(tokenizer.decode(ids))

# ============ unknown ==================

text1 = "Hello, do you like tea?"

text2 = "In the sunlit terraces of the palace."
text = " <|endoftext|> ".join((text1, text2))
print(text)
print(tokenizer.encode(text))

tokenizer = SimpleTokenizerV2(vocab)
print(tokenizer.encode(text))
