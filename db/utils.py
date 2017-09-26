#!/usr/bin/env python
# -*-coding:utf-8-*-

import os
from time import time

TYPE_KEYS = [
    ['mp4', 'mpg', 'mpeg', 'avi', 'rm', 'rmvb', 'mov', 'wmv', 'asf', 'dat', 'mkv', 'asx', 'wvx', 'm2v', 'lza', 'mlv',
     'ivf', 'flc', 'fla', 'fsp', 'dvm', 'dvd', 'dv', 'dir', 'dif', 'dff', 'cmf', 'cel', 'byu', 'at', 'anim', 'anm',
     'fli', 'flt', 'gl', 'mng', 'mpv', 'msl', 'qt', 'qtx', 'rgb', 'spl', 'spa', 'str', 'viv', 'vivo', 'yuv', 'xas',
     'mpe', 'qt', 'vob', 'flv', 'divx', '3gp', 'swf', 'f4v', 'ts', 'm2ts', 'm4v', 'srt', 'ac3', 'mmm', 'm1v'],
    ['mp3', 'wma', 'flac', 'ape', 'wav', 'midi', 'ogg', 'aac', 'amr', 'aif', 'au', 'm4p', 'm4r', 'm4a', 'm4b',
     'mp1', 'mp2', 'asx', 'm3u', 'pls', 'ra', 'mpa', 'snd', 'voc', 'ins', 'cda', 'mid', 'vqf', 'ram', 'wax'],
    ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'psd', 'svg', 'pcx', 'dxf', 'emf', 'raw', 'wmf', 'pcd'],
    ['azw3', 'mobi', 'azw', 'pdf', 'chm', 'txt', 'epub', 'prc', 'azw1', 'azk', 'doc', 'docx',
     'ppt', 'pptx', 'xls', 'xlsx', 'cbz', 'cbr', 'cb7', 'cba', 'cbt', 'djvu', 'fb2'],
    ['exe', 'com', 'bin', 'dll', 'a', 'so', 'msi', 'cmd', 'apk', 'jar', 'vbs', 'bat', 'reg', 'rgss3a', 'nsa', 'obb',
     'inf', 'sav', 'srm', 'ress', 'nes', 'tga', 'pak', '.wolf', 'rpgsave', 'rvdata2', 'rvdata', 'rpgmvp', 'gmk', 'gm6'],
    ['rar', 'zip', '7z', 'arj', 'gz', 'z', 'iso', 'tar', '.01', '.001', 'r01', 'r001', 'z01',
     'z001','isz', 'r02', 'r03', 'dmg', 'tgz', 'chd', 'cab', 'cdr', 'wbs', 'lzma', 'mds', 'gho', 'ima', 'nrg',
     'pkg', 'b5i', 'mdx', 'vmdk'],
    []
]


'''
0:视频
1:音乐
2:图片
3:文档
4:应用程序
5:压缩文件
6:其他或者没有拓展名
'''


def get_file_type(l):
    t = [0 for _ in range(7)]
    for x in l:
        n = os.path.splitext(x.get('n').lower())[1][1:]
        if n != '':
            y = 0
            for y in range(len(TYPE_KEYS)):
                if n in TYPE_KEYS[y]:
                    break
            t[y] += x.get('l') * (10 if y == 4 else 1)
        else:
            t[6] += x.get('l')
    return sorted(range(len(t)), key=lambda k: t[k], reverse=True)[0]


def parse_metadata(metadata, h):
    utf8_enable = False
    files = []
    try:
        bare_name = metadata.get('name')
    except KeyError:
        bare_name = metadata.get('name.utf-8')
        utf8_enable = True
    except:
        return False
    if 'files' in metadata:
        for x in metadata.get('files'):
            files.append({'n': '/'.join(x.get('path.utf-8' if utf8_enable else 'path')),
                          'l': x.get('length')})
    else:
        files.append({'n': bare_name,
                      'l': metadata.get('length')})
    return {
        'n': bare_name,
        'f': files,
        'd': int(time()),
        '_id': h,
        'l': sum(map(lambda y: y.get('l'), files)),
        's': len(files),
        'e': 1,
        't': get_file_type(files)
    }
