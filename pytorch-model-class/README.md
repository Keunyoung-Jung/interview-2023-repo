# pytorch-model-class
pytorch 프레임워크 기반으로 작성된 딥러닝 모델의 class 저장소 입니다.    
파이프라인, 훈련 등을 위해 모델의 클래스를 미리 저장해두고 버젼을 관리합니다.    
여기서 `베이스 모델`은 이미 연구된 모델의 이름을 나타냅니다.    
`베이스 모델`의 이름은 [SOTA Link](https://paperswithcode.com/area/natural-language-processing)에서 등재된 이름을 사용합니다.

# Information
하나의 모델이 가질 수 있는 구성요소는 다음과 같습니다.
* 모델이 훈련 가능한 환경의 `Dockerfile`
* 모델의 구조가 작성된 `python script`
* 모델을 학습 시킬 수 있는 쿠버네티스 Yaml 파일 `pytorchJob`

# Convention
## 디렉토리 구조
모델의 Class를 작성할때는 다음 규칙을 따릅니다.    
     
📁 `프로젝트명 directory`    
├─📃 `베이스모델이름.py`    
├─📃 `베이스모델이름2.py`    
├─📃 `main.py`    
├─🐳 `Dockerfile`    
└─⚙️ `pytorchJob.yaml`

## 모델 스크립트 작성
* 모델 스크립트의 이름은 소문자로 작성합니다. (ex. `rnn.py`)
### 모델 Class 작성
* 클래스의 이름은 `BaseModel`으로(대문자 시작) 작성합니다.
* init에 모델이름을 같이 넣어 식별작업 필요시 사용합니다.
```python
class BaseModel(nn.Module) :
    def __init__(self, **args, **kwargs):
        self.name = 'RNN'
        (...)
```
     
### 모델 훈련,검증함수 작성
* 모델 클래스 안에는 모델과 관련된 함수를 모두 포함시킵니다.
* `train_model()`, `evaluate_model()`, `predict()` 세가지는 반드시 구현되어야 합니다.
```python
class BaseModel(nn.Module) :
    (...)
    def forward(self, x):
        (...)

    def train_model(self, device, optimizer, train_iter, epoch):
        (...)

    def evaluate_model(self, device, val_iter, epoch):
        (...)
        return avg_loss, avg_accuracy

    def predict(self,text):
        (...)
        return output
```

## `main.py` 스크립트 작성
* 훈련 Job을 위해서 하이퍼 파라미터는 argparse를 사용하여 받도록 작성합니다.
* `main()` 함수를 `main.py`에 작성합니다.
* 해당 스크립트는 훈련 및 검증을 위한 동작에서 사용됩니다.
```python
def main():
    # Training settings
    parser = argparse.ArgumentParser(description="PyTorch MNIST Example")
    parser.add_argument("--batch-size", type=int, default=64, metavar="N",
                        help="input batch size for training (default: 64)")
    parser.add_argument("--test-batch-size", type=int, default=1000, metavar="N",
                        help="input batch size for testing (default: 1000)")
    parser.add_argument("--epochs", type=int, default=10, metavar="N",
                        help="number of epochs to train (default: 10)")
    parser.add_argument("--lr", type=float, default=0.01, metavar="LR",
                        help="learning rate (default: 0.01)")
    parser.add_argument("--momentum", type=float, default=0.5, metavar="M",
                        help="SGD momentum (default: 0.5)")
    parser.add_argument("--no-cuda", action="store_true", default=False,
                        help="disables CUDA training")
    parser.add_argument("--seed", type=int, default=1, metavar="S",
                        help="random seed (default: 1)")
    parser.add_argument("--log-interval", type=int, default=10, metavar="N",
                        help="how many batches to wait before logging training status")
    parser.add_argument("--log-path", type=str, default="",
                        help="Path to save logs. Print to StdOut if log-path is not set")
    parser.add_argument("--save-model", action="store_true", default=False,
                        help="For Saving the current Model")

    if dist.is_available():
        parser.add_argument("--backend", type=str, help="Distributed backend",
                            choices=[dist.Backend.GLOO, dist.Backend.NCCL, dist.Backend.MPI],
                            default=dist.Backend.GLOO)
    args = parser.parse_args()
```