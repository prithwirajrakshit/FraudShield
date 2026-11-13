import torch
import torch.nn as nn
import torch.nn.functional as F

class BinaryFocalLoss(nn.Module):
    """
    Binary Focal Loss for severe class imbalance mitigation.
    Formula:
        FL(p_t) = -alpha_t * (1 - p_t)^gamma * log(p_t)
    
    Parameters:
    ----------
    alpha : float, default=0.25
        Balancing factor for the minority class (fraud).
    gamma : float, default=2.0
        Focusing parameter that modulates the loss for easy vs hard examples.
    """
    def __init__(self, alpha: float = 0.25, gamma: float = 2.0):
        super(BinaryFocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        bce = F.binary_cross_entropy_with_logits(logits, targets, reduction='none')
        p_t = torch.exp(-bce)
        alpha_t = targets * self.alpha + (1.0 - targets) * (1.0 - self.alpha)
        focal_weight = alpha_t * torch.pow(1.0 - p_t, self.gamma)
        loss = focal_weight * bce
        return loss.mean()

