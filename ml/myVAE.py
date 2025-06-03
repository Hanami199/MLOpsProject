import torch
import numpy as np
import torch.nn.functional as F
from torch import nn
from torch import Tensor
from einops import rearrange, repeat
from einops.layers.torch import Rearrange



class VAE(nn.Module):
    def __init__(self,  in_dim, latent_dim):
        super().__init__()
        self.in_dim = in_dim
        self.latent_dim = latent_dim

        self.encoder = nn.Sequential(
            nn.Linear(in_dim, in_dim//2),
            nn.ReLU(),
            nn.Linear(in_dim//2, in_dim//4),
            nn.ReLU(),
            nn.Linear(in_dim//4, 2*latent_dim)
        )

        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, in_dim//4),
            nn.ReLU(),
            nn.Linear(in_dim//4, in_dim//2),
            nn.ReLU(),
            nn.Linear(in_dim//2, in_dim),
        )


    def encode(self, x):
        z       = self.encoder(x)
        mu      = z[:, self.latent_dim:]
        log_var = z[:, :self.latent_dim]
        return mu, log_var
        
    
    def decode(self, z):
        return self.decoder(z)


    def forward(self, x: torch.tensor):
        x = x.view(-1, self.in_dim)
        mu, log_var = self.encode(x)
        z = self.reparametrize(mu, log_var)
        return self.decode(z), mu, log_var
    

    def reparametrize(self, mu, log_var):
        std = torch.exp(0.5*log_var)
        eps = torch.randn_like(std)
        return mu + std*eps

    
    def loss(self, x_hat, mu, log_var, x):
        x = x.view(-1, self.in_dim)
        rec = F.mse_loss(x_hat, x, reduction = 'none')                  # in reality it returns the (-1)*cross entropy
        rec = torch.sum(rec, dim = -1)

        KL = -0.5 * (1 + log_var - mu.pow(2) - log_var.exp())           # KL between two Normal has a close form
        KL = torch.sum(KL, dim = -1)

        res = rec + KL
        return res.mean()
    

    @torch.no_grad
    def generate(self, n: int):
        z = torch.randn(n, self.latent_dim)
        return self.decode(z)
    
    
    @torch.no_grad
    def reconstruct(self, x):
        z, mu, log_var = self(x)
        return z