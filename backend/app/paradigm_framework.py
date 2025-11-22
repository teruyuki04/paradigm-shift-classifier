"""
Paradigm Shift 6-Layer Model (Version 4.0 - Fact-Based, 1990+ Startups)
"""

PARADIGM_LAYERS = [
    {
        "id": 0,
        "level": "0️⃣",
        "name": "Pre-Shift",
        "jp_name": "未形成",
        "definition": "事業構造が確立せず、PMF未達で社会波及が観測ゼロの段階。",
        "criteria": {
            "revenue": "<20億円 or ARR <5億円",
            "pmf": "未達",
            "growth": "売上成長が連続しない",
            "pivot": "ピボット／撤退／縮小",
            "impact": {"structure": 0, "system": 0, "culture": 0}
        }
    },
    {
        "id": 1,
        "level": "Ⅰ",
        "name": "Minimal Shift",
        "jp_name": "最小変化",
        "definition": "既存産業の改善・効率化までで、社会構造に変化を起こさない段階。",
        "criteria": {
            "revenue": "20〜50億円 or ARR 5〜10億円",
            "market": "既存市場内の利便性向上のみ",
            "business_practice": "既存商慣習に準拠",
            "impact": {"structure": 0, "system": 0, "culture": 0}
        }
    },
    {
        "id": 2,
        "level": "Ⅱ",
        "name": "Emerging Shift",
        "jp_name": "変化萌芽",
        "definition": "新しい市場構造・顧客行動が実データで観測され始めた段階。",
        "criteria": {
            "revenue": "50〜150億円 or ARR 10〜30億円",
            "behavior_change": "新カテゴリー・新行動がデータで確認可",
            "industry_friction": "価格破壊・チャネル破壊などの摩擦",
            "unit_economics": "LTV/リピートが既存産業を破壊し始める",
            "transaction_change": "C2Cやフリーランス流通の拡張"
        }
    },
    {
        "id": 3,
        "level": "Ⅲ",
        "name": "Structural Shift",
        "jp_name": "構造変化",
        "definition": "産業構造・商流・取引形態を実際に書き換えた段階。",
        "criteria": {
            "revenue": "150〜500億円 or ARR 30〜100億円",
            "industry_standard": "API標準／データ標準の獲得",
            "market_share": "業界シェア構造に変化",
            "flow_change": "商流・データ流の再設計",
            "competitive_mimic": "競合の構造模倣が発生"
        }
    },
    {
        "id": 4,
        "level": "Ⅳ",
        "name": "Systemic Shift",
        "jp_name": "制度変換",
        "definition": "企業構造が制度・政策・社会システムに組み込まれた段階。",
        "criteria": {
            "revenue": "500〜1200億円 or ARR 100〜300億円",
            "government_link": "行政・中央省庁との制度連携",
            "rule_change": "業界団体のルール改定への影響",
            "law_influence": "ガイドライン・法改正を誘発",
            "infrastructure": "社会インフラとして位置付け",
            "system_mimic": "他産業が構造を制度化して模倣"
        }
    },
    {
        "id": 5,
        "level": "Ⅴ",
        "name": "Paradigm Shift",
        "jp_name": "規範転換",
        "definition": "社会規範・文化・生活様式そのものを塗り替えた段階。",
        "criteria": {
            "revenue": "1200億円〜",
            "behavior_change": "国内外で行動変容が持続",
            "ecosystem": "模倣産業・模倣企業がエコシステム化",
            "culture_first": "文化の変化が制度より先行",
            "category_name": "企業名がカテゴリー名化（Airbnb型など）"
        }
    }
]

EVALUATION_NOTES = {
    "scope": "1990年以降創業のスタートアップのみ対象",
    "evaluation_basis": "構造・制度・文化の観測可能な事実に限定",
    "purpose": "AI間でブレないロバストな段階分類"
}
