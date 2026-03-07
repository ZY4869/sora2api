# Sora2API

<div align="center">

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.119.0-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://www.docker.com/)

**一个功能完整的 OpenAI 兼容 API 服务，为 Sora 提供统一的接口**

</div>

---


## ✨ 功能特性

### 核心功能
- 🎨 **文生图** - 根据文本描述生成图片
- 🖼️ **图生图** - 基于上传的图片进行创意变换
- 🎬 **文生视频** - 根据文本描述生成视频
- 🎥 **图生视频** - 基于图片生成相关视频
- 📊 **多尺寸支持** - 横屏、竖屏等多种规格
- 🎭 **视频角色功能** - 创建角色，生成角色视频
- 🎬 **Remix 功能** - 基于已有视频继续创作
- 🎥 **分镜功能** - 支持生成分镜视频

### 高级特性
- 🔐 **Token 管理** - 支持多 Token 管理和轮询负载均衡
- 🌐 **代理支持** - 支持 HTTP 和 SOCKS5 代理
- 📝 **详细日志** - 完整的请求/响应日志记录
- 🔄 **异步处理** - 高效的异步任务处理
- 💾 **数据持久化** - SQLite 数据库存储
- 🎯 **OpenAI 兼容** - 完全兼容 OpenAI API 格式
- 🛡️ **安全认证** - API Key 验证和权限管理
- 📱 **Web 管理界面** - 直观的管理后台

---

## 🚀 快速开始

### 前置要求

- Docker 和 Docker Compose（推荐）
- 或 Python 3.8+

### 方式一：Docker 部署（推荐）

#### 标准模式（不使用代理）

```bash
# 克隆项目
git clone https://github.com/ZY4869/sora2api.git
cd sora2api

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

#### WARP 模式（使用代理）

```bash
# 使用 WARP 代理启动
docker-compose -f docker-compose.warp.yml up -d

# 查看日志
docker-compose -f docker-compose.warp.yml logs -f
```

### 方式二：本地部署

```bash
# 克隆项目
git clone https://github.com/ZY4869/sora2api.git
cd sora2api

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

### 首次启动

服务启动后，访问管理后台进行初始化配置：

- **地址**: http://localhost:8081
- **用户名**: `admin`
- **密码**: `admin`

⚠️ **重要**: 首次登录后请立即修改密码！

---

### 快速参考

| 功能 | 模型 | 说明 |
|------|------|------|
| 文生图 | `gpt-image*` | 使用 `content` 为字符串 |
| 图生图 | `gpt-image*` | 使用 `content` 数组 + `image_url` |
| 文生视频 | `sora2-*` | 使用 `content` 为字符串 |
| 图生视频 | `sora2-*` | 使用 `content` 数组 + `image_url` |
| 视频风格 | `sora2-*` | 在提示词中使用 `{风格ID}` 格式,如 `{anime}提示词` |
| 创建角色 | `sora2-*` | 使用 `content` 数组 + `video_url` |
| 角色生成视频 | `sora2-*` | 使用 `content` 数组 + `video_url` + 文本 |
| Remix | `sora2-*` | 在 `content` 中包含 Remix ID |
| 视频分镜 | `sora2-*` | 在 `content` 中使用```[时长s]提示词```格式触发 |
| 提示词优化 | `prompt-enhance-*` | 将简单提示词扩展为详细的电影级提示词 |

---

### API 调用

#### 基本信息（OpenAI标准格式，需要使用流式）

- **端点**: `http://localhost:8081/v1/chat/completions`
- **认证**: 在请求头中添加 `Authorization: Bearer YOUR_API_KEY`
- **默认 API Key**: `han1234`（建议修改）

#### 支持的模型

**图片模型**

| 模型 | 说明 | 尺寸 |
|------|------|------|
| `gpt-image` | 文生图（正方形） | 360×360 |
| `gpt-image-landscape` | 文生图（横屏） | 540×360 |
| `gpt-image-portrait` | 文生图（竖屏） | 360×540 |

**视频模型**

**标准版（Sora2）**

| 模型 | 时长 | 方向 | 说明 |
|------|------|------|------|
| `sora2-landscape-10s` | 10秒 | 横屏 | 文生视频/图生视频 |
| `sora2-landscape-15s` | 15秒 | 横屏 | 文生视频/图生视频 |
| `sora2-landscape-25s` | 25秒 | 横屏 | 文生视频/图生视频 |
| `sora2-portrait-10s` | 10秒 | 竖屏 | 文生视频/图生视频 |
| `sora2-portrait-15s` | 15秒 | 竖屏 | 文生视频/图生视频 |
| `sora2-portrait-25s` | 25秒 | 竖屏 | 文生视频/图生视频 |

**Pro 版（需要 ChatGPT Pro 订阅）**

| 模型 | 时长 | 方向 | 说明 |
|------|------|------|------|
| `sora2pro-landscape-10s` | 10秒 | 横屏 | Pro 质量文生视频/图生视频 |
| `sora2pro-landscape-15s` | 15秒 | 横屏 | Pro 质量文生视频/图生视频 |
| `sora2pro-landscape-25s` | 25秒 | 横屏 | Pro 质量文生视频/图生视频 |
| `sora2pro-portrait-10s` | 10秒 | 竖屏 | Pro 质量文生视频/图生视频 |
| `sora2pro-portrait-15s` | 15秒 | 竖屏 | Pro 质量文生视频/图生视频 |
| `sora2pro-portrait-25s` | 25秒 | 竖屏 | Pro 质量文生视频/图生视频 |

**Pro HD 版（需要 ChatGPT Pro 订阅，高清质量）**

| 模型 | 时长 | 方向 | 说明 |
|------|------|------|------|
| `sora2pro-hd-landscape-10s` | 10秒 | 横屏 | Pro 高清文生视频/图生视频 |
| `sora2pro-hd-landscape-15s` | 15秒 | 横屏 | Pro 高清文生视频/图生视频 |
| `sora2pro-hd-portrait-10s` | 10秒 | 竖屏 | Pro 高清文生视频/图生视频 |
| `sora2pro-hd-portrait-15s` | 15秒 | 竖屏 | Pro 高清文生视频/图生视频 |

> **注意：** Pro 系列模型需要 ChatGPT Pro 订阅（`plan_type: "chatgpt_pro"`）。如果没有 Pro 账号，请求这些模型会返回错误。

**提示词优化模型**

将简单提示词扩展为详细的电影级提示词，包含场景设置、镜头运动、光影效果、分镜描述等。

| 模型 | 扩展级别 | 时长 | 说明 |
|------|---------|------|------|
| `prompt-enhance-short-10s` | 简短 | 10秒 | 生成简洁的增强提示词 |
| `prompt-enhance-short-15s` | 简短 | 15秒 | 生成简洁的增强提示词 |
| `prompt-enhance-short-20s` | 简短 | 20秒 | 生成简洁的增强提示词 |
| `prompt-enhance-medium-10s` | 中等 | 10秒 | 生成中等长度的增强提示词 |
| `prompt-enhance-medium-15s` | 中等 | 15秒 | 生成中等长度的增强提示词 |
| `prompt-enhance-medium-20s` | 中等 | 20秒 | 生成中等长度的增强提示词 |
| `prompt-enhance-long-10s` | 详细 | 10秒 | 生成详细的增强提示词 |
| `prompt-enhance-long-15s` | 详细 | 15秒 | 生成详细的增强提示词 |
| `prompt-enhance-long-20s` | 详细 | 20秒 | 生成详细的增强提示词 |

**特点：**
- 支持流式和非流式响应
- 自动生成包含PRIMARY、SETTING、LOOK、CAMERA、LIGHT等专业电影术语的提示词
- 包含详细的分镜描述（时间轴、镜头运动、焦点、光影）
- 可直接用于视频生成模型

#### 请求示例

**文生图**

```bash
curl -X POST "http://localhost:8081/v1/chat/completions" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-image",
    "messages": [
      {
        "role": "user",
        "content": "一只可爱的小猫咪"
      }
    ],
    "stream": true
  }'
```

**图生图**

```bash
curl -X POST "http://localhost:8081/v1/chat/completions" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-image",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "将这张图片变成油画风格"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/png;base64,<base64_encoded_image_data>"
            }
          }
        ]
      }
    ],
    "stream": true
  }'
```

**提示词优化（流式）**

```bash
curl -X POST "http://localhost:8081/v1/chat/completions" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "prompt-enhance-medium-10s",
    "messages": [
      {
        "role": "user",
        "content": "猫猫"
      }
    ],
    "stream": true
  }'
```

**提示词优化（非流式）**

```bash
curl -X POST "http://localhost:8081/v1/chat/completions" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "prompt-enhance-long-15s",
    "messages": [
      {
        "role": "user",
        "content": "一只橘猫在窗台玩耍"
      }
    ],
    "stream": false
  }'
```

**文生视频**

```bash
curl -X POST "http://localhost:8081/v1/chat/completions" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sora2-landscape-10s",
    "messages": [
      {
        "role": "user",
        "content": "一只小猫在草地上奔跑"
      }
    ],
    "stream": true
  }'
```

**图生视频**

```bash
curl -X POST "http://localhost:8081/v1/chat/completions" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sora2-landscape-10s",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "这只猫在跳舞"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "data:image/png;base64,<base64_encoded_image_data>"
            }
          }
        ]
      }
    ],
    "stream": true
  }'
```

**视频Remix（基于已有视频继续创作）**

* 提示词内包含remix分享链接或id即可

```bash
curl -X POST "http://localhost:8081/v1/chat/completions" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sora2-landscape-10s",
    "messages": [
      {
        "role": "user",
        "content": "https://sora.chatgpt.com/p/s_68e3a06dcd888191b150971da152c1f5改成水墨画风格"
      }
    ],
    "stream": true
  }'
```

**视频分镜**

* 示例触发提示词：
  ```[5.0s]猫猫从飞机上跳伞 [5.0s]猫猫降落 [10.0s]猫猫在田野奔跑```
* 或
  ```text
  [5.0s]猫猫从飞机上跳伞
  [5.0s]猫猫降落
  [10.0s]猫猫在田野奔跑
  ```

```bash
curl -X POST "http://localhost:8081/v1/chat/completions" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sora2-landscape-10s",
    "messages": [
      {
        "role": "user",
        "content": "[5.0s]猫猫从飞机上跳伞 [5.0s]猫猫降落 [10.0s]猫猫在田野奔跑"
      }
    ],
    "stream": true
  }'
```

### 视频风格功能

Sora2API 支持**视频风格**功能，可以为生成的视频应用预设风格。

#### 使用方法

在提示词中使用 `{风格ID}` 格式指定风格，系统会自动提取并应用该风格。

#### 支持的风格

| 风格ID | 显示名称 | 说明 |
|--------|----------|------|
| `festive` | Festive | 节日风格 |
| `kakalaka` | 🪭👺 | 混沌风格 |
| `news` | News | 新闻风格 |
| `selfie` | Selfie | 自拍风格 |
| `handheld` | Handheld | 手持风格 |
| `golden` | Golden | 金色风格 |
| `anime` | Anime | 动漫风格 |
| `retro` | Retro | 复古风格 |
| `nostalgic` | Vintage | 怀旧风格 |
| `comic` | Comic | 漫画风格 |

#### 示例

**使用动漫风格生成视频**

```bash
curl -X POST "http://localhost:8081/v1/chat/completions" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sora2-landscape-10s",
    "messages": [
      {
        "role": "user",
        "content": "{anime}一只小猫在草地上奔跑"
      }
    ],
    "stream": true
  }'
```

**使用复古风格生成视频**

```bash
curl -X POST "http://localhost:8081/v1/chat/completions" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sora2-landscape-10s",
    "messages": [
      {
        "role": "user",
        "content": "{retro}城市街道夜景"
      }
    ],
    "stream": true
  }'
```

**在Remix中使用风格**

```bash
curl -X POST "http://localhost:8081/v1/chat/completions" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sora2-landscape-10s",
    "messages": [
      {
        "role": "user",
        "content": "{comic}https://sora.chatgpt.com/p/s_68e3a06dcd888191b150971da152c1f5改成漫画风格"
      }
    ],
    "stream": true
  }'
```

**注意事项**
- 风格标记 `{风格ID}` 可以放在提示词的任意位置
- 系统会自动提取风格ID并从提示词中移除风格标记
- 如果不指定风格，将使用默认风格生成

### 视频角色功能

Sora2API 支持**视频角色生成**功能。

#### 功能说明

- **角色创建**: 如果只有视频，无prompt，则生成角色自动提取角色信息，输出角色名
- **角色生成**: 有视频、prompt，则上传视频创建角色，使用角色和prompt进行生成，输出视频

#### API调用（OpenAI标准格式，需要使用流式）

**场景 1: 仅创建角色（不生成视频）**

上传视频提取角色信息，获取角色名称和头像。

```bash
curl -X POST "http://localhost:8081/v1/chat/completions" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sora2-landscape-10s",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "video_url",
            "video_url": {
              "url": "data:video/mp4;base64,<base64_encoded_video_data>"
            }
          }
        ]
      }
    ],
    "stream": true
  }'
```

**场景 2: 创建角色并生成视频**

上传视频创建角色，然后使用该角色生成新视频。

```bash
curl -X POST "http://localhost:8081/v1/chat/completions" \
  -H "Authorization: Bearer han1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sora2-landscape-10s",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "video_url",
            "video_url": {
              "url": "data:video/mp4;base64,<base64_encoded_video_data>"
            }
          },
          {
            "type": "text",
            "text": "角色做一个跳舞的动作"
          }
        ]
      }
    ],
    "stream": true
  }'
```

#### Python 代码示例

```python
import requests
import base64

# 读取视频文件并编码为 Base64
with open("video.mp4", "rb") as f:
    video_data = base64.b64encode(f.read()).decode("utf-8")

# 仅创建角色
response = requests.post(
    "http://localhost:8081/v1/chat/completions",
    headers={
        "Authorization": "Bearer han1234",
        "Content-Type": "application/json"
    },
    json={
        "model": "sora2-landscape-10s",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "video_url",
                        "video_url": {
                            "url": f"data:video/mp4;base64,{video_data}"
                        }
                    }
                ]
            }
        ],
        "stream": True
    },
    stream=True
)

# 处理流式响应
for line in response.iter_lines():
    if line:
        print(line.decode("utf-8"))
```

---

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢
- 项目源码、使用说明与后续更新统一维护在 [GitHub 仓库](https://github.com/ZY4869/sora2api)
- 感谢所有贡献者和使用者的支持！

---

## 🔄 同步上游更新

仅在同步上游更新时使用以下地址：

`https://github.com/TheSmallHanCat/sora2api.git`

```bash
git remote add upstream https://github.com/TheSmallHanCat/sora2api.git
# 若 upstream 已存在
git remote set-url upstream https://github.com/TheSmallHanCat/sora2api.git

git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

## 📞 联系方式

- 仓库主页：[GitHub 仓库](https://github.com/ZY4869/sora2api)
- 提交 Issue：[GitHub Issues](https://github.com/ZY4869/sora2api/issues)

---

**⭐ 如果这个项目对你有帮助，欢迎给仓库点个 Star！**

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ZY4869/sora2api&type=date&legend=top-left)](https://www.star-history.com/#ZY4869/sora2api&type=date&legend=top-left)
