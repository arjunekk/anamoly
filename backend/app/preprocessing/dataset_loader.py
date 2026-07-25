"""
PyTorch Dataset for loading MVTec AD training images.

Only loads from train/good/, since PatchCore trains exclusively on
defect-free samples. There are no labels here because this dataset
is only used to build the anomaly detector's reference feature bank,
not to train a classifier.
"""

from pathlib import Path
from PIL import Image
from torch.utils.data import Dataset

from app.preprocessing.transforms import get_transform


class MVTecGoodImageDataset(Dataset):
    """Loads only defect-free ('good') training images for one category."""

    def __init__(self, category_root: Path, transform=None):
        """
        Args:
            category_root: path to a category folder, e.g. dataset/mvtec_ad/bottle
            transform: optional transform pipeline; defaults to get_transform()
        """
        self.good_dir = Path(category_root) / "train" / "good"

        if not self.good_dir.exists():
            raise FileNotFoundError(
                f"Expected training folder not found: {self.good_dir}"
            )

        valid_extensions = {".png", ".jpg", ".jpeg"}
        self.image_paths = sorted(
            f for f in self.good_dir.iterdir()
            if f.suffix.lower() in valid_extensions
        )

        if len(self.image_paths) == 0:
            raise ValueError(f"No images found in {self.good_dir}")

        self.transform = transform or get_transform()

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        image = Image.open(image_path).convert("RGB")
        image_tensor = self.transform(image)
        return image_tensor