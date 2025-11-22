"""
Paradigm Shift 6-Layer Model (Unified with Visualization Guide)
"""

PARADIGM_LAYERS = [
    {
        "id": 0,
        "level": "0️⃣",
        "name": "Pre-Shift",
        "jp_name": "プレシフト",
        "definition": "PMF前。事業仮説が崩壊、再構築中",
        "criteria": {
            "revenue": "ARR < 1億円",
            "pmf": "未達",
            "status": "事業転換中、資金調達停止",
            "impact": {"structure": 0, "system": 0, "culture": 0}
        }
    },
    {
        "id": 1,
        "level": "Ⅰ",
        "name": "Minimal Shift",
        "jp_name": "最小シフト",
        "definition": "既存市場の改善型モデル。技術・UX改善中心",
        "criteria": {
            "revenue": "ARR 1〜5億円",
            "market": "既存市場の改善型モデル",
            "focus": "技術・UX改善中心",
            "status": "NPS改善、初期顧客獲得",
            "impact": {"structure": 1, "system": 0, "culture": 0}
        }
    },
    {
        "id": 2,
        "level": "Ⅱ",
        "name": "Emerging Shift",
        "jp_name": "変化萌芽シフト",
        "definition": "新しい顧客・市場構造を形成し始める。既存業界の\"隙間\"で成立",
        "criteria": {
            "revenue": "ARR 5〜20億円",
            "market": "新しい顧客・市場構造を形成",
            "position": "既存業界の隙間で成立",
            "status": "PoC成功、シリーズB前後",
            "impact": {"structure": 2, "system": 0, "culture": 0}
        }
    },
    {
        "id": 3,
        "level": "Ⅲ",
        "name": "Structural Shift",
        "jp_name": "構造シフト",
        "definition": "既存プレイヤーを巻き込み、市場ルールや取引構造を再定義",
        "criteria": {
            "revenue": "ARR 20〜100億円",
            "market_impact": "市場ルールや取引構造を再定義",
            "players": "既存プレイヤーを巻き込む",
            "status": "業界標準化、シリーズC〜D",
            "impact": {"structure": 3, "system": 1, "culture": 0}
        }
    },
    {
        "id": 4,
        "level": "Ⅳ",
        "name": "Systemic Shift",
        "jp_name": "システムシフト",
        "definition": "行政・規制・業界団体と連携し、新しい制度・仕組みを実装",
        "criteria": {
            "revenue": "ARR 100億円〜",
            "government_link": "行政・規制・業界団体と連携",
            "system_impact": "新しい制度・仕組みを実装",
            "status": "社会制度・政策連動、IPO〜上場後",
            "impact": {"structure": 4, "system": 4, "culture": 2}
        }
    },
    {
        "id": 5,
        "level": "Ⅴ",
        "name": "Paradigm Shift",
        "jp_name": "パラダイムシフト",
        "definition": "社会的価値観・生活様式を変え、文化的規範として定着",
        "criteria": {
            "revenue": "ARR 300億円〜",
            "cultural_impact": "社会的価値観・生活様式を変革",
            "status": "文化現象化、海外波及",
            "global": "グローバルな影響力",
            "impact": {"structure": 5, "system": 5, "culture": 5}
        }
    }
]

EVALUATION_NOTES = {
    "scope": "1990年以降創業のスタートアップのみ対象",
    "evaluation_basis": "構造・制度・文化の観測可能な事実に限定",
    "purpose": "AI間でブレないロバストな段階分類"
}
