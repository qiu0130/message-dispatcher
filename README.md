
## :trident: 消息派发服务

### 功能

> 一个独立的后台消息派发器，通过配置不同类型的消息和编写请求第三方接口函数，实现各自消息的发送任务

### 使用

> 首先在`handler`目录下定义不同的消息`channel`,继承`MessageDispatchChannel`，然后实现对应的`callback`函数,最后编写`yaml`配置文件,轻松实现不同消息派发任务:v:

在`message.yaml`中定义消息，`{{ }}`中的内容将被替换成回调函数的返回值
```yaml
A:
  name: "消息类型一"
  type:
    mail:
      title: "我是标题1"
      content: "你好，{{ username }}"
      target: "{{ email }}"
    throughout:
      title: "我是标题1"
      content: "你好，{{ username }}"
      target: "{{ phone }}"
    sms:
      title: "我是标题1"
      content: "你好，{{ username }}"
      target: "{{ phone }}"
```
运行
```python
message = MessageDispatcher.initialize(code="A")
message.dispatch()
```

+ 目前支持的消息类型：邮件，手机短信，APP 透穿消息
