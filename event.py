import os
import pkgutil
import sys
import traceback
from typing import Callable

from tornado import web

import datatypes
from log import log

event_funcs = [[], [], []]  # 0:pri 1:gro 2:evt
modules = []


def load_plugins():
    global event_funcs
    global modules
    event_funcs = [[], [], []]  # 0:pri 1:gro 2:evt
    for module in modules:
        del sys.modules[module]
    modules = []
    log('开始加载插件', 'PLUGIN')
    urls = []
    commands = []
    plugin_list = []
    if not os.path.exists('./plugins'):
        os.mkdir('./plugins')
    for finder, name, _ in pkgutil.walk_packages(["./plugins"]):
        log(f'正在加载插件{name}', 'PLUGIN')
        try:
            module = finder.find_module(name).load_module(name)
            modules.append(name)
            info: datatypes.PluginInfo = module.startup()
        except Exception:
            log(f'加载插件{name}失败\n{traceback.format_exc()}', 'PLUGIN')
            try:
                del sys.modules[name]
            except:
                pass
        else:
            if isinstance(info, datatypes.PluginInfo):
                if info.func_private:
                    if isinstance(info.func_private, Callable):
                        event_funcs[0].append(((info.func_private, name), info.priority))
                        log(f'{name} -> 已设置私聊消息监听函数', 'PLUGIN')
                    else:
                        log(f'{name} -> 设置私聊消息监听函数失败：提供参数不为函数', 'PLUGIN')
                if info.func_group:
                    if isinstance(info.func_group, Callable):
                        event_funcs[1].append(((info.func_group, name), info.priority))
                        log(f'{name} -> 已设置群聊消息监听函数', 'PLUGIN')
                    else:
                        log(f'{name} -> 设置群聊消息监听函数失败：提供参数不为函数', 'PLUGIN')
                if info.func_event:
                    if isinstance(info.func_event, Callable):
                        event_funcs[2].append(((info.func_event, name), info.priority))
                        log(f'{name} -> 已设置事件消息监听函数', 'PLUGIN')
                    else:
                        log(f'{name} -> 设置事件消息监听函数失败：提供参数不为函数', 'PLUGIN')
                if info.listen_urls:
                    for a in info.listen_urls:
                        if len(a) == 2:
                            if isinstance(a[1], Callable) and issubclass(a[1], web.RequestHandler):
                                if (a[0] if not a[0].endswith('/') else a[0][:len(a[0]) - 1]) not in \
                                        [(x[0] if not x[0].endswith('/') else x[0][:len(x[0]) - 1]) for x in urls] and \
                                        (a[0] != '/' and (a[0] != '/file' and not a[0].startswith('/file/'))):
                                    urls.append(a)
                                    log(f'{name} -> 已向服务器添加url {a[0]}', 'PLUGIN')
                                else:
                                    log(f'{name} -> 向服务器添加url {a[0]} 失败：url重复', 'PLUGIN')
                            else:
                                log(f'{name} -> 向服务器添加url {a[0]} 失败：提供参数不为RequestHandler类', 'PLUGIN')
                        else:
                            log(f'{name} -> 向服务器添加url失败：提供参数数量错误', 'PLUGIN')
                if info.listen_commands:
                    for a in info.listen_commands:
                        if len(a) == 3:
                            if isinstance(a[1], Callable):
                                if a[0] not in [x[0] for x in commands] and a[0] not in ['help', 'pluginli', 'reload']:
                                    b = f'{a[2]} [{info.name}]'
                                    commands.append((a[0], a[1], b))
                                    log(f'{name} -> 添加控制台指令 {a[0]} 成功，用途：{a[2]}', 'PLUGIN')
                                else:
                                    log(f'{name} -> 添加控制台指令 {a[0]} 失败：指令重复', 'PLUGIN')
                            else:
                                log(f'{name} -> 添加控制台指令 {a[0]} 失败：提供处理指令参数不为函数', 'PLUGIN')
                        else:
                            log(f'{name} -> 添加控制台指令失败：提供参数数量错误', 'PLUGIN')
                plugin_list.append((name, info.name, info.author, info.version, info.description, info.priority))
                log((f'加载插件{name}成功，插件名：{info.name}，作者：{info.author}，版本号：{info.version}，'
                     f'简介：{info.description}'), 'PLUGIN')
            else:
                log(f'加载插件{name}失败：初始化函数返回值错误', 'PLUGIN')
                del sys.modules[name]

    if len(event_funcs[0]):
        event_funcs[0].sort(key=lambda x: x[1], reverse=True)
        event_funcs[0] = [x[0] for x in event_funcs[0]]

    if len(event_funcs[1]):
        event_funcs[1].sort(key=lambda x: x[1], reverse=True)
        event_funcs[1] = [x[0] for x in event_funcs[1]]

    if len(event_funcs[2]):
        event_funcs[2].sort(key=lambda x: x[1], reverse=True)
        event_funcs[2] = [x[0] for x in event_funcs[2]]

    log('插件加载完毕', 'PLUGIN')
    return urls, commands, plugin_list


def event_private(org_data):
    data = datatypes.PrivateMsg(org_data)
    log(f'Bot{data.self_id} -> [{data.message_type},{data.message_subtype},{data.message_temp_subtype}]'
        f'[{data.event_from_nickname}({data.from_id})]：{data.message}', 'PRIVATE')
    call(event_funcs[0], data)


def event_group(org_data):
    data = datatypes.GroupMsg(org_data)
    log(f'Bot{data.self_id} -> '
        f'[{data.group_name}({data.group_id}) -> {data.from_gm_card}({data.from_id})]：{data.message}', 'GROUP')
    call(event_funcs[1], data)


def event_event(org_data):
    data = datatypes.EventMsg(org_data)
    log(f'Bot{data.self_id} -> [{data.event_type},{data.event_subtype}]'
        f'[{data.group_name}({data.group_id})] -> '
        f'[{data.oper_nickname}({data.oper_id}) -> {data.trigger_nickname}({data.trigger_id})]：'
        f'{data.message}', 'EVENT')
    call(event_funcs[2], data)


def call(funcs, data):
    for func, plugin_name in funcs:
        try:
            ret = func(data)
        except Exception:
            log(f'Bot{data.self_id} -> 调用插件{plugin_name}处理函数失败\n{traceback.format_exc()}', 'PLUGIN')
            continue
        else:
            if ret:
                log(f'Bot{data.self_id} -> 插件{plugin_name}已拦截消息，消息类型：{data.post_type}，消息内容：{data.message}',
                    'PLUGIN')
                break
