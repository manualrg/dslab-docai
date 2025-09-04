from typing import List
from pathlib import Path
import json
import pandas as pd
from langchain_core.documents import Document


def corpus_stats(encoding, corpus: List[Document]) -> pd.Series:
    lst_docs = [encoding.encode(doc.page_content) for doc in corpus]
    data = [len(x) for x in lst_docs]
    return pd.Series(data)


def save_documents(corpus: List[Document], path: Path) -> None:

    assert path.suffix is not "", "Extension not detected! Please, pass a path ended in .json?"
    path.parent.mkdir(
        parents=True, exist_ok=True
    )


    lst_chunks = []
    for doc in corpus:
        lst_chunks.append(
            json.loads(doc.model_dump_json())
            )

    with open(path , 'w') as f:
        json.dump(lst_chunks, f)

def load_documents(path: Path) -> List[Document]:

    assert path.is_file(), "File not found"
    
    with open(path, 'r') as f:
        lst_chunks = json.load(f)

    lst_docs = []
    for chunk in lst_chunks:
        lst_docs.append(
            Document(**chunk)
            )
    return lst_docs