"""Constrained decoding primitives."""
import numpy as np

from llm_sdk import Small_LLM_Model
from src.vocab import Vocabulary
import re

NUMBER_CHARS = set("-0123456789.")
_PREFIX = re.compile(r"-?(?:0|[1-9][0-9]*)?(?:\.[0-9]*)?")


def pick_token(logits: list[float], allowed: list[int]) -> int:
    """Pick the best token among the allowed ones.

    Every token that is not allowed gets a logit of -inf, so it can
    never be selected.

    Args:
        logits: raw logits from the model (one per token id).
        allowed: ids of tokens that may be chosen.

    Returns:
        The id of the allowed token with the highest logit.
    """
    scores = np.asarray(logits, dtype=np.float64)
    masked = np.full_like(scores, -np.inf)
    masked[allowed] = scores[allowed]
    return int(np.argmax(masked))


def generate_choice(
    model: Small_LLM_Model,
    vocab: Vocabulary,
    ids: list[int],
    targets: list[str],
) -> str:
    """Let the model choose one string among `targets`, token by token.

    The list `ids` is extended in place with every generated token.
    As soon as only one target is still compatible with the text
    generated so far, the rest of it is forced without calling the model.

    Args:
        model: the LLM wrapper.
        vocab: decoded vocabulary.
        ids: current context, modified in place.
        targets: the only strings the model is allowed to produce.

    Returns:
        The chosen target string.

    Raises:
        ValueError: if no token can continue any target.
    """
    generated = ""
    while generated not in targets:
        remaining = [t for t in targets if t.startswith(generated)]
        if len(remaining) == 1:
            rest = remaining[0][len(generated):]
            ids.extend(model.encode(rest)[0].tolist())
            return remaining[0]
        allowed = vocab.allowed_prefixes(generated, targets)
        if not allowed:
            raise ValueError(f"No valid token after {generated!r}")
        if len(allowed) == 1:
            token = allowed[0]
        else:
            logits = model.get_logits_from_input_ids(ids)
            token = pick_token(logits, allowed)
        ids.append(token)
        text = vocab.texts[token]
        generated += text if text is not None else ""
    return generated


def is_number_prefix(text: str, integer: bool = False) -> bool:
    """Tell whether `text` can still become a valid JSON number.

    Args:
        text: characters generated so far.
        integer: forbid the decimal point when True.

    Returns:
        True if `text` is a valid beginning of a number.
    """
    if integer and "." in text:
        return False
    if _PREFIX.fullmatch(text) is None:
        return False
    return not text.lstrip("-").startswith(".")


def is_number_complete(text: str, integer: bool = False) -> bool:
    """Tell whether `text` is a complete valid number (ends with a digit)."""
    return (
        bool(text)
        and text[-1].isdigit()
        and is_number_prefix(text, integer)
    )
