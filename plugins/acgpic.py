import json
import random

import api
import datatypes

keywords = []
apis = []
fuzzy_match = False


# 建议安装ChinesePinyin-CodeCompletionHelper插件，以获取更好中文函数及常量编程体验，支持PyCharm及VS Code（说白了就是我懒得翻译）

def startup():
    """
    插件初始化函数
    除全局变量等声明，其他初始化代码建议在此处执行
    返回插件信息
    如果想拒绝加载，直接raise Exception('原因即可')
    """

    # 如果有，可在此处放置初始化代码
    reload_conf([])

    return datatypes.PluginInfo(  # 返回插件信息
        "示例插件-二次元图片",  # 插件名称
        "student_2333",  # 作者
        version="2021.4.9beta",  # 版本号 无需可注释
        description="二次元图片",  # 插件简介 无需可注释
        # priority=1,  # 消息处理优先级 如无特殊需求请勿更改，请注释
        func_private=private_msg,  # 私聊消息处理函数 无需可注释
        func_group=group_msg,  # 群聊消息处理函数 无需可注释
        # func_event=event_msg,  # 事件消息处理函数 无需可注释
        # listen_urls=[('/example', example_url)],  # 向服务器添加的url 格式[('相对路径', 处理类),...] 无需可注释
        listen_commands=[('acg_reload', reload_conf, '重载配置文件')]  # 向控制台添加的指令 格式[('指令', 处理函数, '功能简介'),...] 无需可注释
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
            if fuzzy_match:
                for k in keywords:
                    if data.message.find(k) != -1:
                        api.发送群临时消息(data.self_id, data.group_id, data.from_id, '请稍等，图片正在来的路上～')
                        api.发送群临时消息(data.self_id, data.group_id, data.from_id, acg())
                        return True
            else:
                for k in keywords:
                    if data.message.strip() == k:
                        api.发送群临时消息(data.self_id, data.group_id, data.from_id, '请稍等，图片正在来的路上～')
                        api.发送群临时消息(data.self_id, data.group_id, data.from_id, acg())
                        return True

    elif data.message_type == datatypes.消息类型_好友通常消息:
        # 在2.7.1以上的版本当中，真正的红包等将传入文本代码，但由于oopshttpapi特性，已将方括号转义，所以……
        if fuzzy_match:
            for k in keywords:
                if data.message.find(k) != -1:
                    api.发送好友消息(data.self_id, data.from_id, '请稍等，图片正在来的路上～')
                    api.发送好友消息(data.self_id, data.from_id, acg())
                    return True
        else:
            for k in keywords:
                if data.message.strip() == k:
                    api.发送好友消息(data.self_id, data.from_id, '请稍等，图片正在来的路上～')
                    api.发送好友消息(data.self_id, data.from_id, acg())
                    return True

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

    if fuzzy_match:
        for k in keywords:
            if data.message.find(k) != -1:
                api.发送群消息(data.self_id, data.group_id, '请稍等，图片正在来的路上～')
                api.发送群消息(data.self_id, data.group_id, acg())
                return True
    else:
        for k in keywords:
            if data.message.strip() == k:
                api.发送群消息(data.self_id, data.group_id, '请稍等，图片正在来的路上～')
                api.发送群消息(data.self_id, data.group_id, acg())
                return True

    return False


def acg():
    return api.取图片文本代码(random.choice(apis))


def reload_conf(args: list):
    """
    添加的控制台指令处理函数，可添加更多，无需可删除

    :param args: 指令参数（就是空格分隔的内容）
    :return: 执行结果（会输出到控制台） 可以无返回值
    """
    data_path = api.取插件数据目录()
    try:
        with open(data_path + 'conf.json') as f:
            conf = json.load(f)
        global keywords
        global apis
        global fuzzy_match
        assert isinstance(conf['keywords'], list)
        assert isinstance(conf['apis'], list)
        assert isinstance(conf['fuzzy_match'], bool)
        keywords = conf['keywords']
        apis = conf['apis']
        fuzzy_match = conf['fuzzy_match']
    except:
        keywords = ['二次元', '色图']
        apis = ['https://www.dmoe.cc/random.php']
        fuzzy_match = False
        with open(data_path + 'conf.json', 'w') as f:
            json.dump({'keywords': keywords, 'apis': apis, 'fuzzy_match': fuzzy_match}, f)

    api.输出日志('[二次元图片] 配置：')
    api.输出日志(f'触发关键词：{"，".join(keywords)}')
    api.输出日志(f'图片api：{"，".join(apis)}')
    api.输出日志(f'是否模糊匹配：{"是" if fuzzy_match else "否"}')

    return '重载完毕'
