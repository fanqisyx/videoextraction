# videoextraction
功能是从输入的视频文件中截取指定帧范围的视频，并将截取的视频保存为新的视频文件。

使用方法：
1. 在输入文件路径和输出文件夹路径的输入框中输入相应的路径。
2. 设置是否需要使用显卡加速此工作。
3. 点击截取按钮开始提取视频。

注意事项：
- 输入文件中可以有多行内容，每一行内容由“视频文件路径,起始帧,终止帧”构成（不含双引号），每行内容用英文逗号（半角）隔开。
- 输出文件夹路径用于存储生成的视频，视频名称包含起始、终止帧号和原始文件名。
- 使用显卡加速需要在电脑中配置好ffmpeg，默认使用cpu完成此工作。

如有问题，请联系我（我是一名机器视觉工程师） fanqisyx@foxmail.com。
