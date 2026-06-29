# VMStream

> A lightweight low-latency H.264 streaming framework based on Python, OpenCV and PyAV.

VMStream 是一个使用 **Python** 开发的低延迟视频流框架。

项目目标并不是替代 FFmpeg 或 GStreamer，而是以清晰的架构实现一个完整的视频传输流程，用于学习和研究：

* 视频采集
* H.264 编码
* Socket 网络传输
* H.264 解码
* 多线程流水线
* 软件工程设计

---

# Features

* H.264 (PyAV/libx264) 编码
* OpenCV 摄像头采集
* TCP 数据传输
* 自定义 Length-Prefix 协议
* 多线程 Producer-Consumer 架构
* 实时码率统计
* Logging 日志系统
* 模块化设计
* 易于扩展

---

# Project Structure

```
VMStream
│
├── capture.py        # 摄像头采集
├── codec.py          # H.264 / JPEG 编解码
├── transport.py      # Socket 通信
├── protocol.py       # 数据包协议
├── worker.py         # 工作线程
├── statistics.py     # 实时统计
├── logger.py         # 日志
├── config.py         # 配置
│
├── sender.py         # Sender
└── receiver.py       # Receiver
```

---

# Architecture

```
Camera

↓

CaptureThread

↓

Queue

↓

EncodeThread

↓

Socket

↓

Receiver

↓

Decoder

↓

Display
```

采用经典 **Producer-Consumer** 架构。

* CaptureThread 负责采集图像
* Queue 负责线程通信
* EncodeThread 负责编码与发送
* Receiver 负责解码显示

各模块职责单一，便于维护和扩展。

---

# Dependencies

* Python 3.13+
* OpenCV
* PyAV
* NumPy

安装：

```bash
pip install -r requirements.txt
```

---

# Run

Sender：

```bash
python sender.py
```

Receiver：

```bash
python receiver.py
```

---

# Design Principles

VMStream 遵循以下设计原则：

* Single Responsibility Principle
* Producer-Consumer Pattern
* Lazy Initialization
* Modular Design
* Explicit Resource Management

项目重点放在代码可读性、可维护性以及架构设计，而不仅仅是实现功能。

---

# Roadmap

## v1.0

* H.264 编解码
* Socket 传输
* 多线程流水线
* 实时统计
* 日志系统

## v1.1

* 自动重连
* 网络状态监控
* 自适应码率
* 更多统计信息

## v1.2

* H.265
* GPU 编码
* 音频支持
* 多路视频

---

# License

MIT License
