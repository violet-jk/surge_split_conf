#!/usr/bin/env python3
"""把 General.conf / ProxyGroup.conf / Rule.conf 合并成可通过 URL 下载的托管配置 Managed.conf。

Managed.conf 第一行是 #!MANAGED-CONFIG，Surge 会按 interval 自动从 URL 更新它。
它本身是合法的完整配置，主配置 Main.conf 通过 #!include Managed.conf 引用其中各段。
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = "https://raw.githubusercontent.com/violet-jk/surge_split_conf/main/Managed.conf"
INTERVAL = 43200  # 秒，Surge 两次检查更新的最短间隔
SOURCES = ["General.conf", "ProxyGroup.conf", "Rule.conf"]

HEADER = f"""#!MANAGED-CONFIG {URL} interval={INTERVAL} strict=false
# =====================================================================
#  Managed.conf  ——  自动生成，请勿直接编辑
#  来源：{' + '.join(SOURCES)}（由 scripts/build_managed.py 合并）
#  用法：不要把本文件设为当前配置，由 Main.conf 以 #!include 引用。
# =====================================================================

[Proxy]
# 托管配置不含节点；节点由 Main.conf 的 [Proxy] 段引入
"""


def main() -> None:
    parts = [HEADER]
    for name in SOURCES:
        text = (ROOT / name).read_text(encoding="utf-8").strip("\n")
        parts.append(f"\n# ######## 以下来自 {name} ########\n{text}\n")
    out = ROOT / "Managed.conf"
    content = "".join(parts)
    if not out.exists() or out.read_text(encoding="utf-8") != content:
        out.write_text(content, encoding="utf-8")
        print(f"updated {out.name}")
    else:
        print(f"{out.name} unchanged")


if __name__ == "__main__":
    main()
