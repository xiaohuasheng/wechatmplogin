# wechatmplogin
微信公众平台登录，提取cookie和token，方便自动给用户回复消息


# 调试经验
1. 发现扫码后一直没成功，因为是等待页面的某个元素出现，现在页面元素变了，就没法继续了，可以开启有头模式，看看页面的变化

# 升级 selenium，不用再下载驱动了
```shell
pip install selenium==4.12.0              
```
```python
driver = webdriver.Chrome(options=chrome_options)
```