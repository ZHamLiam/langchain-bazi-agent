"""八字取名系统 - 命令行入口

提供交互式八字计算和取名服务
"""

import sys
from bazi_calculator.chains.interactive_agent import main


def run_cli():
    """运行命令行界面"""
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已退出")
        sys.exit(0)
    except Exception as e:
        print(f"\n发生错误：{e}")
        sys.exit(1)


if __name__ == "__main__":
    run_cli()
