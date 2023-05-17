import torch
import torch.nn as nn
import torch.nn.functional as F
import base64
import logging

class BaseModel(nn.Module):
    def __init__(self):
        super(BaseModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 20, 5, 1)
        self.conv2 = nn.Conv2d(20, 50, 5, 1)
        self.fc1 = nn.Linear(4*4*50, 500)
        self.fc2 = nn.Linear(500, 10)
        
        self.name = 'CNN'
        USE_CUDA = torch.cuda.is_available()
        self.device = torch.device("cuda" if USE_CUDA else "cpu")
        self.to(self.device)
        print("The next device among cpu and cuda:", self.device)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 4*4*50)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


    def train_model(self, args, train_loader, optimizer, epoch):
        self.train()
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(self.device), target.to(self.device)
            optimizer.zero_grad()
            output = self(data)
            loss = F.nll_loss(output, target)
            loss.backward()
            optimizer.step()
            if batch_idx % args.log_interval == 0:
                msg = "Train Epoch: {} [{}/{} ({:.0f}%)]\tloss={:.4f}".format(
                    epoch, batch_idx * len(data), len(train_loader.dataset),
                    100. * batch_idx / len(train_loader), loss.item())
                logging.info(msg)
                niter = epoch * len(train_loader) + batch_idx


    def evaluate_model(self, args, test_loader, epoch):
        self.eval()
        test_loss = 0
        correct = 0
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = self(data)
                test_loss += F.nll_loss(output, target, reduction="sum").item()  # sum up batch loss
                pred = output.max(1, keepdim=True)[1]  # get the index of the max log-probability
                correct += pred.eq(target.view_as(pred)).sum().item()

        test_loss /= len(test_loader.dataset)
        logging.info("{{metricName: accuracy, metricValue: {:.4f}}};{{metricName: loss, metricValue: {:.4f}}}\n".format(
            float(correct) / len(test_loader.dataset), test_loss))
    
    def predict(self,x) :
        input_image = base64.b64decode(x['image'])
        input_tensor = torch.LongTensor(input_image).to(self.device)
        output = self(input_tensor)
        return output
    
    def set_device(self,device) :
        self.device = device