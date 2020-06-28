FROM python:3

ADD ascii.py /
ADD gui.py /
ADD example.jpg /

RUN pip install numpy==1.18.4
RUN pip install Pillow==7.1.2

CMD [ "python", "./gui.py" ]
