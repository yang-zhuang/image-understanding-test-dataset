# Image Understanding Test Dataset

该项目为图像大模型（如 qwen 2.5 VL、glm-4v 等）的 API 测试提供 **图片 URL 托管服务**，通过 GitHub 直接生成可访问的图片链接，方便测试模型对图像的理解能力。

---

## 🎯 项目目标

- **快速生成 API 可用的图片 URL**：无需搭建服务器，直接通过 GitHub 原始链接调用
- **按 PDF 文件分类管理图片**：每个 PDF 提取的图片单独存放在文件夹中
- **标准化测试数据集**：便于团队协作和持续扩展

---

## 📦 目录结构说明

```
image-understanding-test-dataset/
├── README.md                  # 项目说明文档
├── images/                    # 存储所有测试图片的主目录
│   ├── example1/              # PDF 文件名（不含后缀）对应的文件夹
│   │   ├── image_0.png        # 从 PDF 提取的原始图片
│   │   ├── metadata_image_0.json  # 图片对应的元数据文件
│   │   ├── image_1.png
│   │   └── metadata_image_1.json
│   └── example2/              # 另一个 PDF 文件夹
├── pdfs/                      # 存放待处理的 PDF 文件（用于手动操作）
│   └── example1.pdf
├── scripts/                   # 存放自动化脚本
│   ├── extract_images_from_pdf.py  # 从 PDF 提取图片
│   └── upload_to_github.py     # 自动提交到 GitHub
└── usage_examples.md          # API 调用示例文档
```

---

## 🔧 如何使用

### 1.1 **手动上传图片（适用于非 PDF 场景）**

- 在 `images/` 下创建以任意名称命名的文件夹（如 `custom_dataset/`）

- 将图片和对应的元数据文件（`.json`）放入该文件夹：
  
  ```
  images/
  └── custom_dataset/
      ├── image_0.jpg
      └── metadata_image_0.json
  ```

- **元数据文件格式示例**（每个图片对应一个 `.json` 文件）：
  
  ```json
  {
    "source": "manual_upload",
    "description": "A cat on a windowsill"
  }
  ```

---

### 1.2 **从 PDF 提取图片（两种方式）**

#### 方式一：集成到其他项目中

- 在其他项目中调用 `scripts/extract_images_from_pdf.py`

#### 方式二：直接在本项目中处理 PDF

- 将待处理的 PDF 文件放入 `pdfs/` 目录（如 `pdfs/example1.pdf`）
- 运行 `scripts/extract_images_from_pdf.py`：
  - 会先检查 `images/` 下是否已有同名文件夹（如 `example1/`）
    - 如果存在：跳过处理并提示 `Folder already exists: example1`
    - 如果不存在：创建文件夹并提取图片
  - 自动创建以 PDF 文件名（不含后缀）命名的文件夹（如 `images/example1/`）
  - 提取图片并保存到该文件夹
  - 为每张图片生成对应的 `metadata_image_X.json` 文件
  - 
- ```python
  from extract_images_from_pdf import extract_images
  
  # 方式二：本项目中处理 PDF
  pdf_path = "../datasets/2402.03216v4---M3-Embedding.pdf"
  images_dir = "../images/"
  extract_images(pdf_path, images_dir)
  ```

---

## 📄 示例输出（PDF 提取后）

假设处理 `pdfs/example1.pdf`，生成以下结构：

```
images/
└── example1/
    ├── image_0.png
    ├── metadata_image_0.json
    ├── image_1.png
    └── metadata_image_1.json
```

- **`metadata_image_0.json` 内容示例**：
  
  ```json
  {
    "source": "example1.pdf",
    "page": 3,
    "description": "A red traffic light on a street"
  }
  ```

---

## ⚙️ 自动提交功能增强

```python
from upload_to_github import auto_git_commit_push

REPO_PATH = "G:/Code/image-understanding-test-dataset"  # 替换为你的本地仓库路径
COMMIT_MESSAGE = "[feat]：完善README.md说明"
TARGET_BRANCH = "main"

# 执行自动提交
auto_git_commit_push(REPO_PATH, COMMIT_MESSAGE, TARGET_BRANCH)
```

### 1. **超时控制**

- **超时参数**：默认 10 分钟（可配置）
- **自动终止机制**：超时后自动终止当前操作，防止卡死

### 2. **大文件处理**

- **非阻塞操作**：使用 `Popen` 实现异步执行
- **进度提示**：显示阶段状态符号（⏳/📝/🚀）

### 3. **实时反馈**

- **状态可视化**：每个操作阶段（添加、提交、推送）均有明确状态提示
- **错误处理**：捕获并显示 Git 警告信息（如 `LF will be replaced by CRLF`）

---

## 🌐 GitHub 项目地址处理

- **自动识别远程仓库**：如果本地仓库已关联 GitHub 远程仓库，则无需手动提供仓库地址

---

## 🛠️ 编码冲突解决方案（Windows 系统适配）

### 关键修复点

1. **显式设置编码环境**：
   
   ```python
   env = os.environ.copy()
   env['PYTHONIOENCODING'] = 'utf-8'
   env['GIT_PYTHON_REFRESH'] = 'quiet'
   ```

2. **提交信息处理**：
   
   ```python
   safe_commit_message = commit_message.replace('"', "'").replace('`', "'")
   text=False  # 禁用文本模式
   ```

3. **统一命令编码处理**：
   
   ```python
   stdout_bytes, stderr_bytes = commit_process.communicate(timeout=timeout)
   stdout = stdout_bytes.decode('utf-8', errors='replace')
   stderr = stderr_bytes.decode('utf-8', errors='replace')
   ```

4. **路径处理优化**：
   
   ```python
   REPO_PATH = r"G:\Code\AI-Model-Customization-Suite"  # 使用原始字符串避免转义问题
   ```

---

## 🧩 API 调用示例（`usage_examples.md`）

**OpenAI Vision API 示例**：

```python
import requests

image_url = "https://raw.githubusercontent.com/your-username/image-understanding-test-dataset/main/images/example1.pdf/image_0.png"
response = requests.post(
    "https://api.openai.com/v1/images/generate",
    json={"image_url": image_url},
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
```

**Google Cloud Vision API 示例**：

```json
{
  "requests": [
    {
      "image": {
        "source": {
          "imageUri": "https://raw.githubusercontent.com/your-username/image-understanding-test-dataset/main/images/example1.pdf/image_1.png"
        }
      },
      "features": [
        {
          "type": "TEXT_DETECTION",
          "maxResults": 10
        }
      ]
    }
  ]
}
```

---

## ⚠️ 注意事项

- **避免重复处理**：若 `images/` 下已有与 PDF 文件名同名的文件夹，脚本将自动跳过处理

- **文件大小限制**：单个文件不超过 100MB，建议压缩大尺寸图片  
- **元数据管理**：每个图片有独立的 `.json` 文件，便于扩展和查询

---

## ✅ 项目优势总结

| 功能       | 优势                         |
| -------- | -------------------------- |
| 超时控制     | 避免操作卡死，提升稳定性               |
| 大文件处理    | 支持异步监控，实时反馈进度              |
| 编码修复     | 解决 Windows 系统 GBK/UTF-8 冲突 |
| 自动识别远程仓库 | 简化配置流程，提升易用性               |

---

## 📬 联系方式

- 邮箱：18372513320@163.com
