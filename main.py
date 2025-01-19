import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image


# 图像分割函数
def split_image_by_adjacent_heights(image_path, heights, output_dir):
    image = Image.open(image_path)
    image_width, image_height = image.size
    heights.append(image_height)
    os.makedirs(output_dir, exist_ok=True)
    current_y = 0
    split_images = []

    for i in range(len(heights) - 1):
        height_end = heights[i + 1]
        region_height = height_end - current_y
        if region_height <= 0:
            continue
        if current_y + region_height > image_height:
            region_height = image_height - current_y

        box = (0, current_y, image_width, current_y + region_height)
        split_image = image.crop(box)
        split_images.append(split_image)
        split_image_path = os.path.join(output_dir, f"split_{len(split_images)}.png")
        split_image.save(split_image_path)
        current_y = height_end

    if current_y < image_height:
        box = (0, current_y, image_width, image_height)
        split_image = image.crop(box)
        split_images.append(split_image)
        split_image_path = os.path.join(output_dir, f"split_{len(split_images)}.png")
        split_image.save(split_image_path)


def generate_height_array(image_height, interval):
    array_length = image_height // interval + 1
    heights = [0] * array_length
    for i in range(1, array_length):
        heights[i] = heights[i - 1] + interval
    return heights


def is_row_all_white(image, row):
    width = image.width
    for x in range(width):
        pixel_color = image.getpixel((x, row))
        if pixel_color != (255, 255, 255, 255):
            return False
    return True


# UI 生成函数
def generate_images():
    image_path = image_path_entry.get()
    output_dir = output_dir_entry.get()
    split_height = int(split_height_entry.get())

    image = Image.open(image_path)
    image_height = image.size[1]
    heights = generate_height_array(image_height, split_height)

    j = 0
    for i in heights:
        if i == 0:
            j += 1
            continue
        else:
            if is_row_all_white(image, i):
                heights[j] = i
                j += 1
                continue
            else:
                while not is_row_all_white(image, i):
                    i -= 1
                    if is_row_all_white(image, i):
                        break
                heights[j] = i
                j += 1
                continue

    split_image_by_adjacent_heights(image_path, heights, output_dir)


# 创建主窗口
root = tk.Tk()
root.title("图像分割工具")
root.geometry("500x300")

# 图片路径输入框
tk.Label(root, text="图片路径:").pack()
image_path_entry = tk.Entry(root, width=50)
image_path_entry.pack()


def select_image():
    file_path = filedialog.askopenfilename()
    image_path_entry.delete(0, tk.END)
    image_path_entry.insert(0, file_path)


tk.Button(root, text="选择图片", command=select_image).pack(pady=5)

# 输出目录输入框
tk.Label(root, text="输出目录:").pack()
output_dir_entry = tk.Entry(root, width=50)
output_dir_entry.insert(0, "/Users/emersonjack/Downloads")
output_dir_entry.pack()


def select_output_dir():
    directory = filedialog.askdirectory()
    output_dir_entry.delete(0, tk.END)
    output_dir_entry.insert(0, directory)


tk.Button(root, text="选择输出目录", command=select_output_dir).pack(pady=5)

# 切分高度输入框
tk.Label(root, text="切分高度:").pack()
split_height_entry = tk.Entry(root, width=50)
split_height_entry.insert(0, "1400")
split_height_entry.pack()

# 执行分割按钮
tk.Button(root, text="生成分割图片", command=generate_images).pack(pady=10)

# 启动主循环
root.mainloop()
