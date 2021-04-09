import threading
import traceback

from tornado import web, httpserver, ioloop

import config
import event
from log import log

print('py-xlz-http version 2021.4.9beta by student_2333')

commands = []
plugins = []


class Main(web.RequestHandler):
    def get(self):
        self.write('<center><h1>如果你能看到这个，就证明服务器启动成功啦！</hi></center>')

    def post(self):
        data = self.request.body_arguments
        post_type = data['post_type'][0].decode('utf-8')
        try:
            if post_type == 'private':
                threading.Thread(target=event.event_private, args=(data,)).start()
            elif post_type == 'group':
                threading.Thread(target=event.event_group, args=(data,)).start()
            elif post_type == 'event':
                threading.Thread(target=event.event_event, args=(data,)).start()
        except Exception as err:
            log('发生错误：' + str(err), 'ERROR')


class File(web.RequestHandler):
    def get(self, file_name):
        try:
            with open('tmp/' + file_name, 'rb') as f:
                file = f.read()
        except:
            self.set_status(404)
        else:
            self.write(file)


class BasicCommands:
    @staticmethod
    def help(args):
        return '指令列表：\n' + '\n'.join([f'{x[0]} - {x[2]}' for x in commands])

    @staticmethod
    def plugins_list(args):
        return '已加载插件列表：\n文件名 - 插件名 - 作者 - 版本号 - 简介 - 优先级\n' + '\n'.join(
            [f'{x[0]} - {x[1]} - {x[2]} - {x[3]} - {x[4]} - {x[5]}' for x in plugins])

    @staticmethod
    def reload(args):
        reload()
        return '重载插件完毕，向服务器新添加的url需重启生效'


def command_input():
    cmd = input().strip().split()
    if len(cmd) > 0 and cmd[0] in [x[0] for x in commands]:
        try:
            ret = [x[1] for x in commands if cmd[0] == x[0]][0](cmd[1:])
        except:
            print(f'执行指令出错\n{traceback.format_exc()}')
        else:
            if ret:
                print(ret)
            del ret
    else:
        print('未知指令。使用 help 查看指令列表')
    del cmd
    command_input()


def reload():
    global commands
    global plugins
    func = event.load_plugins()
    commands = [('help', BasicCommands.help, '查看指令列表'),
                ('pluginli', BasicCommands.plugins_list, '查看已加载插件列表'),
                ('reload', BasicCommands.reload, '重载插件')] + func[1]
    func[2].sort(key=lambda x: x[5], reverse=True)
    plugins = func[2]
    return func[0]


if __name__ == '__main__':
    log('服务器启动中……')
    config.plugin_api = config.plugin_api if config.plugin_api.endswith('/') else config.plugin_api + '/'
    config.plugin_api = config.plugin_api if (config.plugin_api.startswith('http://') or config.plugin_api.startswith(
        'https://')) else 'http://' + config.plugin_api
    log('服务器端口：' + str(config.server_port))
    log('插件API地址：' + config.plugin_api)
    log('插件请求token：' + config.token)
    svr = httpserver.HTTPServer(
        web.Application([('/', Main), ('/file/(.*)', File)] + reload())
    )
    svr.bind(config.server_port)
    svr.start()
    threading.Thread(target=command_input).start()
    log(f'服务器启动成功，可测试访问 http://localhost:{config.server_port}/')
    ioloop.IOLoop.current().start()
