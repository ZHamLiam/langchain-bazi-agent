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
from bazi_calculator.tools.naming.stroke_analysis import check_strokes_luck, check_strokes_comprehensive, format_strokes_luck_analysis
from bazi_calculator.tools.naming.pingze_analysis import check_pingze_harmony
from bazi_calculator.tools.naming.sangcai_wuge import analyze_sancai_wuge

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


def extract_gender_from_input(user_input: str) -> str:
    """从用户输入中提取性别

    Args:
        user_input: 用户输入的文本

    Returns:
        性别（男/女），如果没有则返回空字符串
    """
    user_input = user_input.strip()
    
    # 检查性别关键词
    male_keywords = ['男', '男性', '男孩', '公子', '先生']
    female_keywords = ['女', '女性', '女孩', '千金', '女士']
    
    for keyword in male_keywords:
        if keyword in user_input:
            return '男'
    
    for keyword in female_keywords:
        if keyword in user_input:
            return '女'
    
    return ''


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

        # 生成名字建议
        print("正在生成名字建议...")
        name_result = generate_name_suggestions.invoke({
            "bazi_analysis": bazi_analysis,
            "count": 10
        })

        if name_result.get("names"):
            # 格式化输出 - 直接使用函数而不是工具
            names_list = name_result.get("names", [])

            formatted_output = []
            formatted_output.append("=" * 60)
            formatted_output.append("名字建议（含81数理分析）")
            formatted_output.append("=" * 60)

            for i, name_info in enumerate(names_list, 1):
                name = name_info.get("name", "")
                name_type = name_info.get("type", "")
                pinyin = name_info.get("pinyin", "")
                meaning = name_info.get("meaning", "")
                source = name_info.get("source", "")
                bazi_match = name_info.get("bazi_match", "")
                score = name_info.get("score", 0)
                numerology = name_info.get("numerology", {})

                formatted_output.append(f"\n{i}. 【{name}】（{pinyin}）- {name_type}")
                formatted_output.append(f"   寓意：{meaning}")

                if source:
                    formatted_output.append(f"   出处：{source}")

                if bazi_match:
                    formatted_output.append(f"   八字匹配：{bazi_match}")

                # 五行、平仄、笔画
                wuxing = name_info.get("wuxing", {})
                pingze = name_info.get("pingze", {})
                strokes = name_info.get("strokes", {})

                wuxing_str = "，".join([f"{k}: {v}" for k, v in wuxing.items()])
                pingze_str = "，".join([f"{k}: {v}" for k, v in pingze.items()])
                strokes_str = "，".join([f"{k}: {v}画" for k, v in strokes.items()])

                formatted_output.append(f"   五行：{wuxing_str}")
                formatted_output.append(f"   平仄：{pingze_str}")
                formatted_output.append(f"   笔画：{strokes_str}")

                    # 81数理分析（如果LLM提供了）
                if numerology:
                    total_numerology = numerology.get("total_strokes_numerology", "")
                    total_luck = numerology.get("total_luck", "")
                    total_score = numerology.get("total_score", 0)
                    total_description = numerology.get("total_description", "")
                    total_detail = numerology.get("total_detail", "")
                    char_numerology = numerology.get("char_numerology", [])

                    formatted_output.append(f"\n   【81数理分析】")
                    formatted_output.append(f"   总笔画81数理：{total_numerology}数")
                    formatted_output.append(f"   吉凶：{total_luck}")
                    formatted_output.append(f"   评分：{total_score}/100")
                    formatted_output.append(f"   含义：{total_description}")
                    formatted_output.append(f"   详细：{' '.join(total_detail) if total_detail else '暂无'}")

                    # 单字81数理
                    if char_numerology:
                        formatted_output.append(f"   单字81数理：")
                        for char_info in char_numerology:
                            char = char_info.get("char", "")
                            strokes_num = char_info.get("strokes_numerology", "")
                            luck = char_info.get("luck", "")
                            description = char_info.get("description", "")
                            formatted_output.append(f"     {char}字{strokes_num}数：{luck} - {description}")

                formatted_output.append(f"   综合评分：{score}/100")

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


def analyze_user_name(user_name: str, bazi, wuxing_analysis, llm):
    """分析用户提供的姓名"""

    print("\n" + "=" * 80)
    print("正在分析姓名...")
    print("=" * 80)

    try:
        # 准备八字分析数据
        bazi_data = {
            "zodiac": get_zodiac(bazi.get("birth_info", {}).get("year", 0)),
            "day_master": bazi["day"]["gan"],
            "day_master_wuxing": bazi["day"]["gan_wuxing"],
            "yong_shen": wuxing_analysis["yong_shen_info"]["yong_shen"],
            "xi_shen": wuxing_analysis["yong_shen_info"]["xi_shen"],
            "ji_shen": wuxing_analysis["yong_shen_info"]["ji_shen"],
            "strength": wuxing_analysis["strength"]
        }

        # 1. 使用工具函数进行分析
        name = user_name

        # 笔画吉凶分析
        stroke_luck_result = check_strokes_luck.invoke({"name": name})

        # 笔画综合分析（和谐度+吉凶）
        stroke_comprehensive_result = check_strokes_comprehensive.invoke({"name": name})

        # 平仄分析
        pingze_result = check_pingze_harmony.invoke({"name": name})

        # 三才五格分析（使用"李"作为默认姓氏）
        surname = "李"
        sangcai_wuge_result = analyze_sancai_wuge.invoke({"name": name, "surname": surname})

        # 构建prompt让LLM补充寓意、出处等信息
        prompt = f"""请对以下姓名进行分析，补充寓意和出处信息。

【八字信息】
- 生肖：{bazi_data['zodiac']}
- 日主：{bazi_data['day_master']}（{bazi_data['day_master_wuxing']}）
- 日主强弱：{bazi_data['strength']}
- 用神：{bazi_data['yong_shen']}
- 喜神：{bazi_data['xi_shen']}
- 忌神：{', '.join(bazi_data['ji_shen'])}

【待分析姓名】
姓名：{name}

【注意】
- 姓名的第一个字是姓氏，这是家族传承，不应建议更换
- 只需要分析名（即除第一个字之外的部分），或整体分析即可
- 如果名只有一个字，就分析这个字

【81数理分析结果】
- 总笔画81数理：{stroke_luck_result['total_strokes']}数
- 81数理吉凶：{stroke_luck_result['overall_luck']}（{stroke_luck_result['luck_description']}）

【分析要求】
1. 分析每个字的五行属性
2. 分析每个字的平仄声调（一声二声为平，三声四声为仄）
3. 评估姓名与八字的匹配度（是否符合用神、喜神）
4. 分析姓名的寓意和出处
5. 给出改进建议（如果需要的话，但不要建议更换姓氏）

请严格按照以下JSON格式输出：
{{
    "name": "姓名",
    "pinyin": "pīnyīn",
    "chars": ["字1", "字2"],
    "wuxing": {{"字1": "五行", "字2": "五行"}},
    "strokes": {{"字1": 笔画, "字2": 笔画}},
    "pingze": {{"字1": "平/仄", "字2": "平/仄"}},
    "wuxing_match": "符合用神/喜神/忌神",
    "meaning": "寓意解释",
    "source": "出处",
    "bazi_score": {{
        "yong_shen_match": 用神匹配分数(0-30),
        "xi_shen_match": 喜神匹配分数(0-20),
        "meaning_quality": 寓意质量分数(0-20)
    }},
    "analysis": "详细分析说明",
    "suggestions": ["改进建议1", "改进建议2"]
}}

评分标准：
- 符合用神：+30分
- 符合喜神：+20分
- 寓意质量：+20分

请只返回JSON对象，不要有其他说明文字。"""

        # 调用LLM分析
        response = llm.invoke(prompt)
        content = response.content

        if isinstance(content, str):
            content_str = content
        else:
            content_str = str(content)

        # 尝试解析JSON
        import json
        import re
        try:
            analysis_result = json.loads(content_str)
        except json.JSONDecodeError:
            json_match = re.search(r'\{.*\}', content_str, re.DOTALL)
            if json_match:
                analysis_result = json.loads(json_match.group(0))
            else:
                raise ValueError(f"无法解析LLM响应：{content_str}")

        # 格式化输出
        print("\n" + "-" * 80)
        print("【姓名分析】")
        print("-" * 80)

        pinyin = analysis_result.get("pinyin", "")
        chars = analysis_result.get("chars", [])
        wuxing = analysis_result.get("wuxing", {})
        strokes = analysis_result.get("strokes", {})
        pingze = analysis_result.get("pingze", {})
        total_strokes = stroke_luck_result['total_strokes']
        wuxing_match = analysis_result.get("wuxing_match", "")
        meaning = analysis_result.get("meaning", "")
        source = analysis_result.get("source", "")
        analysis_text = analysis_result.get("analysis", "")
        suggestions = analysis_result.get("suggestions", [])

        # 计算综合评分
        bazi_score = analysis_result.get("bazi_score", {})
        yong_shen_score = bazi_score.get('yong_shen_match', 0)
        xi_shen_score = bazi_score.get('xi_shen_match', 0)
        meaning_score = bazi_score.get('meaning_quality', 0)

        # 使用工具函数的评分
        pingze_score = pingze_result.get('score', 0)
        stroke_luck_score = stroke_luck_result.get('luck_score', 0)
        sangcai_wuge_score = sangcai_wuge_result.get('overall_score', 0)

        # 综合评分：八字五行50%（用神+喜神+寓意），平仄15%，笔画吉凶20%，三才五格15%
        total_score = (
            (yong_shen_score + xi_shen_score + meaning_score) * 0.50 +
            pingze_score * 0.15 +
            stroke_luck_score * 0.20 +
            sangcai_wuge_score * 0.15
        )

        print(f"\n姓名：{name}（{pinyin}）")
        print(f"总笔画：{total_strokes}画")

        print(f"\n【单字分析】")
        for char in chars:
            print(f"  {char}")
            print(f"    五行：{wuxing.get(char, '')}")
            print(f"    笔画：{strokes.get(char, '')}画")
            print(f"    平仄：{pingze.get(char, '')}")

        print(f"\n【八字匹配度】（权重50%）")
        print(f"  用神匹配：{yong_shen_score}/30")
        print(f"  喜神匹配：{xi_shen_score}/20")
        print(f"  寓意质量：{meaning_score}/20")

        print(f"\n【81数理吉凶分析】（权重20%）")
        harmony = stroke_comprehensive_result.get('harmony', {})
        luck = stroke_comprehensive_result.get('luck', {})
        print(f"  和谐得分：{harmony.get('score', 0)}/100 - {harmony.get('description', '')}")
        print(f"  81数理吉凶得分：{luck.get('luck_score', 0)}/100 - {luck.get('luck_description', '')}")
        print(f"  整体81数理吉凶：{luck.get('overall_luck', '')}")
        print(f"  综合得分：{stroke_comprehensive_result.get('comprehensive_score', 0)}/100")

        print(f"\n【平仄分析】（权重15%）")
        print(f"  模式：{pingze_result.get('pattern', '')}")
        print(f"  得分：{pingze_score}/100 - {pingze_result.get('description', '')}")

        print(f"\n【三才五格分析】（权重15%）")
        sancai = sangcai_wuge_result.get('sancai', {})
        wuge = sangcai_wuge_result.get('wuge', {})
        print(f"  三才配置：{sancai.get('sancai_pattern', '')}（{sancai.get('sancai_score', 0)}分）")
        print(f"  综合得分：{sangcai_wuge_score}/100 - {sangcai_wuge_result.get('evaluation', '')}")

        print(f"\n【综合评分】：{total_score:.1f}/100")

        print(f"\n【匹配结果】")
        print(f"  {wuxing_match}")

        print(f"\n【寓意说明】")
        print(f"  {meaning}")

        if source:
            print(f"\n【出处】")
            print(f"  {source}")

        print(f"\n【详细分析】")
        print(f"  {analysis_text}")

        if suggestions:
            print(f"\n【改进建议】")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  {i}. {suggestion}")

        # 给出总体评价
        if total_score >= 80:
            print(f"\n【总体评价】")
            print(f"  ✅ 优秀！{name} 与八字匹配度很高，81数理吉凶良好，寓意美好，是一个很好的名字。")
        elif total_score >= 60:
            print(f"\n【总体评价】")
            print(f"  ⚠️  良好！{name} 与八字匹配度较好，但还有提升空间。")
        elif total_score >= 40:
            print(f"\n【总体评价】")
            print(f"  ❌ 一般。{name} 与八字匹配度一般，建议考虑改进。")
        else:
            print(f"\n【总体评价】")
            print(f"  ⚠️  较差。{name} 与八字匹配度较低，建议参考改进建议。")

        print("\n" + "-" * 80)

        return True

    except Exception as e:
        print(f"\n❌ 分析姓名时出错：{e}")
        import traceback
        traceback.print_exc()
        return False


def interactive_bazi_with_naming():
    """交互式八字分析和取名"""

    print("\n" + "=" * 80)
    print("八字分析 + 取名建议 + 姓名分析 交互系统")
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
            print("示例1：1990年3月15日上午10点30分，男")
            print("示例2：1990年3月15日10点30分，女孩")
            print("示例3：1990-03-15 10:30，男性")

            user_input = input("\n请输入：").strip()

            if not user_input:
                continue

            if user_input.lower() in ['quit', '退出', 'exit']:
                print("\n感谢使用！")
                break

            try:
                # 提取性别信息
                gender = extract_gender_from_input(user_input)
                
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
                    # 如果用户已在输入中提供性别，则直接使用；否则询问
                    naming_gender = gender
                    if not naming_gender:
                        # 询问性别（用于取名）
                        print("\n请选择需要取名的人：")
                        print("1. 男孩")
                        print("2. 女孩")

                        gender_choice = input("请选择（1或2）: ").strip()
                        if gender_choice == '1':
                            naming_gender = '男'
                        elif gender_choice == '2':
                            naming_gender = '女'
                    
                    if naming_gender:
                        # 生成取名建议
                        print(f"\n为{naming_gender}孩生成取名建议...")
                        success = generate_naming_suggestions(bazi, wuxing_analysis, llm)
                        if not success:
                            print("\n取名建议生成失败，请稍后再试")
                    else:
                        print("\n无效选择，跳过取名建议")
                else:
                    print("\n跳过取名建议")

                # 询问是否有心仪的姓名需要分析
                print("\n" + "=" * 80)
                need_name_analysis = input("是否有心仪的姓名需要分析？(y/n): ").strip().lower()

                if need_name_analysis in ['y', 'yes', '是', 'Y', 'YES']:
                    user_name = input("\n请输入姓名：").strip()
                    if user_name:
                        # 分析用户提供的姓名
                        analyze_user_name(user_name, bazi, wuxing_analysis, llm)
                    else:
                        print("\n姓名不能为空，跳过姓名分析")
                else:
                    print("\n跳过姓名分析")

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
