from PIL import Image  
import os  
  
def convert_jpg_to_png(jpg_path, png_path):  
    """  
    将jpg文件转换为png文件  
    :param jpg_path: jpg文件的路径  
    :param png_path: 转换后的png文件的路径  
    """  
    try:  
        with Image.open(jpg_path) as img:  
            rgb_img = img.convert('RGB')  # 确保转换为RGB模式，因为PNG不支持某些JPEG模式  
            rgb_img.save(png_path)  
        print(f"成功转换: {jpg_path} -> {png_path}")  
    except Exception as e:  
        print(f"转换失败: {jpg_path}, 错误: {e}")  
  
def main():  
    # 获取当前目录路径  
    current_directory = os.getcwd()  
  
    # 遍历当前目录中的所有文件  
    for filename in os.listdir(current_directory):  
        if filename.endswith('.jpg') or filename.endswith('.JPG'):  
            # 构造jpg和png文件的完整路径  
            jpg_path = os.path.join(current_directory, filename)  
            png_filename = filename.replace('.jpg', '.png')  # 假设所有jpg文件都是小写  
            png_path = os.path.join(current_directory, png_filename)  
  
            # 调用函数进行转换  
            convert_jpg_to_png(jpg_path, png_path)  
  
if __name__ == "__main__":  
    main()