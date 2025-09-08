import logging
from pathlib import Path
import re


logger = logging.getLogger(__name__)


def is_valid_input(pattern, text):
  """
  Checks if a given text matches a regex pattern.

  Args:
    pattern: The regular expression pattern.
    text: The string to be searched.

  Returns:
    True if a match is found, False otherwise.
  """
  return re.search(pattern, text) is not None


def clean_md_heading(heading: str) -> str:
    pattern = r'^#+\s*'

    return  re.sub(pattern, '', heading)


def fix_section_title_l1_candidate(text, lst_titles):
    # los headers que esten en la lista, se corrigen para tener solo un #
    clean_text = clean_md_heading(text)  # remove # if present
    # may add to_lower and strip()
    
    if clean_text in lst_titles:
        replacement = r'# \1'

        pattern_not_l1 = re.compile(r'^#{2,}\s*(.+)$', re.MULTILINE) 

        fixed_text = pattern_not_l1.sub(replacement, text)
    else:
        fixed_text = text
    return fixed_text
