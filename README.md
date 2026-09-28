\# NDVI from Landsat 8 –  Southwest-Nigeria, 2025



Vegetation index map computed from Landsat Collection 2 Level-2 surface reflectance data.



!\[NDVI map](ndvi\_preview.png)



\## Data

\- Sensor: Landsat 8

\- Scene date: 2025-11-26

\- Path/Row: \[190/055]

\- Product: Collection 2 Level-2 (surface reflectance)

\- Source: USGS EarthExplorer



\## Method

NDVI = (NIR - Red) / (NIR + Red), using bands SR\_B5 (NIR) and SR\_B4 (Red).

The script reads both bands with rasterio, computes NDVI, and saves a GeoTIFF and a preview PNG.



\## Results

Sampled pixel values, checked against a manual QGIS calculation:



| Land cover | NDVI |

|------------|------|

| Vegetation | 0.40 |

| Water      | 0.00 |

| Built-up   | 0.09 |

| Bare rock  | 0.18 |



Vegetation shows the highest values, water is near zero, and built-up and bare surfaces fall in between, as expected.



\## How to run

pip install rasterio numpy matplotlib

python compute\_ndvi.py --nir path/to/SR\_B5.TIF --red path/to/SR\_B4.TIF



\## Tools

Python, rasterio, NumPy, Matplotlib, QGIS

