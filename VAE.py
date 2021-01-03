# -*- coding: utf-8 -*-
"""VAE-MNIST.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17p9G32eagRuP1cIGWCnHE6ZBxL1UEEks
"""

# prerequisites
import torch
import torch.nn.functional as F
import torch.nn as nn
from torch.autograd import Variable
from torchvision.utils import save_image
import torch.optim as optim
from torchvision import datasets, transforms


bs = 100
# MNIST Dataset
train_dataset = datasets.MNIST(root='./mnist_data/', train=True, transform=transforms.ToTensor(), download=True)
test_dataset = datasets.MNIST(root='./mnist_data/', train=False, transform=transforms.ToTensor(), download=False)
train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=bs, shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=bs, shuffle=False)

class VAE(nn.Module):
    def __init__(self, dimension_x, dimension_1, dimension_2, latent_space_dimenion):
        super(VAE, self).__init__()
        
        # encoder
        self.fc1 = nn.Linear(dimension_x, dimension_1)
        self.fc2 = nn.Linear(dimension_1, dimension_2)
        self.fc31 = nn.Linear(dimension_2, latent_space_dimenion)
        self.fc32 = nn.Linear(dimension_2, latent_space_dimenion)
        
        # decoder
        self.fc4 = nn.Linear(latent_space_dimenion, dimension_2)
        self.fc5 = nn.Linear(dimension_2, dimension_1)
        self.fc6 = nn.Linear(dimension_1, dimension_x)
        
    def encoder(self, x):
        h = F.relu(self.fc1(x))
        h = F.relu(self.fc2(h))
        # mu, log_var
        return self.fc31(h), self.fc32(h) 
        
    def decoder(self, z):
        h = F.relu(self.fc4(z))
        h = F.relu(self.fc5(h))
        return F.sigmoid(self.fc6(h)) 
    
    def forward(self, x):
        mu, log_variable = self.encoder(x.view(-1, 784))
        z = self.sampling(mu, log_variable)
        return self.decoder(z), mu, log_variable
    
    def sampling(self, mu, log_variable):
        standard_dev = torch.exp(0.5*log_variable)
        eps = torch.randn_like(standard_dev)
        return eps.mul(standard_dev).add_(mu) # return z sample

# build model
vae = VAE(dimension_x=784, dimension_1= 512, dimension_2=256, latent_space_dimenion=2)
if torch.cuda.is_available():
    vae.cuda()

optimizer = optim.Adam(vae.parameters())
# return reconstruction error + KL divergence losses
def loss_function(recon_x, x, mu, log_variable):
    BCE = F.binary_cross_entropy(recon_x, x.view(-1, 784), reduction='sum')
    KLD = -0.5 * torch.sum(1 + log_variable - mu.pow(2) - log_variable.exp())
    return BCE + KLD

def train(epoch):
    vae.train()
    train_loss = 0
    for batch_idx, (data, _) in enumerate(train_loader):
        data = data.cuda()
        optimizer.zero_grad()
        
        recon_batch, mu, log_variable = vae(data)
        loss = loss_function(recon_batch, data, mu, log_variable)
        
        loss.backward()
        train_loss += loss.item()
        optimizer.step()
        
        if batch_idx % 100 == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item() / len(data)))
    print('====> Epoch: {} Average loss: {:.4f}'.format(epoch, train_loss / len(train_loader.dataset)))

def test():
    vae.eval()
    test_loss= 0
    with torch.no_grad():
        for data, _ in test_loader:
            data = data.cuda()
            recon, mu, log_var = vae(data)
            
            # sum up batch loss
            test_loss += loss_function(recon, data, mu, log_var).item()
        
    test_loss /= len(test_loader.dataset)
    print('====> Test set loss: {:.4f}'.format(test_loss))

for epoch in range(1, 51):
    train(epoch)
    test()

with torch.no_grad():
    z = torch.randn(64, 2).cuda()
    sample = vae.decoder(z).cuda()
    
    save_image(sample.view(64, 1, 28, 28), './Vae_output' + '.png')

