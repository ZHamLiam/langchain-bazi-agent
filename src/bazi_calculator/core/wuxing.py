"""五行分析模块

此模块提供五行分析功能，包括日主强弱分析和用神推算。
"""

from typing import Dict, List, Tuple
from collections import Counter
from bazi_calculator.core.ganzhi import GanzhiCalculator


class WuxingAnalyzer:
    """五行分析器
    
    提供五行统计、日主强弱分析和用神推算功能。
    """
    
    @staticmethod
    def count_wuxing_in_pillar(pillar: Dict[str, str]) -> Dict[str, int]:
        """统计单个柱中的五行数量
        
        Args:
            pillar: 柱信息字典，包含gan和zhi
            
        Returns:
            五行计数字典
        """
        wuxing_count = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
        
        # 统计天干五行
        if "gan" in pillar and "gan_wuxing" in pillar:
            gan_wuxing = pillar["gan_wuxing"]
            wuxing_count[gan_wuxing] += 1
        
        # 统计地支五行
        if "zhi" in pillar and "zhi_wuxing" in pillar:
            zhi_wuxing = pillar["zhi_wuxing"]
            wuxing_count[zhi_wuxing] += 1
        
        return wuxing_count
    
    @staticmethod
    def count_wuxing_in_bazi(bazi: Dict) -> Dict[str, int]:
        """统计八字四柱中的五行数量
        
        Args:
            bazi: 八字信息字典
            
        Returns:
            五行计数字典
        """
        wuxing_count = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
        
        for pillar_name in ["year", "month", "day", "hour"]:
            if pillar_name in bazi:
                pillar_count = WuxingAnalyzer.count_wuxing_in_pillar(bazi[pillar_name])
                for wuxing, count in pillar_count.items():
                    wuxing_count[wuxing] += count
        
        return wuxing_count
    
    @staticmethod
    def analyze_day_master_strength(bazi: Dict) -> Tuple[str, Dict[str, float]]:
        """分析日主强弱
        
        Args:
            bazi: 八字信息字典
            
        Returns:
            (强弱描述, 强弱评分) 元组
            强弱评分：日主能量、印星能量、比劫能量、食伤能量、财星能量、官杀能量
        """
        day_master = bazi["day"]["gan"]
        day_master_wuxing = bazi["day"]["gan_wuxing"]
        
        # 统计各类干支
        scores = {
            "day_master": 0.0,
            "yin": 0.0,  # 印星（生日主）
            "bijie": 0.0,  # 比劫（同五行）
            "shishang": 0.0,  # 食伤（克日主）
            "cai": 0.0,  # 财星（日主克）
            "guansha": 0.0  # 官杀（克日主）
        }
        
        # 五行生克关系
        sheng_relation = GanzhiCalculator.WUXING_SHENG
        ke_relation = GanzhiCalculator.WUXING_KE
        
        # 遍历四柱分析
        for pillar_name in ["year", "month", "day", "hour"]:
            if pillar_name not in bazi:
                continue
                
            pillar = bazi[pillar_name]
            
            # 分析天干
            if "gan" in pillar and "gan_wuxing" in pillar:
                gan_wuxing = pillar["gan_wuxing"]
                
                if gan_wuxing == day_master_wuxing:
                    # 日主本身
                    scores["day_master"] += 10.0
                elif sheng_relation.get(gan_wuxing) == day_master_wuxing:
                    # 印星（生日主）
                    scores["yin"] += 8.0
                elif ke_relation.get(gan_wuxing) == day_master_wuxing:
                    # 官杀（克日主）
                    scores["guansha"] += 6.0
                elif sheng_relation.get(day_master_wuxing) == gan_wuxing:
                    # 食伤（日主生）
                    scores["shishang"] += 4.0
                elif ke_relation.get(day_master_wuxing) == gan_wuxing:
                    # 财星（日主克）
                    scores["cai"] += 5.0
            
            # 分析地支
            if "zhi" in pillar and "zhi_wuxing" in pillar:
                zhi_wuxing = pillar["zhi_wuxing"]
                
                if zhi_wuxing == day_master_wuxing:
                    # 比劫（同五行地支）
                    scores["bijie"] += 6.0
                elif sheng_relation.get(zhi_wuxing) == day_master_wuxing:
                    # 印星地支
                    scores["yin"] += 4.0
                elif ke_relation.get(zhi_wuxing) == day_master_wuxing:
                    # 官杀地支
                    scores["guansha"] += 3.0
                elif sheng_relation.get(day_master_wuxing) == zhi_wuxing:
                    # 食伤地支
                    scores["shishang"] += 2.0
                elif ke_relation.get(day_master_wuxing) == zhi_wuxing:
                    # 财星地支
                    scores["cai"] += 2.5
        
        # 计算日主总能量
        total_energy = (
            scores["day_master"] + scores["yin"] + scores["bijie"]
        )
        
        # 计算克泄耗能量
        output_energy = (
            scores["shishang"] + scores["cai"] + scores["guansha"]
        )
        
        # 判断强弱
        if total_energy > output_energy * 1.3:
            strength = "强"
        elif total_energy > output_energy * 0.8:
            strength = "中和"
        else:
            strength = "弱"
        
        return strength, scores
    
    @staticmethod
    def determine_yong_shen(bazi: Dict) -> Dict:
        """推算用神、喜神、忌神
        
        Args:
            bazi: 八字信息字典
            
        Returns:
            用神信息字典
        """
        day_master = bazi["day"]["gan"]
        day_master_wuxing = bazi["day"]["gan_wuxing"]
        
        # 分析日主强弱
        strength, scores = WuxingAnalyzer.analyze_day_master_strength(bazi)
        
        # 五行生克关系
        sheng_relation = GanzhiCalculator.WUXING_SHENG
        ke_relation = GanzhiCalculator.WUXING_KE
        
        # 根据强弱确定用神
        yong_shen = ""
        xi_shen = ""
        ji_shen_list = []
        
        if strength == "弱":
            # 日主弱，需要生助（印星、比劫）
            # 找到生日主的五行
            sheng_wuxing = None
            for wuxing, sheng_to in sheng_relation.items():
                if sheng_to == day_master_wuxing:
                    sheng_wuxing = wuxing
                    break
            
            # 用神为印星或比劫
            if scores["yin"] > scores["bijie"]:
                yong_shen = sheng_wuxing if sheng_wuxing else day_master_wuxing
            else:
                yong_shen = day_master_wuxing
            
            # 喜神为与用神相生的五行
            if yong_shen in sheng_relation:
                xi_shen = sheng_relation[yong_shen]
            
            # 忌神为克用神的五行
            for wuxing, ke_to in ke_relation.items():
                if ke_to == yong_shen:
                    ji_shen_list.append(wuxing)
        
        elif strength == "强":
            # 日主强，需要克泄耗（官杀、食伤、财星）
            # 找到克日主的五行
            ke_wuxing = None
            for wuxing, ke_to in ke_relation.items():
                if ke_to == day_master_wuxing:
                    ke_wuxing = wuxing
                    break
            
            # 用神为官杀、食伤或财星
            max_score = 0
            best_type = ""
            
            if scores["guansha"] > max_score:
                max_score = scores["guansha"]
                best_type = "guansha"
            if scores["shishang"] > max_score:
                max_score = scores["shishang"]
                best_type = "shishang"
            if scores["cai"] > max_score:
                max_score = scores["cai"]
                best_type = "cai"
            
            if best_type == "guansha":
                yong_shen = ke_wuxing if ke_wuxing else day_master_wuxing
            elif best_type == "shishang":
                yong_shen = sheng_relation.get(day_master_wuxing, day_master_wuxing)
            else:
                yong_shen = ke_relation.get(day_master_wuxing, day_master_wuxing)
            
            # 喜神为与用神相生的五行
            if yong_shen in sheng_relation:
                xi_shen = sheng_relation[yong_shen]
            
            # 忌神为生用神的五行
            for wuxing, sheng_to in sheng_relation.items():
                if sheng_to == yong_shen:
                    ji_shen_list.append(wuxing)
        
        else:  # 中和
            # 日主中和，用神取月支或季节
            month_zhi = bazi["month"]["zhi"]
            month_wuxing = bazi["month"]["zhi_wuxing"]
            yong_shen = month_wuxing
            
            # 喜神为与用神相生的五行
            if yong_shen in sheng_relation:
                xi_shen = sheng_relation[yong_shen]
            
            # 忌神为克用神的五行
            for wuxing, ke_to in ke_relation.items():
                if ke_to == yong_shen:
                    ji_shen_list.append(wuxing)
        
        return {
            "yong_shen": yong_shen,
            "xi_shen": xi_shen,
            "ji_shen": ji_shen_list,
            "strength": strength,
            "day_master": day_master,
            "day_master_wuxing": day_master_wuxing,
            "scores": scores
        }
    
    @staticmethod
    def analyze_comprehensive(bazi: Dict) -> Dict:
        """综合分析八字五行
        
        Args:
            bazi: 八字信息字典
            
        Returns:
            综合分析结果字典
        """
        # 统计五行
        wuxing_count = WuxingAnalyzer.count_wuxing_in_bazi(bazi)
        
        # 分析日主强弱
        strength, scores = WuxingAnalyzer.analyze_day_master_strength(bazi)
        
        # 推算用神
        yong_shen_info = WuxingAnalyzer.determine_yong_shen(bazi)
        
        # 五行缺失
        missing_wuxing = [wuxing for wuxing, count in wuxing_count.items() if count == 0]
        
        # 五行过多
        excessive_wuxing = [wuxing for wuxing, count in wuxing_count.items() if count >= 5]
        
        return {
            "wuxing_count": wuxing_count,
            "strength": strength,
            "scores": scores,
            "yong_shen_info": yong_shen_info,
            "missing_wuxing": missing_wuxing,
            "excessive_wuxing": excessive_wuxing,
            "summary": {
                "day_master": bazi["day"]["gan"],
                "day_master_wuxing": bazi["day"]["gan_wuxing"],
                "yong_shen": yong_shen_info["yong_shen"],
                "xi_shen": yong_shen_info["xi_shen"],
                "ji_shen": yong_shen_info["ji_shen"],
                "strength_description": strength
            }
        }
