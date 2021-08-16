FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN wget https://ghproxy.com/https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz \
&& tar -x geckodriver -zf geckodriver-v0.23.0-linux64.tar.gz -O > /usr/bin/geckodriver \
&& chmod +x /usr/bin/geckodriver \
&& rm geckodriver-v0.23.0-linux64.tar.gz

RUN apt install

RUN

COPY . .

CMD [ "python", "./main.py" ]