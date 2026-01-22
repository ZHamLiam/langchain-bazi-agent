"""测试八字Agent - 手动输入版本"""

import os
import sys

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from bazi_calculator.chains.bazi_agent import BaziAgent


def get_user_input():
    """获取用户输入的出生信息"""
    print("=" * 60)
    print("八字计算 - 智能解析模式")
    print("=" * 60)

    # 直接获取用户输入
    print("\n请输入您的出生信息：")
    print("示例：")
    print("  - 我出生于1999年10月17日凌晨3点，男性")
    print("  - 2025年12月30日下午6点，女的，公历")
    print("  - 男孩，出生在甲辰年二月十五日上午10点")
    print("  - 1999年10月17日3点 男 公历")
    print("-" * 60)

    user_input = input("请输入：").strip()

    if not user_input:
        print("输入不能为空！")
        return None

    return user_input


def test_bazi_with_input(user_input):
    """根据用户输入测试八字计算 - 统一使用LLM解析"""
    print("\n开始八字计算...")
    print("-" * 60)

    try:
        # 加载环境变量
        import dotenv
        dotenv.load_dotenv()

        # 获取API配置
        api_key = os.getenv("QWEN_API_KEY") or os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("QWEN_BASE_URL") or os.getenv("OPENAI_BASE_URL")
        model = os.getenv('QWEN_MODEL', 'gpt-3.5-turbo')

        if not api_key:
            print("错误：未找到API密钥")
            print("请确保.env文件中配置了QWEN_API_KEY或OPENAI_API_KEY")
            return False

        # 创建LLM实例，直接传递API密钥
        from langchain_openai import ChatOpenAI
        llm_kwargs = {
            "model": model,
            "api_key": api_key,
            "temperature": 0
        }

        if base_url:
            llm_kwargs["base_url"] = base_url

        llm = ChatOpenAI(**llm_kwargs)

        # 统一使用LLM智能解析器
        from bazi_calculator.tools.bazi.intelligent_parser import IntelligentBaziCalculator

        calculator = IntelligentBaziCalculator(llm)

        # 直接将用户输入传递给LLM解析
        result = calculator.calculate_from_natural_language(user_input)
        formatted_result = calculator.format_result(result)

        print(formatted_result)
        print("\n✅ 计算完成")

        return True

    except Exception as e:
        print(f"\n❌ 计算失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def interactive_mode():
    """交互式模式"""
    print("\n" + "=" * 60)
    print("交互式八字计算")
    print("=" * 60)
    print("输入'quit'或'退出'可退出程序\n")

    while True:
        try:
            user_input = get_user_input()

            if user_input is None:
                print("\n请重新输入...")
                continue

            # 检查退出命令
            if user_input.lower() in ['quit', '退出', 'exit']:
                print("\n感谢使用！")
                break

            success = test_bazi_with_input(user_input)

            print("\n" + "=" * 60)

            # 询问是否继续
            continue_input = input("是否继续计算？(y/n): ").strip().lower()
            if continue_input not in ['y', 'yes', '是', 'Y', 'YES']:
                print("感谢使用！")
                break

            print()

        except KeyboardInterrupt:
            print("\n\n程序已退出")
            break
        except Exception as e:
            print(f"\n发生错误：{e}")
            import traceback
            traceback.print_exc()
            print("\n请重新输入...\n")


def single_test_mode():
    """单次测试模式"""
    user_input = get_user_input()

    if user_input is None:
        print("输入无效，程序退出")
        return

    # 检查退出命令
    if user_input.lower() in ['quit', '退出', 'exit']:
        print("程序已退出")
        return

    success = test_bazi_with_input(user_input)

    if success:
        print("\n计算成功完成！")
    else:
        print("\n计算失败，请检查输入信息")


if __name__ == "__main__":
    print("\n八字智能计算系统")
    print("=" * 60)
    print("功能：")
    print("  - 智能解析自然语言输入")
    print("  - 准确计算八字四柱")
    print("  - 支持多种表达方式")
    print("=" * 60)

    print("\n请选择运行模式：")
    print("1. 交互式模式（可多次输入）")
    print("2. 单次测试模式（计算一次后退出）")

    mode_choice = input("请选择（1或2）：").strip()

    if mode_choice == "1":
        interactive_mode()
    elif mode_choice == "2":
        single_test_mode()
    else:
        print("无效选择，默认使用交互式模式")
        interactive_mode()
