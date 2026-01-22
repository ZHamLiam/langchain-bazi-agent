"""名字生成工具

使用LLM生成名字建议，包含详细分析
"""

import json
import os
from typing import Dict, Any, List, Optional
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def generate_name_suggestions(
    suitable_chars: Dict[str, Any],
    bazi_analysis: Dict[str, Any],
    count: int = 10
) -> Dict[str, Any]:
    """生成名字建议

    使用LLM根据八字分析和适合字列表生成10个名字
    包含单字名和双字名，每个名字都有详细分析

    Args:
        suitable_chars: 适合字字典
        bazi_analysis: 八字分析结果
        count: 生成名字数量，默认10个

    Returns:
        名字建议列表
    """

    llm = ChatOpenAI(
        model=os.getenv('QWEN_MODEL', 'qwen-flash'),
        api_key=os.getenv('QWEN_API_KEY'),
        base_url=os.getenv('QWEN_BASE_URL'),
        temperature=0.7
    )

    # 提取适合字
    suitable_chars_dict = suitable_chars.get("suitable_chars", {})

    # 为每个五行选择几个代表字
    representative_chars = {}
    for wuxing, chars in suitable_chars_dict.items():
        representative_chars[wuxing] = [
            f"{char_info['char']}({char_info.get('pinyin', '')})"
            for char_info in chars[:5]
        ]

    # 构建prompt
    prompt = f"""请根据以下信息生成{count}个适合的名字（单字名和双字名各一半）

【八字信息】
- 生肖：{bazi_analysis['zodiac']}
- 日主：{bazi_analysis['day_master']}（{bazi_analysis['day_master_wuxing']}）
- 用神：{bazi_analysis['yong_shen']}
- 喜神：{bazi_analysis['xi_shen']}

【适合字列表】
{json.dumps(representative_chars, ensure_ascii=False, indent=2)}

【取名要求】
1. 优先使用用神和喜神的字
2. 名字寓意要美好、积极向上
3. 平仄搭配要和谐
4. 笔画要适中（5-15画之间）
5. 出自经典文献优先（如《诗经》、《楚辞》、《论语》等）
6. 避免生僻字和容易读错的字
7. 单字名和双字名各一半

请严格按照以下JSON格式输出：
[
    {{
        "name": "名字",
        "type": "单字/双字",
        "chars": ["字1", "字2"],
        "pinyin": "pīnyīn",
        "wuxing": {{"字1": "五行", "字2": "五行"}},
        "pingze": {{"字1": "平/仄", "字2": "平/仄"}},
        "strokes": {{"字1": 笔画, "字2": 笔画}},
        "meaning": "字义解释",
        "source": "出处，如《诗经·XXX》",
        "bazi_match": "与八字的匹配度说明",
        "score": 90
    }}
]

评分标准：
- 符合用神：+30分
- 符合喜神：+20分
- 寓意优美：+20分
- 平仄和谐：+15分
- 出自经典：+15分

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
            name_suggestions = json.loads(content_str)
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\[.*\]', content_str, re.DOTALL)
            if json_match:
                name_suggestions = json.loads(json_match.group(0))
            else:
                raise ValueError(f"无法解析LLM响应：{content_str}")

        if not isinstance(name_suggestions, list):
            name_suggestions = []

        # 补充生肖信息
        for name_info in name_suggestions:
            name_info["zodiac"] = bazi_analysis['zodiac']
            name_info["yong_shen"] = bazi_analysis['yong_shen']
            name_info["xi_shen"] = bazi_analysis['xi_shen']

        return {
            "names": name_suggestions,
            "count": len(name_suggestions),
            "bazi_analysis": bazi_analysis,
            "summary": f"已生成{len(name_suggestions)}个名字建议"
        }

    except Exception as e:
        print(f"生成名字建议失败：{e}")
        return {
            "names": [],
            "count": 0,
            "error": str(e),
            "summary": "生成名字建议失败"
        }


@tool
def format_name_suggestions(name_suggestions: List[Dict[str, Any]]) -> str:
    """格式化名字建议为文本

    Args:
        name_suggestions: 名字建议列表

    Returns:
        格式化后的文本
    """
    output = []
    output.append("=" * 60)
    output.append("名字建议")
    output.append("=" * 60)

    for i, name_info in enumerate(name_suggestions, 1):
        name = name_info.get("name", "")
        name_type = name_info.get("type", "")
        pinyin = name_info.get("pinyin", "")
        meaning = name_info.get("meaning", "")
        source = name_info.get("source", "")
        bazi_match = name_info.get("bazi_match", "")
        score = name_info.get("score", 0)

        output.append(f"\n{i}. 【{name}】（{pinyin}）- {name_type}")
        output.append(f"   寓意：{meaning}")

        if source:
            output.append(f"   出处：{source}")

        if bazi_match:
            output.append(f"   八字匹配：{bazi_match}")

        # 五行和平仄
        wuxing = name_info.get("wuxing", {})
        pingze = name_info.get("pingze", {})
        strokes = name_info.get("strokes", {})

        wuxing_str = "，".join([f"{k}: {v}" for k, v in wuxing.items()])
        pingze_str = "，".join([f"{k}: {v}" for k, v in pingze.items()])
        strokes_str = "，".join([f"{k}: {v}画" for k, v in strokes.items()])

        output.append(f"   五行：{wuxing_str}")
        output.append(f"   平仄：{pingze_str}")
        output.append(f"   笔画：{strokes_str}")
        output.append(f"   评分：{score}/100")

    output.append("\n" + "=" * 60)

    return "\n".join(output)


@tool
def filter_names_by_score(
    name_suggestions: List[Dict[str, Any]],
    min_score: int = 80
) -> List[Dict[str, Any]]:
    """按分数过滤名字

    Args:
        name_suggestions: 名字建议列表
        min_score: 最低分数，默认80

    Returns:
        过滤后的名字列表
    """
    return [name for name in name_suggestions if name.get("score", 0) >= min_score]


@tool
def sort_names_by_score(name_suggestions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """按分数排序名字

    Args:
        name_suggestions: 名字建议列表

    Returns:
        排序后的名字列表
    """
    return sorted(name_suggestions, key=lambda x: x.get("score", 0), reverse=True)


@tool
def get_top_names(
    name_suggestions: List[Dict[str, Any]],
    top_count: int = 15
) -> List[Dict[str, Any]]:
    """获取Top N名字

    Args:
        name_suggestions: 名字建议列表
        top_count: 返回的顶级名字数，默认5个

    Returns:
        Top名字列表
    """
    sorted_names = sort_names_by_score(name_suggestions)
    return sorted_names[:top_count]
