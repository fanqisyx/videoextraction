import subprocess
import os
import datetime
import tkinter as tk
from tkinter import filedialog
import tkinter
from tkinter import messagebox

work_time_point_file = 'D:/快盘/Work/ChuangChi/Work Everyday/2023/2023-03-03 T18/Tool/CC_Framework/CC_Framework/bin/Release/WorkTimePoint.txt'
output_path = 'F:/T18/05_WorkpointtimeVideo'
output_bitrate = '2M'

def get_video_framerate(video_file):
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate', '-of', 'csv=p=0', video_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    framerate = result.stdout.strip()
    return eval(framerate)

def get_video_bitrate(video_file):
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=bit_rate', '-of', 'default=noprint_wrappers=1:nokey=1', video_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    bitrate = result.stdout.strip()
    return bitrate

def extract_frames(input_file, output_file, start_frame, end_frame):
    # 使用FFmpeg提取特定帧
    framerate=get_video_framerate(input_file)
    # start_time = str(int(start_frame/framerate))
    # duration = str(int((end_frame-start_frame)/framerate))
    start_time = str(start_frame / framerate)
    duration = str((end_frame - start_frame) / framerate)

    output_bitrate=get_video_bitrate(input_file)
    print('output_bitrate:'+str(output_bitrate))
    if use_gpu_var.get():
        cmd = ['ffmpeg', '-hwaccel', 'auto', '-i', input_file, '-ss', start_time, '-t', duration, '-vf',
               'select=between(n\,{0}\,{1})'.format(start_frame, end_frame), '-vsync', '0', '-c:v', 'h264_nvenc',
               '-b:v', output_bitrate, output_file]
    else:
        cmd = ['ffmpeg', '-hwaccel', 'auto', '-i', input_file, '-ss', start_time, '-t', duration, '-vf',
               'select=between(n\,{0}\,{1})'.format(start_frame, end_frame), '-vsync', '0', '-c:v', 'libx264',
               '-b:v', output_bitrate, output_file]
    subprocess.call(cmd)

def select_work_time_point_file():
    filename = filedialog.askopenfilename(title="Select Work Time Point File")
    work_time_point_file_entry.delete(0, tk.END)
    work_time_point_file_entry.insert(tk.END, filename)

def select_output_path():
    path = filedialog.askdirectory(title="Select Output Path")
    output_path_entry.delete(0, tk.END)
    output_path_entry.insert(tk.END, path)

def start_extraction():
    output_path = output_path_entry.get()
    # 进行截取操作
    work_time_point_file = work_time_point_file_entry.get()
    if not os.path.isfile(work_time_point_file):
        print("Invalid Work Time Point File.")
        return

    with open(work_time_point_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        video_path, start_frame, end_frame = line.strip().split(',')
        if int(end_frame) <= int(start_frame):
            continue

        video_name = os.path.basename(video_path)
        output_video = os.path.join(output_path, 'extracted_{0}-{1}frames_{2}.mp4'.format(start_frame,end_frame,video_name.split('.')[0]))
        extract_frames(video_path, output_video, int(start_frame), int(end_frame))

        current_time1 = datetime.datetime.now()
        
def show_help():
    help_text = """功能是从输入的视频文件中截取指定帧范围的视频，并将截取的视频保存为新的视频文件。

使用方法：
1. 在输入文件路径和输出文件夹路径的输入框中输入相应的路径。
2. 设置是否需要使用显卡加速此工作。
3. 点击截取按钮开始提取视频。

注意事项：
- 输入文件中可以有多行内容，每一行内容由“视频文件路径,起始帧,终止帧”构成（不含双引号），每行内容用英文逗号（半角）隔开。
- 输出文件夹路径用于存储生成的视频，视频名称包含起始、终止帧号和原始文件名。
- 使用显卡加速需要在电脑中配置好ffmpeg，默认使用cpu完成此工作。

如有问题，请联系我（我是一名机器视觉工程师） fanqisyx@foxmail.com。"""

    messagebox.showinfo("帮助", help_text)



# 创建GUI窗口
window = tk.Tk()
window.title("视频截取程序")
window.geometry("550x100")

# 创建行列表格
row = 0

# 设置默认值
default_work_time_point_file = "请选择输入的txt文件路径"
default_output_path = "请选择输出视频路径"
# default_output_bitrate = "2M"
#
# # 设置输出码率
# output_bitrate = tk.StringVar()
# output_bitrate.set(default_output_bitrate)

# 选择工作时间点文件
work_time_point_file_label = tk.Label(window, text="Work Time Point File:")
work_time_point_file_entry = tk.Entry(window, width=50)
work_time_point_file_entry.insert(tk.END, default_work_time_point_file)
work_time_point_file_button = tk.Button(window, text="选择文件", command=select_work_time_point_file)

work_time_point_file_label.grid(row=row, column=0, sticky="e")
work_time_point_file_entry.grid(row=row, column=1)
work_time_point_file_button.grid(row=row, column=2)

# 增加行索引
row += 1

# 选择输出路径
output_path_label = tk.Label(window, text="Output Path:")
output_path_entry = tk.Entry(window, width=50)
output_path_entry.insert(tk.END, default_output_path)
output_path_button = tk.Button(window, text="选择路径", command=select_output_path)

output_path_label.grid(row=row, column=0, sticky="e")
output_path_entry.grid(row=row, column=1)
output_path_button.grid(row=row, column=2)

# 增加行索引
row += 1
use_gpu_var = tkinter.BooleanVar()
use_gpu_checkbox = tkinter.Checkbutton(window, text="使用显卡处理", variable=use_gpu_var)
use_gpu_checkbox.grid(row=row, column=1, sticky="w")

# 创建帮助按钮
help_button = tk.Button(window, text="帮助", command=show_help)
help_button.grid(row=row, column=0, columnspan=1, padx=10, pady=5)

# # 设置输出码率
# output_bitrate_label = tk.Label(window, text="Output Bitrate:")
# output_bitrate_entry = tk.Entry(window, width=20, textvariable=output_bitrate)
# output_bitrate_label.grid(row=row, column=0, sticky="e")
# output_bitrate_entry.grid(row=row, column=1)


# 增加行索引
row +=0

# 开始截取
start_button = tk.Button(window, text="截取", command=start_extraction)
start_button.grid(row=row, column=2,columnspan=1)

# 启动事件循环
window.mainloop()