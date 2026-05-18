import os

def save_filenames_to_txt(directory, output_filename):
    try:
        # 确保目录存在
        if not os.path.isdir(directory):
            print(f"目录 '{directory}' 不存在。")
            return
        
        # 获取目录下的所有文件名，并去掉后缀
        filenames = [os.path.splitext(filename)[0] for filename in os.listdir(directory)]
        
        # 构造输出文件的完整路径
        output_file_path = os.path.join(directory, output_filename)
        
        # 将文件名（无后缀）写入txt文件
        with open(output_file_path, 'w', encoding='utf-8') as f:
            for filename in filenames:
                f.write(filename + '\n')
        
        print(f"文件名已成功保存到 '{output_file_path}'")
    except Exception as e:
        print(f"发生错误: {e}")

# 使用示例
directory_path = '/home/gaot/Experiments_now/pugan_16/data/PCPNet'  # 替换为你的目录路径
output_file_name = 'result.txt'  # 你希望保存文件名的txt文件名
save_filenames_to_txt(directory_path, output_file_name)
