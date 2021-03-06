# -*- coding: utf-8 -*-
"""Ques_3_Assignment_3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1v5ap4DfJnk5YA0L2USWcpvLoueZWPOo0

### Implement GAN using Frey Face Dataset
"""

# Commented out IPython magic to ensure Python compatibility.
import torch.nn as nn
import torch.nn.functional as F
import torch

from torch.utils.data import DataLoader
from torch.autograd import Variable


import torchvision.transforms as transforms
from torchvision.utils import save_image

import os
import numpy as np
import math
import scipy.io

import matplotlib
import matplotlib.pyplot as plt
# %matplotlib inline

"""##### Loading Frey Face dataset"""

# Loading Frey Face dataset
from google.colab import drive
drive.mount('/content/drive')

dataset = scipy.io.loadmat('/content/drive/MyDrive/ML-2_Assignments/Assignment-3/Ques_3/frey_rawface.mat')
data = dataset['ff'].T.reshape(-1, 1, 28, 20)
data = data.astype('float32') / 255.0
data_set = torch.tensor(data, dtype=torch.float)
print(f"Number of Images: {len(data)}")

##DataLoader
batch_size = 256
data_loader = DataLoader(data_set, batch_size=batch_size)

#Finding the Image Shape
for d in data_set:
  img_shape = d.shape
  print(f'The image shape is : {img_shape}')
  break

##Visualizing the images
def show_image(dl):
  img = dl[5]
  plt.imshow(np.squeeze(img))
  plt.show()

show_image(data_set)

"""##### Building GAN"""

##Generator Class
image_shape = (1,28,20)
latent_dim = 100

class GAN_Generator(nn.Module):
    def __init__(self):
        super(GAN_Generator, self).__init__()

        def block(feat_in, feat_out, normalize=True):
            layers = [nn.Linear(feat_in, feat_out)]
            if normalize:
                layers.append(nn.BatchNorm1d(feat_out, 0.8))
            layers.append(nn.LeakyReLU(0.2, inplace=True))
            return layers

        self.model = nn.Sequential(
            *block(latent_dim, 128, normalize=False),
            *block(128, 256),
            *block(256, 512),
            *block(512, 1024),
            nn.Linear(1024, int(np.prod(image_shape))),
            nn.Tanh()
        )

    def forward(self, z):
        img = self.model(z)
        img = img.view(img.size(0), *image_shape)
        return img

#GAN Discriminator CLass
class GAN_Discriminator(nn.Module):
    def __init__(self):
        super(GAN_Discriminator, self).__init__()

        self.model = nn.Sequential(
            nn.Linear(int(np.prod(image_shape)), 512),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(256, 128),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(128, 1),
            nn.Sigmoid(),
        )

    def forward(self, img):
        img_flat = img.view(img.size(0), -1)
        validity = self.model(img_flat)

        return validity

# Defining the Loss function
loss = torch.nn.BCELoss()

# Initializing generator and discriminator
generator = GAN_Generator()
discriminator = GAN_Discriminator()

cuda = True if torch.cuda.is_available() else False

if cuda:
    generator.cuda()
    discriminator.cuda()
    loss.cuda()

lr = 0.0002
b1 = 0.02
b2 = 0.999
optimizer_G = torch.optim.Adam(generator.parameters(), lr=lr,betas = (b1,b2) )
optimizer_D = torch.optim.Adam(discriminator.parameters(), lr=lr,betas = (b1,b2))

Tensor = torch.cuda.FloatTensor if cuda else torch.FloatTensor

# Commented out IPython magic to ensure Python compatibility.
epochs = 100
sample_interval = 400
for epoch in range(epochs):
    for i, imgs in enumerate(data_loader):

        # Adversarial ground truths
        valid = Variable(Tensor(imgs.size(0), 1).fill_(1.0), requires_grad=False)
        fake = Variable(Tensor(imgs.size(0), 1).fill_(0.0), requires_grad=False)

        # Configure input
        real_imgs = Variable(imgs.type(Tensor))

        #De-accumulate the gradient
        optimizer_G.zero_grad()

        z = Variable(Tensor(np.random.normal(0, 1, (imgs.shape[0], latent_dim))))

        # Generate a batch of images
        gen_imgs = generator(z)
        gen_loss = loss(discriminator(gen_imgs), valid)

        gen_loss.backward()
        optimizer_G.step()

        #De-accumulate the gradient

        optimizer_D.zero_grad()

        
        real_loss = loss(discriminator(real_imgs), valid)
        fake_loss = loss(discriminator(gen_imgs.detach()), fake)
        d_loss = (real_loss + fake_loss) / 2

        d_loss.backward()
        optimizer_D.step()

        batches_done = epoch * len(data_loader) + i
        if batches_done % sample_interval == 0:
          print(
            "[Epoch %d/%d] [Batch %d/%d] [D loss: %f] [G loss: %f]"
#             % (epoch, epochs, i, len(data_loader), d_loss.item(), gen_loss.item()))
          show_image(imgs)
          show_image(gen_imgs.detach().numpy())
print(
      "[Epoch %d/%d] [Batch %d/%d] [D loss: %f] [G loss: %f]"
#       % (epoch, epochs, i, len(data_loader), d_loss.item(), gen_loss.item()))
show_image(imgs)
show_image(gen_imgs.detach().numpy())

torch.save(generator,'/content/drive/MyDrive/ML-2_Assignments/Assignment-3/generator.pth')

torch.save(discriminator,'/content/drive/MyDrive/ML-2_Assignments/Assignment-3/discriminator.pth')

