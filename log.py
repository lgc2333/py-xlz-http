"""输出日志"""
import datetime
# import inspect
import os


def log(text, log_type='INFO'):
    # 获取时间并格式化
    time_obj = datetime.datetime.today()
    hr = time_obj.strftime('%Y-%m-%d %H:%M:%S')
    date = time_obj.strftime('%Y-%m-%d')

    # 获取运行文件名称及行数
    # stack = inspect.stack()[1]
    # stack = f"{stack.filename[stack.filename.rfind(os.sep) + 1:]}:{stack.lineno}"

    log_txt = f'[{hr}] [{log_type}] {text}'  # 日志文本
    print(log_txt)  # 输出日志

    if not os.path.exists('./logs'):  # 文件夹不存在则创建
        os.mkdir('./logs')
    with open(f'./logs/{date}.log', "a") as f:
        f.write(log_txt + '\n')  # 写到文件
