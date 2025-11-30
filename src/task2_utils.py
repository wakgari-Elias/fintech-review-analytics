# src/task2_utils.py
"""
Helper utilities for Task-2: sentiment and thematic analysis.
"""

from langdetect.lang_detect_exception import LangDetectException
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0


def is_english(text: str) -> bool:
    """Return True if text is detected as English, else False."""
    try:
        return detect(str(text)) == "en"
    except LangDetectException:
        return False
