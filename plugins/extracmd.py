import api
import datatypes


def startup():
    return datatypes.PluginInfo(
        "示例插件-更多实用控制台指令",
        "student_2333",
        "2021.4.7beta",
        "向控制台添加更多实用指令",
        listen_commands=[
            ('sendmsg', sendmsg, '发送消息'),
            ('addfriend', addfriend, '添加好友'),
            ('addgroup', addgroup, '添加群'),
            ('delfriend', delfriend, '删除好友'),
            ('leavegroup', leavegroup, '退出群'),
        ]
    )


def sendmsg(args):
    if len(args) >= 4:
        api.发送消息(args[0], ' '.join(args[3:]), args[2], args[1])
    else:
        return '使用方法：sendmsg <框架QQ> <好友QQ(无填0)> <群号(无填0)> <消息内容>'


def addgroup(args):
    if len(args) >= 2:
        api.添加群(args[0], args[1], (' '.join(args[2:]) if len(args) > 2 else None))
    else:
        return '使用方法：addgroup <框架QQ> <群号> [验证消息/问题答案]'


def addfriend(args):
    if len(args) >= 2:
        api.添加好友(args[0], args[1], (' '.join(args[2:]) if len(args) > 2 else None))
    else:
        return '使用方法：addfriend <框架QQ> <目标QQ> [验证消息/问题答案(多个用|隔开)]'


def delfriend(args):
    if len(args) == 2:
        api.删除好友(args[0], args[1])
    else:
        return '使用方法：delfriend <框架QQ> <目标QQ>'


def leavegroup(args):
    if len(args) == 2:
        api.退群(args[0], args[1])
        return ''
    else:
        return '使用方法：leavegroup <框架QQ> <目标群号>'
