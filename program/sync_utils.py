#!/usr/bin/env python3
"""词库同步脚本的公共工具：解析上游目录、读取词频。"""

import argparse
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def upstream_root(explicit=None):
    """返回上游 rime-frost 根目录。优先级：命令行 > 环境变量 > 本地默认路径。"""
    if explicit:
        return Path(explicit).expanduser().resolve()
    env = os.environ.get('RIME_FROST_DIR')
    if env:
        return Path(env).expanduser().resolve()
    for candidate in (
        REPO_ROOT.parent / 'rime-frost',
        Path(r'D:\vscode\rime-frost'),
        Path('/path/to/rime-frost'),
    ):
        if (candidate / 'cn_dicts').is_dir():
            return candidate.resolve()
    return Path(r'D:\vscode\rime-frost')


def add_upstream_arg(parser, description='同步 rime-frost 词库'):
    parser.add_argument(
        '--upstream-dir',
        default=None,
        help='rime-frost 仓库根目录（默认取环境变量 RIME_FROST_DIR 或本地同级目录）',
    )
    return parser


def load_word_freq(root):
    """读取上游知频.txt，返回 {词: 频次}。文件不存在时返回空表。"""
    freq_file = root / 'others' / '知频.txt'
    word_freq = {}
    if not freq_file.is_file():
        return word_freq
    with open(freq_file, 'r', encoding='utf-8') as f:
        for line in f:
            params = line.strip().split('\t')
            if len(params) < 2:
                continue
            try:
                freq = int(params[1])
            except ValueError:
                continue
            word = params[0]
            word_freq[word] = word_freq.get(word, 0) + freq
    return word_freq
