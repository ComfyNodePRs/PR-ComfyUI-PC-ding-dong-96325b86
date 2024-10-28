# ⏰ ComfyUI Workflow Notification Plugin 
[中文版](./readme.zh.md)


Just like when your pizza is ready and the oven goes "Ding! 🍕", this plugin lets your ComfyUI notify you when your AI creations are done baking! 

A ComfyUI custom node that sends you a friendly "ding-dong" notification when your workflows are fully cooked and ready to serve. No more staring at the screen waiting - let the AI kitchen tell you when dinner's ready! 👨‍🍳

## Features

![setting](./image/setting1.jpg)

- Sound notifications when workflows complete
- Adjustable notification volume
- Sound toggle control
- Support for single workflow or batch workflow completion notifications
- Support for custom notification sound upload

## Nodes

### DingDong Node

![dingdong](./image/node1.jpg)

A notification node that plays a custom sound file when workflow execution reaches it. You can select your own audio file and adjust the volume to get notified exactly how you want.

### DingDongText Node

![dingdong](./image/node2.jpg)

A text-to-speech notification node that speaks custom text when workflow execution reaches it. The speech can be customized with adjustable pitch, speed and volume settings.


## Installation

1. Download the node files
2. Place in ComfyUI's `custom_nodes` folder
3. Restart ComfyUI
