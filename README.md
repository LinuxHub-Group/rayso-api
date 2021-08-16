# rayso-api

通过ray.so渲染一张图片并返回

# 原理

- 使用selenium访问`ray.so`获取网页
- 使用selenium和js操作网页
- 返回base64编码的图片

# api

`/rayso`: `[POST]`, `[GET]`
- `content`: 代码块，需要用base64编码
- `font`: 字体，默认Fira code
- `padding`: 图片 padding，默认26
- `title`: 标题
- `size`: 缩放倍数： 1-2，原图为2k屏渲染

# 使用

```shell
pip install -r requirements.txt
python main.py

# docker
docker run --rm -p 5567:5567 -it ghcr.io/linuxhub-group/rayso-api:latest
```

# 贡献

pr之前先检查代码：
```shell
pip install flake8 bandit black
black .
flake8 . --max-line-length=200
bandit --recursive .
```

# TODO

- [ ] 多线程
- [ ] 语言选择
- [ ] 主题选择