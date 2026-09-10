import logging
from threading import Lock

import torch
from transformers import MarianMTModel, MarianTokenizer

from app.core.config import get_settings
from app.core.models import MODEL_REGISTRY

logger = logging.getLogger(__name__)


class ModelManager:
    def __init__(self):
        self.settings = get_settings()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.models = {}
        self.tokenizers = {}
        self._lock = Lock()
        logger.info("Translation device: %s", self.device)

    def load_model(self, source_lang: str, target_lang: str):
        key = (source_lang, target_lang)
        if key not in MODEL_REGISTRY:
            raise ValueError(f"Unsupported language pair: {source_lang} -> {target_lang}")
        if key in self.models:
            return self.tokenizers[key], self.models[key]
        with self._lock:
            if key in self.models:
                return self.tokenizers[key], self.models[key]
            model_id = MODEL_REGISTRY[key]["id"]
            logger.info("Loading translation model: %s", model_id)
            tokenizer = MarianTokenizer.from_pretrained(model_id, token=self.settings.hf_token, cache_dir=self.settings.model_cache_dir)
            model = MarianMTModel.from_pretrained(model_id, token=self.settings.hf_token, cache_dir=self.settings.model_cache_dir)
            model.to(self.device)
            model.eval()
            self.tokenizers[key] = tokenizer
            self.models[key] = model
            logger.info("Loaded %s on %s", model_id, self.device)
        return self.tokenizers[key], self.models[key]

    def loaded_models(self):
        return [
            {"source": source, "target": target, "model": MODEL_REGISTRY[(source, target)]["id"], "device": str(self.device)}
            for source, target in self.models
        ]


model_manager = ModelManager()
