import os
import time
import subprocess

# 定义要检查的文件名
file_name = "mp_auth.json"

# 获取文件的最后修改时间
if os.path.exists(file_name):
    file_stat = os.stat(file_name)
    file_mtime = file_stat.st_mtime

    # 计算文件的最后修改时间与当前时间的差值，以小时为单位
    current_time = time.time()
    time_difference_hours = (current_time - file_mtime) / 3600

    # 如果文件的最后修改时间超过82小时，则执行 main.py
    if time_difference_hours > 82:
        subprocess.run(["python3", "main.py"])
else:
    print(f"文件 {file_name} 不存在")
