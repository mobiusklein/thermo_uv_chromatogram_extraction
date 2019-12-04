FROM mono:5.20.1.34

RUN apt-get update
RUN apt-get install -y python3 python3-pip clang curl libglib2.0-dev
RUN python3 --version
RUN pip3 --version
RUN pip3 install pycparser==2.17
RUN pip3 install pythonnet==2.4.0
RUN pip3 install numpy
RUN pip3 install ms_deisotope

COPY uv_chromatogram.py /root/uv_chromatogram.py