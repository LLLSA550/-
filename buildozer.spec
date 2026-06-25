[app]

# 应用标题（显示在安卓设备上）
title = PRTS 综合集成监控终端

# 包名（必须是唯一标识符，格式：com.你的域名.应用名）
package.name = prts_terminal

# 包域名（反向域名格式）
package.domain = org.example

# 源码目录（当前目录为项目根目录）
source.dir = .

# 主Python文件
source.include_exts = py,png,jpg,kv,atlas,ttf,json

# 版本号
version = 1.0.0

# 应用图标（需要准备不同尺寸，可选）
#icon.filename = %(source.dir)s/assets/icon.png

# 应用描述
description = PRTS 综合集成监控终端 - 赛博农场管理工具

# 作者信息
author = PRTS Development Team

# 许可证
license = MIT

# 是否联网（需要网络权限）
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# 是否显示全屏（推荐安卓应用）
fullscreen = 0

# 屏幕方向（portrait=竖屏, landscape=横屏）
orientation = portrait

# 是否支持安卓API自动下载
#android.api = 33
#android.minapi = 21
#android.sdk = 33
#android.ndk = 25b

# 需要的Python包（按需添加）
requirements = python3,kivy==2.2.1,requests,urllib3,certifi,charset-normalizer,idna

# 如果你的app用了其他库，比如numpy, pillow等，在这里添加
# requirements = python3,kivy,numpy,pillow

# 排除不需要的文件
source.exclude_patterns = 
    license,
    images/*,
    *.spec,
    .git,
    buildozer.spec

[buildozer]

# Buildozer日志级别（1-2为详细模式）
log_level = 2

# 构建缓存目录
cache_dir = ~/.buildozer/cache

# 构建输出目录
bin_dir = ./bin

# 是否使用虚拟环境（推荐开启）
use_virtualenv = True

# 构建前执行的命令（如果有额外资源需要复制）
# prebuild =

[android]

# 使用的Python版本
python_version = 3.10

# 目标Android API版本（Android 13）
android.api = 33

# 最低Android API版本（Android 5.0）
android.minapi = 21

# SDK版本
android.sdk = 33

# NDK版本
android.ndk = 25b

# 安卓ABI架构（arm64-v8a为现代手机，armeabi-v7a为兼容旧手机）
android.archs = arm64-v8a, armeabi-v7a

# 是否保留旧的构建缓存（0为每次清理，1为保留）
android.allow_backup = 1

# 应用启动模式
android.entrypoint = org.kivy.android.PythonActivity

# 是否启用AndroidX
android.enable_androidx = True

# 是否使用p4a（Python-for-Android）本地源码
# android.p4a_dir =

# p4a分支版本
android.p4a_branch = master

# 是否包含私有数据
android.private_storage = True

# 启动画面颜色（显示在应用加载时）
android.presplash_color = #F4F6F9

# 是否隐藏系统导航栏
android.window_flags = FLAG_KEEP_SCREEN_ON

# 签名配置（发布APK时需要）
# 先运行以下命令生成密钥：
# keytool -genkey -v -keystore my-release-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000
# android.signing.keystore = my-release-key.keystore
# android.signing.alias = alias_name

[ios]
# iOS相关配置（暂不需要）
