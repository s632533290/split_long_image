import os
from PIL import Image


def split_image_by_adjacent_heights(image_path, heights, output_dir):
    # 打开图片  
    image = Image.open(image_path)
    image_width, image_height = image.size

    # 添加图片高度作为最后一组划分
    heights.append(image_height)

    # 确保输出目录存在  
    os.makedirs(output_dir, exist_ok=True)

    # 初始化当前y坐标（从0开始，因为数组第一个数被视为起始点）  
    current_y = 0 if heights and heights[0] == 0 else 0  # 如果第一个数是0，则current_y为0；否则也为0（但这里主要是为了满足条件判断）  
    split_images = []

    # 遍历高度数组，注意是每两个相邻数确定一个区域的高度  
    for i in range(len(heights) - 1):  # 遍历到倒数第二个数，因为每两个数确定一个区域  
        # 获取当前划分区域的高度（由当前数和下一个数共同确定）  
        # 注意：这里我们假设heights[i]是起始高度（但实际上是上一个区域的结束高度，除了第一个区域），heights[i+1]是当前区域的结束高度  
        # 由于是从0开始，所以第一个区域的高度实际上是heights[1]（如果heights[0]是0的话）  
        # 对于后续区域，我们取heights[i]到heights[i+1]之间的差值作为高度（但要考虑current_y的累加）  
        height_end = heights[i + 1]
        region_height = height_end - current_y  # 计算当前区域的高度  

        # 检查区域高度是否合理（不应该为负且不应该超过图片剩余高度）  
        if region_height <= 0:
            continue  # 跳过不合理的区域（虽然按照逻辑不应该出现）  
        if current_y + region_height > image_height:
            region_height = image_height - current_y  # 修正为图片剩余高度  

        # 裁剪当前划分区域的图片  
        box = (0, current_y, image_width, current_y + region_height)
        split_image = image.crop(box)
        split_images.append(split_image)

        # 保存分割后的图片  
        split_image_path = os.path.join(output_dir, f"split_{len(split_images)}.png")
        split_image.save(split_image_path)

        # 更新当前y坐标到下一个区域的起始点  
        current_y = height_end

        # 如果current_y还没有到达图片底部，则处理剩余部分（理论上不应该发生，除非heights数组有误）
    if current_y < image_height:
        remaining_height = image_height - current_y
        box = (0, current_y, image_width, image_height)
        split_image = image.crop(box)
        split_images.append(split_image)

        # 保存分割后的图片（理论上这个分支不应该被执行）  
        split_image_path = os.path.join(output_dir, f"split_{len(split_images)}.png")
        split_image.save(split_image_path)


def generate_height_array(image_height, interval):
    """
    生成一个数组，数组中的元素表示图像高度的分割点。

    参数:
    image_height (int): 图像的高度。
    interval (int): 分割的间隔。

    返回:
    list: 包含分割点的数组。
    """
    # 计算数组的长度
    array_length = image_height // interval + 1
    # 初始化数组
    heights = [0] * array_length
    # 填充数组
    for i in range(1, array_length):
        heights[i] = heights[i - 1] + interval
    return heights


def is_row_all_white(image, row):
    """
    判断图片在指定行的像素是否全部为白色。

    参数:
    image (PIL.Image.Image): 要检查的图片。
    row (int): 要检查的行号。

    返回:
    bool: 如果该行全部为白色像素，则返回True，否则返回False。
    """
    # 获取图片的宽度
    width = image.width
    # 遍历该行的所有像素
    for x in range(width):
        # 获取当前像素的颜色
        pixel_color = image.getpixel((x, row))

        # print(x,",",row,"color is",pixel_color)
        # 检查像素是否为白色
        if pixel_color != (255, 255, 255, 255):
            return False
    return True


# --- #

image_path = '/Users/emersonjack/Downloads/Obsidian中最佳的分享方式——笔记图片生成.png'  # 替换为你的图片路径
output_dir = '/Users/emersonjack/Downloads/图片生成/'  # 输出目录

# 打开图片
image = Image.open(image_path)
image_width, image_height = image.size

# 获取图片高度数组
heights = generate_height_array(image_height, 1100)

# 初始化索引计数器
j = 0
# 遍历 heights 数组中的每个元素
for i in heights:
    # 如果当前元素为 0，则跳过本次循环
    if i == 0:
        j = j + 1
        continue
    # 否则，检查当前行是否为全白
    else:
        # 如果当前行是全白的
        if is_row_all_white(image, i):
            # 将当前行的索引记录到 heights 数组中
            heights[j] = i
            # 更新索引计数器
            j = j + 1
            # 继续下一次循环
            continue
        # 如果当前行不是全白的
        else:
            # 从当前行开始，向上查找第一个全白行
            while not is_row_all_white(image, i):
                # 向上移动一行
                i = i - 1
                # 如果找到了全白行
                if is_row_all_white(image, i):
                    # 跳出循环
                    break
            # 将找到的全白行的索引记录到 heights 数组中
            heights[j] = i
            # 更新索引计数器
            j = j + 1
            # 继续下一次循环
            continue

split_image_by_adjacent_heights(image_path, heights, output_dir)