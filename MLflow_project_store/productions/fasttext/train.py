# -*- coding: utf-8 -*-
import mlflow
import boto3
import os
import argparse
from datetime import datetime
import logging
from fasttext_model import FastTextMLFModel
import requests

def get_latest_run_id(experiment_id):
    response = requests.post(
        "http://k8s.mysterico.com:31516/mlflow/ajax-api/2.0/preview/mlflow/runs/search",
        json={ "experiment_ids": [experiment_id], "max_results": 26 }
        ).json()
    last_run = [runs for runs in response['runs'] if runs['info']['status'] == "FINISHED"][0]
    artifact_uri = last_run['info']['artifact_uri']
    model_prefix = artifact_uri.split("mysterico-model-store/")[1]+"/model"
    params_list = last_run['data']['params']
    model_version = [params['value'] for params in params_list if params['key'] == 'model_version'][0]
    return model_prefix,model_version

def download_latest_model(model_version,model_prefix,pre_model_version):
    print(f'{str(datetime.now())}-[INFO] Downloading Latest Model')
    pre_bin_file = f'/model/fasttext_{pre_model_version}.bin'
    pre_syn1neg = f'/model/fasttext_{pre_model_version}.bin.syn1neg.npy'
    pre_ngrams = f'/model/fasttext_{pre_model_version}.bin.wv.vectors_ngrams.npy'
    pre_vocab = f'/model/fasttext_{pre_model_version}.bin.wv.vectors_vocab.npy'
    
    bin_file = f'/model/fasttext_{model_version}.bin'
    syn1neg = f'/model/fasttext_{model_version}.bin.syn1neg.npy'
    ngrams = f'/model/fasttext_{model_version}.bin.wv.vectors_ngrams.npy'
    vocab = f'/model/fasttext_{model_version}.bin.wv.vectors_vocab.npy'
    if os.path.exists(bin_file) :
        os.remove(bin_file)
    if os.path.exists(syn1neg) :
        os.remove(syn1neg)
    if os.path.exists(ngrams) :
        os.remove(ngrams)
    if os.path.exists(vocab) :
        os.remove(vocab)
    if not os.path.exists('/model') :
            os.makedirs('/model')
    if not os.path.exists('/model/new') :
            os.makedirs('/model/new')
    s3 = boto3.client('s3',
                aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                region_name=os.environ['AWS_DEFAULT_REGION']
                )
    
    print(model_prefix+pre_bin_file)
    s3.download_file('mysterico-model-store',model_prefix+pre_bin_file, bin_file)
    s3.download_file('mysterico-model-store',model_prefix+pre_syn1neg, syn1neg)
    s3.download_file('mysterico-model-store',model_prefix+pre_ngrams, ngrams)
    s3.download_file('mysterico-model-store',model_prefix+pre_vocab, vocab)
            
def download_excel_data(excel_file):
    print(f'{str(datetime.now())}-[INFO] Downloading Excel Data')
    if not os.path.exists('/data') :
        os.makedirs('/data')
    s3 = boto3.client('s3',
                aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                region_name=os.environ['AWS_DEFAULT_REGION']
                )
    s3.download_file('mysterico-feature-store','fasttext_feature/'+excel_file, '/data/'+excel_file)
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--model-version",default='latest')
    parser.add_argument("--excel-file",default='latest.xlsx')
    args = parser.parse_args()
    # download_base_model()

    model_path = f'/model/fasttext_{args.model_version}.bin'
    save_model_path = f'/model/new/fasttext_{args.model_version}.bin'
    excel_path = args.excel_file
    
    model_prefix,pre_model_version = get_latest_run_id(experiment_id=6)
    download_excel_data(excel_path)
    download_latest_model(args.model_version,model_prefix,pre_model_version)
    with mlflow.start_run():
        mlflow.log_param('model_version',args.model_version)
        mlflow.log_param('excel_file',args.excel_file)
        fasttext = FastTextMLFModel(model_path,'/data/'+excel_path,save_model_path)
        fasttext.train()
        metrics = fasttext.evaluate()
        mlflow.log_metrics(metrics)
        fasttext.clear_context()
        mlflow.pyfunc.log_model(artifact_path="model",python_model=fasttext)
        mlflow.log_artifacts('/model/new',artifact_path='model/model')