FROM python:3.9-alpine

WORKDIR /usr/src/app
ENV gecko_version=v0.29.1

RUN wget https://ghproxy.com/https://github.com/mozilla/geckodriver/releases/download/${gecko_version}/geckodriver-${gecko_version}-linux64.tar.gz \
&& tar -x geckodriver -zf geckodriver-${gecko_version}-linux64.tar.gz -O > /usr/bin/geckodriver \
&& chmod +x /usr/bin/geckodriver \
&& rm geckodriver-${gecko_version}-linux64.tar.gz

RUN apk add --no-cache firefox

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]