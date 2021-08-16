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

# TODO

- [ ] 多线程
- [ ] 语言选择
- [ ] 主题选择