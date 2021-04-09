from tornado import web  # 无需向服务器添加url可删除

import datatypes


# 建议安装ChinesePinyin-CodeCompletionHelper插件，以获取更好中文函数及常量编程体验，支持PyCharm及VS Code（说白了就是我懒得翻译）

def startup():
    """
    插件初始化函数
    除全局变量等声明，其他初始化代码建议在此处执行
    返回插件信息
    如果想拒绝加载，直接raise Exception('原因即可')
    """

    # 如果有，可在此处放置初始化代码

    return datatypes.PluginInfo(  # 返回插件信息
        "插件开发空壳",  # 插件名称
        "student_2333",  # 作者
        version="1.0.0",  # 版本号 无需可注释
        description="这是一个开发空壳",  # 插件简介 无需可注释
        # priority=1,  # 消息处理优先级 如无特殊需求请勿更改，请注释
        func_private=private_msg,  # 私聊消息处理函数 无需可注释
        func_group=group_msg,  # 群聊消息处理函数 无需可注释
        func_event=event_msg,  # 事件消息处理函数 无需可注释
        listen_urls=[('/example', example_url)],  # 向服务器添加的url 格式[('相对路径', 处理类),...] 无需可注释
        listen_commands=[('example', example_cmd, '示例指令')]  # 向控制台添加的指令 格式[('指令', 处理函数, '功能简介'),...] 无需可注释
    )


def private_msg(data: datatypes.PrivateMsg):
    """
    私聊消息处理函数，无需可删除
    返回True拦截消息，返回False忽略消息
    """
    if int(data.message_cut_iden) > 0 and (int(data.message_cut) + 1 != int(data.message_cut_num)):
        # 序列从0开始，过滤腾讯长消息自动分片的片段内容，你也可以删除这里获取分片片段内容
        return False

    # 因oopshttpapi特性，这里无需过滤框架自身消息
    if data.message_type == datatypes.消息类型_临时会话:
        if data.message_temp_subtype == datatypes.消息类型_临时会话_群临时:
            pass

        elif data.message_temp_subtype == datatypes.消息类型_临时会话_公众号:
            pass

        elif data.message_temp_subtype == datatypes.消息类型_临时会话_网页QQ咨询:
            pass

    elif data.message_type == datatypes.消息类型_好友通常消息:
        # 在2.7.1以上的版本当中，真正的红包等将传入文本代码，但由于oopshttpapi特性，已将方括号转义，所以……
        pass

    return False


def group_msg(data: datatypes.GroupMsg):
    """
    群聊消息处理函数，无需可删除
    返回True拦截消息，返回False忽略消息
    """
    if int(data.message_cut_iden) > 0 and (int(data.message_cut) + 1 != int(data.message_cut_num)):
        # 序列从0开始，过滤腾讯长消息自动分片的片段内容，你也可以删除这里获取分片片段内容
        return False

    # 因oopshttpapi特性，这里无需过滤框架自身消息
    # 在2.7.1以上的版本当中，真正的红包等将传入文本代码，但由于oopshttpapi特性，已将方括号转义，所以……

    return False


def event_msg(data: datatypes.EventMsg):
    """
    事件消息处理函数，无需可删除
    返回True拦截消息，返回False忽略消息
    tip:此处内容过于长，如果想继续往下看建议折叠此函数
    """
    if data.event_type == datatypes.好友事件_签名变更:
        # data.self_id 框架QQ
        # data.trigger_id  签名变更的QQ
        # data.message_timestamp 现在的时间
        # data.oper_nickname 新的签名内容
        # data.trigger_nickname 变更QQ的昵称
        pass

    elif data.event_type == datatypes.好友事件_昵称改变:
        # data.self_id 框架QQ
        # data.trigger_id  昵称变更的QQ
        # data.message_timestamp 现在的时间
        # data.trigger_nickname 新的昵称内容
        pass

    elif data.event_type == datatypes.好友事件_有新好友:
        # data.self_id 框架QQ
        # data.trigger_id 新好友的QQ
        # data.message_timestamp 现在的时间
        # data.trigger_nickname 新好友的昵称
        pass

    elif data.event_type == datatypes.好友事件_好友请求:
        # data.self_id 框架QQ
        # data.trigger_id 对方QQ
        # data.trigger_nickname 对方QQ昵称
        # data.event_subtype 为1：被添加为单向好友,为2：请求添加为好友
        # data.message 验证消息
        pass

    elif data.event_type == datatypes.好友事件_被好友删除:
        # data.self_id 框架QQ
        # data.trigger_id  删除者QQ
        # data.message_timestamp 现在的时间
        # data.trigger_nickname 删除者QQ昵称
        pass

    elif data.event_type == datatypes.好友事件_某人撤回事件:
        # data.self_id 框架QQ
        # data.trigger_id  撤回者QQ
        # data.message_seq  可用于取缓存消息
        # data.message_timestamp 撤回消息发送时间
        # data.trigger_nickname 撤回者QQ昵称
        # data.message 撤回消息内容
        pass

    elif data.event_type == datatypes.好友事件_对方同意了您的好友请求:
        # data.self_id 框架QQ
        # data.trigger_id 同意者QQ
        # data.message_timestamp 同意时间
        # data.trigger_nickname 同意者QQ昵称
        pass

    elif data.event_type == datatypes.好友事件_对方拒绝了您的好友请求:
        # data.self_id 框架QQ
        # data.trigger_id 拒绝者QQ
        # data.message_timestamp 拒绝时间
        # data.trigger_nickname 拒绝者昵称
        pass

    elif data.event_type == datatypes.好友事件_资料卡点赞:
        # data.self_id 框架QQ
        # data.trigger_id  点赞者QQ
        # data.message_timestamp 点赞时间
        # data.trigger_nickname 点赞者QQ昵称
        # data.message 点赞事件文本
        pass

    elif data.event_type == datatypes.好友事件_签名点赞:
        # data.self_id 框架QQ
        # data.trigger_id  点赞者QQ
        # data.message_timestamp 点赞时间
        # data.trigger_nickname 点赞者QQ昵称
        # data.message 点赞事件文本
        # data.oper_nickname 签名内容
        pass

    elif data.event_type == datatypes.好友事件_签名回复:
        # data.self_id 框架QQ
        # data.trigger_id  回复者QQ
        # data.message_timestamp 回复时间
        # data.trigger_nickname 回复者QQ昵称
        # data.message 回复内容
        # data.oper_nickname 签名内容
        pass

    elif data.event_type == datatypes.好友事件_个性标签点赞:
        # data.self_id 框架QQ
        # data.trigger_id  点赞者QQ
        # data.message_timestamp 点赞时间
        # data.trigger_nickname 点赞者QQ昵称
        # data.message 点赞事件文本
        # data.oper_nickname 个性标签内容
        pass

    elif data.event_type == datatypes.好友事件_随心贴回复:
        # data.self_id 框架QQ
        # data.trigger_id  回复者QQ
        # data.oper_id 随心贴发送者QQ
        # data.message_timestamp 回复时间
        # data.group_name 随心贴内容
        # data.trigger_nickname 回复者QQ昵称
        # data.oper_nickname 随心贴发送者QQ昵称
        # data.message 回复内容
        pass

    elif data.event_type == datatypes.好友事件_随心贴增添:
        # data.self_id 框架QQ
        # data.trigger_id  增添者QQ
        # data.message_timestamp 增添时间
        # data.trigger_nickname 增添者QQ昵称
        # data.message 增添事件文本
        # data.oper_nickname 随心贴内容
        pass

    elif data.event_type == datatypes.好友事件_系统提示:
        # data.self_id 框架QQ
        # data.trigger_id 提示触发者QQ
        # data.trigger_nickname 提示触发者QQ昵称
        # data.message QQ系统提示数据
        pass

    elif data.event_type == datatypes.群事件_群被解散:
        # data.self_id 框架QQ
        # data.group_id 解散群号
        # data.message_timestamp  解散时间
        # data.group_name 解散群名
        # data.oper_id、data.trigger_id 解散者QQ
        # data.oper_nickname、 data.trigger_nickname 解散者QQ昵称
        pass

    elif data.event_type == datatypes.群事件_某人被禁言:
        # data.self_id 框架QQ
        # data.group_id 事件群号
        # data.oper_id 禁言者QQ
        # data.trigger_id 被禁者QQ
        # data.message_seq 被禁秒数
        # data.message_timestamp 被禁时间
        # data.group_name 事件群名
        # data.oper_nickname 禁言者QQ昵称
        # data.trigger_nickname 被禁者QQ昵称
        pass

    elif data.event_type == datatypes.群事件_某人被解除禁言:
        # data.self_id 框架QQ
        # data.group_id 事件群号
        # data.oper_id 解除者QQ
        # data.trigger_id 被解除者QQ
        # data.message_timestamp 被解除时间
        # data.group_name 事件群名
        # data.oper_nickname 解除者QQ昵称
        # data.trigger_nickname 被解除者QQ昵称
        pass

    elif data.event_type == datatypes.群事件_某人加入了群:
        # data.self_id 框架QQ
        # data.group_id 事件群号
        # data.oper_id 审批者QQ
        # data.message_timestamp 入群时间
        # data.group_name 事件群名
        # data.oper_nickname 审批者QQ昵称
        # data.trigger_nickname 入群者QQ昵称
        # 注意！触发此事件的同时可能会触发某人被邀请入群事件
        pass

    elif data.event_type == datatypes.群事件_某人被邀请入群:
        # data.self_id 框架QQ
        # data.group_id 事件群号
        # data.oper_id 邀请者QQ
        # data.trigger_id 入群者QQ
        # data.message_timestamp 入群时间
        # data.group_name 事件群名
        # data.oper_nickname 邀请者QQ昵称
        # data.trigger_nickname 入群者QQ昵称
        # 注意！此事件与某人加入了群事件互不影响，独立触发
        pass

    elif data.event_type == datatypes.群事件_我被邀请加入群:
        # data.self_id 框架QQ
        # data.group_id 被邀群号
        # data.oper_id 邀请者QQ
        # data.message_seq   处理所需Seq
        # data.message_timestamp 邀请时间
        # data.group_name 被邀群名称
        # data.oper_nickname 邀请者QQ昵称
        # data.trigger_nickname 本人昵称
        # data.trigger_id  邀请者QQ
        pass

    elif data.event_type == datatypes.群事件_某人申请加群:
        # data.self_id 框架QQ
        # data.group_id 被申群号
        # data.oper_id 邀请者QQ
        # data.message_timestamp 申请时间
        # data.group_name 被申群名称
        # data.oper_nickname 邀请者QQ昵称
        # data.trigger_nickname 进群者QQ昵称
        # data.trigger_id  进群者QQ
        # data.message 为：验证消息 加上 加群来源,格式为：验证消息[加群来源:xxx],如果加群者QQ存在风险被腾讯过滤,那么将加上[该帐号存在风险，请谨慎操作]后缀,验证消息内的[、]将被转义
        pass

    elif data.event_type == datatypes.群事件_某人退出了群:
        # data.self_id 框架QQ
        # data.group_id 被退群号
        # data.message_timestamp 退群时间
        # data.group_name 被退群名称
        # data.trigger_nickname 退群者QQ昵称
        # data.trigger_id  退群者QQ
        pass

    elif data.event_type == datatypes.群事件_某人被踢出群:
        # data.self_id 框架QQ
        # data.group_id 少人群号
        # data.message_timestamp 被踢时间
        # data.group_name 少人群名称
        # data.trigger_nickname 退群者QQ昵称
        # data.trigger_id  退群者QQ
        # data.oper_id 踢人QQ
        # data.oper_nickname 踢人QQ昵称
        pass

    elif data.event_type == datatypes.群事件_某人撤回事件:
        # data.self_id 框架QQ
        # data.group_id 被撤群号
        # data.oper_id 撤消QQ (对方本人或管理员)
        # data.trigger_id 被撤QQ
        # data.message_seq 消息Seq
        # data.message_timestamp 消息发送时间
        # data.group_name 被撤群名称
        # data.oper_nickname 撤消QQ昵称
        # data.message 撤回内容
        pass

    elif data.event_type == datatypes.群事件_开启全员禁言:
        # data.self_id 框架QQ
        # data.group_id 启用群号
        # data.oper_id 开启人QQ
        # data.message_timestamp  开启时间
        # data.group_name 启用群名称
        # data.oper_nickname 开启人QQ昵称
        pass

    elif data.event_type == datatypes.群事件_关闭全员禁言:
        # data.self_id 框架QQ
        # data.group_id 关闭群号
        # data.oper_id 关闭人QQ
        # data.message_timestamp  关闭时间
        # data.group_name 关闭群名称
        # data.oper_nickname 关闭人QQ昵称
        pass

    elif data.event_type == datatypes.群事件_开启匿名聊天:
        # data.self_id 框架QQ
        # data.group_id 启用群号
        # data.oper_id 开启人QQ
        # data.message_timestamp  开启时间
        # data.group_name 启用群名称
        # data.oper_nickname 开启人QQ昵称
        pass

    elif data.event_type == datatypes.群事件_关闭匿名聊天:
        # data.self_id 框架QQ
        # data.group_id 关闭群号
        # data.oper_id 关闭人QQ
        # data.message_timestamp  关闭时间
        # data.group_name 关闭群名称
        # data.oper_nickname 关闭人QQ昵称
        pass

    elif data.event_type == datatypes.群事件_某人被取消管理:
        # data.self_id 框架QQ
        # data.group_id 发生群号
        # data.trigger_id  被取消者QQ
        # data.message_timestamp  取消时间
        # data.group_name 发生群名
        # data.trigger_nickname 被取消者QQ昵称
        pass

    elif data.event_type == datatypes.群事件_某人被赋予管理:
        # data.self_id 框架QQ
        # data.group_id 发生群号
        # data.trigger_id  被赋予者QQ
        # data.message_timestamp  取消时间
        # data.group_name 发生群名
        # data.trigger_nickname 被赋予者QQ昵称
        pass

    elif data.event_type == datatypes.群事件_开启坦白说:
        # data.self_id 框架QQ
        # data.group_id 发生群号
        # data.group_name 发生群名
        pass

    elif data.event_type == datatypes.群事件_关闭坦白说:
        # data.self_id 框架QQ
        # data.group_id 发生群号
        # data.group_name 发生群名
        pass

    elif data.event_type == datatypes.群事件_允许群临时会话:
        # data.self_id 框架QQ
        # data.group_id 发生群号
        # data.group_name 发生群名
        pass

    elif data.event_type == datatypes.群事件_禁止群临时会话:
        # data.self_id 框架QQ
        # data.group_id 发生群号
        # data.group_name 发生群名
        pass

    elif data.event_type == datatypes.群事件_允许发起新的群聊:
        # data.self_id 框架QQ
        # data.group_id 发生群号
        # data.group_name 发生群名
        pass

    elif data.event_type == datatypes.群事件_禁止发起新的群聊:
        # data.self_id 框架QQ
        # data.group_id 发生群号
        # data.group_name 发生群名
        pass

    elif data.event_type == datatypes.群事件_允许上传群文件:
        # data.self_id 框架QQ
        # data.group_id 发生群号
        # data.group_name 发生群名
        pass

    elif data.event_type == datatypes.群事件_禁止上传群文件:
        # data.self_id 框架QQ
        # data.group_id 发生群号
        # data.group_name 发生群名
        pass

    elif data.event_type == datatypes.群事件_允许上传相册:
        # data.self_id 框架QQ
        # data.group_id 发生群号
        # data.group_name 发生群名
        pass

    elif data.event_type == datatypes.群事件_禁止上传相册:
        # data.self_id 框架QQ
        # data.group_id 发生群号
        # data.group_name 发生群名
        pass

    elif data.event_type == datatypes.群事件_展示成员群头衔:
        # data.self_id 框架QQ
        # data.group_id 发生群号
        # data.group_name 发生群名
        pass

    elif data.event_type == datatypes.群事件_隐藏成员群头衔:
        # data.self_id 框架QQ
        # data.group_id 发生群号
        # data.group_name 发生群名
        pass

    elif data.event_type == datatypes.群事件_我被踢出:
        # data.self_id 框架QQ
        # data.group_id 发生群号
        # data.group_name 发生群名
        pass

    elif data.event_type == datatypes.群事件_群名变更:
        # data.self_id 框架QQ
        # data.group_id 发生群号
        # data.group_name 新的群名
        # data.trigger_id 更名者QQ
        # data.trigger_nickname 更名者QQ昵称
        pass

    elif data.event_type == datatypes.群事件_系统提示:
        # data.self_id 框架QQ
        # data.group_id 来源群号
        # data.group_name 来源群名
        # data.trigger_id 提示触发者QQ
        # data.trigger_nickname 提示触发者QQ昵称
        # data.message QQ系统提示数据
        pass

    elif data.event_type == datatypes.群事件_群头像事件:
        # 这个事件表示此群更换了群头像或者上传了群头像(但是没换成这个)
        # data.self_id 框架QQ
        # data.group_id 发生群号
        # data.group_name 发生群名
        # data.trigger_id 操作者QQ
        # data.trigger_nickname 操作者QQ昵称
        pass

    elif data.event_type == datatypes.群事件_入场特效:
        # data.self_id 框架QQ
        # data.group_id 入场群号
        # data.group_name 入场群名
        # data.trigger_id 入场者QQ
        # data.trigger_nickname 入场者QQ昵称
        # data.message_timestamp 入场时间戳
        # data.message 入场特效Id
        pass

    elif data.event_type == datatypes.空间事件_与我相关:
        # data.self_id 框架QQ
        # data.oper_id 触发者QQ
        # data.oper_nickname 触发者QQ昵称
        # data.message 事件内容(包括说说点赞、评论、留言等，这个是腾讯返回的，不怎么详细)
        pass

    elif data.event_type == datatypes.框架事件_登录成功:
        # data.self_id 登录成功的框架QQ
        # data.trigger_id 登录成功的框架QQ
        # data.trigger_nickname 登录成功的框架QQ昵称
        # data.message_timestamp 登录成功的时间戳
        pass

    return False


class example_url(web.RequestHandler):
    """
    添加的url，可添加更多，无需可删除
    """

    def get(self):
        self.write('示例url')


def example_cmd(args: list):
    """
    添加的控制台指令处理函数，可添加更多，无需可删除

    :param args: 指令参数（就是空格分隔的内容）
    :return: 执行结果（会输出到控制台） 可以无返回值
    """
    return '示例指令'
