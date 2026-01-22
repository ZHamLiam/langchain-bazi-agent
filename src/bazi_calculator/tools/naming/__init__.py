"""取名分析工具模块"""

from bazi_calculator.tools.naming.bazi_for_naming import (
    analyze_bazi_for_naming,
    get_naming_priorities,
    check_name_wuxing_balance,
)
from bazi_calculator.tools.naming.suitable_chars import (
    get_suitable_chars,
    filter_suitable_chars_by_strokes,
    get_top_suitable_chars,
    get_suitable_chars_by_wuxing,
    format_suitable_chars,
)
from bazi_calculator.tools.naming.name_generator import (
    generate_name_suggestions,
    format_name_suggestions,
    filter_names_by_score,
    sort_names_by_score,
    get_top_names,
)
from bazi_calculator.tools.naming.batch_name_generator import (
    generate_batch_names,
    format_batch_names,
    filter_batch_names_by_score,
)
from bazi_calculator.tools.naming.pingze_analysis import (
    analyze_name_pingze,
    check_pingze_harmony,
    compare_name_pingze,
    get_pingze_suggestions,
    format_pingze_analysis,
    check_multiple_names_pingze,
    get_pingze_pattern_statistics,
)
from bazi_calculator.tools.naming.stroke_analysis import (
    analyze_name_strokes,
    check_strokes_harmony,
    compare_name_strokes,
    get_strokes_suggestions,
    format_strokes_analysis,
    check_multiple_names_strokes,
    get_strokes_by_range,
)
from bazi_calculator.tools.naming.sangcai_wuge import (
    calculate_wuge,
    calculate_sancai,
    analyze_sancai_wuge,
    format_sancai_wuge_analysis,
    compare_sancai_wuge,
)
from bazi_calculator.tools.naming.comprehensive_analysis import (
    comprehensive_name_analysis,
    compare_names_comprehensive,
    get_best_names,
    format_comprehensive_analysis,
)
from bazi_calculator.tools.naming.char_library_generator import (
    generate_character_library,
    save_character_library,
    load_character_library,
    get_chars_by_wuxing,
    filter_chars_by_zodiac,
)

__all__ = [
    # 八字取名分析
    "analyze_bazi_for_naming",
    "get_naming_priorities",
    "check_name_wuxing_balance",
    # 适合字查询
    "get_suitable_chars",
    "filter_suitable_chars_by_strokes",
    "get_top_suitable_chars",
    "get_suitable_chars_by_wuxing",
    "format_suitable_chars",
    # 名字生成
    "generate_name_suggestions",
    "format_name_suggestions",
    "filter_names_by_score",
    "sort_names_by_score",
    "get_top_names",
    # 批量取名
    "generate_batch_names",
    "format_batch_names",
    "filter_batch_names_by_score",
    # 平仄分析
    "analyze_name_pingze",
    "check_pingze_harmony",
    "compare_name_pingze",
    "get_pingze_suggestions",
    "format_pingze_analysis",
    "check_multiple_names_pingze",
    "get_pingze_pattern_statistics",
    # 笔画分析
    "analyze_name_strokes",
    "check_strokes_harmony",
    "compare_name_strokes",
    "get_strokes_suggestions",
    "format_strokes_analysis",
    "check_multiple_names_strokes",
    "get_strokes_by_range",
    # 三才五格
    "calculate_wuge",
    "calculate_sancai",
    "analyze_sancai_wuge",
    "format_sancai_wuge_analysis",
    "compare_sancai_wuge",
    # 综合分析
    "comprehensive_name_analysis",
    "compare_names_comprehensive",
    "get_best_names",
    "format_comprehensive_analysis",
    # 字库生成
    "generate_character_library",
    "save_character_library",
    "load_character_library",
    "get_chars_by_wuxing",
    "filter_chars_by_zodiac",
]
