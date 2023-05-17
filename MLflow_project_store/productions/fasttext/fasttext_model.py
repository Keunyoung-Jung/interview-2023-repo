import mlflow.pyfunc
from gensim.models import FastText
import pandas as pd
from datetime import datetime
 
class FastTextMLFModel(mlflow.pyfunc.PythonModel):
    def __init__(self, model_path,excel_path,save_model_path):
        self.model_path = model_path
        self.excel_path = excel_path
        self.save_model_path = save_model_path
        
    def load_context(self, context):
        print(f'{str(datetime.now())}-[INFO] Load Model ... ')
        self.model = FastText.load(model_path)
        
    def clear_context(self):
        self.model = None
    
    def data_loader(self,excel_path):
        print(f'{str(datetime.now())}-[INFO] Load Excel Data & Small Preprocess')
        excel = pd.read_excel(excel_path)
        document = []
        for doc in excel['text'].values.tolist() :
            if isinstance(doc, str):
                if len(doc) > 2:
                    document.append(doc.split(' '))
        return document
    
    def train(self):
        print(f'{str(datetime.now())}-[INFO] Load Model ... ')
        self.model = FastText.load(self.model_path)
        self.document = self.data_loader(self.excel_path)
        print(f'{str(datetime.now())}-[INFO] Building vocabulary')
        self.model.build_vocab(self.document, update=True)
        print(f'{str(datetime.now())}-[INFO] Start Train Fasttext Model')
        self.model.train(self.document, total_examples=len(self.document), epochs=self.model.epochs)
        self.model.save(self.save_model_path)
        
    def evaluate(self):
        vocab_count = len(self.model.wv.key_to_index)
        coffe_sentence = '나른한 봄날 오후, 졸음을 떨치고 기운을 북돋는 데는 커피만한 게 없다. 그러나 적당히 마실 것. 미국 식품의약국(FDA)는 카페인 섭취를 하루 400mg 이하로 제한할 것을 권한다. 한국 식품의약품안전처도 마찬가지. 즉 커피는 네 잔 이하로 마시는 게 좋다.그밖에 커피를 과하게 마시면 나타날 수 있는 증상, 미국 ‘에브리데이 헬스’가 정리했다.'
        mcd_sentence = '한국맥도날드가 이탈리아의 맛을 느낄 수 있는 ‘아라비아따 리코타 치킨 버거’를 한정 출시하고, 맥런치 라인업에 추가한다고 밝혔다.맥도날드 아라비아따 리코타 치킨 버거는 인기 메뉴인 맥스파이시 상하이 버거 패티에 이탈리아를 대표하는 아라비아따 소스와 리코타 치즈를 가미해 색다르고 이국적인 풍미를 느낄 수 있는 메뉴다.100% 닭가슴살 통살에 매콤한 토마토 베이스의 아라비아따 소스로 한국인이 사랑하는 매운맛을 추가했으며, 리코타 치즈는 부드러운 식감과 고소한 맛을 선사한다. 아라비아따 소스 특유의 중독성 있는 매콤함과 담백한 리코타 치즈의 상반된 매력이 조화롭게 어우러진 것이 특징이다. '
        budae_sentence = '레시지가 채널A의 밀리터리 서바이벌 예능 프로그램 강철부대2와 협업해 강철부대 밀키트(부대찌개 & 마라부대볶음) 2종을 출시했다고 14일 밝혔다. 강철부대 부대찌개는 다양한 소시지와 각종 야채 등 재료를 푸짐하게 담아낸 점이 큰 특징이다. 소시지를 비롯해 다양한 재료들의 조화를 이뤘다. 쫄면 사리까지 들어있어 여럿이 함께 즐길 수 있는 넉넉한 구성을 자랑한다. 강철부대 마라부대볶음은 쫄깃한 떡과 소시지에 얼얼한 비법 마라소스를 더해 화끈함 매운맛을 즐길 수 있다. 새롭게 출시된 강철부대 밀키트는 롯데마트를 시작으로 프레시지 자사몰을 비롯한 각종 온·오프라인 채널을 통해 판매된다. 박형기 프레시지 상품기획자는 프레시지만의 간편식 퍼블리싱 역량을 통해 앞으로도 소비자들에게 새로운 즐거움을 전달할 수 있는 다양한 제품들을 선보일 것 이라고 밝혔다.'
        starbucks = self.model.wv.similarity(coffe_sentence, '스타벅스')
        macdonald = self.model.wv.similarity(mcd_sentence, '맥도날드')
        ham_soup = self.model.wv.similarity(budae_sentence, '부대찌개')
        
        return {
                "단어 수":vocab_count,
                "스타벅스 유사도":starbucks,
                "맥도날드 유사도":macdonald,
                "부대찌개 유사도":ham_soup
            }