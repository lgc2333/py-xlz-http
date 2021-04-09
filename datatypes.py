"""数据类型"""
from typing import Callable, Optional


# 消息类型
class PrivateMsg(object):
    """
    私聊消息\n
    self_id: 框架QQ\n
    from_id: 发送人QQ\n
    group_id: 消息群号\n
    message: 消息内容\n
    message_req: 消息Req\n
    message_seq: 消息Seq\n
    message_random: 消息Random\n
    message_hand: 数据指针\n
    message_get_timestamp: 消息接收时间\n
    message_send_timestamp: 消息发送时间\n
    message_cut: 消息分片序列\n
    message_cut_num: 消息分片数量\n
    message_cut_iden: 消息分片标识\n
    message_type: 消息类型\n
    message_subtype: 消息子类型\n
    message_temp_subtype: 消息子临时类型\n
    post_type: 上报消息类型(判断私聊/群聊/事件)\n
    bubble_id: 气泡Id\n
    redpack_type: 红包类型\n
    inter_token: 会话token\n
    event_from_id: 事件来源QQ\n
    event_from_nickname: 事件来源QQ昵称\n
    file_id: 文件Id\n
    file_md5: 文件Md5\n
    filename: 文件名\n
    file_size: 文件大小\n
    access_token: 用来判断通信权限\n
    plugin_version: 插件版本(1.2.1版本新增)
    """

    def __init__(self, data):
        self.self_id: str = data['self_id'][0].decode('utf-8').replace('[br]', '\n')
        self.from_id: str = data['from_id'][0].decode('utf-8').replace('[br]', '\n')
        self.group_id: str = data['group_id'][0].decode('utf-8').replace('[br]', '\n')
        self.message: str = data['message'][0].decode('utf-8').replace('[br]', '\n')
        self.message_req: str = data['message_req'][0].decode('utf-8').replace('[br]', '\n')
        self.message_seq: str = data['message_seq'][0].decode('utf-8').replace('[br]', '\n')
        self.message_random: str = data['message_random'][0].decode('utf-8').replace('[br]', '\n')
        self.message_hand: str = data['message_hand'][0].decode('utf-8').replace('[br]', '\n')
        self.message_get_timestamp: str = data['message_get_timestamp'][0].decode('utf-8').replace('[br]', '\n')
        self.message_send_timestamp: str = data['message_send_timestamp'][0].decode('utf-8').replace('[br]', '\n')
        self.message_cut: str = data['message_cut'][0].decode('utf-8').replace('[br]', '\n')
        self.message_cut_num: str = data['message_cut_num'][0].decode('utf-8').replace('[br]', '\n')
        self.message_cut_iden: str = data['message_cut_iden'][0].decode('utf-8').replace('[br]', '\n')
        self.message_type: str = data['message_type'][0].decode('utf-8').replace('[br]', '\n')
        self.message_subtype: str = data['message_subtype'][0].decode('utf-8').replace('[br]', '\n')
        self.message_temp_subtype: str = data['message_temp_subtype'][0].decode('utf-8').replace('[br]', '\n')
        self.post_type: str = data['post_type'][0].decode('utf-8').replace('[br]', '\n')
        self.bubble_id: str = data['bubble_id'][0].decode('utf-8').replace('[br]', '\n')
        self.redpack_type: str = data['redpack_type'][0].decode('utf-8').replace('[br]', '\n')
        self.inter_token: str = data['inter_token'][0].decode('utf-8').replace('[br]', '\n')
        self.event_from_id: str = data['event_from_id'][0].decode('utf-8').replace('[br]', '\n')
        self.event_from_nickname: str = data['event_from_nickname'][0].decode('utf-8').replace('[br]', '\n')
        self.file_id: str = data['file_id'][0].decode('utf-8').replace('[br]', '\n')
        self.file_md5: str = data['file_md5'][0].decode('utf-8').replace('[br]', '\n')
        self.filename: str = data['filename'][0].decode('utf-8').replace('[br]', '\n')
        self.file_size: str = data['file_size'][0].decode('utf-8').replace('[br]', '\n')
        self.access_token: str = data['access_token'][0].decode('utf-8').replace('[br]', '\n')
        self.plugin_version: str = data['plugin_version'][0].decode('utf-8').replace('[br]', '\n')


class GroupMsg(object):
    """
    群聊消息\n
    self_id: 框架QQ\n
    from_id: 发送人QQ\n
    group_id: 消息群号\n
    group_name: 来源群名称\n
    message: 消息内容\n
    message_req: 消息Req\n
    message_random: 消息Random\n
    message_hand: 数据指针\n
    message_get_timestamp: 消息接收时间\n
    message_send_timestamp: 消息发送时间\n
    message_cut: 消息分片序列\n
    message_cut_num: 消息分片数量\n
    message_cut_iden: 消息分片标识\n
    message_subtype: 消息类型(目测没啥用)\n
    post_type: 上报消息类型(判断私聊/群聊/事件)\n
    from_gm_card: 发送人群名片\n
    from_gm_special_title: 发送人群头衔\n
    reply_to_message: 回复对象消息内容\n
    bubble_id: 气泡Id\n
    anonymous_self_id: 框架QQ匿名Id\n
    temp_parm: 保留参数\n
    file_id: 文件Id\n
    file_md5: 文件Md5\n
    filename: 文件名\n
    file_size: 文件大小\n
    message_appid: 消息appid\n
    access_token: 用来判断通信权限\n
    plugin_version: 插件版本(1.2.1版本新增)
    """

    def __init__(self, data):
        self.self_id: str = data['self_id'][0].decode('utf-8').replace('[br]', '\n')
        self.from_id: str = data['from_id'][0].decode('utf-8').replace('[br]', '\n')
        self.group_id: str = data['group_id'][0].decode('utf-8').replace('[br]', '\n')
        self.group_name: str = data['group_name'][0].decode('utf-8').replace('[br]', '\n')
        self.message: str = data['message'][0].decode('utf-8').replace('[br]', '\n')
        self.message_req: str = data['message_req'][0].decode('utf-8').replace('[br]', '\n')
        self.message_random: str = data['message_random'][0].decode('utf-8').replace('[br]', '\n')
        self.message_hand: str = data['message_hand'][0].decode('utf-8').replace('[br]', '\n')
        self.message_get_timestamp: str = data['message_get_timestamp'][0].decode('utf-8').replace('[br]', '\n')
        self.message_send_timestamp: str = data['message_send_timestamp'][0].decode('utf-8').replace('[br]', '\n')
        self.message_cut: str = data['message_cut'][0].decode('utf-8').replace('[br]', '\n')
        self.message_cut_num: str = data['message_cut_num'][0].decode('utf-8').replace('[br]', '\n')
        self.message_cut_iden: str = data['message_cut_iden'][0].decode('utf-8').replace('[br]', '\n')
        self.message_subtype: str = data['message_subtype'][0].decode('utf-8').replace('[br]', '\n')
        self.post_type: str = data['post_type'][0].decode('utf-8').replace('[br]', '\n')
        self.from_gm_card: str = data['from_gm_card'][0].decode('utf-8').replace('[br]', '\n')
        self.from_gm_special_title: str = data['from_gm_special_title'][0].decode('utf-8').replace('[br]', '\n')
        self.reply_to_message: str = data['reply_to_message'][0].decode('utf-8').replace('[br]', '\n')
        self.bubble_id: str = data['bubble_id'][0].decode('utf-8').replace('[br]', '\n')
        self.anonymous_self_id: str = data['anonymous_self_id'][0].decode('utf-8').replace('[br]', '\n')
        self.temp_parm: str = data['temp_parm'][0].decode('utf-8').replace('[br]', '\n')
        self.file_id: str = data['file_id'][0].decode('utf-8').replace('[br]', '\n')
        self.file_md5: str = data['file_md5'][0].decode('utf-8').replace('[br]', '\n')
        self.filename: str = data['filename'][0].decode('utf-8').replace('[br]', '\n')
        self.file_size: str = data['file_size'][0].decode('utf-8').replace('[br]', '\n')
        self.message_appid: str = data['message_appid'][0].decode('utf-8').replace('[br]', '\n')
        self.access_token: str = data['access_token'][0].decode('utf-8').replace('[br]', '\n')
        self.plugin_version: str = data['plugin_version'][0].decode('utf-8').replace('[br]', '\n')


class EventMsg(object):
    """
    事件消息\n
    self_id: 框架QQ\n
    group_id: 来源群号\n
    group_name: 来源群名\n
    oper_id: 操作QQ\n
    oper_nickname: 操作QQ昵称\n
    trigger_id: 触发QQ\n
    trigger_nickname: 触发QQ昵称\n
    message: 消息内容\n
    message_seq: 消息Seq\n
    message_hand: 数据指针\n
    message_timestamp: 消息时间戳\n
    post_type: 上报消息类型(判断私聊/群聊/事件)\n
    event_type: 事件类型\n
    event_subtype: 事件子类型\n
    access_token: 用来判断通信权限\n
    plugin_version: 插件版本(1.2.1版本新增)
    """

    def __init__(self, data):
        self.self_id: str = data['self_id'][0].decode('utf-8').replace('[br]', '\n')
        self.group_id: str = data['group_id'][0].decode('utf-8').replace('[br]', '\n')
        self.group_name: str = data['group_name'][0].decode('utf-8').replace('[br]', '\n')
        self.oper_id: str = data['oper_id'][0].decode('utf-8').replace('[br]', '\n')
        self.oper_nickname: str = data['oper_nickname'][0].decode('utf-8').replace('[br]', '\n')
        self.trigger_id: str = data['trigger_id'][0].decode('utf-8').replace('[br]', '\n')
        self.trigger_nickname: str = data['trigger_nickname'][0].decode('utf-8').replace('[br]', '\n')
        self.message: str = data['message'][0].decode('utf-8').replace('[br]', '\n')
        self.message_seq: str = data['message_seq'][0].decode('utf-8').replace('[br]', '\n')
        self.message_hand: str = data['message_hand'][0].decode('utf-8').replace('[br]', '\n')
        self.message_timestamp: str = data['message_timestamp'][0].decode('utf-8').replace('[br]', '\n')
        self.post_type: str = data['post_type'][0].decode('utf-8').replace('[br]', '\n')
        self.event_type: str = data['event_type'][0].decode('utf-8').replace('[br]', '\n')
        self.event_subtype: str = data['event_subtype'][0].decode('utf-8').replace('[br]', '\n')
        self.access_token: str = data['access_token'][0].decode('utf-8').replace('[br]', '\n')
        self.plugin_version: str = data['plugin_version'][0].decode('utf-8').replace('[br]', '\n')


class PluginInfo(object):
    """
    插件信息\n
    name: 插件名\n
    author: 作者\n
    version: 版本号\n
    description: 简介\n
    priority: 优先级，数字越大消息处理函数越先执行，如无特殊需要不要改动\n
    func_private: 私聊消息处理函数\n
    func_group: 群聊消息处理函数\n
    func_event: 事件消息处理函数\n
    listen_urls: 向服务器添加url，可设置多个 例[('/test', urltest)]，urltest继承tornado的web.RequestHandler类\n
    listen_commands: 向控制台添加指令，可设置多个 例[("test", cmdtest, "description")]，[0]为指令，[1]为处理函数，传入指令参数列表，[2]为指令介绍
    """

    def __init__(self, name: str, author: str, version: str = "1.0.0", description: str = "无", priority: int = 1,
                 func_private: Optional[Callable] = None, func_group: Optional[Callable] = None,
                 func_event: Optional[Callable] = None, listen_urls: Optional[list] = None,
                 listen_commands: Optional[list] = None):
        self.name: str = name
        self.author: str = author
        self.version: str = version
        self.description: str = description
        self.priority: int = priority
        self.func_private: Optional[Callable] = func_private
        self.func_group: Optional[Callable] = func_group
        self.func_event: Optional[Callable] = func_event
        self.listen_urls: Optional[list] = listen_urls
        self.listen_commands: Optional[list] = listen_commands


# 常量

# 消息类型
消息类型_好友通常消息 = '166'
消息类型_临时会话 = '141'

# 消息子临时类型
消息类型_临时会话_群临时 = '0'
消息类型_临时会话_公众号 = '129'
消息类型_临时会话_网页QQ咨询 = '201'

# 群事件类型
群事件_我被邀请加入群 = '1'
群事件_某人加入了群 = '2'
群事件_某人申请加群 = '3'
群事件_群被解散 = '4'
群事件_某人退出了群 = '5'
群事件_某人被踢出群 = '6'
群事件_某人被禁言 = '7'
群事件_某人撤回事件 = '8'
群事件_某人被取消管理 = '9'
群事件_某人被赋予管理 = '10'
群事件_开启全员禁言 = '11'
群事件_关闭全员禁言 = '12'
群事件_开启匿名聊天 = '13'
群事件_关闭匿名聊天 = '14'
群事件_开启坦白说 = '15'
群事件_关闭坦白说 = '16'
群事件_允许群临时会话 = '17'
群事件_禁止群临时会话 = '18'
群事件_允许发起新的群聊 = '19'
群事件_禁止发起新的群聊 = '20'
群事件_允许上传群文件 = '21'
群事件_禁止上传群文件 = '22'
群事件_允许上传相册 = '23'
群事件_禁止上传相册 = '24'
群事件_某人被邀请入群 = '25'
群事件_展示成员群头衔 = '26'
群事件_隐藏成员群头衔 = '27'
群事件_某人被解除禁言 = '28'
群事件_我被踢出 = '30'
群事件_群名变更 = '32'
群事件_系统提示 = '33'
群事件_群头像事件 = '34'
群事件_入场特效 = '35'

# 好友事件类型
好友事件_被好友删除 = '100'
好友事件_签名变更 = '101'
好友事件_昵称改变 = '102'
好友事件_某人撤回事件 = '103'
好友事件_有新好友 = '104'
好友事件_好友请求 = '105'
好友事件_对方同意了您的好友请求 = '106'
好友事件_对方拒绝了您的好友请求 = '107'
好友事件_资料卡点赞 = '108'
好友事件_签名点赞 = '109'
好友事件_签名回复 = '110'
好友事件_个性标签点赞 = '111'
好友事件_随心贴回复 = '112'
好友事件_随心贴增添 = '113'
好友事件_系统提示 = '114'

# 其他事件类型
框架事件_登录成功 = '31'
空间事件_与我相关 = '29'
