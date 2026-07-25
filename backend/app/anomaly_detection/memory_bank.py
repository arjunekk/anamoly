"""
Builds and stores PatchCore's memory bank: the collection of patch feature
vectors representing "normal" appearance, gathered from training images.

Uses random subsampling to shrink the memory bank to a manageable size.
NOTE: The original PatchCore paper uses greedy coreset (k-center) subsampling,
which better preserves coverage of rare-but-normal patch types. Random
subsampling is used here as a simpler, faster alternative appropriate for
a single-developer project; it is a reasonable approximation, not an exact
reproduction of the paper.
"""

import torch


class MemoryBank:
    """Stores and queries a subsampled bank of normal patch feature vectors."""

    def __init__(self, subsample_ratio: float = 0.1):
        """
        Args:
            subsample_ratio: fraction of total patch vectors to keep,
                e.g. 0.1 keeps 10% of all collected patches.
        """
        self.subsample_ratio = subsample_ratio
        self.bank: torch.Tensor | None = None  # shape: [N, 1536]

    def build(self, all_patch_features: torch.Tensor):
        """
        Args:
            all_patch_features: shape [total_patches, 1536], collected
                across every training image.
        """
        num_total = all_patch_features.shape[0]
        num_keep = max(1, int(num_total * self.subsample_ratio))

        # Random subsampling: pick a representative subset without
        # replacement. Simpler than greedy coreset selection, at some
        # cost to how evenly the subset covers rare feature patterns.
        indices = torch.randperm(num_total)[:num_keep]
        self.bank = all_patch_features[indices]

        print(f"Memory bank built: {num_keep} / {num_total} patch vectors retained")

    def query(self, query_patches: torch.Tensor) -> torch.Tensor:
        """
        For each query patch vector, find the distance to its nearest
        neighbor in the memory bank.

        Args:
            query_patches: shape [num_patches, 1536]

        Returns:
            Distances of shape [num_patches] — one nearest-neighbor
            distance per query patch.
        """
        if self.bank is None:
            raise RuntimeError("Memory bank has not been built yet. Call build() first.")

        # Pairwise Euclidean distance: [num_patches, bank_size]
        distances = torch.cdist(query_patches, self.bank, p=2)

        # Nearest neighbor distance per query patch.
        min_distances, _ = distances.min(dim=1)

        return min_distances

    def save(self, path: str):
        """Persist the memory bank to disk so it doesn't need rebuilding every run."""
        torch.save(self.bank, path)
        print(f"Memory bank saved to {path}")

    def load(self, path: str):
        """Load a previously saved memory bank."""
        self.bank = torch.load(path)
        print(f"Memory bank loaded from {path} ({self.bank.shape[0]} vectors)")