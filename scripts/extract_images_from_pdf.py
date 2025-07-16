import os
import fitz  # PyMuPDF
import json
import re


def sanitize_folder_name(name):
    """清理非法字符并标准化文件夹名称"""
    # 替换非法字符为下划线（适用于 Windows 和 Linux/macOS）
    name = re.sub(r'[<>:"/\\|?*\']', '_', name)
    # 去除前后空格和多余的点号
    name = name.strip().rstrip('.')
    # 替换连续下划线为单个
    name = re.sub(r'_+', '_', name)
    # 限制最大长度（Windows 最大路径长度为 260 字符）
    max_length = 255  # 根据实际路径长度调整
    return name[:max_length]


def extract_images(pdf_path, images_dir):
    # 获取 PDF 文件名（不含后缀）
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    sanitized_name = sanitize_folder_name(pdf_name)
    output_dir = os.path.join(images_dir, sanitized_name)

    # 检查文件夹是否已存在
    if os.path.exists(output_dir):
        print(f"⚠️ Folder already exists: {sanitized_name}")
        return

    os.makedirs(output_dir, exist_ok=True)

    # 打开 PDF 文件
    doc = fitz.open(pdf_path)

    # 遍历每一页
    for page_index in range(len(doc)):
        page = doc.load_page(page_index)
        image_list = page.get_images(full=True)  # 获取当前页所有图片

        # 遍历每张图片
        for img_index, img in enumerate(image_list):
            xref = img[0]  # 图片的 xref 编号
            base_image = doc.extract_image(xref)  # 提取图像数据
            image_bytes = base_image["image"]
            ext = base_image["ext"]  # 获取图片扩展名（如 jpg, png）

            # 保存图片文件
            image_path = os.path.join(output_dir, f"image_{page_index}_{img_index}.{ext}")
            with open(image_path, "wb") as f:
                f.write(image_bytes)

            # 生成对应元数据文件
            metadata = {
                "source": pdf_name,
                "page": page_index,
                "img_index": img_index
            }
            metadata_path = os.path.join(output_dir, f"metadata_image_{page_index}_{img_index}.json")
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)

    doc.close()  # 关闭 PDF 文档

if __name__ == "__main__":
    # 方式一：集成到其他项目时传入路径
    # pdf_path = "path/to/your.pdf"
    # images_dir = "path/to/images"

    # 方式二：本项目中处理 PDF
    pdf_path = "../datasets/2402.03216v4---M3-Embedding.pdf"
    images_dir = "../images/"
    extract_images(pdf_path, images_dir)