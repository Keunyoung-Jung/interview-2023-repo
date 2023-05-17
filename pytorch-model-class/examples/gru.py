import torch
import torch.nn as nn
import torch.nn.functional as F

class BaseModel(nn.Module):
    def __init__(self, n_layers, hidden_dim, n_vocab, embed_dim, n_classes, dropout_p=0.2):
        super(BaseModel, self).__init__()
        self.n_layers = n_layers
        self.hidden_dim = hidden_dim

        self.embed = nn.Embedding(n_vocab, embed_dim)
        self.dropout = nn.Dropout(dropout_p)
        self.gru = nn.GRU(embed_dim, self.hidden_dim,
                            num_layers=self.n_layers,
                            batch_first=True)
        self.out = nn.Linear(self.hidden_dim, n_classes)
        
        self.name = 'GRU'
        self.tokenizer = None
        USE_CUDA = torch.cuda.is_available()
        self.device = torch.device("cuda" if USE_CUDA else "cpu")
        self.to(self.device)
        print("The next device among cpu and cuda:", self.device)

    def forward(self, x):
        x = self.embed(x)
        h_0 = self._init_state(batch_size=x.size(0)) # Initialize the first hidden state to 0 vector
        x, _ = self.gru(x, h_0)  # The return value of GRU is (batch size, sequence length, hidden state size)
        h_t = x[:,-1,:] # Resized to a tensor of (batch size, hidden size). That is, only the hidden state of the last time-step is retrieved.
        self.dropout(h_t)
        logit = self.out(h_t)  # (batch size, size of hidden state) -> (batch size, size of output layer)
        return logit

    def _init_state(self, batch_size=1):
        weight = next(self.parameters()).data
        return weight.new(self.n_layers, batch_size, self.hidden_dim).zero_()

    def train_model(self, optimizer, train_iter):
        self.train()
        for b, batch in enumerate(train_iter):
            x, y = batch.text.to(self.device), batch.label.to(self.device)
            optimizer.zero_grad()

            logit = self(x)
            loss = F.cross_entropy(logit, y)
            loss.backward()
            optimizer.step()

    def evaluate_model(self, val_iter):
        """evaluate model"""
        self.eval()
        corrects, total_loss = 0, 0
        for batch in val_iter:
            x, y = batch.text.to(self.device), batch.label.to(self.device)
            logit = self(x)
            loss = F.cross_entropy(logit, y, reduction='sum')
            total_loss += loss.item()
            corrects += (logit.max(1)[1].view(y.size()).data == y.data).sum()
        size = len(val_iter.dataset)
        avg_loss = total_loss / size
        avg_accuracy = 100.0 * corrects / size
        return avg_loss, avg_accuracy

    def set_tokenizer(self,tokenizer):
        self.tokenizer = tokenizer

    def create_tensor(self,text):
        tokenized = self.tokenizer.preprocess(text)
        indexed = [[self.tokenizer.vocab.stoi[t] for t in tokenized]]
        print(indexed)
        tensor = torch.LongTensor(indexed).to(self.device)
        print(tensor)
        return tensor
    def predict(self,text):
        self.eval()
        output = torch.sigmoid(self(self.create_tensor(text)))
        return output