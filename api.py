import hashlib
import inspect
import os
import traceback
import urllib.parse

import requests

import config
from log import log


def _make_request(method, params, plugin_name):
    params['access_token'] = config.token
    data = '&'.join([
        f'{x}={urllib.parse.quote(str(params[x]))}' for x in params.keys() if (params[x] is not None)
    ]).encode('utf-8')  # 由于插件的一些特性，只能这么传参了
    try:
        ret = requests.post(
            config.plugin_api + urllib.parse.quote(method),
            data=data,
        )
    except Exception:
        log(f'{plugin_name} -> {method} -> 失败\n{traceback.format_exc()}', 'APIS')
        return False
    if not ret.status_code == 200:
        log(f'{plugin_name} -> {method} -> 状态码：{ret.status_code}', 'APIS')
        return False
    log(f'{plugin_name} -> {method} -> {ret.text}', 'APIS')
    return ret.text


def _get_plugin_name():
    stack = inspect.stack()[2]
    return f"{stack.filename[stack.filename.rfind(os.sep) + 1:stack.filename.rfind('.')]}"


def 输出日志(text: str):
    """
    输出控制台日志

    :param text: 日志文本
    """
    log(_get_plugin_name() + ' -> ' + text, 'PLUGIN')


def 文件写到服务器(file: bytes, name: str = None):
    """
    将本地文件写到服务器，返回不带域名相对路径，如/file/xxx.png，写到文件失败返回False

    :param file: 文件内容
    :param name: 文件名，不填为文件MD5
    :return: 文件相对路径
    """
    if not name:
        md5 = hashlib.md5()
        md5.update(file)
        name = md5.hexdigest()
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    try:
        with open('tmp/' + name, 'wb') as f:
            f.write(file)
    except:
        return False
    return 'tmp/' + name


def 取图片文本代码(file: str, is_flash: bool = None):
    """
    取oopshttpapi的图片文本代码

    :param file: 图片文件链接
    :param is_flash: 是否闪图
    :return: 文本代码
    """
    return f'[oq:pic={file}{",flash" if is_flash else ""}]'


def 取语音文本代码(file: str, type: int = 0, text: str = ''):
    """
    取oopshttpapi的语音文本代码

    :param file: 语音文件链接
    :param type: 0普通语音,1变声语音,2文字语音,3红包匹配语音
    :param text: 文字语音填附加文字(腾讯貌似会自动替换为语音对应的文本),红包匹配语音评级填a、b、s、ss、sss，注意是小写 其他类型语音可不填
    :return: 文本代码
    """
    return f'[oq:audio={file},{type},{text},0]'


def 取插件数据目录():
    """
    取插件数据存放目录，插件数据建议存放到此文件夹，返回末尾带/的相对路径
    """
    path = 'data/' + _get_plugin_name() + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def 发送消息(self_id, message, group_id=None, to_id=None, message_random=None, message_req=None, logic=False):
    """
    发送消息

    :param self_id: 框架QQ(长整数型)
    :param message: 发送内容(文本型)
    :param to_id: 好友或目标QQ(长整数型,可空,当本参数有效时,优先发送私聊消息)
    :param group_id: 群号(长整数型,可空,当to_id无效时,发送群聊消息)
    :param message_random: 消息Random(长整数型,可空,撤回私聊消息用,群聊无效) //作者注：此参数无效
    :param message_req: 消息Req(整数型,可空,撤回私聊消息用,群聊无效) //作者注：此参数无效
    :param logic: 匿名发送(逻辑型,可空,只有发送群聊时才有效)
    """
    method = "发送消息"
    params = {'self_id': self_id, 'group_id': group_id, 'to_id': to_id, 'message': message,
              'message_random': message_random, 'message_req': message_req, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 发送好友消息(self_id, to_id, message, message_random=None, message_req=None):
    """
    发送好友消息

    :param self_id: 框架QQ(长整数型)
    :param to_id: 好友QQ(长整数型)
    :param message: 发送内容(文本型)
    :param message_random: 消息Random(长整数型,可空,撤回消息用) //作者注：此参数无效
    :param message_req: 消息Req(整数型,可空,撤回消息用) //作者注：此参数无效
    """
    method = "发送好友消息"
    params = {'self_id': self_id, 'to_id': to_id, 'message': message, 'message_random': message_random,
              'message_req': message_req}
    return _make_request(method, params, _get_plugin_name())


def 发送群消息(self_id, group_id, message, logic=False):
    """
    发送群消息

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param message: 发送内容(文本型)
    :param logic: 匿名发送(逻辑型,可空)
    """
    method = "发送群消息"
    params = {'self_id': self_id, 'group_id': group_id, 'message': message, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 发送群临时消息(self_id, group_id, to_id, message, message_random=None, message_req=None):
    """
    发送群临时消息

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param to_id: 对方QQ(长整数型)
    :param message: 发送内容(文本型)
    :param message_random: 消息Random(长整数型,可空,撤回消息用) //作者注：此参数无效
    :param message_req: 消息Req(整数型,可空,撤回消息用) //作者注：此参数无效
    """
    method = "发送群临时消息"
    params = {'self_id': self_id, 'group_id': group_id, 'to_id': to_id, 'message': message,
              'message_random': message_random, 'message_req': message_req}
    return _make_request(method, params, _get_plugin_name())


def 添加好友(self_id, to_id, add_info=None, remark=None):
    """
    添加好友

    :param self_id: 框架QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    :param add_info: 可设置回答问题答案或是验证消息，多个问题答案用"|"分隔开(文本型)
    :param remark: 备注(文本型,自定义给对方的备注)
    """
    method = "添加好友"
    params = {'self_id': self_id, 'to_id': to_id, 'add_info': add_info, 'remark': remark}
    return _make_request(method, params, _get_plugin_name())


def 添加群(self_id, group_id, add_info=None):
    """
    添加群

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param add_info: 验证消息(文本型,可设置回答问题答案或是验证消息)
    """
    method = "添加群"
    params = {'self_id': self_id, 'group_id': group_id, 'add_info': add_info}
    return _make_request(method, params, _get_plugin_name())


def 删除好友(self_id, to_id):
    """
    删除好友

    :param self_id: 框架QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    """
    method = "删除好友"
    params = {'self_id': self_id, 'to_id': to_id}
    return _make_request(method, params, _get_plugin_name())


def 置屏蔽好友(self_id, to_id, logic=False):
    """
    置屏蔽好友

    :param self_id: 框架QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    :param logic: 是否屏蔽(逻辑型)
    """
    method = "置屏蔽好友"
    params = {'self_id': self_id, 'to_id': to_id, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 置特别关心好友(self_id, to_id, logic=False):
    """
    置特别关心好友

    :param self_id: 框架QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    :param logic: 是否关心(逻辑型)
    """
    method = "置特别关心好友"
    params = {'self_id': self_id, 'to_id': to_id, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 发送好友json消息(self_id, to_id, message, message_random=None, message_req=None):
    """
    发送好友json消息

    :param self_id: 框架QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    :param message: json代码(文本型,该接口的message请用标准json代码)
    :param message_random: 消息Random(长整数型,可空,撤回消息用) //作者注：此参数无效
    :param message_req: 消息Req(整数型,可空,撤回消息用) //作者注：此参数无效
    """
    method = "发送好友json消息"
    params = {'self_id': self_id, 'to_id': to_id, 'message': message, 'message_random': message_random,
              'message_req': message_req}
    return _make_request(method, params, _get_plugin_name())


def 发送群json消息(self_id, group_id, message, logic=False):
    """
    发送群json消息

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param message: json代码(文本型,该接口的message请用标准json代码)
    :param logic: 匿名发送(逻辑型,可空)
    """
    method = "发送群json消息"
    params = {'self_id': self_id, 'group_id': group_id, 'message': message, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 上传好友图片(self_id, to_id, file_url, logic=False):
    """
    上传好友图片

    :param self_id: 框架QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    :param file_url: 图片地址(文本型,目前只接受图片地址,由于超过4m的图片数据流转码后字符串异常巨大会造成读入延迟而影响体验,建议使用缓存函数将图片缓存到文件,以文件地址的方式传递)
    :param logic: 是否闪照(逻辑型,可空)
    """
    method = "上传好友图片"
    params = {'self_id': self_id, 'to_id': to_id, 'file_url': file_url, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 上传群图片(self_id, group_id, file_url, logic=False):
    """
    上传群图片

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param file_url: 图片地址(文本型,目前只接受图片地址)
    :param logic: 是否闪照(逻辑型,可空)
    """
    method = "上传群图片"
    params = {'self_id': self_id, 'group_id': group_id, 'file_url': file_url, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 上传好友语音(self_id, to_id, file_url, audio_type=None, audio_add=None):
    """
    上传好友语音

    :param self_id: 框架QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    :param file_url: 语音文件地址(文本型,目前只接受文件地址)
    :param audio_type: 语音类型(整数型,可空,0普通语音,1变声语音,2文字语音,3红包匹配语音)
    :param audio_add: 语音文字(文本型,可空,文字语音填附加文字(腾讯貌似会自动替换为语音对应的文本),匹配语音填a、b、s、ss、sss，注意是小写)
    """
    method = "上传好友语音"
    params = {'self_id': self_id, 'to_id': to_id, 'file_url': file_url, 'audio_type': audio_type,
              'audio_add': audio_add}
    return _make_request(method, params, _get_plugin_name())


def 上传群语音(self_id, group_id, file_url, audio_type=None, audio_add=None):
    """
    上传群语音

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param file_url: 语音文件地址(文本型,目前只接受文件地址)
    :param audio_type: 语音类型(整数型,可空,0普通语音,1变声语音,2文字语音,3红包匹配语音)
    :param audio_add: 语音文字(文本型,可空,文字语音填附加文字(腾讯貌似会自动替换为语音对应的文本),匹配语音填a、b、s、ss、sss，注意是小写)
    """
    method = "上传群语音"
    params = {'self_id': self_id, 'group_id': group_id, 'file_url': file_url, 'audio_type': audio_type,
              'audio_add': audio_add}
    return _make_request(method, params, _get_plugin_name())


def 上传头像(self_id, file_url):
    """
    上传头像

    :param self_id: 框架QQ(长整数型)
    :param file_url: 图片地址(文本型,目前只接受图片地址)
    """
    method = "上传头像"
    params = {'self_id': self_id, 'file_url': file_url}
    return _make_request(method, params, _get_plugin_name())


def silk解码(file_url):
    """
    silk解码 (会将文件字节集转为base64,所以控制文件大小在2m以内,否则太大可能出现异常情况)

    :param file_url: 语音文件地址(文本型,目前只接受图片地址)
    """
    method = "silk解码 "
    params = {'file_url': file_url}
    return _make_request(method, params, _get_plugin_name())


def silk编码(file_url):
    """
    silk编码 (会将文件字节集转为base64,所以控制文件大小在2m以内,否则太大可能出现异常情况)

    :param file_url: 语音文件地址(文本型,目前只接受图片地址)
    """
    method = "silk编码 "
    params = {'file_url': file_url}
    return _make_request(method, params, _get_plugin_name())


def amr编码(file_url):
    """
    amr编码 (会将文件字节集转为base64,所以控制文件大小在2m以内,否则太大可能出现异常情况)

    :param file_url: 语音文件地址(文本型,目前只接受图片地址)
    """
    method = "amr编码 "
    params = {'file_url': file_url}
    return _make_request(method, params, _get_plugin_name())


def 设置群名片(self_id, group_id, to_id, new_card):
    """
    设置群名片

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param to_id: 对方QQ(长整数型,可以是自己，无权限修改别人时会失败)
    :param new_card: 新名片(文本型)
    """
    method = "设置群名片"
    params = {'self_id': self_id, 'group_id': group_id, 'to_id': to_id, 'new_card': new_card}
    return _make_request(method, params, _get_plugin_name())


def 取昵称_从缓存(to_id):
    """
    取昵称_从缓存

    :param to_id: 对方QQ(长整数型)
    """
    method = "取昵称_从缓存"
    params = {'to_id': to_id}
    return _make_request(method, params, _get_plugin_name())


def 强制取昵称(self_id, to_id):
    """
    强制取昵称

    :param self_id: 框架QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    """
    method = "强制取昵称"
    params = {'self_id': self_id, 'to_id': to_id}
    return _make_request(method, params, _get_plugin_name())


def 取群名称_从缓存(group_id):
    """
    取群名称_从缓存

    :param group_id: 群号(长整数型)
    """
    method = "取群名称_从缓存"
    params = {'group_id': group_id}
    return _make_request(method, params, _get_plugin_name())


def 获取skey(self_id):
    """
    获取skey

    :param self_id: 框架QQ(长整数型)
    """
    method = "获取skey"
    params = {'self_id': self_id}
    return _make_request(method, params, _get_plugin_name())


def 获取pskey(self_id, domain):
    """
    获取pskey

    :param self_id: 框架QQ(长整数型)
    :param domain: 域(tenpay.com;openmobile.qq.com;docs.qq.com;connect.qq.com;qzone.qq.com;vip.qq.com;gamecenter.qq.com;qun.qq.com;game.qq.com;qqweb.qq.com;ti.qq.com;office.qq.com;mail.qq.com;mma.qq.com)
    """
    method = "获取pskey"
    params = {'self_id': self_id, 'domain': domain}
    return _make_request(method, params, _get_plugin_name())


def 获取clientkey(self_id):
    """
    获取clientkey

    :param self_id: 框架QQ(长整数型)
    """
    method = "获取clientkey"
    params = {'self_id': self_id}
    return _make_request(method, params, _get_plugin_name())


def 取框架QQ():
    """
    取框架QQ
    """
    method = "取框架QQ"
    params = {}
    return _make_request(method, params, _get_plugin_name())


def 取好友列表(self_id):
    """
    取好友列表

    :param self_id: 框架QQ(长整数型)
    """
    method = "取好友列表"
    params = {'self_id': self_id}
    return _make_request(method, params, _get_plugin_name())


def 取群列表(self_id):
    """
    取群列表

    :param self_id: 框架QQ(长整数型)
    """
    method = "取群列表"
    params = {'self_id': self_id}
    return _make_request(method, params, _get_plugin_name())


def 取群成员列表(self_id, group_id):
    """
    取群成员列表

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    """
    method = "取群成员列表"
    params = {'self_id': self_id, 'group_id': group_id}
    return _make_request(method, params, _get_plugin_name())


def 设置管理员(self_id, group_id, to_id, logic=False):
    """
    设置管理员

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param to_id: 群员QQ(长整数型)
    :param logic: 取消管理(逻辑型)
    """
    method = "设置管理员"
    params = {'self_id': self_id, 'group_id': group_id, 'to_id': to_id, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 取管理层列表(self_id, group_id):
    """
    取管理层列表(包括群主)

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    """
    method = "取管理层列表"
    params = {'self_id': self_id, 'group_id': group_id}
    return _make_request(method, params, _get_plugin_name())


def 取群名片(self_id, group_id, to_id):
    """
    取群名片

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param to_id: 群员QQ(长整数型)
    """
    method = "取群名片"
    params = {'self_id': self_id, 'group_id': group_id, 'to_id': to_id}
    return _make_request(method, params, _get_plugin_name())


def 取个性签名(self_id, to_id):
    """
    取个性签名

    :param self_id: 框架QQ(长整数型)
    :param to_id: 群员QQ(长整数型)
    """
    method = "取个性签名"
    params = {'self_id': self_id, 'to_id': to_id}
    return _make_request(method, params, _get_plugin_name())


def 修改昵称(self_id, nickname):
    """
    修改昵称

    :param self_id: 框架QQ(长整数型)
    :param nickname: 昵称(文本型)
    """
    method = "修改昵称"
    params = {'self_id': self_id, 'nickname': nickname}
    return _make_request(method, params, _get_plugin_name())


def 修改个性签名(self_id, sign, sign_locale=None):
    """
    修改个性签名

    :param self_id: 框架QQ(长整数型)
    :param sign: 签名(文本型)
    :param sign_locale: 签名地点(文本型,可空,可自定义签名地点)
    """
    method = "修改个性签名"
    params = {'self_id': self_id, 'sign': sign, 'sign_locale': sign_locale}
    return _make_request(method, params, _get_plugin_name())


def 删除群成员(self_id, group_id, to_id, logic=False):
    """
    删除群成员

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param to_id: 群员QQ(长整数型)
    :param logic: 拒绝加群申请(逻辑型)
    """
    method = "删除群成员"
    params = {'self_id': self_id, 'group_id': group_id, 'to_id': to_id, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 禁言群成员(self_id, group_id, to_id, ban_time=0):
    """
    禁言群成员

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param to_id: 群员QQ(长整数型)
    :param ban_time: 禁言时长(整数型,单位:秒,为0时解除禁言)
    """
    method = "禁言群成员"
    params = {'self_id': self_id, 'group_id': group_id, 'to_id': to_id, 'ban_time': ban_time}
    return _make_request(method, params, _get_plugin_name())


def 退群(self_id, group_id):
    """
    退群

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    """
    method = "退群"
    params = {'self_id': self_id, 'group_id': group_id}
    return _make_request(method, params, _get_plugin_name())


def 解散群(self_id, group_id):
    """
    解散群

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    """
    method = "解散群"
    params = {'self_id': self_id, 'group_id': group_id}
    return _make_request(method, params, _get_plugin_name())


def 上传群头像(self_id, group_id, file_url):
    """
    上传群头像

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param file_url: 图片地址(文本型,目前只接受图片地址)
    """
    method = "上传群头像"
    params = {'self_id': self_id, 'group_id': group_id, 'file_url': file_url}
    return _make_request(method, params, _get_plugin_name())


def 全员禁言(self_id, group_id, logic=False):
    """
    全员禁言

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param logic: 是否开启(逻辑型)
    """
    method = "全员禁言"
    params = {'self_id': self_id, 'group_id': group_id, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 群权限_发起新的群聊(self_id, group_id, logic=False):
    """
    群权限_发起新的群聊

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param logic: 是否允许(逻辑型)
    """
    method = "群权限_发起新的群聊"
    params = {'self_id': self_id, 'group_id': group_id, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 群权限_发起临时会话(self_id, group_id, logic=False):
    """
    群权限_发起临时会话

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param logic: 是否允许(逻辑型)
    """
    method = "群权限_发起临时会话"
    params = {'self_id': self_id, 'group_id': group_id, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 群权限_上传文件(self_id, group_id, logic=False):
    """
    群权限_上传文件

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param logic: 是否允许(逻辑型)
    """
    method = "群权限_上传文件"
    params = {'self_id': self_id, 'group_id': group_id, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 群权限_上传相册(self_id, group_id, logic=False):
    """
    群权限_上传相册

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param logic: 是否允许(逻辑型)
    """
    method = "群权限_上传相册"
    params = {'self_id': self_id, 'group_id': group_id, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 群权限_邀请好友加群(self_id, group_id, logic=False):
    """
    群权限_邀请好友加群

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param logic: 是否允许(逻辑型)
    """
    method = "群权限_邀请好友加群"
    params = {'self_id': self_id, 'group_id': group_id, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 群权限_匿名聊天(self_id, group_id, logic=False):
    """
    群权限_匿名聊天

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param logic: 是否允许(逻辑型)
    """
    method = "群权限_匿名聊天"
    params = {'self_id': self_id, 'group_id': group_id, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 群权限_坦白说(self_id, group_id, logic=False):
    """
    群权限_坦白说

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param logic: 是否允许(逻辑型)
    """
    method = "群权限_坦白说"
    params = {'self_id': self_id, 'group_id': group_id, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 群权限_新成员查看历史消息(self_id, group_id, logic=False):
    """
    群权限_新成员查看历史消息

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param logic: 是否允许(逻辑型)
    """
    method = "群权限_新成员查看历史消息"
    params = {'self_id': self_id, 'group_id': group_id, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 群权限_邀请方式设置(self_id, group_id, type):
    """
    群权限_邀请方式设置

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param type: 方式(1无需审核;2需要管理员审核;3 100人以内无需审核)
    """
    method = "群权限_邀请方式设置"
    params = {'self_id': self_id, 'group_id': group_id, 'type': type}
    return _make_request(method, params, _get_plugin_name())


def 撤回消息_群聊(self_id, group_id, message_random, message_req):
    """
    撤回消息_群聊

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param message_random: 消息Random(长整数型)
    :param message_req: 消息Req(整数型)
    """
    method = "撤回消息_群聊"
    params = {'self_id': self_id, 'group_id': group_id, 'message_random': message_random, 'message_req': message_req}
    return _make_request(method, params, _get_plugin_name())


def 撤回消息_私聊本身(self_id, to_id, message_random, message_req, message_timestamp):
    """
    撤回消息_私聊本身

    :param self_id: 框架QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    :param message_random: 消息Random(长整数型)
    :param message_req: 消息Req(整数型)
    :param message_timestamp: 消息接收时间(整数型)
    """
    method = "撤回消息_私聊本身"
    params = {'self_id': self_id, 'to_id': to_id, 'message_random': message_random, 'message_req': message_req,
              'message_timestamp': message_timestamp}
    return _make_request(method, params, _get_plugin_name())


def 设置位置共享(self_id, group_id, longitude=None, latitude=None, logic=False):
    """
    设置位置共享

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param longitude: 经度(定位)
    :param latitude: 纬度(定位)
    :param logic: 是否开启(逻辑型)
    """
    method = "设置位置共享"
    params = {'self_id': self_id, 'group_id': group_id, 'longitude': longitude, 'latitude': latitude, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 上报当前位置(self_id, group_id, longitude, latitude):
    """
    上报当前位置

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param longitude: 经度(定位)
    :param latitude: 纬度(定位)
    """
    method = "上报当前位置"
    params = {'self_id': self_id, 'group_id': group_id, 'longitude': longitude, 'latitude': latitude}
    return _make_request(method, params, _get_plugin_name())


def 是否被禁言(self_id, group_id):
    """
    是否被禁言 (返回禁言时长，单位秒，[失败/无权限/未被禁言]返回0)

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    """
    method = "是否被禁言 "
    params = {'self_id': self_id, 'group_id': group_id}
    return _make_request(method, params, _get_plugin_name())


def 处理群验证事件(self_id, group_id, trigger_id, oper_type, event_type, refuse_reason=None, message_seq=None):
    """
    处理群验证事件

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param trigger_id: 触发QQ(长整数型)
    :param oper_type: 操作类型(整数型,11同意 12拒绝  14忽略)
    :param event_type: 事件类型(整数型,3群事件_某人申请加群 1群事件_我被邀请加入群)
    :param refuse_reason: 拒绝理由(文本型,当拒绝时，可在此设置拒绝理由)
    :param message_seq: 消息Seq(整数型,可空,撤回消息用) //作者注：此参数无用
    """
    method = "处理群验证事件"
    params = {'self_id': self_id, 'group_id': group_id, 'trigger_id': trigger_id, 'oper_type': oper_type,
              'event_type': event_type, 'refuse_reason': refuse_reason, 'message_seq': message_seq}
    return _make_request(method, params, _get_plugin_name())


def 处理好友验证事件(self_id, trigger_id, oper_type, message_seq=None):
    """
    处理好友验证事件

    :param self_id: 框架QQ(长整数型)
    :param trigger_id: 触发QQ(长整数型)
    :param oper_type: 操作类型(整数型,1同意 2拒绝)
    :param message_seq: 消息Seq(整数型,可空,撤回消息用) //作者注：此参数无用
    """
    method = "处理好友验证事件"
    params = {'self_id': self_id, 'trigger_id': trigger_id, 'oper_type': oper_type, 'message_seq': message_seq}
    return _make_request(method, params, _get_plugin_name())


def 查看转发聊天记录内容(self_id, resid):
    """
    查看转发聊天记录内容

    :param self_id: 框架QQ(长整数型)
    :param resid: resId(文本型,可在xml消息代码中取到)
    """
    method = "查看转发聊天记录内容"
    params = {'self_id': self_id, 'resid': resid}
    return _make_request(method, params, _get_plugin_name())


def 上传群文件(self_id, group_id, local_file_path, folder_name=None):
    """
    上传群文件

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param local_file_path: 文件路径(文本型,框架所在环境的本地文件路径,非web端路径)
    :param folder_name: 文件夹名(文本型,可空,上传到哪个文件夹，填文件夹名，根目录留空或填/)
    """
    method = "上传群文件"
    params = {'self_id': self_id, 'group_id': group_id, 'local_file_path': local_file_path, 'folder_name': folder_name}
    return _make_request(method, params, _get_plugin_name())


def 创建群文件夹(self_id, group_id, folder_name):
    """
    创建群文件夹

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param folder_name: 文件夹名(文本型)
    """
    method = "创建群文件夹"
    params = {'self_id': self_id, 'group_id': group_id, 'folder_name': folder_name}
    return _make_request(method, params, _get_plugin_name())


def 重命名群文件夹(self_id, group_id, old_folder_name, new_folder_name):
    """
    重命名群文件夹

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param old_folder_name: 旧文件夹名(文本型)
    :param new_folder_name: 新文件夹名(文本型)
    """
    method = "重命名群文件夹"
    params = {'self_id': self_id, 'group_id': group_id, 'old_folder_name': old_folder_name,
              'new_folder_name': new_folder_name}
    return _make_request(method, params, _get_plugin_name())


def 删除群文件夹(self_id, group_id, folder_name):
    """
    删除群文件夹

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param folder_name: 文件夹名(文本型)
    """
    method = "删除群文件夹"
    params = {'self_id': self_id, 'group_id': group_id, 'folder_name': folder_name}
    return _make_request(method, params, _get_plugin_name())


def 删除群文件(self_id, group_id, file_id, folder_name=None):
    """
    删除群文件

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param file_id: 文件fileid(文本型)
    :param folder_name: 文件夹名(文本型,可空,文件所在的文件夹名，根目录留空或填/)
    """
    method = "删除群文件"
    params = {'self_id': self_id, 'group_id': group_id, 'file_id': file_id, 'folder_name': folder_name}
    return _make_request(method, params, _get_plugin_name())


def 保存文件到微云(self_id, group_id, file_id):
    """
    保存文件到微云

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param file_id: 文件fileid(文本型)
    """
    method = "保存文件到微云"
    params = {'self_id': self_id, 'group_id': group_id, 'file_id': file_id}
    return _make_request(method, params, _get_plugin_name())


def 移动群文件(self_id, group_id, file_id, cur_folder_name, obj_folder_name):
    """
    移动群文件

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param file_id: 文件fileid(文本型)
    :param cur_folder_name: 当前文件夹名(文本型)
    :param obj_folder_name: 目标文件夹名(文本型)
    """
    method = "移动群文件"
    params = {'self_id': self_id, 'group_id': group_id, 'file_id': file_id, 'cur_folder_name': cur_folder_name,
              'obj_folder_name': obj_folder_name}
    return _make_request(method, params, _get_plugin_name())


def 取群文件列表(self_id, group_id, folder_name=None):
    """
    取群文件列表 (PS:本接口在实际调试中从未正常通过测试,可能存在bug,请勿使用)

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param folder_name: 文件夹名(文本型,可空,欲查看的文件夹名，根目录留空或填/)
    """
    method = "取群文件列表 "
    params = {'self_id': self_id, 'group_id': group_id, 'folder_name': folder_name}
    return _make_request(method, params, _get_plugin_name())


def 设置在线状态(self_id, ol_main, ol_sun=None, ol_energy=None):
    """
    设置在线状态

    :param self_id: 框架QQ(长整数型)
    :param ol_main: main(整数型,11在线 31离开 41隐身 50忙碌 60Q我吧 70请勿打扰)
    :param ol_sun: sun(整数型,可空,当main=11时，可进一步设置 0普通在线 1000我的电量 1011信号弱 1024在线学习 1025在家旅游 1027TiMi中 1016睡觉中 1017游戏中 1018学习中 1019吃饭中 1021煲剧中 1022度假中 1032熬夜中 1050打球中 1051恋爱中 1052我没事 1028我在听歌)
    :param ol_energy: (整数型,可空,sun=1000时，可以设置上报电量，取值1到100)
    """
    method = "设置在线状态"
    params = {'self_id': self_id, 'ol_main': ol_main, 'ol_sun': ol_sun, 'ol_energy': ol_energy}
    return _make_request(method, params, _get_plugin_name())


def api是否有权限(authority):
    """
    api是否有权限

    :param authority: 权限(整数型)
    """
    method = "api是否有权限"
    params = {'authority': authority}
    return _make_request(method, params, _get_plugin_name())


def 取插件数据目录_xlz():
    """
    取插件数据目录
    """
    method = "取插件数据目录"
    params = {}
    return _make_request(method, params, _get_plugin_name())


def QQ点赞(self_id, to_id):
    """
    QQ点赞

    :param self_id: 框架QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    """
    method = "QQ点赞"
    params = {'self_id': self_id, 'to_id': to_id}
    return _make_request(method, params, _get_plugin_name())


def 取图片下载地址(pic_code, self_id=None, group_id=None):
    """
    取图片下载地址

    :param pic_code: 图片代码(文本型,支持群聊、私聊的图片、闪照代码，注意是图片代码) //作者注：这里的图片代码不是oopshttpapi的文本代码
    :param self_id: 框架QQ(长整数型,群聊图片必填,私聊图片必空)
    :param group_id: 群号(长整数型,群聊图片必填,私聊图片必空)
    """
    method = "取图片下载地址"
    params = {'pic_code': pic_code, 'self_id': self_id, 'group_id': group_id}
    return _make_request(method, params, _get_plugin_name())


def 查询好友信息(self_id, to_id):
    """
    查询好友信息
    用户服务信息说明:
    1svip 105star 102yellow 103green 101red 4film 104yellowlove 6musicpackage 107svip&film  109svip&green 110svip&kMusic

    :param self_id: 框架QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    """
    method = "查询好友信息"
    params = {'self_id': self_id, 'to_id': to_id}
    return _make_request(method, params, _get_plugin_name())


def 查询群信息(self_id, group_id):
    """
    查询群信息

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    """
    method = "查询群信息"
    params = {'self_id': self_id, 'group_id': group_id}
    return _make_request(method, params, _get_plugin_name())


def 重启框架():
    """
    重启框架 //作者注：慎用
    """
    method = "重启框架"
    params = {}
    return _make_request(method, params, _get_plugin_name())


def 群文件转发至群(self_id, from_group_id, group_id, file_id):
    """
    群文件转发至群

    :param self_id: 框架QQ(长整数型)
    :param from_group_id: 来源群号(长整数型)
    :param group_id: 目标群号(长整数型)
    :param file_id: 文件fileId(文本型)
    """
    method = "群文件转发至群"
    params = {'self_id': self_id, 'from_group_id': from_group_id, 'group_id': group_id, 'file_id': file_id}
    return _make_request(method, params, _get_plugin_name())


def 群文件转发至好友(self_id, group_id, to_id, file_id, filename, file_size, message_req=None, message_random=None,
             message_timestamp=None):
    """
    群文件转发至好友

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param to_id: 对方QQ(长整数型)
    :param file_id: 文件fileId(文本型)
    :param filename: 文件名(文本型)
    :param file_size: 文件大小(长整数型,文件大小)
    :param message_req: 消息Req(整数型,可空,撤回消息用) //作者注：该参数无用
    :param message_random: 消息Random(长整数型,可空,撤回消息用) //作者注：该参数无用
    :param message_timestamp: (整数型,可空,撤回消息用) //作者注：该参数无用
    """
    method = "群文件转发至好友"
    params = {'self_id': self_id, 'group_id': group_id, 'to_id': to_id, 'file_id': file_id, 'filename': filename,
              'file_size': file_size, 'message_req': message_req, 'message_random': message_random,
              'message_timestamp': message_timestamp}
    return _make_request(method, params, _get_plugin_name())


def 好友文件转发至好友(self_id, from_id, to_id, file_id, filename, file_size, message_req=None, message_random=None,
              message_timestamp=None):
    """
    好友文件转发至好友

    :param self_id: 框架QQ(长整数型)
    :param from_id: 来源QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    :param file_id: 文件fileId(文本型)
    :param filename: 文件名(文本型)
    :param file_size: 文件大小(长整数型,文件大小)
    :param message_req: 消息Req(整数型,可空,撤回消息用) //作者注：该参数无用
    :param message_random: 消息Random(长整数型,可空,撤回消息用) //作者注：该参数无用
    :param message_timestamp: (整数型,可空,撤回消息用) //作者注：该参数无用
    """
    method = "好友文件转发至好友"
    params = {'self_id': self_id, 'from_id': from_id, 'to_id': to_id, 'file_id': file_id, 'filename': filename,
              'file_size': file_size, 'message_req': message_req, 'message_random': message_random,
              'message_timestamp': message_timestamp}
    return _make_request(method, params, _get_plugin_name())


def 置群消息接收(self_id, group_id, type):
    """
    置群消息接收

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param type: 设置类型(整数型,1接收并提醒 2收进群助手 3屏蔽群消息 4接收不提醒)
    """
    method = "置群消息接收"
    params = {'self_id': self_id, 'group_id': group_id, 'type': type}
    return _make_request(method, params, _get_plugin_name())


def 发送免费礼物(self_id, group_id, to_id, gift_id):
    """
    发送免费礼物

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param to_id: 对方QQ(长整数型)
    :param gift_id: 礼物id(整数型,367告白话筒;299卡布奇诺;302猫咪手表;280牵你的手;281可爱猫咪;284神秘面具;285甜wink;286我超忙的;289快乐肥宅水;290幸运手链;313坚强;307绒绒手套; 312爱心口罩;308彩虹糖果)
    """
    method = "发送免费礼物"
    params = {'self_id': self_id, 'group_id': group_id, 'to_id': to_id, 'gift_id': gift_id}
    return _make_request(method, params, _get_plugin_name())


def 取好友在线状态(self_id, to_id):
    """
    取好友在线状态

    :param self_id: 框架QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    """
    method = "取好友在线状态"
    params = {'self_id': self_id, 'to_id': to_id}
    return _make_request(method, params, _get_plugin_name())


def 取QQ钱包个人信息(self_id):
    """
    取QQ钱包个人信息

    :param self_id: 框架QQ(长整数型)
    """
    method = "取QQ钱包个人信息"
    params = {'self_id': self_id}
    return _make_request(method, params, _get_plugin_name())


def 获取订单详情(self_id, order_id):
    """
    获取订单详情 (测试无效)

    :param self_id: 框架QQ(长整数型)
    :param order_id: 订单号(文本型)
    """
    method = "获取订单详情 "
    params = {'self_id': self_id, 'order_id': order_id}
    return _make_request(method, params, _get_plugin_name())


def 提交支付验证码(self_id, code_info, code, pay_pw):
    """
    提交支付验证码
    ++补充说明:使用[提交支付验证码]接口的前提条件一般是在使用[红包/转账]时使用银行卡支付, 需要短信验证码, 框架端会返回一个json, 该json包含了[验证码信息]所需数据,不需要json_decode解析
    :param self_id: 框架QQ(长整数型)
    :param code_info: 验证码信息(文本型,json)
    :param code: 短信验证码(文本型)
    :param pay_pw: 支付密码(文本型)
    """
    method = "提交支付验证码"
    params = {'self_id': self_id, 'code_info': code_info, 'code': code, 'pay_pw': pay_pw}
    return _make_request(method, params, _get_plugin_name())


def 分享音乐(self_id, to_guid, song, singer, jump_url, cover_url, file_url, app_type=None, share_type=None):
    """
    分享音乐

    :param self_id: 框架QQ(长整数型)
    :param to_guid: 分享的群或分享的好友QQ(长整数型, guid: group_user_id)
    :param song: 歌曲名(文本型)
    :param singer: 歌手名(文本型)
    :param jump_url: 跳转地址(文本型)
    :param cover_url: 封面地址(文本型)
    :param file_url: 文件地址(文本型)
    :param app_type: 应用类型(整数型,可空,0:QQ音乐 1:虾米音乐 2:酷我音乐 3:酷狗音乐 4:网易云音乐  默认0)
    :param share_type: 应用类型(整数型,可空,0私聊 1群聊  默认0)
    """
    method = "分享音乐"
    params = {'self_id': self_id, 'to_guid': to_guid, 'song': song, 'singer': singer, 'jump_url': jump_url,
              'cover_url': cover_url, 'file_url': file_url, 'app_type': app_type, 'share_type': share_type}
    return _make_request(method, params, _get_plugin_name())


def 更改群聊消息内容(message_hand, new_message):
    """
    更改群聊消息内容

    :param message_hand: 数据指针(整数型)
    :param new_message: 消息内容(文本型,要修改成的新消息内容)
    """
    method = "更改群聊消息内容"
    params = {'message_hand': message_hand, 'new_message': new_message}
    return _make_request(method, params, _get_plugin_name())


def 更改私聊消息内容(message_hand, new_message):
    """
    更改私聊消息内容

    :param message_hand: 数据指针(整数型)
    :param new_message: 消息内容(文本型,要修改成的新消息内容)
    """
    method = "更改私聊消息内容"
    params = {'message_hand': message_hand, 'new_message': new_message}
    return _make_request(method, params, _get_plugin_name())


def 群聊口令红包(self_id, num, cent, group_id, word, pay_pw, bank_card_serial=None):
    """
    群聊口令红包

    :param self_id: 框架QQ(长整数型)
    :param num: 红包总数(整数型)
    :param cent: 总金额(整数型,单位:分)
    :param group_id: 群号(长整数型)
    :param word: 口令(文本型)
    :param pay_pw: 支付密码(文本型)
    :param bank_card_serial: 银行卡序列(整数型,可空,大于0时使用银行卡支付)
    """
    method = "群聊口令红包"
    params = {'self_id': self_id, 'num': num, 'cent': cent, 'group_id': group_id, 'word': word, 'pay_pw': pay_pw,
              'bank_card_serial': bank_card_serial}
    return _make_request(method, params, _get_plugin_name())


def 群聊拼手气红包(self_id, num, cent, group_id, bless_word, pay_pw, skin_id=None, bank_card_serial=None):
    """
    群聊拼手气红包

    :param self_id: 框架QQ(长整数型)
    :param num: 红包总数(整数型)
    :param cent: 总金额(整数型,单位:分)
    :param group_id: 群号(长整数型)
    :param bless_word: 祝福语(文本型,支持emoji)
    :param pay_pw: 支付密码(文本型)
    :param skin_id: 红包皮肤id(整数型,可空)
    :param bank_card_serial: 银行卡序列(整数型,可空,大于0时使用银行卡支付)
    """
    method = "群聊拼手气红包"
    params = {'self_id': self_id, 'num': num, 'cent': cent, 'group_id': group_id, 'bless_word': bless_word,
              'skin_id': skin_id, 'pay_pw': pay_pw, 'bank_card_serial': bank_card_serial}
    return _make_request(method, params, _get_plugin_name())


def 群聊普通红包(self_id, num, cent, group_id, bless_word, pay_pw, skin_id=None, bank_card_serial=None):
    """
    群聊普通红包

    :param self_id: 框架QQ(长整数型)
    :param num: 红包总数(整数型)
    :param cent: 总金额(整数型,单位:分)
    :param group_id: 群号(长整数型)
    :param bless_word: 祝福语(文本型,支持emoji)
    :param pay_pw: 支付密码(文本型)
    :param skin_id: 红包皮肤id(整数型,可空)
    :param bank_card_serial: 银行卡序列(整数型,可空,大于0时使用银行卡支付)
    """
    method = "群聊普通红包"
    params = {'self_id': self_id, 'num': num, 'cent': cent, 'group_id': group_id, 'bless_word': bless_word,
              'skin_id': skin_id, 'pay_pw': pay_pw, 'bank_card_serial': bank_card_serial}
    return _make_request(method, params, _get_plugin_name())


def 群聊画图红包(self_id, num, cent, group_id, title, pay_pw, bank_card_serial=None):
    """
    群聊画图红包

    :param self_id: 框架QQ(长整数型)
    :param num: 红包总数(整数型)
    :param cent: 总金额(整数型,单位:分)
    :param group_id: 群号(长整数型)
    :param title: 题目名(文本型,只能填手Q有的,如:庄周)
    :param pay_pw: 支付密码(文本型)
    :param bank_card_serial: 银行卡序列(整数型,可空,大于0时使用银行卡支付)
    """
    method = "群聊画图红包"
    params = {'self_id': self_id, 'num': num, 'cent': cent, 'group_id': group_id, 'title': title, 'pay_pw': pay_pw,
              'bank_card_serial': bank_card_serial}
    return _make_request(method, params, _get_plugin_name())


def 群聊语音红包(self_id, num, cent, group_id, voice_word, pay_pw, bank_card_serial=None):
    """
    群聊语音红包

    :param self_id: 框架QQ(长整数型)
    :param num: 红包总数(整数型)
    :param cent: 总金额(整数型,单位:分)
    :param group_id: 群号(长整数型)
    :param voice_word: 语音口令(文本型)
    :param pay_pw: 支付密码(文本型)
    :param bank_card_serial: 银行卡序列(整数型,可空,大于0时使用银行卡支付)
    """
    method = "群聊语音红包"
    params = {'self_id': self_id, 'num': num, 'cent': cent, 'group_id': group_id, 'voice_word': voice_word,
              'pay_pw': pay_pw, 'bank_card_serial': bank_card_serial}
    return _make_request(method, params, _get_plugin_name())


def 群聊接龙红包(self_id, num, cent, group_id, jielong_word, pay_pw, bank_card_serial=None):
    """
    群聊接龙红包

    :param self_id: 框架QQ(长整数型)
    :param num: 红包总数(整数型)
    :param cent: 总金额(整数型,单位:分)
    :param group_id: 群号(长整数型)
    :param jielong_word: 接龙内容(文本型)
    :param pay_pw: 支付密码(文本型)
    :param bank_card_serial: 银行卡序列(整数型,可空,大于0时使用银行卡支付)
    """
    method = "群聊接龙红包"
    params = {'self_id': self_id, 'num': num, 'cent': cent, 'group_id': group_id, 'jielong_word': jielong_word,
              'pay_pw': pay_pw, 'bank_card_serial': bank_card_serial}
    return _make_request(method, params, _get_plugin_name())


def 群聊专属红包(self_id, num, cent, group_id, to_qq, bless_word, pay_pw, bank_card_serial=None, logic=False):
    """
    群聊专属红包

    :param self_id: 框架QQ(长整数型)
    :param num: 红包总数(整数型)
    :param cent: 总金额(整数型,单位:分)
    :param group_id: 群号(长整数型)
    :param to_qq: 领取人(文本型,多个领取人QQ用|分隔)
    :param bless_word: 接龙内容(文本型,支持emoji)
    :param pay_pw: 支付密码(文本型)
    :param bank_card_serial: 银行卡序列(整数型,可空,大于0时使用银行卡支付)
    :param logic: 是否均分(逻辑性,可空)
    """
    method = "群聊专属红包"
    params = {'self_id': self_id, 'num': num, 'cent': cent, 'group_id': group_id, 'to_qq': to_qq,
              'bless_word': bless_word, 'logic': logic, 'pay_pw': pay_pw, 'bank_card_serial': bank_card_serial}
    return _make_request(method, params, _get_plugin_name())


def 好友口令红包(self_id, num, cent, to_id, word, pay_pw, bank_card_serial=None):
    """
    好友口令红包(不支持非好友)

    :param self_id: 框架QQ(长整数型)
    :param num: 红包总数(整数型)
    :param cent: 总金额(整数型,单位:分)
    :param to_id: 对方QQ(长整数型)
    :param word: 口令(文本型)
    :param pay_pw: 支付密码(文本型)
    :param bank_card_serial: 银行卡序列(整数型,可空,大于0时使用银行卡支付)
    """
    method = "好友口令红包"
    params = {'self_id': self_id, 'num': num, 'cent': cent, 'to_id': to_id, 'word': word, 'pay_pw': pay_pw,
              'bank_card_serial': bank_card_serial}
    return _make_request(method, params, _get_plugin_name())


def 好友普通红包(self_id, num, cent, to_id, bless_word, pay_pw, skin_id=None, bank_card_serial=None):
    """
    好友普通红包(不支持非好友)

    :param self_id: 框架QQ(长整数型)
    :param num: 红包总数(整数型)
    :param cent: 总金额(整数型,单位:分)
    :param to_id: 对方QQ(长整数型)
    :param bless_word: 祝福语(文本型,支持emoji)
    :param pay_pw: 支付密码(文本型)
    :param skin_id: 红包皮肤id(整数型,可空)
    :param bank_card_serial: 银行卡序列(整数型,可空,大于0时使用银行卡支付)
    """
    method = "好友普通红包"
    params = {'self_id': self_id, 'num': num, 'cent': cent, 'to_id': to_id, 'bless_word': bless_word,
              'skin_id': skin_id, 'pay_pw': pay_pw, 'bank_card_serial': bank_card_serial}
    return _make_request(method, params, _get_plugin_name())


def 好友画图红包(self_id, num, cent, to_id, title, pay_pw, bank_card_serial=None):
    """
    好友画图红包(不支持非好友)

    :param self_id: 框架QQ(长整数型)
    :param num: 红包总数(整数型)
    :param cent: 总金额(整数型,单位:分)
    :param to_id: 对方QQ(长整数型)
    :param title: 题目名(文本型,只能填手Q有的,如:庄周)
    :param pay_pw: 支付密码(文本型)
    :param bank_card_serial: 银行卡序列(整数型,可空,大于0时使用银行卡支付)
    """
    method = "好友画图红包"
    params = {'self_id': self_id, 'num': num, 'cent': cent, 'to_id': to_id, 'title': title, 'pay_pw': pay_pw,
              'bank_card_serial': bank_card_serial}
    return _make_request(method, params, _get_plugin_name())


def 好友语音红包(self_id, num, cent, to_id, voice_word, pay_pw, bank_card_serial=None):
    """
    好友语音红包(不支持非好友)

    :param self_id: 框架QQ(长整数型)
    :param num: 红包总数(整数型)
    :param cent: 总金额(整数型,单位:分)
    :param to_id: 对方QQ(长整数型)
    :param voice_word: 语音口令(文本型)
    :param pay_pw: 支付密码(文本型)
    :param bank_card_serial: 银行卡序列(整数型,可空,大于0时使用银行卡支付)
    """
    method = "好友语音红包"
    params = {'self_id': self_id, 'num': num, 'cent': cent, 'to_id': to_id, 'voice_word': voice_word, 'pay_pw': pay_pw,
              'bank_card_serial': bank_card_serial}
    return _make_request(method, params, _get_plugin_name())


def 好友接龙红包(self_id, num, cent, to_id, jielong_word, pay_pw, bank_card_serial=None):
    """
    好友接龙红包(不支持非好友)

    :param self_id: 框架QQ(长整数型)
    :param num: 红包总数(整数型)
    :param cent: 总金额(整数型,单位:分)
    :param to_id: 对方QQ(长整数型)
    :param jielong_word: 接龙内容(文本型)
    :param pay_pw: 支付密码(文本型)
    :param bank_card_serial: 银行卡序列(整数型,可空,大于0时使用银行卡支付)
    """
    method = "好友接龙红包"
    params = {'self_id': self_id, 'num': num, 'cent': cent, 'to_id': to_id, 'jielong_word': jielong_word,
              'pay_pw': pay_pw, 'bank_card_serial': bank_card_serial}
    return _make_request(method, params, _get_plugin_name())


def 设置专属头衔(self_id, group_id, to_id, special_title):
    """
    设置专属头衔

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param to_id: 对方QQ(长整数型)
    :param special_title: 专属头衔(文本型)
    """
    method = "设置专属头衔"
    params = {'self_id': self_id, 'group_id': group_id, 'to_id': to_id, 'special_title': special_title}
    return _make_request(method, params, _get_plugin_name())


def 下线指定QQ(self_id):
    """
    下线指定QQ

    :param self_id: 框架QQ(长整数型)
    """
    method = "下线指定QQ"
    params = {'self_id': self_id}
    return _make_request(method, params, _get_plugin_name())


def 登录指定QQ(self_id):
    """
    登录指定QQ

    :param self_id: 框架QQ(长整数型)
    """
    method = "登录指定QQ"
    params = {'self_id': self_id}
    return _make_request(method, params, _get_plugin_name())


def 取群未领红包(self_id, group_id):
    """
    取群未领红包

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    """
    method = "取群未领红包"
    params = {'self_id': self_id, 'group_id': group_id}
    return _make_request(method, params, _get_plugin_name())


def 发送输入状态(self_id, to_id, input_state=None):
    """
    发送输入状态

    :param self_id: 框架QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    :param input_state: 输入状态(整数型,可空,默认为1,1:正在输入,2:关闭显示,3:正在说话)
    """
    method = "发送输入状态"
    params = {'self_id': self_id, 'to_id': to_id, 'input_state': input_state}
    return _make_request(method, params, _get_plugin_name())


def 修改资料(self_id, nickname=None, sex=None, birthday=None, occupation=None, co_name=None, location=None, hometown=None,
         email=None, description=None):
    """
    修改资料(生日、家乡、所在地 参数格式和子参数数量必须正确，否则修改资料无法成功，不需要修改的项就不要填)

    :param self_id: 框架QQ(长整数型)
    :param nickname: 昵称(文本型,可空)
    :param sex: 性别(整数型,可空,1:男 2:女,默认男)
    :param birthday: 生日(文本型,可空,格式：2020/5/5 均为整数)
    :param occupation: 职业(整数型,可空,1:IT,2:制造,3:医疗,4:金融,5:商业,6:文化,7:艺术,8:法律,9:教育,10:行政,11:模特,12:空姐,13:学生,14:其他职业，默认1)
    :param co_name: 公司名称(文本型,可空)
    :param location: 所在地(文本型,可空,国家代码|省份代码|市代码|区字母|区代码，如：49|13110|56|NK|51，表示中国江西省吉安市青原区，这些数据是腾讯的数据，非国际数据)
    :param hometown: 家乡(文本型,可空,同上)
    :param email: 邮箱(文本型,可空)
    :param description: 个人说明(文本型,可空)
    """
    method = "修改资料"
    params = {'self_id': self_id, 'nickname': nickname, 'sex': sex, 'birthday': birthday, 'occupation': occupation,
              'co_name': co_name, 'location': location, 'hometown': hometown, 'email': email,
              'description': description}
    return _make_request(method, params, _get_plugin_name())


def 取群文件下载地址(self_id, group_id, file_id, filename):
    """
    取群文件下载地址(文件下载地址在返回的json里面，具有时效性，请及时下载)

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param file_id: 文件fileId(文本型)
    :param filename: 文件名(文本型)
    """
    method = "取群文件下载地址"
    params = {'self_id': self_id, 'group_id': group_id, 'file_id': file_id, 'filename': filename}
    return _make_request(method, params, _get_plugin_name())


def 打好友电话(self_id, to_id):
    """
    打好友电话(不建议频繁使用)

    :param self_id: 框架QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    """
    method = "打好友电话"
    params = {'self_id': self_id, 'to_id': to_id}
    return _make_request(method, params, _get_plugin_name())


def 头像双击_好友(self_id, to_id):
    """
    头像双击_好友

    :param self_id: 框架QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    """
    method = "头像双击_好友"
    params = {'self_id': self_id, 'to_id': to_id}
    return _make_request(method, params, _get_plugin_name())


def 头像双击_群(self_id, to_id, group_id):
    """
    头像双击_群

    :param self_id: 框架QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    :param group_id: 群号(长整数型)
    """
    method = "头像双击_群"
    params = {'self_id': self_id, 'to_id': to_id, 'group_id': group_id}
    return _make_request(method, params, _get_plugin_name())


def 取群成员简略信息(self_id, group_id):
    """
    取群成员简略信息

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    """
    method = "取群成员简略信息"
    params = {'self_id': self_id, 'group_id': group_id}
    return _make_request(method, params, _get_plugin_name())


def 群聊置顶(self_id, group_id, logic=False):
    """
    群聊置顶

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param logic: 是否置顶,默认假(逻辑型)
    """
    method = "群聊置顶"
    params = {'self_id': self_id, 'group_id': group_id, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 私聊置顶(self_id, to_id, logic=False):
    """
    私聊置顶

    :param self_id: 框架QQ(长整数型)
    :param to_id: 群号(长整数型)
    :param logic: 是否置顶,默认假(逻辑型)
    """
    method = "私聊置顶"
    params = {'self_id': self_id, 'to_id': to_id, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 取加群链接(self_id, group_id):
    """
    取加群链接

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    """
    method = "取加群链接"
    params = {'self_id': self_id, 'group_id': group_id}
    return _make_request(method, params, _get_plugin_name())


def 设为精华(self_id, group_id, message_req, message_random):
    """
    设为精华(置指定群消息为精华内容,需要管理员权限)

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param message_req: 消息Req(整数型)
    :param message_random: 消息Random(长整数型)
    """
    method = "设为精华"
    params = {'self_id': self_id, 'group_id': group_id, 'message_req': message_req, 'message_random': message_random}
    return _make_request(method, params, _get_plugin_name())


def 群权限_设置群昵称规则(self_id, group_id, card_rule):
    """
    群权限_设置群昵称规则(需要管理员权限)

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param card_rule: 名片规则(文本型,对于易语言不支持的utf8字符,需usc2编码)
    """
    method = "群权限_设置群昵称规则"
    params = {'self_id': self_id, 'group_id': group_id, 'card_rule': card_rule}
    return _make_request(method, params, _get_plugin_name())


def 群权限_设置群发言频率(self_id, group_id, max_num):
    """
    群权限_设置群发言频率(需要管理员权限)

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param max_num: 限制条数(整数型,限制每分钟多少条发言,为0表示无限制)
    """
    method = "群权限_设置群发言频率"
    params = {'self_id': self_id, 'group_id': group_id, 'max_num': max_num}
    return _make_request(method, params, _get_plugin_name())


def 群权限_设置群查找方式(self_id, group_id, type=None):
    """
    群权限_设置群查找方式(需要管理员权限)

    :param self_id: 框架QQ(长整数型)
    :param group_id: 群号(长整数型)
    :param type: 查找方式(整数型,可空,0不允许,1通过群号或关键词,2仅可通过群号,默认1)
    """
    method = "群权限_设置群查找方式"
    params = {'self_id': self_id, 'group_id': group_id, 'type': type}
    return _make_request(method, params, _get_plugin_name())


def 邀请好友加群(self_id, group_id, to_id, from_group_id=None):
    """
    邀请好友加群(需要群聊开启了邀请)

    :param self_id: 框架QQ(长整数型)
    :param group_id: 目标群号(长整数型)
    :param to_id: 对方QQ(长整数型)
    :param from_group_id: 来源群号(长整数型,可空,若对方为群友,在此填入来源群号)
    """
    method = "邀请好友加群"
    params = {'self_id': self_id, 'group_id': group_id, 'to_id': to_id, 'from_group_id': from_group_id}
    return _make_request(method, params, _get_plugin_name())


def 置群内消息通知(self_id, group_id, to_id, type=None):
    """
    置群内消息通知(置群内指定QQ消息通知类型)

    :param self_id: 框架QQ(长整数型)
    :param group_id: 目标群号(长整数型)
    :param to_id: 对方QQ(长整数型)
    :param type: 通知类型(整数型,可空,0不接收此人消息,1特别关注,2接收此人消息,默认2)
    """
    method = "置群内消息通知"
    params = {'self_id': self_id, 'group_id': group_id, 'to_id': to_id, 'type': type}
    return _make_request(method, params, _get_plugin_name())


def 修改群名称(self_id, group_id, group_name):
    """
    修改群名称 (需要管理员权限)

    :param self_id: 框架QQ(长整数型)
    :param group_id: 目标群号(长整数型)
    :param group_name: 新的群名称(文本型)
    """
    method = "修改群名称 "
    params = {'self_id': self_id, 'group_id': group_id, 'group_name': group_name}
    return _make_request(method, params, _get_plugin_name())


def 重载自身(new_dll_path=None):
    """
    重载自身 //作者注：慎用且基本无用

    :param new_dll_path: 插件文件所在路径(文本型,可空)
    """
    method = "重载自身"
    params = {'new_dll_path': new_dll_path}
    return _make_request(method, params, _get_plugin_name())


def 下线PCQQ(self_id):
    """
    下线PCQQ

    :param self_id: 框架QQ(长整数型)
    """
    method = "下线PCQQ"
    params = {'self_id': self_id}
    return _make_request(method, params, _get_plugin_name())


def 登录网页取ck(self_id, callback_url, appid, daid):
    """
    登录网页取ck

    :param self_id: 框架QQ(长整数型)
    :param callback_url: 回调跳转地址(文本型,不能url编码!如QQ空间是:https://h5.qzone.qq.com/mqzone/index)
    :param appid: appid(文本型)
    :param daid: daid(文本型)
    """
    method = "登录网页取ck"
    params = {'self_id': self_id, 'callback_url': callback_url, 'appid': appid, 'daid': daid}
    return _make_request(method, params, _get_plugin_name())


def 发送群公告(self_id, group_id, title, content, image_url=None, video_url=None, popshow=None, confirm=None, istop=None,
          send=None, change_card=None):
    """
    发送群公告

    :param self_id: 框架QQ(长整数型)
    :param group_id: 目标群号(长整数型)
    :param title: 标题(文本型,支持emoji表情,如：\uD83D\uDE01)
    :param content: 内容(文本型,支持emoji表情,如：\uD83D\uDE01)
    :param image_url: 图片(文本型,可空,在公告当中插入图片,如果设置了[腾讯视频]参数,则不显示图片只显示视频)
    :param video_url: 视频(文本型,可空,公告当中插入视频,只支持腾讯视频,如:https://v.qq.com/x/cover/4gl2i78zd9idpi0/j0024zknymk.html)
    :param popshow: 弹窗展示(逻辑型,可空)
    :param confirm: 需要确认(逻辑型,可空)
    :param istop: 置顶(逻辑型,可空)
    :param send: 发送给新成员(逻辑型,可空)
    :param change_card: 引导修改群昵称(逻辑型,可空)
    """
    method = "发送群公告"
    params = {'self_id': self_id, 'group_id': group_id, 'title': title, 'content': content, 'image_url': image_url,
              'video_url': video_url, 'popshow': popshow, 'confirm': confirm, 'istop': istop, 'send': send,
              'change_card': change_card}
    return _make_request(method, params, _get_plugin_name())


def 取框架版本():
    """
    取框架版本
    """
    method = "取框架版本"
    params = {}
    return _make_request(method, params, _get_plugin_name())


def 取群成员信息(self_id, group_id, to_id):
    """
    取群成员信息(获取一个群成员的相关信息)

    :param self_id: 框架QQ(长整数型)
    :param group_id: 目标群号(长整数型)
    :param to_id: 对方QQ(文本型)
    """
    method = "取群成员信息"
    params = {'self_id': self_id, 'group_id': group_id, 'to_id': to_id}
    return _make_request(method, params, _get_plugin_name())


def 发送邮件(self_id, email, title, content):
    """
    发送邮件

    :param self_id: 框架QQ(长整数型)
    :param email: 邮箱地址(文本型)
    :param title: 邮件标题(文本型)
    :param content: 邮件内容(文本型,支持html)
    """
    method = "发送邮件"
    params = {'self_id': self_id, 'email': email, 'title': title, 'content': content}
    return _make_request(method, params, _get_plugin_name())


def 取钱包cookie(self_id):
    """
    取钱包cookie(敏感API,框架4h刷新一次)

    :param self_id: 框架QQ(长整数型)
    """
    method = "取钱包cookie"
    params = {'self_id': self_id}
    return _make_request(method, params, _get_plugin_name())


def 取群网页cookie(self_id):
    """
    取群网页cookie(敏感API,框架4h刷新一次)

    :param self_id: 框架QQ(长整数型)
    """
    method = "取群网页cookie"
    params = {'self_id': self_id}
    return _make_request(method, params, _get_plugin_name())


def 取手Q邮箱cookie(self_id):
    """
    取手Q邮箱cookie(敏感API,框架4h刷新一次,邮箱sid在cookie当中,键名为xxsid)

    :param self_id: 框架QQ(长整数型)
    """
    method = "取手Q邮箱cookie"
    params = {'self_id': self_id}
    return _make_request(method, params, _get_plugin_name())


def 转账(self_id, group_id, cent, to_id, type, pay_pw, msg=None, bank_card_serial=None):
    """
    转账

    :param self_id: 框架QQ(长整数型)
    :param group_id: 目标群号(长整数型)
    :param cent: 转账金额(整数型,单位:分)
    :param to_id: 对方QQ(长整数型)
    :param type: 转账类型(整数型,0好友转账,1陌生人转账,默认0)
    :param pay_pw: 支付密码(文本型)
    :param msg: 转账留言(文本型,可空,支持emoji)
    :param bank_card_serial: 银行卡序列(整数型,可空,大于0时使用银行卡支付)
    """
    method = "转账"
    params = {'self_id': self_id, 'group_id': group_id, 'cent': cent, 'to_id': to_id, 'msg': msg, 'type': type,
              'pay_pw': pay_pw, 'bank_card_serial': bank_card_serial}
    return _make_request(method, params, _get_plugin_name())


def 余额提现(self_id, cent, pay_pw, bank_card_serial):
    """
    余额提现

    :param self_id: 框架QQ(长整数型)
    :param cent: 提现金额(整数型,单位:分)
    :param pay_pw: 支付密码(文本型)
    :param bank_card_serial: 银行卡序列(整数型,大于0时使用银行卡支付)
    """
    method = "余额提现"
    params = {'self_id': self_id, 'cent': cent, 'pay_pw': pay_pw, 'bank_card_serial': bank_card_serial}
    return _make_request(method, params, _get_plugin_name())


def 取收款链接(self_id, msg, cent=None):
    """
    取收款链接(返回收款链接,可借此生成收款二维码)

    :param self_id: 框架QQ(长整数型)
    :param msg: 说明文本(文本型,备注)
    :param cent: 收款金额(整数型,可空,单位:分)
    """
    method = "取收款链接"
    params = {'self_id': self_id, 'cent': cent, 'msg': msg}
    return _make_request(method, params, _get_plugin_name())


def 取群小视频下载地址(self_id, group_id, from_id, param, hash1, filename):
    """
    取群小视频下载地址(成功返回json含下载链接)

    :param self_id: 框架QQ(长整数型)
    :param group_id: 目标群号(长整数型)
    :param from_id: 来源QQ(长整数型)
    :param param: 支付密码(文本型,可通过文本代码获取)
    :param hash1: 银行卡序列(文本型,可通过文本代码获取)
    :param filename: 文件名(文本型,xxx.mp4,必须带上文件后缀)
    """
    method = "取群小视频下载地址"
    params = {'self_id': self_id, 'group_id': group_id, 'from_id': from_id, 'param': param, 'hash1': hash1,
              'filename': filename}
    return _make_request(method, params, _get_plugin_name())


def 取私聊小视频下载地址(self_id, from_id, param, hash1, filename):
    """
    取私聊小视频下载地址(成功返回json含下载链接)

    :param self_id: 框架QQ(长整数型)
    :param from_id: 来源QQ(长整数型)
    :param param: 支付密码(文本型,可通过文本代码获取)
    :param hash1: 银行卡序列(文本型,可通过文本代码获取)
    :param filename: 文件名(文本型,xxx.mp4,必须带上文件后缀)
    """
    method = "取私聊小视频下载地址"
    params = {'self_id': self_id, 'from_id': from_id, 'param': param, 'hash1': hash1, 'filename': filename}
    return _make_request(method, params, _get_plugin_name())


def 上传小视频(self_id, group_id, file_path, cover_url):
    """
    上传小视频(成功返回文本代码,使用的手机录小视频入口,因此不支持较大文件)

    :param self_id: 框架QQ(长整数型)
    :param group_id: 目标群号(长整数型)
    :param file_path: 本地小视频路径(文本型,本地路径指框架端,当值为url地址时,框架端会自动缓存到本地后再上传)
    :param cover_url: 小视频封面图(文本型,图片地址,留空使用默认封面)
    """
    method = "上传小视频"
    params = {'self_id': self_id, 'group_id': group_id, 'file_path': file_path, 'cover_url': cover_url}
    return _make_request(method, params, _get_plugin_name())


def 发送好友xml消息(self_id, to_id, xml, msg_random=None, msg_req=None):
    """
    发送好友xml消息

    :param self_id: 框架QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    :param xml: xml代码(文本型)
    :param msg_random: Random(长整数型,可空,撤回消息用) //作者注：参数无用
    :param msg_req: Req(整数型,可空,撤回消息用) //作者注：参数无用
    """
    method = "发送好友xml消息"
    params = {'self_id': self_id, 'to_id': to_id, 'xml': xml, 'random': msg_random, 'req': msg_req}
    return _make_request(method, params, _get_plugin_name())


def 发送群xml消息(self_id, group_id, xml, logic=False):
    """
    发送群xml消息

    :param self_id: 框架QQ(长整数型)
    :param group_id: 目标群号(长整数型)
    :param xml: xml代码(文本型)
    :param logic: 匿名发送(逻辑型,可空)
    """
    method = "发送群xml消息"
    params = {'self_id': self_id, 'group_id': group_id, 'xml': xml, 'logic': logic}
    return _make_request(method, params, _get_plugin_name())


def 取群成员概况(self_id, group_id):
    """
    取群成员概况(成功返回json,含有群上限、群人数、群成员统计概况)

    :param self_id: 框架QQ(长整数型)
    :param group_id: 目标群号(长整数型)
    """
    method = "取群成员概况"
    params = {'self_id': self_id, 'group_id': group_id}
    return _make_request(method, params, _get_plugin_name())


def 添加好友_取验证类型(self_id, to_id):
    """
    添加好友_取验证类型(成功返回验证类型json,失败返回403无权限或404未找到对应框架QQ或405框架QQ未登录,ret：101已是好友 2拒绝添加 1需要身份验证 0任何人可添加 4需要回答问题,并返回所有需要回答的问题 3需要正确回答问题,并返回需要回答的问题)

    :param self_id: 框架QQ(长整数型)
    :param to_id: 对方QQ(长整数型)
    """
    method = "添加好友_取验证类型"
    params = {'self_id': self_id, 'to_id': to_id}
    return _make_request(method, params, _get_plugin_name())


def 群聊打卡(self_id, group_id):
    """
    群聊打卡(返回json)

    :param self_id: 框架QQ(长整数型)
    :param group_id: 目标群号(长整数型)
    """
    method = "群聊打卡"
    params = {'self_id': self_id, 'group_id': group_id}
    return _make_request(method, params, _get_plugin_name())


def 群聊签到(self_id, group_id, test=None):
    """
    群聊签到(暂不支持自定义内容)

    :param self_id: 框架QQ(长整数型)
    :param group_id: 目标群号(长整数型)
    :param test: 保留参数(文本型,可空)
    """
    method = "群聊签到"
    params = {'self_id': self_id, 'group_id': group_id, 'test': test}
    return _make_request(method, params, _get_plugin_name())


def 置群聊备注(self_id, group_id, remark=None):
    """
    置群聊备注

    :param self_id: 框架QQ(长整数型)
    :param group_id: 目标群号(长整数型)
    :param remark: 备注(文本型)
    """
    method = "置群聊备注"
    params = {'self_id': self_id, 'group_id': group_id, 'remark': remark}
    return _make_request(method, params, _get_plugin_name())


def 红包转发(self_id, rp_id, to_guid, type):
    """
    红包转发(转发自己的红包到其他群或好友)

    :param self_id: 框架QQ(长整数型)
    :param rp_id: 红包ID(文本型)
    :param to_guid: QQ/群号(长整数型,以type类型为准,如果是1则判断为QQ号否则判断为群号)
    :param type: 类型(整数型,1为好友,2为群)
    """
    method = "红包转发"
    params = {'self_id': self_id, 'rp_id': rp_id, 'to_guid': to_guid, 'type': type}
    return _make_request(method, params, _get_plugin_name())


def 发送数据包(self_id, ssoseq, wait_time=None):
    """
    发送数据包(向腾讯服务器发送数据包(完整的原始包),无权限等返回假,加密秘钥通过【取sessionkey】API获取)

    :param self_id: 框架QQ(长整数型)
    :param ssoseq: 包体序号(整数型)
    :param wait_time: 最大等待时长(整数型,可空)
    """
    method = "发送数据包"
    params = {'self_id': self_id, 'ssoseq': ssoseq, 'wait_time': wait_time}
    return _make_request(method, params, _get_plugin_name())


def 请求ssoseq(self_id):
    """
    请求ssoseq

    :param self_id: 框架QQ(长整数型)
    """
    method = "请求ssoseq"
    params = {'self_id': self_id}
    return _make_request(method, params, _get_plugin_name())


def 取sessionkey(self_id):
    """
    取sessionkey(成功返回16进制秘钥,敏感权限)

    :param self_id: 框架QQ(长整数型)
    """
    method = "取sessionkey"
    params = {'self_id': self_id}
    return _make_request(method, params, _get_plugin_name())


def 取插件运行状态():
    """
    _取插件运行状态(插件扩展api)
    """
    method = "_取插件运行状态"
    params = {}
    return _make_request(method, params, _get_plugin_name())


def 清理插件缓存(type='all'):
    """
    _清理插件缓存(插件扩展api)

    :param type: 1或image_hash清空image_hash缓存目录, 2或audio_hash, 3或voice, 4或cache, all为删除全部缓存目录
    """
    method = "_清理插件缓存"
    params = {'type': type}
    return _make_request(method, params, _get_plugin_name())


def 取群成员信息2(self_id, group_id, to_id):
    """
    _取群成员信息(插件扩展api,返回包含所有原始数据的json 自行筛选所需数据)

    :param self_id: 框架QQ(长整数型)
    :param group_id: 目标群号(长整数型)
    :param to_id: 目标QQ(长整数型)
    """
    method = "_取群成员信息"
    params = {'self_id': self_id, 'group_id': group_id, 'to_id': to_id}
    return _make_request(method, params, _get_plugin_name())
