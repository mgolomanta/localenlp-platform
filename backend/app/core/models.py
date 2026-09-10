MODEL_REGISTRY = {
    ("eng", "wol"): {
        "id": "LocaleNLP/localenlp-eng-wol-0.03",
        "name": "English → Wolof",
    },
    ("wol", "eng"): {
        "id": "LocaleNLP/localenlp-wol-eng-0.03",
        "name": "Wolof → English",
    },
    ("eng", "hau"): {
        "id": "LocaleNLP/localenlp-eng-hau-0.01",
        "name": "English → Hausa",
    },
    ("hau", "eng"): {
        "id": "LocaleNLP/localenlp-hau-eng-0.01",
        "name": "Hausa → English",
    },
}

LANGUAGES = {
    "eng": {"code": "eng", "name": "English"},
    "wol": {"code": "wol", "name": "Wolof"},
    "hau": {"code": "hau", "name": "Hausa"},
}


def supported_pairs():
    return [
        {
            "source": source,
            "target": target,
            "model": info["id"],
            "name": info["name"],
        }
        for (source, target), info in MODEL_REGISTRY.items()
    ]
