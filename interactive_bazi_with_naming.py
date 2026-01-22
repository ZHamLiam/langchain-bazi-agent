"""交互式八字分析+取名建议

在八字分析完成后，询问用户是否需要取名建议
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from bazi_calculator.tools.bazi.intelligent_parser import IntelligentBaziCalculator
from bazi_calculator.core.wuxing import WuxingAnalyzer
from bazi_calculator.core.mingge import MingGeAnalyzer
from bazi_calculator.tools.naming.suitable_chars import get_suitable_chars
from bazi_calculator.tools.naming.name_generator import generate_name_suggestions

load_dotenv()


def create_qwen_llm():
    """创建Qwen LLM实例"""

    api_key = os.getenv("QWEN_API_KEY")
    base_url = os.getenv("QWEN_BASE_URL")
    model = os.getenv("QWEN_MODEL", "qwen-flash")

    if not api_key:
        raise ValueError("未找到QWEN_API_KEY，请检查.env文件")

    llm = ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=0.3
    )

    return llm


def get_zodiac(year: int) -> str:
    """根据年份获取生肖"""

    zodiacs = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
    # 1984年是鼠年（甲子年）
    base_year = 1984
    index = (year - base_year) % 12
    return zodiacs[index]


def generate_naming_suggestions(bazi, wuxing_analysis, llm):
    """生成取名建议"""

    print("\n" + "=" * 80)
    print("正在生成取名建议...")
    print("=" * 80)

    try:
        # 获取生肖
        birth_year = bazi.get("birth_info", {}).get("year", 0)
        zodiac = get_zodiac(birth_year)

        # 准备八字分析数据
        bazi_analysis = {
            "zodiac": zodiac,
            "day_master": bazi["day"]["gan"],
            "day_master_wuxing": bazi["day"]["gan_wuxing"],
            "yong_shen": wuxing_analysis["yong_shen_info"]["yong_shen"],
            "xi_shen": wuxing_analysis["yong_shen_info"]["xi_shen"],
            "ji_shen": wuxing_analysis["yong_shen_info"]["ji_shen"]
        }

        # 构建适合字字典（简化版）
        # 根据用神和喜神提供一些常见适合字
        yong_shen = bazi_analysis["yong_shen"]
        xi_shen = bazi_analysis["xi_shen"]

        # 简化的适合字库
        simple_chars = {
            "木": [
                {"char": "林", "pinyin": "lín", "kangxi_strokes": 8, "pingze": "平", "meaning": "树木茂盛"},
                {"char": "梓", "pinyin": "zǐ", "kangxi_strokes": 11, "pingze": "仄", "meaning": "梓木"},
                {"char": "楷", "pinyin": "kǎi", "kangxi_strokes": 13, "pingze": "仄", "meaning": "楷模"},
                {"char": "楷", "pinyin": "kǎi", "kangxi_strokes": 13, "pingze": "仄", "meaning": "楷模"},
                {"char": "松", "pinyin": "sōng", "kangxi_strokes": 8, "pingze": "平", "meaning": "松树"},
            ],
            "火": [
                {"char": "炎", "pinyin": "yán", "kangxi_strokes": 8, "pingze": "平", "meaning": "火焰"},
                {"char": "烁", "pinyin": "shuò", "kangxi_strokes": 9, "pingze": "仄", "meaning": "闪耀"},
                {"char": "焕", "pinyin": "huàn", "kangxi_strokes": 11, "pingze": "仄", "meaning": "焕发"},
                {"char": "昱", "pinyin": "yù", "kangxi_strokes": 9, "pingze": "仄", "meaning": "光明"},
            ],
            "土": [
                {"char": "坤", "pinyin": "kūn", "kangxi_strokes": 8, "pingze": "平", "meaning": "大地"},
                {"char": "城", "pinyin": "chéng", "kangxi_strokes": 9, "pingze": "平", "meaning": "城市"},
                {"char": "宇", "pinyin": "yǔ", "kangxi_strokes": 6, "pingze": "仄", "meaning": "宇宙"},
                {"char": "安", "pinyin": "ān", "kangxi_strokes": 6, "pingze": "平", "meaning": "平安"},
            ],
            "金": [
                {"char": "鑫", "pinyin": "xīn", "kangxi_strokes": 24, "pingze": "平", "meaning": "多金"},
                {"char": "锐", "pinyin": "ruì", "kangxi_strokes": 15, "pingze": "仄", "meaning": "锐利"},
                {"char": "锋", "pinyin": "fēng", "kangxi_strokes": 15, "pingze": "平", "meaning": "锋芒"},
                {"char": "铭", "pinyin": "míng", "kangxi_strokes": 11, "pingze": "平", "meaning": "铭记"},
            ],
            "水": [
                {"char": "涵", "pinyin": "hán", "kangxi_strokes": 12, "pingze": "平", "meaning": "涵养"},
                {"char": "浩", "pinyin": "hào", "kangxi_strokes": 11, "pingze": "仄", "meaning": "浩大"},
                {"char": "涛", "pinyin": "tāo", "kangxi_strokes": 10, "pingze": "平", "meaning": "波涛"},
                {"char": "泽", "pinyin": "zé", "kangxi_strokes": 8, "pingze": "平", "meaning": "恩泽"},
                {"char": "渊", "pinyin": "yuān", "kangxi_strokes": 12, "pingze": "平", "meaning": "深渊"},
            ]
        }

        # 准备适合字字典
        suitable_chars_dict = {
            "suitable_chars": simple_chars,
            "priority_order": [yong_shen, xi_shen] if yong_shen != xi_shen else [yong_shen],
            "zodiac": zodiac,
            "yong_shen": yong_shen,
            "xi_shen": xi_shen
        }

        # 生成名字建议
        print("正在生成名字建议...")
        name_result = generate_name_suggestions.invoke({
            "suitable_chars": suitable_chars_dict,
            "bazi_analysis": bazi_analysis,
            "count": 10
        })

        if name_result.get("names"):
            # 格式化输出 - 直接使用函数而不是工具
            names_list = name_result.get("names", [])

            formatted_output = []
            formatted_output.append("=" * 60)
            formatted_output.append("名字建议")
            formatted_output.append("=" * 60)

            for i, name_info in enumerate(names_list, 1):
                name = name_info.get("name", "")
                name_type = name_info.get("type", "")
                pinyin = name_info.get("pinyin", "")
                meaning = name_info.get("meaning", "")
                source = name_info.get("source", "")
                bazi_match = name_info.get("bazi_match", "")
                score = name_info.get("score", 0)

                formatted_output.append(f"\n{i}. 【{name}】（{pinyin}）- {name_type}")
                formatted_output.append(f"   寓意：{meaning}")

                if source:
                    formatted_output.append(f"   出处：{source}")

                if bazi_match:
                    formatted_output.append(f"   八字匹配：{bazi_match}")

                wuxing = name_info.get("wuxing", {})
                pingze = name_info.get("pingze", {})
                strokes = name_info.get("strokes", {})

                wuxing_str = "，".join([f"{k}: {v}" for k, v in wuxing.items()])
                pingze_str = "，".join([f"{k}: {v}" for k, v in pingze.items()])
                strokes_str = "，".join([f"{k}: {v}画" for k, v in strokes.items()])

                formatted_output.append(f"   五行：{wuxing_str}")
                formatted_output.append(f"   平仄：{pingze_str}")
                formatted_output.append(f"   笔画：{strokes_str}")
                formatted_output.append(f"   评分：{score}/100")

            formatted_output.append("\n" + "=" * 60)

            print("\n" + "-" * 80)
            print("【四、取名建议】")
            print("-" * 80)

            print("\n".join(formatted_output))

            return True
        else:
            print(f"\n❌ 取名建议生成失败：{name_result.get('error', '未知错误')}")
            return False

    except Exception as e:
        print(f"\n❌ 生成取名建议时出错：{e}")
        import traceback
        traceback.print_exc()
        return False


def interactive_bazi_with_naming():
    """交互式八字分析和取名"""

    print("\n" + "=" * 80)
    print("八字分析 + 取名建议 交互系统")
    print("=" * 80)

    try:
        # 创建LLM
        print("\n连接Qwen模型...")
        llm = create_qwen_llm()
        print("✓ 连接成功")

        # 创建计算器
        calculator = IntelligentBaziCalculator(llm)

        # 交互循环
        while True:
            print("\n\n" + "=" * 80)
            print("请输入出生信息（或输入'quit'退出）")
            print("=" * 80)
            print("示例：1990年3月15日上午10点30分，男")

            user_input = input("\n请输入：").strip()

            if not user_input:
                continue

            if user_input.lower() in ['quit', '退出', 'exit']:
                print("\n感谢使用！")
                break

            try:
                # 计算八字
                result = calculator.calculate_from_natural_language(user_input)
                bazi = result.get('bazi')

                if not bazi:
                    print("\n❌ 八字计算失败")
                    continue

                # 输出八字
                print("\n" + "-" * 80)
                print("【一、八字四柱】")
                print("-" * 80)
                print(f"年柱：{bazi['year']['full']}（{bazi['year']['gan_wuxing']} {bazi['year']['zhi_wuxing']}）")
                print(f"月柱：{bazi['month']['full']}（{bazi['month']['gan_wuxing']} {bazi['month']['zhi_wuxing']}）节气：{bazi['month']['jieqi']}")
                print(f"日柱：{bazi['day']['full']}（{bazi['day']['gan_wuxing']} {bazi['day']['zhi_wuxing']}）日主：{bazi['day']['gan']}")
                print(f"时柱：{bazi['hour']['full']}（{bazi['hour']['gan_wuxing']} {bazi['hour']['zhi_wuxing']}）")

                # 五行分析
                wuxing_analysis = WuxingAnalyzer.analyze_comprehensive(bazi)

                print("\n" + "-" * 80)
                print("【二、五行分析】")
                print("-" * 80)

                wuxing_count = wuxing_analysis["wuxing_count"]
                print("\n五行统计：")
                for wuxing in ["木", "火", "土", "金", "水"]:
                    count = wuxing_count.get(wuxing, 0)
                    bar = "█" * count
                    print(f"  {wuxing}：{count}个 {bar}")

                print(f"\n日主强弱：{wuxing_analysis['strength']}")

                yong_shen_info = wuxing_analysis["yong_shen_info"]
                print(f"\n用神推算：")
                print(f"  用神：{yong_shen_info['yong_shen']}")
                print(f"  喜神：{yong_shen_info['xi_shen']}")
                print(f"  忌神：{', '.join(yong_shen_info['ji_shen'])}")

                # 命格分析
                mingge_analysis = MingGeAnalyzer.analyze_comprehensive(bazi, wuxing_analysis)

                print("\n" + "-" * 80)
                print("【三、命格分析】")
                print("-" * 80)

                pattern = mingge_analysis["pattern_analysis"]
                print(f"\n格局：{pattern['pattern_name']}")

                personality = mingge_analysis["personality_analysis"]
                print(f"性格：{', '.join(personality['traits'])}")

                career_wealth = mingge_analysis["career_wealth_analysis"]
                print(f"适合事业：{', '.join(career_wealth['suitable_careers'][:5])}")

                health = mingge_analysis["health_analysis"]
                if health['health_issues']:
                    print(f"健康：{', '.join(health['health_issues'])}")

                # 询问是否需要取名建议
                print("\n" + "=" * 80)
                need_naming = input("是否需要取名建议？(y/n): ").strip().lower()

                if need_naming in ['y', 'yes', '是', 'Y', 'YES']:
                    # 询问性别（用于取名）
                    print("\n请选择需要取名的人：")
                    print("1. 男孩")
                    print("2. 女孩")

                    gender_choice = input("请选择（1或2）: ").strip()
                    if gender_choice in ['1', '2']:
                        # 生成取名建议
                        success = generate_naming_suggestions(bazi, wuxing_analysis, llm)
                        if not success:
                            print("\n取名建议生成失败，请稍后再试")
                    else:
                        print("\n无效选择，跳过取名建议")
                else:
                    print("\n跳过取名建议")

                print("\n" + "=" * 80)

            except Exception as e:
                print(f"\n❌ 处理失败：{e}")
                import traceback
                traceback.print_exc()

    except KeyboardInterrupt:
        print("\n\n程序已退出")
    except Exception as e:
        print(f"\n❌ 初始化失败：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    interactive_bazi_with_naming()
