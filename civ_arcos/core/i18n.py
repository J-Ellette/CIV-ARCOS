"""
Internationalization and Localization Module for CIV-ARCOS.

Provides multi-language support for UI, dashboards, and reports with
compliance framework mapping for different regions.
"""

from typing import Dict, List, Optional, Any
from enum import Enum


class Language(Enum):
    """Supported languages."""

    EN_US = "en-US"  # English (US)
    EN_GB = "en-GB"  # English (UK)
    ES_ES = "es-ES"  # Spanish (Spain)
    FR_FR = "fr-FR"  # French (France)
    DE_DE = "de-DE"  # German (Germany)
    ZH_CN = "zh-CN"  # Chinese (Simplified)
    JA_JP = "ja-JP"  # Japanese (Japan)
    KO_KR = "ko-KR"  # Korean (Korea)
    PT_BR = "pt-BR"  # Portuguese (Brazil)
    IT_IT = "it-IT"  # Italian (Italy)


class Region(Enum):
    """Supported regions with specific compliance requirements."""

    NORTH_AMERICA = "north_america"
    EUROPE = "europe"
    UNITED_KINGDOM = "united_kingdom"
    ASIA_PACIFIC = "asia_pacific"
    LATIN_AMERICA = "latin_america"
    MIDDLE_EAST = "middle_east"
    AFRICA = "africa"


class ComplianceFramework(Enum):
    """Regional compliance frameworks."""

    # International
    ISO_27001 = "ISO_27001"
    ISO_9001 = "ISO_9001"

    # North America
    HIPAA = "HIPAA"
    SOC2 = "SOC2"
    FEDRAMP = "FedRAMP"
    NIST_800_53 = "NIST_800_53"

    # Europe
    GDPR = "GDPR"
    NIS_DIRECTIVE = "NIS_Directive"
    ENISA = "ENISA"

    # United Kingdom
    CYBER_ESSENTIALS = "Cyber_Essentials"
    CYBER_ESSENTIALS_PLUS = "Cyber_Essentials_Plus"
    UK_GDPR = "UK_GDPR"
    NCSC_GUIDANCE = "NCSC_Guidance"

    # Asia-Pacific
    PDPA_SINGAPORE = "PDPA_Singapore"
    APEC_PRIVACY = "APEC_Privacy"
    PIPL_CHINA = "PIPL_China"
    PIPA_KOREA = "PIPA_Korea"
    MY_NUMBER_JAPAN = "My_Number_Japan"
    PRIVACY_ACT_AUSTRALIA = "Privacy_Act_Australia"


# Translation dictionaries for different languages
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en-US": {
        "app.name": "CIV-ARCOS",
        "app.tagline": "Civilian Assurance-based Risk Computation and Orchestration System",
        "dashboard.title": "Quality Dashboard",
        "dashboard.overview": "System Overview",
        "dashboard.quality_score": "Quality Score",
        "dashboard.security_score": "Security Score",
        "dashboard.coverage": "Test Coverage",
        "dashboard.compliance": "Compliance Status",
        "evidence.title": "Evidence Collection",
        "evidence.type": "Type",
        "evidence.source": "Source",
        "evidence.timestamp": "Timestamp",
        "assurance.title": "Assurance Cases",
        "assurance.create": "Create Case",
        "assurance.status": "Status",
        "report.executive": "Executive Report",
        "report.technical": "Technical Report",
        "compliance.status": "Compliance Status",
        "compliance.framework": "Framework",
        "compliance.requirement": "Requirement",
        "compliance.met": "Requirements Met",
        "alert.high": "High Priority",
        "alert.medium": "Medium Priority",
        "alert.low": "Low Priority",
        "action.save": "Save",
        "action.cancel": "Cancel",
        "action.export": "Export",
        "action.refresh": "Refresh",
    },
    "en-GB": {
        "app.name": "CIV-ARCOS",
        "app.tagline": "Civilian Assurance-based Risk Computation and Orchestration System",
        "dashboard.title": "Quality Dashboard",
        "dashboard.overview": "System Overview",
        "dashboard.quality_score": "Quality Score",
        "dashboard.security_score": "Security Score",
        "dashboard.coverage": "Test Coverage",
        "dashboard.compliance": "Compliance Status",
        "evidence.title": "Evidence Collection",
        "evidence.type": "Type",
        "evidence.source": "Source",
        "evidence.timestamp": "Timestamp",
        "assurance.title": "Assurance Cases",
        "assurance.create": "Create Case",
        "assurance.status": "Status",
        "report.executive": "Executive Report",
        "report.technical": "Technical Report",
        "compliance.status": "Compliance Status",
        "compliance.framework": "Framework",
        "compliance.requirement": "Requirement",
        "compliance.met": "Requirements Met",
        "alert.high": "High Priority",
        "alert.medium": "Medium Priority",
        "alert.low": "Low Priority",
        "action.save": "Save",
        "action.cancel": "Cancel",
        "action.export": "Export",
        "action.refresh": "Refresh",
    },
    "es-ES": {
        "app.name": "CIV-ARCOS",
        "app.tagline": "Sistema Civil de Cálculo y Orquestación de Riesgos Basado en Aseguramiento",
        "dashboard.title": "Panel de Calidad",
        "dashboard.overview": "Resumen del Sistema",
        "dashboard.quality_score": "Puntuación de Calidad",
        "dashboard.security_score": "Puntuación de Seguridad",
        "dashboard.coverage": "Cobertura de Pruebas",
        "dashboard.compliance": "Estado de Cumplimiento",
        "evidence.title": "Recopilación de Evidencia",
        "evidence.type": "Tipo",
        "evidence.source": "Fuente",
        "evidence.timestamp": "Marca de Tiempo",
        "assurance.title": "Casos de Aseguramiento",
        "assurance.create": "Crear Caso",
        "assurance.status": "Estado",
        "report.executive": "Informe Ejecutivo",
        "report.technical": "Informe Técnico",
        "compliance.status": "Estado de Cumplimiento",
        "compliance.framework": "Marco",
        "compliance.requirement": "Requisito",
        "compliance.met": "Requisitos Cumplidos",
        "alert.high": "Prioridad Alta",
        "alert.medium": "Prioridad Media",
        "alert.low": "Prioridad Baja",
        "action.save": "Guardar",
        "action.cancel": "Cancelar",
        "action.export": "Exportar",
        "action.refresh": "Actualizar",
    },
    "fr-FR": {
        "app.name": "CIV-ARCOS",
        "app.tagline": "Système Civil de Calcul et d'Orchestration des Risques Basé sur l'Assurance",
        "dashboard.title": "Tableau de Qualité",
        "dashboard.overview": "Aperçu du Système",
        "dashboard.quality_score": "Score de Qualité",
        "dashboard.security_score": "Score de Sécurité",
        "dashboard.coverage": "Couverture des Tests",
        "dashboard.compliance": "État de Conformité",
        "evidence.title": "Collection de Preuves",
        "evidence.type": "Type",
        "evidence.source": "Source",
        "evidence.timestamp": "Horodatage",
        "assurance.title": "Cas d'Assurance",
        "assurance.create": "Créer un Cas",
        "assurance.status": "Statut",
        "report.executive": "Rapport Exécutif",
        "report.technical": "Rapport Technique",
        "compliance.status": "État de Conformité",
        "compliance.framework": "Cadre",
        "compliance.requirement": "Exigence",
        "compliance.met": "Exigences Respectées",
        "alert.high": "Haute Priorité",
        "alert.medium": "Priorité Moyenne",
        "alert.low": "Basse Priorité",
        "action.save": "Enregistrer",
        "action.cancel": "Annuler",
        "action.export": "Exporter",
        "action.refresh": "Actualiser",
    },
    "de-DE": {
        "app.name": "CIV-ARCOS",
        "app.tagline": "Ziviles Versicherungsbasiertes Risikoberechnungs- und Orchestrierungssystem",
        "dashboard.title": "Qualitäts-Dashboard",
        "dashboard.overview": "Systemübersicht",
        "dashboard.quality_score": "Qualitätsbewertung",
        "dashboard.security_score": "Sicherheitsbewertung",
        "dashboard.coverage": "Testabdeckung",
        "dashboard.compliance": "Compliance-Status",
        "evidence.title": "Evidenzsammlung",
        "evidence.type": "Typ",
        "evidence.source": "Quelle",
        "evidence.timestamp": "Zeitstempel",
        "assurance.title": "Versicherungsfälle",
        "assurance.create": "Fall Erstellen",
        "assurance.status": "Status",
        "report.executive": "Führungsbericht",
        "report.technical": "Technischer Bericht",
        "compliance.status": "Compliance-Status",
        "compliance.framework": "Rahmenwerk",
        "compliance.requirement": "Anforderung",
        "compliance.met": "Erfüllte Anforderungen",
        "alert.high": "Hohe Priorität",
        "alert.medium": "Mittlere Priorität",
        "alert.low": "Niedrige Priorität",
        "action.save": "Speichern",
        "action.cancel": "Abbrechen",
        "action.export": "Exportieren",
        "action.refresh": "Aktualisieren",
    },
    "zh-CN": {
        "app.name": "CIV-ARCOS",
        "app.tagline": "民用基于保证的风险计算和编排系统",
        "dashboard.title": "质量仪表板",
        "dashboard.overview": "系统概览",
        "dashboard.quality_score": "质量评分",
        "dashboard.security_score": "安全评分",
        "dashboard.coverage": "测试覆盖率",
        "dashboard.compliance": "合规状态",
        "evidence.title": "证据收集",
        "evidence.type": "类型",
        "evidence.source": "来源",
        "evidence.timestamp": "时间戳",
        "assurance.title": "保证案例",
        "assurance.create": "创建案例",
        "assurance.status": "状态",
        "report.executive": "执行报告",
        "report.technical": "技术报告",
        "compliance.status": "合规状态",
        "compliance.framework": "框架",
        "compliance.requirement": "要求",
        "compliance.met": "已满足要求",
        "alert.high": "高优先级",
        "alert.medium": "中等优先级",
        "alert.low": "低优先级",
        "action.save": "保存",
        "action.cancel": "取消",
        "action.export": "导出",
        "action.refresh": "刷新",
    },
    "ja-JP": {
        "app.name": "CIV-ARCOS",
        "app.tagline": "民間保証ベースのリスク計算およびオーケストレーションシステム",
        "dashboard.title": "品質ダッシュボード",
        "dashboard.overview": "システム概要",
        "dashboard.quality_score": "品質スコア",
        "dashboard.security_score": "セキュリティスコア",
        "dashboard.coverage": "テストカバレッジ",
        "dashboard.compliance": "コンプライアンス状況",
        "evidence.title": "証拠収集",
        "evidence.type": "タイプ",
        "evidence.source": "ソース",
        "evidence.timestamp": "タイムスタンプ",
        "assurance.title": "保証ケース",
        "assurance.create": "ケース作成",
        "assurance.status": "ステータス",
        "report.executive": "エグゼクティブレポート",
        "report.technical": "技術レポート",
        "compliance.status": "コンプライアンス状況",
        "compliance.framework": "フレームワーク",
        "compliance.requirement": "要件",
        "compliance.met": "満たされた要件",
        "alert.high": "高優先度",
        "alert.medium": "中優先度",
        "alert.low": "低優先度",
        "action.save": "保存",
        "action.cancel": "キャンセル",
        "action.export": "エクスポート",
        "action.refresh": "更新",
    },
}


# Regional compliance framework mappings
REGIONAL_COMPLIANCE: Dict[Region, List[ComplianceFramework]] = {
    Region.NORTH_AMERICA: [
        ComplianceFramework.ISO_27001,
        ComplianceFramework.ISO_9001,
        ComplianceFramework.HIPAA,
        ComplianceFramework.SOC2,
        ComplianceFramework.FEDRAMP,
        ComplianceFramework.NIST_800_53,
    ],
    Region.EUROPE: [
        ComplianceFramework.ISO_27001,
        ComplianceFramework.ISO_9001,
        ComplianceFramework.GDPR,
        ComplianceFramework.NIS_DIRECTIVE,
        ComplianceFramework.ENISA,
    ],
    Region.UNITED_KINGDOM: [
        ComplianceFramework.ISO_27001,
        ComplianceFramework.ISO_9001,
        ComplianceFramework.CYBER_ESSENTIALS,
        ComplianceFramework.CYBER_ESSENTIALS_PLUS,
        ComplianceFramework.UK_GDPR,
        ComplianceFramework.NCSC_GUIDANCE,
    ],
    Region.ASIA_PACIFIC: [
        ComplianceFramework.ISO_27001,
        ComplianceFramework.ISO_9001,
        ComplianceFramework.PDPA_SINGAPORE,
        ComplianceFramework.APEC_PRIVACY,
        ComplianceFramework.PIPL_CHINA,
        ComplianceFramework.PIPA_KOREA,
        ComplianceFramework.MY_NUMBER_JAPAN,
        ComplianceFramework.PRIVACY_ACT_AUSTRALIA,
    ],
    Region.LATIN_AMERICA: [
        ComplianceFramework.ISO_27001,
        ComplianceFramework.ISO_9001,
    ],
    Region.MIDDLE_EAST: [
        ComplianceFramework.ISO_27001,
        ComplianceFramework.ISO_9001,
    ],
    Region.AFRICA: [
        ComplianceFramework.ISO_27001,
        ComplianceFramework.ISO_9001,
    ],
}


class TranslationEngine:
    """
    Translation engine for multi-language support.
    """

    def __init__(self, default_language: Language = Language.EN_US):
        """
        Initialize translation engine.

        Args:
            default_language: Default language for translations
        """
        self.default_language = default_language
        self.current_language = default_language

    def set_language(self, language: Language) -> None:
        """
        Set current language.

        Args:
            language: Language to set as current
        """
        self.current_language = language

    def translate(self, key: str, language: Optional[Language] = None) -> str:
        """
        Translate a key to the current or specified language.

        Args:
            key: Translation key (e.g., "dashboard.title")
            language: Optional language override

        Returns:
            Translated string or key if translation not found
        """
        lang = language or self.current_language
        lang_code = lang.value

        if lang_code in TRANSLATIONS and key in TRANSLATIONS[lang_code]:
            return TRANSLATIONS[lang_code][key]

        # Fallback to default language
        if self.default_language.value in TRANSLATIONS:
            if key in TRANSLATIONS[self.default_language.value]:
                return TRANSLATIONS[self.default_language.value][key]

        # Return key if no translation found
        return key

    def get_available_languages(self) -> List[Language]:
        """
        Get list of available languages.

        Returns:
            List of supported languages
        """
        return list(Language)

    def translate_dict(
        self, data: Dict[str, Any], language: Optional[Language] = None
    ) -> Dict[str, Any]:
        """
        Translate all string values in a dictionary that are translation keys.

        Args:
            data: Dictionary to translate
            language: Optional language override

        Returns:
            Dictionary with translated values
        """
        result = {}
        for key, value in data.items():
            if isinstance(value, str) and "." in value:
                # Try to translate if it looks like a translation key
                result[key] = self.translate(value, language)
            elif isinstance(value, dict):
                result[key] = self.translate_dict(value, language)
            elif isinstance(value, list):
                result[key] = [
                    self.translate_dict(item, language) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                result[key] = value
        return result


class LocalizationManager:
    """
    Manages localization settings including language, region, and compliance frameworks.
    """

    def __init__(self):
        """Initialize localization manager."""
        self.translation_engine = TranslationEngine()
        self.current_region: Optional[Region] = None
        self.user_preferences: Dict[str, Dict[str, Any]] = {}

    def set_user_language(self, user_id: str, language: Language) -> None:
        """
        Set language preference for a user.

        Args:
            user_id: User identifier
            language: Preferred language
        """
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        self.user_preferences[user_id]["language"] = language

    def set_user_region(self, user_id: str, region: Region) -> None:
        """
        Set region preference for a user.

        Args:
            user_id: User identifier
            region: Preferred region
        """
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        self.user_preferences[user_id]["region"] = region

    def get_user_language(self, user_id: str) -> Language:
        """
        Get language preference for a user.

        Args:
            user_id: User identifier

        Returns:
            User's preferred language or default
        """
        if user_id in self.user_preferences:
            return self.user_preferences[user_id].get("language", Language.EN_US)
        return Language.EN_US

    def get_user_region(self, user_id: str) -> Optional[Region]:
        """
        Get region preference for a user.

        Args:
            user_id: User identifier

        Returns:
            User's preferred region or None
        """
        if user_id in self.user_preferences:
            return self.user_preferences[user_id].get("region")
        return None

    def get_regional_compliance_frameworks(
        self, region: Region
    ) -> List[ComplianceFramework]:
        """
        Get applicable compliance frameworks for a region.

        Args:
            region: Region to query

        Returns:
            List of applicable compliance frameworks
        """
        return REGIONAL_COMPLIANCE.get(region, [])

    def localize_dashboard(
        self, dashboard_data: Dict[str, Any], user_id: str
    ) -> Dict[str, Any]:
        """
        Localize dashboard data for a user.

        Args:
            dashboard_data: Dashboard data to localize
            user_id: User identifier

        Returns:
            Localized dashboard data
        """
        language = self.get_user_language(user_id)
        return self.translation_engine.translate_dict(dashboard_data, language)

    def localize_report(
        self, report_data: Dict[str, Any], user_id: str
    ) -> Dict[str, Any]:
        """
        Localize report data for a user.

        Args:
            report_data: Report data to localize
            user_id: User identifier

        Returns:
            Localized report data
        """
        language = self.get_user_language(user_id)
        localized = self.translation_engine.translate_dict(report_data, language)

        # Add regional compliance information if region is set
        region = self.get_user_region(user_id)
        if region:
            localized["regional_compliance"] = {
                "region": region.value,
                "frameworks": [
                    fw.value for fw in self.get_regional_compliance_frameworks(region)
                ],
            }

        return localized

    def get_compliance_requirements(
        self, framework: ComplianceFramework
    ) -> Dict[str, Any]:
        """
        Get compliance requirements for a specific framework.

        Args:
            framework: Compliance framework

        Returns:
            Dictionary of compliance requirements
        """
        # Mapping of frameworks to their key requirements
        requirements = {
            ComplianceFramework.GDPR: {
                "name": "General Data Protection Regulation",
                "region": "Europe",
                "key_requirements": [
                    "Data protection by design and by default",
                    "Right to be forgotten",
                    "Data portability",
                    "Breach notification within 72 hours",
                    "Privacy impact assessments",
                    "Data processing agreements",
                ],
            },
            ComplianceFramework.CYBER_ESSENTIALS: {
                "name": "Cyber Essentials",
                "region": "United Kingdom",
                "key_requirements": [
                    "Boundary firewalls and internet gateways",
                    "Secure configuration",
                    "Access control",
                    "Malware protection",
                    "Patch management",
                ],
            },
            ComplianceFramework.CYBER_ESSENTIALS_PLUS: {
                "name": "Cyber Essentials Plus",
                "region": "United Kingdom",
                "key_requirements": [
                    "All Cyber Essentials requirements",
                    "Hands-on technical verification",
                    "Internal vulnerability scanning",
                    "External vulnerability scanning",
                ],
            },
            ComplianceFramework.PDPA_SINGAPORE: {
                "name": "Personal Data Protection Act",
                "region": "Singapore",
                "key_requirements": [
                    "Consent for data collection",
                    "Purpose limitation",
                    "Data accuracy",
                    "Protection of personal data",
                    "Retention limitation",
                    "Transfer limitation",
                ],
            },
            ComplianceFramework.APEC_PRIVACY: {
                "name": "APEC Privacy Framework",
                "region": "Asia-Pacific",
                "key_requirements": [
                    "Preventing harm",
                    "Notice",
                    "Collection limitation",
                    "Uses of personal information",
                    "Choice",
                    "Integrity of personal information",
                    "Security safeguards",
                    "Access and correction",
                    "Accountability",
                ],
            },
        }

        return requirements.get(
            framework, {"name": framework.value, "key_requirements": []}
        )

    def get_localization_stats(self) -> Dict[str, Any]:
        """
        Get localization statistics.

        Returns:
            Dictionary of localization statistics
        """
        return {
            "supported_languages": len(Language),
            "supported_regions": len(Region),
            "compliance_frameworks": len(ComplianceFramework),
            "active_users": len(self.user_preferences),
            "translation_keys": sum(len(TRANSLATIONS[lang]) for lang in TRANSLATIONS),
        }
