*This project has been created as part of the 42 curriculum by srasolov.*

# call me maybe — Function calling in LLMs

## Description

**Goal.** Translate a natural-language request into a structured function call.
Given `"What is the sum of 40 and 2?"`, the program does not answer `42`: it
outputs the function to call and its typed arguments.

```json
{"prompt": "What is the sum of 40 and 2?", "name": "fn_add_numbers", "parameters": {"a": 40.0, "b": 2.0}}
```

**Overview.** The program reads a list of available functions and a list of
prompts, asks a small LLM (`Qwen/Qwen3-0.6B`, 0.6B parameters) to pick the right
function and extract the arguments, and writes the result to a JSON file.
Small models are unreliable at writing JSON on their own, so the output is
**never left to the model alone**: the structure is built by the program and the
model only chooses *values*, token by token, through **constrained decoding**.
The result is valid JSON that follows the schema by construction.

**Features**
- Constrained decoding implemented from scratch (no `outlines`, `transformers`
  generation helpers, `dspy`, etc. in our code).
- Function chosen by the LLM, not by heuristics.
- Typed arguments: `number`, `integer`, `string`, `boolean`.
- Graceful handling of missing files, invalid JSON and invalid entries.
- Custom byte-level BPE vocabulary decoding (uses only `get_path_to_vocab_file`
  and `get_logits_from_input_ids` for generation).

## Instructions

**Requirements:** Python 3.12+, [`uv`](https://docs.astral.sh/uv/), internet
access on the first run (the model is downloaded from the Hugging Face Hub,
about 1.2 GB).

```bash
make install     # uv sync
make run         # uv run python -m src
make debug       # run under pdb
make lint        # flake8 + mypy
make lint-strict # flake8 + mypy --strict
make clean       # remove caches
```

Direct usage:

```bash
uv run python -m src \
    --functions_definition data/input/functions_definition.json \
    --input data/input/function_calling_tests.json \
    --output data/output/function_calling_results.json
```

All three options are optional; the values above are the defaults.

### Project layout

```
src/__main__.py   CLI arguments
src/motor.py      pipeline: load files, generate, write results
src/readfile.py   JSON reading with clear errors
src/parser.py     pydantic models (Prompt, Parameter, Function)
src/prompt.py     prompt given to the model
src/vocab.py      vocabulary decoding and token lookup
src/constraints.py  logits masking, choice and number rules
src/generator.py  constrained generation of a full function call
llm_sdk/          provided wrapper around the model
data/input/       example inputs
```

## Example usage

Input (`function_calling_tests.json`):

```json
[{"prompt": "What is the sum of 265 and 345?"}, {"prompt": "Greet shrek"}]
```

Command:

```bash
uv run python -m src
```

Console:

```
[1/2] What is the sum of 265 and 345?
[2/2] Greet shrek
2/2 calls written to data/output/function_calling_results.json in 18.4s
```

Output (`data/output/function_calling_results.json`):

```json
[
    {
        "prompt": "What is the sum of 265 and 345?",
        "name": "fn_add_numbers",
        "parameters": {"a": 265.0, "b": 345.0}
    },
    {
        "prompt": "Greet shrek",
        "name": "fn_greet",
        "parameters": {"name": "shrek"}
    }
]
```

Errors are reported on stderr and never crash the program:

```
$ uv run python -m src --input missing.json
Error: File not found: missing.json
```

## Algorithm explanation

At every step the model returns one logit per token of its vocabulary (151,936
values). Plain decoding takes the best one. **Constrained decoding** first sets
the logit of every token that would break the expected structure to `-inf`,
then takes the best of what is left. The model can then only produce valid
continuations.

### 1. Vocabulary (`src/vocab.py`)

`vocab.json` stores tokens of a *byte-level BPE* tokenizer: each byte is written
as a printable character (a space is `Ġ`, a newline is `Ċ`). We rebuild the
GPT-2 byte-to-character table, invert it, and decode every token into its real
text. This gives:

- `texts[id]`: the real string of each token (`'{"'`, `'":'`, `' "'`, ...).
- `index[text]`: the ids of the tokens having exactly that text.

Tokens that are not valid UTF-8 on their own (a fragment of a multi-byte
character) are excluded. Ids above the size of `vocab.json` are special tokens
(`<|im_end|>`, ...): they have no text and are therefore always masked.
A token often contains several characters (`":` is one token), so masks always
reason on the full text of a token and never on single characters.

### 2. Generation of one function call (`src/generator.py`)

The prompt lists the available functions with their parameters and two small
examples, followed by the request. The program then builds the answer:

| Part | Who decides |
|---|---|
| `{"name": "` | forced by the program |
| function name | **the model**, restricted to existing names |
| `, "parameters": {` | forced |
| `"param": ` (schema order) | forced |
| the value | **the model**, restricted by the declared type |
| `, ` / closing braces | forced |

Forced text is appended to the context without calling the model.

### 3. Masks by type

- **Function name** (`generate_choice`): the targets are `name"` for every
  function (the closing quote makes names that are prefixes of others, such as
  `fn_add` and `fn_add_numbers`, unambiguous). At each step only tokens whose
  text is a prefix of what remains of a target are allowed. When a single
  target remains compatible, the rest is forced.
- **number / integer**: a token is allowed if the text so far plus the token
  is still a valid JSON number prefix (checked with a regular expression, no
  leading zeros, no decimal point for integers). Once the number is complete,
  tokens starting with `,` or `}` are also allowed and act as the stop signal.
- **string**: any token without a double quote or control character, plus the
  tokens starting with `"` which close the string. The text is then unescaped
  with `json.loads`, so the model can write `\\d+` and the result is `\d+`.
- **boolean**: choice between `true` and `false`, same mechanism as function
  names.

### 4. Safety nets

- `MAX_STRING_TOKENS` (48) and `MAX_NUMBER_CHARS` (20) bound every value.
- A loop detector stops a string when a block of 2 to 8 tokens repeats three
  times in a row, and removes the repeated copies.
- Every value is validated by pydantic before being written.

## Design decisions

- **Structure by the program, values by the model.** The model never has to
  write braces, quotes or key names, which is where small models fail.
- **Forced tokens skip the model.** The SDK has no KV cache, so each model call
  recomputes the whole prompt (about 2 s on CPU). Forcing deterministic parts
  and shortening the prompt are the main speed levers.
- **Do not force the beginning of function names.** Forcing a common prefix such
  as `fn_` split it in a way the tokenizer never produces naturally and made the
  model choose a wrong function. The model now writes the whole name.
- **Generic prompt examples.** The two examples use different functions and
  arguments than the tests, only to show the output format and how to close
  strings.
- **Resilience per prompt.** A failure on one prompt is reported and skipped,
  the others are still processed.
- **`package = false` in `pyproject.toml`.** The project is a program run with
  `python -m src`, not an installable package. `llm_sdk` is excluded from
  flake8 and mypy because it is the provided code.
- **Pydantic** is used for all data models (`Prompt`, `Function`,
  `FunctionCall`, `Vocabulary`).

## Performance analysis

Measured on a laptop **without GPU** (CPU, 6 torch threads), with the 11 example
prompts provided in the subject:

| Metric | Result |
|---|---|
| Valid JSON | 100 % (guaranteed by construction) |
| Correct function chosen | 11 / 11 |
| Fully correct arguments | 9 / 11 |
| Total time | about 200 s (about 2 s per model call) |

- **Reliability.** Output structure and types are always correct, because tokens
  that would break them cannot be selected.
- **Accuracy.** Numbers and simple strings are extracted correctly. The weak
  point is *regular expressions*: the 0.6B model sometimes adds a useless
  `\s` or a leading space in a replacement (for example `" *"` instead of
  `"*"`). The model has no way to know the exact regex expected, only the
  prompt examples help it.
- **Speed.** Time is almost proportional to the number of model calls. Simple
  prompts need 4 to 6 calls (about 10 s); regex prompts need 13 to 24 calls
  because strings are longer. A GPU would be much faster.

## Challenges faced

- **Vocabulary vs logits sizes.** The model returns 151,936 logits but
  `vocab.json` has 151,643 entries. The extra ids are special tokens and are
  masked, otherwise the model could emit an end-of-text token inside the JSON.
- **Byte-level BPE.** Tokens are not readable text (`Ġ`, `Ċ`). Solved by
  rebuilding the byte-to-unicode table to decode them.
- **Multi-character tokens.** `{"`, `":` or ` "` are single tokens, so masks work
  on token text, with prefix matching, not on characters.
- **Strings that never end.** The model sometimes repeated a pattern until the
  token limit. Solved with a loop detector and a token cap.
- **Speed.** The first version took about 410 s for 11 prompts. Forcing tokens
  that have no real choice, shortening the prompt and stopping loops early
  reduced it to about 200 s.
- **Wrong function after forcing a prefix.** See design decisions.
- **Escapes.** The model writes JSON-escaped text (`\\s`); unescaping it with
  `json.loads` avoids writing it twice.

## Testing strategy

- **Manual runs on the provided examples**, checking the function chosen, the
  types (`2.0` for a number) and the arguments extracted.
- **Error cases**: missing input file, invalid JSON, entries with a wrong type
  (`{"prompt": 5}`), entries with no `prompt` key, empty list of prompts.
  Each one must print a clear message and never raise a traceback.
- **Output validation**: the result file is loaded with `python3 -m json.tool`
  and compared with the definitions (names, keys, types).
- **Other function sets**: running with a different `functions_definition.json`
  (including `integer` and `boolean` parameters) to make sure nothing depends
  on the provided examples.
- **Static checks**: `make lint` (flake8 and mypy) must pass.

## Resources

**References**
- Qwen3 model card — https://huggingface.co/Qwen/Qwen3-0.6B
- Hugging Face tokenizers documentation — https://huggingface.co/docs/tokenizers
- Sennrich et al., *Neural Machine Translation of Rare Words with Subword
  Units* (BPE), 2016.
- Radford et al., *Language Models are Unsupervised Multitask Learners*
  (GPT-2, byte-level BPE), 2019.
- Willard & Louf, *Efficient Guided Generation for Large Language Models*, 2023
  (idea of masking logits with a structure; no library from it is used).
- Pydantic documentation — https://docs.pydantic.dev
- uv documentation — https://docs.astral.sh/uv/

**Use of AI.** Claude (Anthropic) was used as a tutor and pair-programming
assistant:
- to understand constrained decoding and byte-level BPE, and to plan the
  architecture of the project;
- to draft first versions of `vocab.py`, `constraints.py`, `generator.py` and
  `motor.py`, which were then run, measured and modified step by step;
- to debug (a wrong function chosen after forcing a token prefix, strings
  looping, `uv` and `mypy` configuration) and to reduce the running time;
- to help write this README.

All generated code was read, tested and is understood by the author. The
function choice itself is always made by the LLM, never by AI-written heuristics.
