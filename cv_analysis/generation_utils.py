import re

import torch

from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer
)


MODEL_NAME = "google/flan-t5-base"


_tokenizer = None
_model = None


def get_text_generator():

    global _tokenizer
    global _model

    if (
        _tokenizer is None
        or
        _model is None
    ):

        print(
            "Loading text generation model..."
        )

        _tokenizer = (
            AutoTokenizer.from_pretrained(
                MODEL_NAME
            )
        )

        _model = (
            AutoModelForSeq2SeqLM.from_pretrained(
                MODEL_NAME
            )
        )

        _model.eval()

    return (
        _tokenizer,
        _model
    )


def clean_generated_text(
    text: str
) -> str:

    if not text:
        return ""

    text = text.strip()

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def generate_text(
    prompt: str,
    max_new_tokens: int = 160
) -> str:

    tokenizer, model = (
        get_text_generator()
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.inference_mode():

        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            num_beams=4,
            repetition_penalty=1.15,
            no_repeat_ngram_size=3,
            early_stopping=True
        )

    text = tokenizer.decode(
        output_ids[0],
        skip_special_tokens=True
    )

    return clean_generated_text(
        text
    )


def is_bad_generation(
    text: str,
    minimum_words: int = 12,
    forbidden_phrases: list[str] | None = None
) -> bool:

    if not text:
        return True

    words = text.split()

    if len(words) < minimum_words:
        return True

    lower = text.lower()

    if forbidden_phrases:

        for phrase in forbidden_phrases:

            if phrase.lower() in lower:
                return True

    return False