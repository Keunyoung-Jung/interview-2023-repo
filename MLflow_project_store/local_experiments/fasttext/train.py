# -*- coding: utf-8 -*-
from gensim.models import FastText
import pandas as pd
import mlflow
import boto3
import os
import argparse
from datetime import datetime
import logging

def download_latest_model(model_version):
    print(f'{str(datetime.now())}-[INFO] Downloading Latest Model')
    bin_file = f'model/fasttext_{model_version}.bin'
    syn1neg = f'model/fasttext_{model_version}.bin.syn1neg.npy'
    ngrams = f'model/fasttext_{model_version}.bin.wv.vectors_ngrams.npy'
    vocab = f'model/fasttext_{model_version}.bin.wv.vectors_vocab.npy'
    if not os.path.exists('model') :
            os.makedirs('model')
    if not os.path.exists('model/new') :
            os.makedirs('model/new')
    if os.path.exists(bin_file) \
        and os.path.exists(syn1neg) \
        and os.path.exists(ngrams) \
        and os.path.exists(vocab) :
        pass
    else :
        s3 = boto3.client('s3',
                    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                    region_name=os.environ['AWS_DEFAULT_REGION']
                    )
        prefix='mlflow/artifacts/6/bde89ae9ac0f459bbe9a6268e73f14de/artifacts'
        s3.download_file('mysterico-model-store',prefix+'/'+bin_file, bin_file)
        s3.download_file('mysterico-model-store',prefix+'/'+syn1neg, syn1neg)
        s3.download_file('mysterico-model-store',prefix+'/'+ngrams, ngrams)
        s3.download_file('mysterico-model-store',prefix+'/'+vocab, vocab)
            
def download_excel_data(excel_file):
    print(f'{str(datetime.now())}-[INFO] Downloading Excel Data')
    if not os.path.exists('data') :
        os.makedirs('data')
    s3 = boto3.client('s3',
                aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                region_name=os.environ['AWS_DEFAULT_REGION']
                )
    s3.download_file('mysterico-feature-store','fasttext_feature/'+excel_file, 'data/'+excel_file)

def train_model(model_path, excel_path, save_model_path): 
    model = load_model(model_path)
    document = data_loader(excel_path)
    print(f'{str(datetime.now())}-[INFO] Building vocabulary')
    model.build_vocab(document, update=True)
    print(f'{str(datetime.now())}-[INFO] Start Train Fasttext Model')
    model.train(document, total_examples=len(document), epochs=5)
    vocab_count,starbucks,macdonald,ham_soup = check_model(model)
    mlflow.log_metric("단어 수", vocab_count)
    mlflow.log_metric("스타벅스 유사도", starbucks)
    mlflow.log_metric("맥도날드 유사도", macdonald)
    mlflow.log_metric("부대찌개 유사도", ham_soup)
    print('save')
    save_model(model, save_model_path)
    mlflow.log_artifacts('model/new',artifact_path='model')

def load_model(model_path):
    print(f'{str(datetime.now())}-[INFO] Load Model ... ')
    return FastText.load(model_path)    

def data_loader(excel_path):
    print(f'{str(datetime.now())}-[INFO] Load Excel Data & Small Preprocess')
    excel = pd.read_excel(excel_path)
    document = []
    for doc in excel['text'].values.tolist() :
        if isinstance(doc, str):
            if len(doc) > 2:
                document.append(doc.split(' '))
    return document  

def check_model(model):
    vocab_count = len(model.wv.key_to_index)
    coffe_sentence = '나른한 봄날 오후, 졸음을 떨치고 기운을 북돋는 데는 커피만한 게 없다. 그러나 적당히 마실 것. 미국 식품의약국(FDA)는 카페인 섭취를 하루 400mg 이하로 제한할 것을 권한다. 한국 식품의약품안전처도 마찬가지. 즉 커피는 네 잔 이하로 마시는 게 좋다.그밖에 커피를 과하게 마시면 나타날 수 있는 증상, 미국 ‘에브리데이 헬스’가 정리했다.'
    mcd_sentence = '한국맥도날드가 이탈리아의 맛을 느낄 수 있는 ‘아라비아따 리코타 치킨 버거’를 한정 출시하고, 맥런치 라인업에 추가한다고 밝혔다.맥도날드 아라비아따 리코타 치킨 버거는 인기 메뉴인 맥스파이시 상하이 버거 패티에 이탈리아를 대표하는 아라비아따 소스와 리코타 치즈를 가미해 색다르고 이국적인 풍미를 느낄 수 있는 메뉴다.100% 닭가슴살 통살에 매콤한 토마토 베이스의 아라비아따 소스로 한국인이 사랑하는 매운맛을 추가했으며, 리코타 치즈는 부드러운 식감과 고소한 맛을 선사한다. 아라비아따 소스 특유의 중독성 있는 매콤함과 담백한 리코타 치즈의 상반된 매력이 조화롭게 어우러진 것이 특징이다. '
    budae_sentence = '레시지가 채널A의 밀리터리 서바이벌 예능 프로그램 강철부대2와 협업해 강철부대 밀키트(부대찌개 & 마라부대볶음) 2종을 출시했다고 14일 밝혔다. 강철부대 부대찌개는 다양한 소시지와 각종 야채 등 재료를 푸짐하게 담아낸 점이 큰 특징이다. 소시지를 비롯해 다양한 재료들의 조화를 이뤘다. 쫄면 사리까지 들어있어 여럿이 함께 즐길 수 있는 넉넉한 구성을 자랑한다. 강철부대 마라부대볶음은 쫄깃한 떡과 소시지에 얼얼한 비법 마라소스를 더해 화끈함 매운맛을 즐길 수 있다. 새롭게 출시된 강철부대 밀키트는 롯데마트를 시작으로 프레시지 자사몰을 비롯한 각종 온·오프라인 채널을 통해 판매된다. 박형기 프레시지 상품기획자는 프레시지만의 간편식 퍼블리싱 역량을 통해 앞으로도 소비자들에게 새로운 즐거움을 전달할 수 있는 다양한 제품들을 선보일 것 이라고 밝혔다.'
    starbucks = model.wv.similarity(coffe_sentence, '스타벅스')
    macdonald = model.wv.similarity(mcd_sentence, '맥도날드')
    ham_soup = model.wv.similarity(budae_sentence, '부대찌개')
    
    return vocab_count,starbucks,macdonald,ham_soup

def save_model(model, save_model_path):
    model.save(save_model_path)  
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--model-version",default='latest')
    parser.add_argument("--excel-file",default='latest.xlsx')
    args = parser.parse_args()
    # download_base_model()

    model_path = f'model/fasttext_{args.model_version}.bin'
    save_model_path = f'model/new/fasttext_{args.model_version}.bin'
    excel_path = args.excel_file
    
    download_excel_data(excel_path)
    download_latest_model(args.model_version)
    with mlflow.start_run():
        mlflow.log_param('model_version',args.model_version)
        mlflow.log_param('excel_file',args.excel_file)
        train_model(model_path, 'data/'+excel_path, save_model_path)