# Docker Image to run UV Chromatogram

Build the image:

```
$ ./build
```

Run the image:

```
docker run \
  -v /path/to/directory/raw:/raw \
  -v /path/to/directory/output:/output \
  -it docker-uv-chromatogram-extraction \
  python3 /root/uv_chromatogram.py /raw/filename.raw /output/output.csv
```