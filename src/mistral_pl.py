import logging
from pathlib import Path
from typing import Dict

from mistralai import Mistral, DocumentURLChunk
from mistralai.models import OCRResponse
from mistralai.extra import response_format_from_pydantic_model
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

MODEL_OCR = "mistral-ocr-latest"

def get_files(client) -> Dict[str, str]:
    resp_files  = client.files.list()
    dc_files = {file.filename: file.id for file in resp_files.data}

    return dc_files


def upload_if_not_exists(client, input_doc_path: Path) -> str:

    input_file = input_doc_path.stem  # no ext

    dc_files =  get_files(client)

    if input_doc_path in dc_files:
        logger.info("File %s is on Mistral Files.", input_file)
        id_file = dc_files[input_file]
    else:
        logger.info("File %s not found in Mistral Files.", input_file)
        assert input_doc_path.is_file()
        uploaded_file = client.files.upload(
            file={
                "file_name": input_file,
                "content": input_doc_path.read_bytes(),
            },
            purpose="ocr",
        )
            
        id_file = uploaded_file.id
        logger.info("Uploaded file %s to in Mistral Files.", input_file)
    
    return id_file



# Document Annotation response format
class Document(BaseModel):
  language: str = Field(..., description="Language in ISO 639 code")
  index_detected: bool  = Field(..., description="Whether an index is detected in the document")
  chapter_titles_from_index: list[str] = Field(..., description="If an index is detected, extract only the titles. If there is none, return an empty list")
  title_detected: bool  = Field(..., description="Whether a title is detected in the document. Ommit things like page headers or section titles. Look for it on the first page")
  title: str  = Field(..., description="Extract the document title. If there is none, return an empty string")
  page_header_detected: bool  = Field(..., description="Whether a page header is detected in any on the pages of the document. Ommit things like document title or section titles.")
  page_header: list[str]  = Field(..., description="Extract the candidates to be a page header. If there is none, return an empty list")
  page_footer_detected: bool  = Field(..., description="Whether a page footer is detected in any on the pages of the document")
  page_footer: list[str]  = Field(..., description="Extract the candidates to be a page footer, like page numbers.")

import json

def analyze_document(client,
                     document_url: str, 
                     path_doc_analysis: Path,
                    num_pages: int =3,
                    model: str = MODEL_OCR) -> Document:

    if path_doc_analysis.exists():
        logger.info("Document analysis exists. Reading it.")
        with open(path_doc_analysis, 'r') as f:
            dc_doc_analysis = json.load(f)
    else:
        logger.info("Document analysis does not exists. Calling Mistral OCR to create it")
        response_doc_annot = client.ocr.process(
            model=model,
            document=DocumentURLChunk(
            document_url=document_url
            ),
            document_annotation_format=response_format_from_pydantic_model(
                Document),
            pages=list(range(num_pages)),
            include_image_base64=True
        )

        dc_doc_analysis = json.loads(response_doc_annot.document_annotation)

        with open(path_doc_analysis, 'w') as f:
            json.dump(dc_doc_analysis, f, indent=4)


    return Document(**dc_doc_analysis)


def process_images(client, dc_images_b64, model: str = MODEL_OCR):

    res = {}
    for image_name, image_b64 in dc_images_b64.items():
        response_bbox_annot = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{image_b64}" 
            },

            include_image_base64=True
        )
        content = response_bbox_annot.pages[0].markdown
    
        res[image_name] = content

    return res