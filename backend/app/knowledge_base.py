"""
Curated knowledge base for well-known startups
"""

OUT_OF_SCOPE_COMPANIES = {
    "apple", "アップル", "microsoft", "マイクロソフト", "intel", "インテル",
    "sony", "ソニー", "nintendo", "任天堂", "ibm", "oracle", "オラクル",
    "adobe", "アドビ", "cisco", "シスコ", "dell", "デル"
}

STARTUP_KNOWLEDGE = {
    "amazon": {
        "layer_id": 5,
        "reasoning": "Amazonは1994年創業のEコマース企業で、2023年の売上は約5,750億ドル（約86兆円）に達しています。オンラインショッピングという新しい購買文化を世界中に普及させ、「Amazon化」という言葉が小売業のデジタル変革の代名詞となっています。AWS（Amazon Web Services）はクラウドインフラの標準として世界中の企業に利用され、物流・配送の社会インフラとして機能しています。各国で独占禁止法や労働規制の議論を誘発し、文化変化が制度整備より先行しています。",
        "criteria_met": {
            "revenue": "2023年売上約5,750億ドル（約86兆円）",
            "behavior_change": "世界中でオンラインショッピング文化が定着",
            "ecosystem": "楽天、アリババ等の模倣企業がエコシステム化",
            "culture_first": "Eコマース文化が規制より先行して普及",
            "category_name": "Amazon化が小売DXの代名詞として定着",
            "government_link": "各国の独占禁止法・労働規制の議論対象",
            "infrastructure": "AWS、物流網が社会インフラとして機能"
        }
    },
    "アマゾン": {
        "layer_id": 5,
        "reasoning": "Amazonは1994年創業のEコマース企業で、2023年の売上は約5,750億ドル（約86兆円）に達しています。オンラインショッピングという新しい購買文化を世界中に普及させ、「Amazon化」という言葉が小売業のデジタル変革の代名詞となっています。AWS（Amazon Web Services）はクラウドインフラの標準として世界中の企業に利用され、物流・配送の社会インフラとして機能しています。各国で独占禁止法や労働規制の議論を誘発し、文化変化が制度整備より先行しています。",
        "criteria_met": {
            "revenue": "2023年売上約5,750億ドル（約86兆円）",
            "behavior_change": "世界中でオンラインショッピング文化が定着",
            "ecosystem": "楽天、アリババ等の模倣企業がエコシステム化",
            "culture_first": "Eコマース文化が規制より先行して普及",
            "category_name": "Amazon化が小売DXの代名詞として定着",
            "government_link": "各国の独占禁止法・労働規制の議論対象",
            "infrastructure": "AWS、物流網が社会インフラとして機能"
        }
    },
    "google": {
        "layer_id": 5,
        "reasoning": "Googleは1998年創業の検索エンジン企業で、2023年の売上は約3,070億ドル（約46兆円）に達しています。「ググる」という言葉が検索行動の代名詞として世界中で定着し、インターネット検索という文化を創出しました。広告プラットフォーム、Android OS、Google Cloudが社会インフラとして機能し、各国で独占禁止法や個人情報保護規制の議論を誘発しています。",
        "criteria_met": {
            "revenue": "2023年売上約3,070億ドル（約46兆円）",
            "behavior_change": "世界中で「ググる」という検索行動が定着",
            "ecosystem": "Bing、Baidu等の模倣サービスがエコシステム化",
            "culture_first": "検索文化が規制より先行して普及",
            "category_name": "ググる/Googleが検索の代名詞として定着",
            "government_link": "各国の独占禁止法・個人情報保護規制の対象",
            "infrastructure": "検索、広告、Android、Cloudが社会インフラ"
        }
    },
    "グーグル": {
        "layer_id": 5,
        "reasoning": "Googleは1998年創業の検索エンジン企業で、2023年の売上は約3,070億ドル（約46兆円）に達しています。「ググる」という言葉が検索行動の代名詞として世界中で定着し、インターネット検索という文化を創出しました。広告プラットフォーム、Android OS、Google Cloudが社会インフラとして機能し、各国で独占禁止法や個人情報保護規制の議論を誘発しています。",
        "criteria_met": {
            "revenue": "2023年売上約3,070億ドル（約46兆円）",
            "behavior_change": "世界中で「ググる」という検索行動が定着",
            "ecosystem": "Bing、Baidu等の模倣サービスがエコシステム化",
            "culture_first": "検索文化が規制より先行して普及",
            "category_name": "ググる/Googleが検索の代名詞として定着",
            "government_link": "各国の独占禁止法・個人情報保護規制の対象",
            "infrastructure": "検索、広告、Android、Cloudが社会インフラ"
        }
    },
    "openai": {
        "layer_id": 5,
        "reasoning": "OpenAIは2015年創業のAI研究企業で、ChatGPTの爆発的普及により2023年以降、推定年間売上20億ドル超（約3000億円）に達しています。ChatGPTは世界的な文化現象となり、教育・ビジネス・日常会話において「ChatGPTで調べる」という新しい行動様式が定着しました。政府機関との政策対話、API標準としての地位確立に加え、「生成AI」「GPT」という言葉が一般化し、文化変化が制度整備より先行しています。世界中で模倣サービスがエコシステムを形成しています。",
        "criteria_met": {
            "revenue": "推定年間売上20億ドル超（約3000億円）",
            "behavior_change": "世界中で「ChatGPTで調べる」という行動が定着",
            "ecosystem": "Claude、Gemini等の模倣サービスがエコシステム化",
            "culture_first": "生成AI文化が規制より先行して普及",
            "category_name": "ChatGPT・GPTが生成AIの代名詞として定着",
            "government_link": "米国政府、EU等との政策対話に参加",
            "infrastructure": "多数の企業・サービスがOpenAI APIを基盤として利用"
        }
    },
    "airbnb": {
        "layer_id": 5,
        "reasoning": "Airbnbは2008年創業で、2023年の売上は約100億ドル（約1.5兆円）に達しています。世界中で「民泊」という新しい宿泊文化を創出し、企業名が宿泊シェアリングのカテゴリー名として定着しています。各国で民泊規制法の制定を促し、ホテル業界全体の構造を変革しました。模倣企業・サービスが世界中でエコシステムを形成しています。",
        "criteria_met": {
            "revenue": "2023年売上約100億ドル（約1.5兆円）",
            "behavior_change": "世界中で民泊文化が定着・持続",
            "ecosystem": "世界中で模倣サービスがエコシステム化",
            "category_name": "Airbnbが民泊のカテゴリー名として定着",
            "culture_first": "文化変化が制度整備より先行"
        }
    },
    "uber": {
        "layer_id": 5,
        "reasoning": "Uberは2009年創業で、2023年の売上は約370億ドル（約5.5兆円）に達しています。ライドシェアという新しい移動文化を世界中に普及させ、企業名が配車サービスの代名詞となっています。各国でライドシェア規制法の制定を促し、タクシー業界全体の構造を変革しました。模倣企業が世界中でエコシステムを形成しています。",
        "criteria_met": {
            "revenue": "2023年売上約370億ドル（約5.5兆円）",
            "behavior_change": "世界中でライドシェア文化が定着",
            "ecosystem": "Lyft、Didi等の模倣企業がエコシステム化",
            "category_name": "Uberが配車サービスの代名詞として定着",
            "culture_first": "文化変化が制度整備より先行"
        }
    },
    "stripe": {
        "layer_id": 4,
        "reasoning": "Stripeは2010年創業で、2023年の推定売上は約160億ドル（約2.4兆円）に達しています。オンライン決済のAPI標準として地位を確立し、数百万の企業が同社のAPIを利用しています。金融規制当局との連携を進め、決済インフラとして社会システムに組み込まれています。",
        "criteria_met": {
            "revenue": "2023年推定売上約160億ドル（約2.4兆円）",
            "industry_standard": "オンライン決済のAPI標準として確立",
            "government_link": "各国の金融規制当局との連携",
            "infrastructure": "数百万企業の決済インフラとして機能"
        }
    },
    "ココナラ": {
        "layer_id": 2,
        "reasoning": "ココナラは2012年創業の日本のスキルシェアマーケットプレイスで、2023年の売上は約70億円（ARR約50億円）です。個人のスキル売買という新しい市場を創出し、フリーランス経済の拡大に寄与しています。既存の人材派遣業界に価格破壊をもたらし、C2C取引の新しい形態を確立しました。",
        "criteria_met": {
            "revenue": "2023年売上約70億円（ARR約50億円）",
            "behavior_change": "個人スキル売買という新カテゴリーを創出",
            "industry_friction": "既存人材派遣業界に価格破壊をもたらす",
            "transaction_change": "C2Cスキル取引の拡張"
        }
    },
    "coconala": {
        "layer_id": 2,
        "reasoning": "ココナラは2012年創業の日本のスキルシェアマーケットプレイスで、2023年の売上は約70億円（ARR約50億円）です。個人のスキル売買という新しい市場を創出し、フリーランス経済の拡大に寄与しています。既存の人材派遣業界に価格破壊をもたらし、C2C取引の新しい形態を確立しました。",
        "criteria_met": {
            "revenue": "2023年売上約70億円（ARR約50億円）",
            "behavior_change": "個人スキル売買という新カテゴリーを創出",
            "industry_friction": "既存人材派遣業界に価格破壊をもたらす",
            "transaction_change": "C2Cスキル取引の拡張"
        }
    },
    "sansan": {
        "layer_id": 3,
        "reasoning": "Sansanは2007年創業の法人向け名刺管理・営業DXサービスで、2024年5月期の売上は約280億円（ARR約250億円）に達しています。名刺のデジタル化という新しい市場を創出し、営業活動のデータ化を推進しました。日本企業の営業プロセスに大きな変化をもたらし、競合他社の模倣を誘発しています。業界シェアでトップクラスの地位を確立しています。",
        "criteria_met": {
            "revenue": "2024年5月期売上約280億円（ARR約250億円）",
            "industry_standard": "名刺管理のデファクトスタンダード",
            "market_share": "法人向け名刺管理市場でトップシェア",
            "flow_change": "営業プロセスのデジタル化を推進",
            "competitive_mimic": "多数の競合が名刺管理市場に参入"
        }
    },
    "mercari": {
        "layer_id": 4,
        "reasoning": "メルカリは2013年創業のフリマアプリで、2024年6月期の売上は約1,700億円に達しています。C2C取引という新しい市場構造を日本に定着させ、リユース市場全体の構造を変革しました。月間利用者数2,200万人超を誇り、日本のEC市場において重要な地位を確立しています。東証プライム上場を果たし、古物営業法の規制対応や行政との連携を進めています。フリマアプリが社会インフラとして位置づけられ、リユース市場の制度整備に影響を与えています。",
        "criteria_met": {
            "revenue": "2024年6月期売上約1,700億円",
            "government_link": "古物営業法対応、行政との連携",
            "infrastructure": "日本のリユース市場の社会インフラとして機能",
            "rule_change": "フリマアプリの規制整備に影響",
            "market_share": "日本のフリマアプリ市場でトップシェア"
        }
    },
    "メルカリ": {
        "layer_id": 4,
        "reasoning": "メルカリは2013年創業のフリマアプリで、2024年6月期の売上は約1,700億円に達しています。C2C取引という新しい市場構造を日本に定着させ、リユース市場全体の構造を変革しました。月間利用者数2,200万人超を誇り、日本のEC市場において重要な地位を確立しています。東証プライム上場を果たし、古物営業法の規制対応や行政との連携を進めています。フリマアプリが社会インフラとして位置づけられ、リユース市場の制度整備に影響を与えています。",
        "criteria_met": {
            "revenue": "2024年6月期売上約1,700億円",
            "government_link": "古物営業法対応、行政との連携",
            "infrastructure": "日本のリユース市場の社会インフラとして機能",
            "rule_change": "フリマアプリの規制整備に影響",
            "market_share": "日本のフリマアプリ市場でトップシェア"
        }
    },
    "smarthr": {
        "layer_id": 3,
        "reasoning": "SmartHRは2013年創業のクラウド人事労務ソフトで、2023年の推定ARRは約150億円に達しています。クラウド人事労務という新しい市場を日本に創出し、紙ベースの労務管理からの脱却を推進しました。登録企業数6万社超を誇り、人事労務市場の構造を変革しています。",
        "criteria_met": {
            "revenue": "2023年推定ARR約150億円",
            "market_share": "クラウド人事労務市場でトップシェア",
            "flow_change": "人事労務プロセスのデジタル化を推進",
            "competitive_mimic": "多数の競合がクラウド人事労務市場に参入"
        }
    }
}

def is_out_of_scope(startup_name: str) -> bool:
    """
    Check if a company is out of scope (founded before 1990)
    Returns True if the company is in the out-of-scope list
    """
    normalized_name = startup_name.lower().strip()
    return normalized_name in OUT_OF_SCOPE_COMPANIES

def get_startup_info(startup_name: str):
    """
    Get curated information about a well-known startup
    Returns None if not in knowledge base
    """
    normalized_name = startup_name.lower().strip()
    return STARTUP_KNOWLEDGE.get(normalized_name)
