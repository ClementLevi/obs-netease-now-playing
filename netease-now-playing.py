# obs-netease-now-playing
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownParameterType=false
# pyright: reportMissingParameterType=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportUnknownVariableType=false

# @author @NSLC https://obsproject.com/forum/members/nslc.483240/
# @release 2024-05-27
# @fix @Clement_Levi https://github.com/ClementLevi
# @release 2024-08-06

import obspython as obs
try:
    import win32gui
except:
    import os
    os.system("pip install pywin32")
finally:
    import win32gui

# global var
source_name: str = ""
interval: int = 500
info_format: str = "Now Playing:[%A] %T"
artists_split: str = "、"
title = artists = ""


def script_description() -> str:
    msg = "A Script for Obtaining Song Titles/Artists from [NetEase Cloud Music] Based on Process Class Lookups \n\n" +\
    "Reload this Script if you can't find your text source (or you have changed the name of the source)"
    return msg


def script_defaults(settings) -> None:
    obs.obs_data_set_default_int(settings, "interval", interval)
    obs.obs_data_set_default_string(settings, "info_format", info_format)
    obs.obs_data_set_default_string(settings, "artists_split", " | ")


def script_update(settings) -> None:
    global source_name, info_format, artists_split
    source_name = obs.obs_data_get_string(settings, "source")
    info_format = obs.obs_data_get_string(settings, "info_format")
    artists_split = obs.obs_data_get_string(settings, "artists_split")


def script_properties():
    props = obs.obs_properties_create()
    p = obs.obs_properties_add_list(
        props, "source", "Text Source", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            # print("Source id: ", obs.obs_source_get_id(source),"; Source name: ", obs.obs_source_get_name(source))
            source_id = obs.obs_source_get_id(source)
            if source_id in ["text_gdiplus_v3","text_gdiplus_v2", "text_gdiplus", "text_ft2_source"]:
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)
        obs.source_list_release(sources)

    obs.obs_properties_add_text(
        props, "info_format", "display style", obs.OBS_TEXT_DEFAULT)
    obs.obs_property_set_long_description(obs.obs_properties_get(props, "info_format"),
                                          "%A = artists list\n%T = title")

    obs.obs_properties_add_text(
        props, "artists_split", "split string for artists list", obs.OBS_TEXT_DEFAULT)
    return props


def update_text() -> None:
    global source_name, info_format, artists_split
    source = obs.obs_get_source_by_name(source_name)
    if source is not None:
        np_text = get_now_playing_info(info_format, artists_split)
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", np_text)
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)

        obs.obs_source_release(source)


def script_load(settings) -> None:
    obs.timer_add(update_text, interval)


def script_unload() -> None:
    obs.timer_remove(update_text)


class WindowInfo:
    def __init__(self, hwnd: int, window_text: str, class_name: str, rect: tuple[int, int, int, int]) -> None:
        self.hwnd = hex(hwnd)
        self.window_text = window_text
        self.class_name = class_name
        self.rect = rect

    def __str__(self) -> str:
        return f"hwnd: {self.hwnd}, window_text: {self.window_text}, class_name: {self.class_name}, rect: {self.rect}"


def get_visible_window() -> list[WindowInfo]:
    visible_window: list[WindowInfo] = []

    def enum_windows_proc(hwnd: int, lparam: ...):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            rect = win32gui.GetWindowRect(hwnd)
            visible_window.append(WindowInfo(
                hwnd, window_text, class_name, rect))

    win32gui.EnumWindows(enum_windows_proc, 0)
    return visible_window


def abbr_str(s: str, max_length: int = 25) -> str:
    if len(s) <= max_length:
        return s
    else:
        return s[:12] + '...' + s[-12:]


def get_now_playing_info(info_format: str, artists_split: str) -> str:
    global title, artists
    window_info = get_visible_window()
    for info in window_info:
        if info.class_name == "OrpheusBrowserHost":
        # if info.class_name == "OrpheusShadow":  # 后台运行叫这个，但是不能获取窗口名
            # print(info.window_text)
            title, artists = info.window_text.split(" - ", 1)
            title = abbr_str(title)
            artists = artists_split.join(
                [abbr_str(x) for x in artists.split("/")])
            break
        else:
            pass
    return info_format.replace("%A", artists).replace("%T", title)

print("Plugin is successfully loaded!")
got = get_now_playing_info("正在播放:[%A] @%T"," - ")
print("Got it: ",get_now_playing_info("正在播放:[%A] By: @%T"," - "))
