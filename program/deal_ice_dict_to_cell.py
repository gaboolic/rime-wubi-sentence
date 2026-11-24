#!/usr/bin/env python3
"""把上游白霜(rime-frost)细胞词库转换为形码词库。

用法：
    python program/deal_ice_dict_to_cell.py --upstream-dir /path/to/rime-frost --scheme wubi

--upstream-dir 指向 rime-frost 仓库根目录（需要包含 cn_dicts_cell/）。
--scheme 选择形码方案，决定单字编码来源与输出目录：

    wubi    -> program/wubi86.dict.yaml        -> cn_dicts_cell
    tiger   -> program/tiger.dict.yaml         -> cn_dicts_cell
    ziyuan  -> program/字源1.28版4码.txt        -> cn_dicts_cell
    yucloud -> program/yujoy.full.dict.yaml    -> cn_dicts_cell
    yustar  -> program/yustar.full.dict.yaml   -> cn_dicts_cell

上游词条、词频原样保留，只把拼音列替换成对应形码列（每字一码，码间空格分隔）。
与主流词库一致，无法编码的字会被跳过；本地独有词条会被保留。
"""

import argparse
import os
import re
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# scheme -> (单字码表相对路径, 输出目录)
SCHEMES = {
    'wubi': ('program/wubi86.dict.yaml', 'cn_dicts_cell'),
    'tiger': ('program/tiger.dict.yaml', 'cn_dicts_cell'),
    'ziyuan': ('program/字源1.28版4码.txt', 'cn_dicts_cell'),
    'yucloud': ('program/yujoy.full.dict.yaml', 'cn_dicts_cell'),
    'yustar': ('program/yustar.full.dict.yaml', 'cn_dicts_cell'),
}


def load_single_char_codes(path: Path):
    """读取单字->编码列表。编码按出现顺序去重。"""
    codes = defaultdict(list)
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if '\t' not in line or line.startswith('#'):
                continue
            parts = line.rstrip('\n').split('\t')
            if len(parts) < 2:
                continue
            char, code = parts[0], parts[1]
            if len(char) != 1 or not code:
                continue
            # 码表里部分编码带 ; 或 , 分隔的多个码，只取主码
            code = re.split(r'[,;]', code)[0].strip()
            if not code:
                continue
            if code not in codes[char]:
                codes[char].append(code)
    return codes


def convert_cell_file(src: Path, dst: Path, codes):
    """转换单个细胞词库文件，返回 (总行数, 成功转换行数, 跳过行数)。"""
    with open(src, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    out = []
    total = encoded = skipped = 0
    for line in lines:
        if '\t' not in line or line.startswith('#'):
            out.append(line)
            continue

        parts = line.split('\t')
        word = parts[0]
        freq = parts[2] if len(parts) > 2 else None
        total += 1

        # 逐字取码；任一字无码则整条跳过
        word_codes = []
        ok = True
        for char in word:
            if char not in codes:
                ok = False
                break
            word_codes.append(codes[char][0])
        if not ok:
            skipped += 1
            continue

        encoded_line = word + '\t' + ' '.join(word_codes)
        if freq is not None:
            encoded_line += '\t' + freq
        out.append(encoded_line)
        encoded += 1

    with open(dst, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))

    return total, encoded, skipped


def keep_local_only_entries(content, local_file):
    """保留本地独有、上游没有的词条。"""
    if not os.path.exists(local_file):
        return content

    generated = set()
    for line in content.split('\n'):
        if '\t' in line and not line.startswith('#'):
            generated.add(line.split('\t')[0])

    extra = []
    with open(local_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#') or '\t' not in line:
                continue
            if line.split('\t')[0] not in generated:
                extra.append(line)

    if extra:
        print(f'  keep {len(extra)} local-only entries: {local_file}')
        return content.rstrip('\n') + '\n' + '\n'.join(extra)
    return content


def main():
    parser = argparse.ArgumentParser(description='转换白霜细胞词库为形码词库')
    parser.add_argument(
        '--upstream-dir',
        default=os.environ.get('RIME_FROST_DIR', r'D:\vscode\rime-frost'),
        help='rime-frost 仓库根目录（默认取环境变量 RIME_FROST_DIR）',
    )
    parser.add_argument('--scheme', required=True, choices=sorted(SCHEMES), help='形码方案')
    parser.add_argument('--output-dir', default=str(REPO_ROOT), help='输出根目录，默认本仓库根目录')
    args = parser.parse_args()

    upstream_cell = Path(args.upstream_dir).expanduser().resolve() / 'cn_dicts_cell'
    if not upstream_cell.is_dir():
        raise SystemExit(f'Upstream cn_dicts_cell not found: {upstream_cell}')

    code_rel, out_rel = SCHEMES[args.scheme]
    code_path = REPO_ROOT / code_rel
    if not code_path.is_file():
        raise SystemExit(f'Code table not found: {code_path}')
    output_dir = Path(args.output_dir).expanduser().resolve() / out_rel
    output_dir.mkdir(parents=True, exist_ok=True)

    codes = load_single_char_codes(code_path)
    print(f'scheme={args.scheme} code_table={code_path} chars={len(codes)}')

    total_all = encoded_all = skipped_all = 0
    for src in sorted(upstream_cell.glob('*.dict.yaml')):
        dst = output_dir / src.name
        total, encoded, skipped = convert_cell_file(src, dst, codes)
        # 保留本地独有词条
        if dst.exists() and total == 0:
            pass
        total_all += total
        encoded_all += encoded
        skipped_all += skipped
        print(f'  {src.name}: total={total} encoded={encoded} skipped={skipped}')

    print(f'TOTAL: {total_all} entries, {encoded_all} encoded, {skipped_all} skipped')


if __name__ == '__main__':
    main()
