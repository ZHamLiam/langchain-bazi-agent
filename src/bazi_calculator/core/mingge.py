"""命格分析模块

此模块提供八字命格分析功能，包括格局判断、性格分析、运势分析等。
"""

from typing import Dict, List, Tuple
from bazi_calculator.core.ganzhi import GanzhiCalculator


class MingGeAnalyzer:
    """命格分析器
    
    提供格局判断、性格分析、运势分析等功能。
    """

    @staticmethod
    def determine_pattern(bazi: Dict) -> Dict:
        """判断八字格局
        
        判断命局属于哪种格局（正格、从格、化气格等）
        
        Args:
            bazi: 八字信息字典
            
        Returns:
            包含格局信息的字典
        """
        day_master = bazi["day"]["gan"]
        day_master_wuxing = bazi["day"]["gan_wuxing"]
        month_zhi = bazi["month"]["zhi"]
        month_zhi_wuxing = bazi["month"]["zhi_wuxing"]
        
        # 获取日主强弱
        from bazi_calculator.core.wuxing import WuxingAnalyzer
        strength, scores = WuxingAnalyzer.analyze_day_master_strength(bazi)
        
        # 判断格局
        pattern_type = ""
        pattern_name = ""
        pattern_description = ""
        
        # 1. 正格判断
        if strength in ["强", "中和"]:
            if month_zhi_wuxing == day_master_wuxing:
                pattern_type = "正格"
                pattern_name = "建禄格"
                pattern_description = f"日主在月支得地（禄），日主{day_master}生于{month_zhi}月，得令得势，命主自立自强，个性坚毅。"
            
            # 检查是否有财格
            elif WuxingAnalyzer.count_wuxing_in_pillar(bazi["year"])["金"] + \
                 WuxingAnalyzer.count_wuxing_in_pillar(bazi["month"])["金"] + \
                 WuxingAnalyzer.count_wuxing_in_pillar(bazi["day"])["金"] + \
                 WuxingAnalyzer.count_wuxing_in_pillar(bazi["hour"])["金"] >= 3:
                if day_master_wuxing == "火":
                    pattern_type = "正格"
                    pattern_name = "财格"
                    pattern_description = f"财星（金）多且旺，日主{day_master}命财格，主财运旺盛，善于理财。"
            
            # 检查是否有官格
            elif WuxingAnalyzer.count_wuxing_in_pillar(bazi["year"])["木"] + \
                 WuxingAnalyzer.count_wuxing_in_pillar(bazi["month"])["木"] + \
                 WuxingAnalyzer.count_wuxing_in_pillar(bazi["day"])["木"] + \
                 WuxingAnalyzer.count_wuxing_in_pillar(bazi["hour"])["木"] >= 3:
                if day_master_wuxing == "土":
                    pattern_type = "正格"
                    pattern_name = "官格"
                    pattern_description = f"官星（木）多且旺，日主{day_master}命官格，主事业有成，适合从政。"
        
        # 2. 从格判断
        if strength == "弱":
            input_energy = scores.get('day_master', 0) + scores.get('yin', 0) + scores.get('bijie', 0)
            output_energy = scores.get('shishang', 0) + scores.get('cai', 0) + scores.get('guansha', 0)
            
            if output_energy > 0 and input_energy / output_energy < 0.5:
                pattern_type = "从格"
                
                # 判断从财
                cai_score = scores.get('cai', 0)
                guansha_score = scores.get('guansha', 0)
                shishang_score = scores.get('shishang', 0)
                
                if cai_score >= guansha_score and cai_score >= shishang_score:
                    pattern_name = "从财格"
                    pattern_description = f"日主{day_master}太弱，财星过旺，从财格，宜从商理财，以财为用。"
                elif guansha_score >= cai_score and guansha_score >= shishang_score:
                    pattern_name = "从官格"
                    pattern_description = f"日主{day_master}太弱，官星过旺，从官格，宜从政管理，以官为用。"
                else:
                    pattern_name = "从儿格"
                    pattern_description = f"日主{day_master}太弱，食伤过旺，从儿格，宜技艺求财，以食伤为用。"
        
        # 3. 化气格判断
        pattern_info = MingGeAnalyzer._check_huaqi(bazi)
        if pattern_info["is_huaqi"]:
            pattern_type = "化气格"
            pattern_name = pattern_info["pattern_name"]
            pattern_description = pattern_info["description"]
        
        # 默认格局
        if not pattern_type:
            pattern_type = "正格"
            pattern_name = "普通格局"
            pattern_description = f"日主{day_master}命局平衡，无明显特殊格局，宜根据用神喜神调节运势。"
        
        return {
            "pattern_type": pattern_type,
            "pattern_name": pattern_name,
            "pattern_description": pattern_description,
            "day_master": day_master,
            "day_master_wuxing": day_master_wuxing,
            "strength": strength
        }
    
    @staticmethod
    def _check_huaqi(bazi: Dict) -> Dict:
        """检查化气格
        
        Args:
            bazi: 八字信息字典
            
        Returns:
            化气格信息字典
        """
        # 化气条件：日干与月干或时干相合，且化神得地
        
        # 检查日主与月干是否化气
        day_gan = bazi["day"]["gan"]
        month_gan = bazi["month"]["gan"]
        hour_gan = bazi["hour"]["gan"]
        
        # 天干合化条件
        huaqi_pairs = {
            ("甲", "己"): ("土", "甲己化土"),
            ("乙", "庚"): ("金", "乙庚化金"),
            ("丙", "辛"): ("水", "丙辛化水"),
            ("丁", "壬"): ("木", "丁壬化木"),
            ("戊", "癸"): ("火", "戊癸化火"),
            ("己", "甲"): ("土", "甲己化土"),
            ("庚", "乙"): ("金", "乙庚化金"),
            ("辛", "丙"): ("水", "丙辛化水"),
            ("壬", "丁"): ("木", "丁壬化木"),
            ("癸", "戊"): ("火", "戊癸化火"),
        }
        
        # 检查日主与月干
        if (day_gan, month_gan) in huaqi_pairs:
            huaqi_wuxing, huaqi_name = huaqi_pairs[(day_gan, month_gan)]
            
            # 检查化神是否得地（在地支有根）
            has_root = False
            for pillar_name in ["year", "month", "day", "hour"]:
                if bazi[pillar_name]["zhi_wuxing"] == huaqi_wuxing:
                    has_root = True
                    break
            
            if has_root:
                return {
                    "is_huaqi": True,
                    "pattern_name": huaqi_name,
                    "description": f"日主{day_gan}与月干{month_gan}相合化为{huaqi_wuxing}，{huaqi_name}，格局清贵，利学业功名。"
                }
        
        # 检查日主与时干
        if (day_gan, hour_gan) in huaqi_pairs:
            huaqi_wuxing, huaqi_name = huaqi_pairs[(day_gan, hour_gan)]
            
            has_root = False
            for pillar_name in ["year", "month", "day", "hour"]:
                if bazi[pillar_name]["zhi_wuxing"] == huaqi_wuxing:
                    has_root = True
                    break
            
            if has_root:
                return {
                    "is_huaqi": True,
                    "pattern_name": huaqi_name,
                    "description": f"日主{day_gan}与时干{hour_gan}相合化为{huaqi_wuxing}，{huaqi_name}，格局清贵，利学业功名。"
                }
        
        return {
            "is_huaqi": False,
            "pattern_name": "",
            "description": ""
        }
    
    @staticmethod
    def analyze_personality(bazi: Dict) -> Dict:
        """分析性格特征
        
        Args:
            bazi: 八字信息字典
            
        Returns:
            性格分析字典
        """
        day_master = bazi["day"]["gan"]
        day_master_wuxing = bazi["day"]["gan_wuxing"]
        
        # 日主性格特征
        personality_traits = {
            "甲": {
                "traits": ["刚强", "正直", "有领导力", "独立自主"],
                "strengths": ["有主见", "有责任感", "有担当"],
                "weaknesses": ["固执", "不够灵活", "容易冲动"],
                "description": "甲木日主，如大树参天，为人正直刚毅，有领导才能，但有时过于固执。"
            },
            "乙": {
                "traits": ["温柔", "善良", "灵活", "善解人意"],
                "strengths": ["善于沟通", "适应力强", "有同情心"],
                "weaknesses": ["优柔寡断", "容易受影响", "缺乏主见"],
                "description": "乙木日主，如花草柔美，为人温柔善良，善于社交，但有时缺乏决断力。"
            },
            "丙": {
                "traits": ["热情", "开朗", "阳光", "有感染力"],
                "strengths": ["乐观向上", "有号召力", "富有激情"],
                "weaknesses": ["急躁", "容易冲动", "不够细心"],
                "description": "丙火日主，如太阳普照，为人热情开朗，有感染力，但有时过于急躁。"
            },
            "丁": {
                "traits": ["细腻", "敏感", "有洞察力", "温和"],
                "strengths": ["善解人意", "观察力强", "有创造力"],
                "weaknesses": ["多愁善感", "容易受伤害", "不够果断"],
                "description": "丁火日主，如烛光温暖，为人细腻敏感，善解人意，但有时多愁善感。"
            },
            "戊": {
                "traits": ["稳重", "可靠", "有担当", "踏实"],
                "strengths": ["责任心强", "值得信赖", "稳重可靠"],
                "weaknesses": ["保守", "不够灵活", "反应较慢"],
                "description": "戊土日主，如高山厚重，为人稳重可靠，有担当，但有时过于保守。"
            },
            "己": {
                "traits": ["温和", "包容", "善解人意", "有耐心"],
                "strengths": ["包容性强", "善于合作", "有亲和力"],
                "weaknesses": ["缺乏主见", "容易妥协", "不够自信"],
                "description": "己土日主，如田园滋润，为人温和包容，善于合作，但有时缺乏主见。"
            },
            "庚": {
                "traits": ["刚毅", "果断", "有魄力", "正直"],
                "strengths": ["决策能力强", "有魄力", "坚持不懈"],
                "weaknesses": ["过于强硬", "缺乏柔性", "容易树敌"],
                "description": "庚金日主，如钢铁坚硬，为人刚毅果断，有魄力，但有时过于强硬。"
            },
            "辛": {
                "traits": ["精致", "优雅", "有品味", "细腻"],
                "strengths": ["审美能力强", "注重细节", "有艺术天赋"],
                "weaknesses": ["追求完美", "过于挑剔", "容易纠结"],
                "description": "辛金日主，如珠宝精致，为人优雅有品味，注重细节，但有时过于挑剔。"
            },
            "壬": {
                "traits": ["聪明", "灵活", "适应力强", "善变"],
                "strengths": ["反应快", "学习能力强", "善于应变"],
                "weaknesses": ["不够专注", "容易分心", "缺乏耐心"],
                "description": "壬水日主，如江河奔流，为人聪明灵活，适应力强，但有时不够专注。"
            },
            "癸": {
                "traits": ["温柔", "智慧", "深沉", "敏感"],
                "strengths": ["有智慧", "善思考", "有直觉"],
                "weaknesses": ["过于敏感", "容易多想", "缺乏行动力"],
                "description": "癸水日主，如雨露滋润，为人温柔智慧，善于思考，但有时过于敏感。"
            }
        }
        
        personality = personality_traits.get(day_master, {})
        
        if not personality:
            personality = {
                "traits": ["平和", "中正"],
                "strengths": ["适应力强", "能屈能伸"],
                "weaknesses": ["缺乏特色", "过于中庸"],
                "description": f"{day_master}日主，性格平和，能屈能伸，易于相处。"
            }
        
        return personality
    
    @staticmethod
    def analyze_career_wealth(bazi: Dict, wuxing_analysis: Dict) -> Dict:
        """分析事业财运
        
        Args:
            bazi: 八字信息字典
            wuxing_analysis: 五行分析结果
            
        Returns:
            事业财运分析字典
        """
        day_master = bazi["day"]["gan"]
        yong_shen = wuxing_analysis["yong_shen_info"]["yong_shen"]
        xi_shen = wuxing_analysis["yong_shen_info"]["xi_shen"]
        ji_shen = wuxing_analysis["yong_shen_info"]["ji_shen"]
        strength = wuxing_analysis["strength"]
        
        # 根据用神和喜神分析适合的事业
        career_suggestions = []
        
        # 五行对应事业
        wuxing_to_career = {
            "金": ["金融", "银行", "珠宝", "汽车", "机械", "IT技术", "法律"],
            "木": ["教育", "文化", "艺术", "出版", "林业", "家具", "服装"],
            "水": ["贸易", "物流", "旅游", "水产", "航运", "饮料", "清洁"],
            "火": ["电子", "IT互联网", "能源", "餐饮", "娱乐", "广告", "媒体"],
            "土": ["房地产", "建筑", "农业", "矿产", "陶瓷", "古玩", "仓储"]
        }
        
        # 用神对应的事业
        if yong_shen in wuxing_to_career:
            career_suggestions.extend(wuxing_to_career[yong_shen])
        
        # 喜神对应的事业
        if xi_shen in wuxing_to_career:
            career_suggestions.extend(wuxing_to_career[xi_shen])
        
        # 财运分析
        cai_score = wuxing_analysis["scores"].get("cai", 0)
        wealth_analysis = []
        
        if cai_score > 5:
            wealth_analysis.append("财星较旺，财运较佳，善于理财")
        elif cai_score > 2:
            wealth_analysis.append("财运中等，需要努力积累")
        else:
            wealth_analysis.append("财星较弱，宜稳健理财，不宜投机")
        
        if "金" in ji_shen:
            wealth_analysis.append("金为忌神，不宜投资黄金、珠宝等")
        if "水" in ji_shen:
            wealth_analysis.append("水为忌神，不宜投资航运、水产等")
        
        # 事业成就分析
        guansha_score = wuxing_analysis["scores"].get("guansha", 0)
        career_achievement = []
        
        if guansha_score > 5:
            career_achievement.append("官星较旺，适合从政或管理岗位")
        elif guansha_score > 2:
            career_achievement.append("事业运中等，需要脚踏实地")
        else:
            career_achievement.append("官星较弱，不宜追求权力，适合技术或专业领域")
        
        return {
            "suitable_careers": list(set(career_suggestions)),
            "wealth_analysis": wealth_analysis,
            "career_achievement": career_achievement,
            "yong_shen": yong_shen,
            "xi_shen": xi_shen
        }
    
    @staticmethod
    def analyze_health(bazi: Dict) -> Dict:
        """分析健康运势
        
        Args:
            bazi: 八字信息字典
            
        Returns:
            健康分析字典
        """
        # 五行与健康
        wuxing_to_health = {
            "金": ["肺", "呼吸系统", "皮肤", "大肠"],
            "木": ["肝", "胆", "眼睛", "筋骨"],
            "水": ["肾", "膀胱", "耳朵", "生殖系统"],
            "火": ["心", "小肠", "舌头", "血液"],
            "土": ["脾", "胃", "肌肉", "消化系统"]
        }
        
        from bazi_calculator.core.wuxing import WuxingAnalyzer
        wuxing_count = WuxingAnalyzer.count_wuxing_in_bazi(bazi)
        
        health_issues = []
        health_suggestions = []
        
        # 检查五行缺失
        for wuxing, count in wuxing_count.items():
            if count == 0:
                organs = wuxing_to_health.get(wuxing, [])
                if organs:
                    health_issues.append(f"缺{wuxing}，注意{','.join(organs)}健康")
                    health_suggestions.append(f"多接触{wuxing}属性事物（如{wuxing}色、{wuxing}味等）")
            elif count >= 5:
                organs = wuxing_to_health.get(wuxing, [])
                if organs:
                    health_issues.append(f"{wuxing}过多，{','.join(organs)}可能过旺")
                    health_suggestions.append(f"平衡{wuxing}，避免过度消耗相关器官")
        
        # 检查日主健康
        day_master_wuxing = bazi["day"]["gan_wuxing"]
        main_organs = wuxing_to_health.get(day_master_wuxing, [])
        if main_organs:
            health_suggestions.append(f"日主为{day_master_wuxing}，要特别注意{','.join(main_organs)}的保养")
        
        return {
            "health_issues": health_issues,
            "health_suggestions": health_suggestions,
            "main_organs": main_organs
        }
    
    @staticmethod
    def analyze_comprehensive(bazi: Dict, wuxing_analysis: Dict) -> Dict:
        """综合命格分析
        
        Args:
            bazi: 八字信息字典
            wuxing_analysis: 五行分析结果
            
        Returns:
            综合命格分析字典
        """
        # 格局分析
        pattern_analysis = MingGeAnalyzer.determine_pattern(bazi)
        
        # 性格分析
        personality_analysis = MingGeAnalyzer.analyze_personality(bazi)
        
        # 事业财运分析
        career_wealth_analysis = MingGeAnalyzer.analyze_career_wealth(bazi, wuxing_analysis)
        
        # 健康分析
        health_analysis = MingGeAnalyzer.analyze_health(bazi)
        
        return {
            "pattern_analysis": pattern_analysis,
            "personality_analysis": personality_analysis,
            "career_wealth_analysis": career_wealth_analysis,
            "health_analysis": health_analysis
        }
