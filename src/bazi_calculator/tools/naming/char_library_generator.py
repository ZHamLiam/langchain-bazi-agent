"""字库生成工具

使用LLM生成汉字字库，包含五行、拼音、康熙笔画、生肖宜忌、平仄、寓意、出处等信息
"""

import json
from typing import Dict, Any, List, Optional
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def generate_character_library(
    wuxing_categories: Optional[List[str]] = None,
    count_per_category: int = 50
) -> Dict[str, Any]:
    """生成汉字字库

    为指定的五行分类生成汉字，每个汉字包含：
    - 字符
    - 拼音
    - 五行属性
    - 康熙笔画
    - 生肖宜忌
    - 平仄声调
    - 寓意
    - 出处

    Args:
        wuxing_categories: 五行分类列表，如["木", "火", "土", "金", "水"]，默认全部
        count_per_category: 每个分类生成的字数，默认50个

    Returns:
        字库字典，按五行分类
    """
    if wuxing_categories is None:
        wuxing_categories = ["木", "火", "土", "金", "水"]

    llm = ChatOpenAI(model="gpt-4", temperature=0.7)

    char_library = {}

    for wuxing in wuxing_categories:
        prompt = f"""请为{wuxing}属性的汉字生成{count_per_category}个适合取名的汉字。

请严格按照以下JSON格式输出：
[
    {{
        "char": "字",
        "pinyin": "pīnyīn",
        "wuxing": "{wuxing}",
        "kangxi_strokes": 笔画数,
        "zodiac_favor": ["生肖1", "生肖2"],
        "zodiac_avoid": ["生肖1", "生肖2"],
        "pingze": "平/仄",
        "meaning": "字义解释",
        "source": "出处，如《诗经》、《楚辞》等"
    }}
]

要求：
1. 选择寓意美好、适合取名的常用汉字
2. 确保五行属性准确
3. 康熙笔画要准确（参考康熙字典）
4. 生肖宜忌要准确
5. 平仄要准确（一声二声为平，三声四声为仄）
6. 寓意要简洁优美
7. 出处尽可能注明经典文献

请只返回JSON数组，不要有其他说明文字。"""

        try:
            response = llm.invoke(prompt)
            content = response.content

            if isinstance(content, str):
                content_str = content
            else:
                content_str = str(content)

            # 尝试解析JSON
            try:
                chars_data = json.loads(content_str)
            except json.JSONDecodeError:
                import re
                json_match = re.search(r'\[.*\]', content_str, re.DOTALL)
                if json_match:
                    chars_data = json.loads(json_match.group(0))
                else:
                    raise ValueError(f"无法解析LLM响应：{content_str}")

            if not isinstance(chars_data, list):
                chars_data = []

            char_library[wuxing] = chars_data

        except Exception as e:
            print(f"生成{wuxing}属性字库失败：{e}")
            char_library[wuxing] = []

    return char_library


@tool
def save_character_library(char_library: Dict[str, Any], filepath: str) -> Dict[str, Any]:
    """保存字库到文件

    Args:
        char_library: 字库字典
        filepath: 保存路径

    Returns:
        保存结果
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(char_library, f, ensure_ascii=False, indent=2)

        return {
            "success": True,
            "filepath": filepath,
            "message": f"字库已保存到 {filepath}"
        }
    except Exception as e:
        return {
            "success": False,
            "filepath": filepath,
            "message": f"保存失败：{str(e)}"
        }


@tool
def load_character_library(filepath: str) -> Dict[str, Any]:
    """从文件加载字库

    Args:
        filepath: 文件路径

    Returns:
        字库字典
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            char_library = json.load(f)

        return {
            "success": True,
            "char_library": char_library,
            "message": f"字库已从 {filepath} 加载"
        }
    except Exception as e:
        return {
            "success": False,
            "char_library": None,
            "message": f"加载失败：{str(e)}"
        }


@tool
def get_chars_by_wuxing(char_library: Dict[str, Any], wuxing: str, count: int = 25) -> List[Dict[str, Any]]:
    """按五行获取适合的字

    Args:
        char_library: 字库字典
        wuxing: 五行属性
        count: 返回的字数，默认25个

    Returns:
        字符列表
    """
    if wuxing not in char_library:
        return []

    chars = char_library[wuxing]
    return chars[:count]


@tool
def filter_chars_by_zodiac(
    chars: List[Dict[str, Any]],
    zodiac: str,
    favor_only: bool = True
) -> List[Dict[str, Any]]:
    """按生肖过滤字符

    Args:
        chars: 字符列表
        zodiac: 生肖
        favor_only: 是否只显示宜用的字，默认True

    Returns:
        过滤后的字符列表
    """
    filtered = []

    for char_info in chars:
        if favor_only:
            if "zodiac_favor" in char_info and zodiac in char_info["zodiac_favor"]:
                filtered.append(char_info)
        else:
            if "zodiac_favor" in char_info and zodiac not in char_info["zodiac_avoid"]:
                filtered.append(char_info)

    return filtered
