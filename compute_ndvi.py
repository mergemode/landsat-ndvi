"""
compute_ndvi.py

Computes NDVI from Landsat 8/9 Surface Reflectance bands and saves:
  1. A GeoTIFF (ndvi_output.tif) you can open in QGIS
  2. A quick-look PNG (ndvi_preview.png) with a red-yellow-green color ramp

Usage:
    python compute_ndvi.py --nir path/to/SR_B5.TIF --red path/to/SR_B4.TIF

Notes:
- Landsat Collection 2 Level-2 bands are scaled integers. NDVI is a ratio,
  so the scale factor cancels out and you don't need to apply it here.
- NDVI = (NIR - Red) / (NIR + Red), range -1 to 1.
"""

import argparse
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def compute_ndvi(nir_path, red_path, out_tif, out_png):
    with rasterio.open(nir_path) as nir_src:
        nir = nir_src.read(1).astype("float32")
        profile = nir_src.profile

    with rasterio.open(red_path) as red_src:
        red = red_src.read(1).astype("float32")

    # Avoid divide-by-zero on nodata/black-edge pixels
    denom = nir + red
    denom[denom == 0] = np.nan

    ndvi = (nir - red) / denom
    ndvi = np.clip(ndvi, -1, 1)

    # --- Save as GeoTIFF (open this in QGIS) ---
    profile.update(dtype="float32", count=1, nodata=np.nan)
    with rasterio.open(out_tif, "w", **profile) as dst:
        dst.write(ndvi, 1)
    print(f"Saved GeoTIFF: {out_tif}")

    # --- Save a styled preview PNG ---
    colors = ["#a50026", "#f46d43", "#fee08b", "#a6d96a", "#1a9850"]
    cmap = LinearSegmentedColormap.from_list("ndvi", colors)

    plt.figure(figsize=(10, 8))
    im = plt.imshow(ndvi, cmap=cmap, vmin=-1, vmax=1)
    plt.colorbar(im, label="NDVI")
    plt.title("NDVI")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    print(f"Saved preview: {out_png}")

    # --- Quick stats, same idea as your hand-sampled points ---
    valid = ndvi[~np.isnan(ndvi)]
    print("\nNDVI summary stats:")
    print(f"  min:    {valid.min():.3f}")
    print(f"  max:    {valid.max():.3f}")
    print(f"  mean:   {valid.mean():.3f}")
    print(f"  median: {np.median(valid):.3f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute NDVI from Landsat NIR and Red bands.")
    parser.add_argument("--nir", required=True, help="Path to NIR band (e.g. SR_B5.TIF)")
    parser.add_argument("--red", required=True, help="Path to Red band (e.g. SR_B4.TIF)")
    parser.add_argument("--out-tif", default="ndvi_output.tif", help="Output GeoTIFF path")
    parser.add_argument("--out-png", default="ndvi_preview.png", help="Output PNG preview path")
    args = parser.parse_args()

    compute_ndvi(args.nir, args.red, args.out_tif, args.out_png)
