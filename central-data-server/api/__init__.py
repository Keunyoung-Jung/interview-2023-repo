from fastapi import APIRouter, HTTPException
from typing import List, Optional, Type
from fastapi.responses import StreamingResponse
from urllib.parse import quote
from datetime import date

from central import control
from central import dto

from central.api.dictionary import clickhouse
from central.api.dictionary import tokenizer
from central.api.dictionary import word_dict
from central.api.model import category_model
from central.api.model import sentiment_model
from central.api.model import doc_type_model
from central.api.model import subject_model
from central.api.model import spam_model
from central.api.analyzer import niz_sample_data
from central.api.analyzer import power_score
from central.api.analyzer import document_recommender
from central.api.analyzer import text_to_tensor
from central.api.download import storage

# Model Route
model_router = APIRouter(tags=['Model Server'], prefix= '/model-server')
model_router.include_router(category_model.router, prefix= '/category-model')
model_router.include_router(sentiment_model.router, prefix= '/sentiment-model')
model_router.include_router(doc_type_model.router, prefix= '/doc-type-model')
model_router.include_router(subject_model.router, prefix= '/subject-model')
model_router.include_router(spam_model.router, prefix= '/spam-model')

# Analyzer Route
analyzer_router = APIRouter(tags=['Analyzer'], prefix= '/analyzer')
analyzer_router.include_router(niz_sample_data.router, prefix= '/niz_sample_data')
analyzer_router.include_router(text_to_tensor.router, prefix= '/text-to-tensor')
analyzer_router.include_router(power_score.router, prefix= '/power-score')
analyzer_router.include_router(document_recommender.router, prefix= '/document-recommender')

# Download Route
download_router = APIRouter(tags=["Download"], prefix= '/download')
download_router.include_router(storage.router, prefix= '/storage')

# Dictionary Route
dictionary_router = APIRouter(tags=['Dictionary'], prefix= '/dictionary')
dictionary_router.include_router(clickhouse.router, prefix='/clickhouse')
dictionary_router.include_router(tokenizer.router, prefix='/tokenizer')
dictionary_router.include_router(word_dict.router, prefix='/word_dict')