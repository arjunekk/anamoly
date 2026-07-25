"""
DataLoader factory for training data.

Wraps MVTecGoodImageDataset in a PyTorch DataLoader so images are
delivered in batches, shuffled, and ready for feature extraction (Phase 5).
Kept separate from dataset_loader.py so batching/loading configuration
can change independently of how individual images are read and transformed.
"""

from pathlib import Path
from torch.utils.data import DataLoader

from app.preprocessing.dataset_loader import MVTecGoodImageDataset


def get_train_dataloader(category_root: Path, batch_size: int = 16, shuffle: bool = True):
    """
    Args:
        category_root: path to a category folder, e.g. dataset/mvtec_ad/bottle
        batch_size: number of images per batch
        shuffle: whether to shuffle image order each epoch

    Returns:
        A DataLoader yielding batches of shape [batch_size, 3, 224, 224]
    """
    dataset = MVTecGoodImageDataset(category_root)

    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=0,  # kept at 0 for now to avoid platform-specific multiprocessing issues
    )