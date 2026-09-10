import torch

from app.core.config import get_settings
from app.services.model_manager import model_manager
from app.services.text_utils import batch_list, sentence_case, split_sentences


def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    settings = get_settings()
    if not text or not text.strip():
        return ""
    if len(text) > settings.max_input_chars:
        raise ValueError(f"Input is too large. Maximum is {settings.max_input_chars} characters.")
    tokenizer, model = model_manager.load_model(source_lang, target_lang)
    paragraphs = re_normalize_paragraphs(text)
    output_paragraphs = []
    for paragraph in paragraphs:
        if not paragraph.strip():
            output_paragraphs.append("")
            continue
        sentences = split_sentences(paragraph)
        translated_sentences = []
        for batch in batch_list(sentences, settings.translation_batch_size):
            inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=settings.max_translation_tokens)
            inputs = {key: value.to(model.device) for key, value in inputs.items()}
            with torch.inference_mode():
                outputs = model.generate(**inputs, max_length=settings.max_translation_tokens, num_beams=settings.num_beams, early_stopping=True, no_repeat_ngram_size=3, repetition_penalty=1.5, length_penalty=1.2)
            translated_sentences.extend(tokenizer.batch_decode(outputs, skip_special_tokens=True))
        output_paragraphs.append(sentence_case(" ".join(s.strip() for s in translated_sentences if s.strip())))
    return "\n".join(output_paragraphs).strip()


def re_normalize_paragraphs(text: str) -> list[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.split("\n")
