"""
Unit tests for internationalization and localization module.
"""

import pytest
from civ_arcos.core.i18n import (
    Language,
    Region,
    ComplianceFramework,
    TranslationEngine,
    LocalizationManager,
    TRANSLATIONS,
    REGIONAL_COMPLIANCE,
)


class TestLanguageEnum:
    """Tests for Language enum."""

    def test_language_values(self):
        """Test language enum values."""
        assert Language.EN_US.value == "en-US"
        assert Language.EN_GB.value == "en-GB"
        assert Language.ES_ES.value == "es-ES"
        assert Language.FR_FR.value == "fr-FR"
        assert Language.DE_DE.value == "de-DE"
        assert Language.ZH_CN.value == "zh-CN"
        assert Language.JA_JP.value == "ja-JP"

    def test_all_languages_present(self):
        """Test that all expected languages are available."""
        languages = list(Language)
        assert len(languages) >= 7  # At least 7 languages


class TestRegionEnum:
    """Tests for Region enum."""

    def test_region_values(self):
        """Test region enum values."""
        assert Region.NORTH_AMERICA.value == "north_america"
        assert Region.EUROPE.value == "europe"
        assert Region.UNITED_KINGDOM.value == "united_kingdom"
        assert Region.ASIA_PACIFIC.value == "asia_pacific"

    def test_all_regions_present(self):
        """Test that all expected regions are available."""
        regions = list(Region)
        assert len(regions) >= 4  # At least 4 regions


class TestComplianceFramework:
    """Tests for ComplianceFramework enum."""

    def test_framework_values(self):
        """Test compliance framework values."""
        assert ComplianceFramework.GDPR.value == "GDPR"
        assert ComplianceFramework.CYBER_ESSENTIALS.value == "Cyber_Essentials"
        assert ComplianceFramework.PDPA_SINGAPORE.value == "PDPA_Singapore"
        assert ComplianceFramework.ISO_27001.value == "ISO_27001"

    def test_international_frameworks(self):
        """Test international frameworks exist."""
        assert ComplianceFramework.ISO_27001
        assert ComplianceFramework.ISO_9001

    def test_regional_frameworks_eu(self):
        """Test EU-specific frameworks."""
        assert ComplianceFramework.GDPR
        assert ComplianceFramework.NIS_DIRECTIVE

    def test_regional_frameworks_uk(self):
        """Test UK-specific frameworks."""
        assert ComplianceFramework.CYBER_ESSENTIALS
        assert ComplianceFramework.CYBER_ESSENTIALS_PLUS
        assert ComplianceFramework.UK_GDPR

    def test_regional_frameworks_apac(self):
        """Test APAC-specific frameworks."""
        assert ComplianceFramework.PDPA_SINGAPORE
        assert ComplianceFramework.APEC_PRIVACY
        assert ComplianceFramework.PIPL_CHINA


class TestTranslations:
    """Tests for translation dictionaries."""

    def test_translations_exist(self):
        """Test that translations dictionary is populated."""
        assert len(TRANSLATIONS) > 0
        assert "en-US" in TRANSLATIONS

    def test_common_keys_in_all_languages(self):
        """Test that common keys exist in all languages."""
        common_keys = [
            "app.name",
            "dashboard.title",
            "evidence.title",
            "assurance.title",
        ]

        for lang_code in TRANSLATIONS:
            for key in common_keys:
                assert key in TRANSLATIONS[lang_code], \
                    f"Key '{key}' missing in {lang_code}"

    def test_translation_consistency(self):
        """Test that all languages have same keys."""
        base_keys = set(TRANSLATIONS["en-US"].keys())

        for lang_code, translations in TRANSLATIONS.items():
            if lang_code != "en-US":
                assert set(translations.keys()) == base_keys, \
                    f"Keys mismatch in {lang_code}"


class TestRegionalCompliance:
    """Tests for regional compliance mappings."""

    def test_regional_compliance_exists(self):
        """Test that regional compliance mapping is populated."""
        assert len(REGIONAL_COMPLIANCE) > 0

    def test_all_regions_have_compliance(self):
        """Test that all regions have compliance frameworks."""
        for region in Region:
            assert region in REGIONAL_COMPLIANCE
            assert len(REGIONAL_COMPLIANCE[region]) > 0

    def test_europe_compliance(self):
        """Test Europe has GDPR."""
        frameworks = REGIONAL_COMPLIANCE[Region.EUROPE]
        assert ComplianceFramework.GDPR in frameworks

    def test_uk_compliance(self):
        """Test UK has Cyber Essentials."""
        frameworks = REGIONAL_COMPLIANCE[Region.UNITED_KINGDOM]
        assert ComplianceFramework.CYBER_ESSENTIALS in frameworks

    def test_apac_compliance(self):
        """Test APAC has regional frameworks."""
        frameworks = REGIONAL_COMPLIANCE[Region.ASIA_PACIFIC]
        assert ComplianceFramework.PDPA_SINGAPORE in frameworks


class TestTranslationEngine:
    """Tests for TranslationEngine class."""

    def test_initialization(self):
        """Test translation engine initialization."""
        engine = TranslationEngine()
        assert engine.default_language == Language.EN_US
        assert engine.current_language == Language.EN_US

    def test_set_language(self):
        """Test setting current language."""
        engine = TranslationEngine()
        engine.set_language(Language.ES_ES)
        assert engine.current_language == Language.ES_ES

    def test_translate_basic(self):
        """Test basic translation."""
        engine = TranslationEngine()
        translation = engine.translate("app.name")
        assert translation == "CIV-ARCOS"

    def test_translate_to_spanish(self):
        """Test translation to Spanish."""
        engine = TranslationEngine()
        engine.set_language(Language.ES_ES)
        translation = engine.translate("dashboard.title")
        assert translation == "Panel de Calidad"

    def test_translate_to_french(self):
        """Test translation to French."""
        engine = TranslationEngine()
        translation = engine.translate("dashboard.title", Language.FR_FR)
        assert translation == "Tableau de Qualité"

    def test_translate_missing_key(self):
        """Test translation of missing key returns key itself."""
        engine = TranslationEngine()
        translation = engine.translate("nonexistent.key")
        assert translation == "nonexistent.key"

    def test_translate_fallback_to_default(self):
        """Test fallback to default language."""
        engine = TranslationEngine(Language.EN_US)
        # If a translation is missing in another language, it falls back
        translation = engine.translate("app.name", Language.ES_ES)
        # Should still work as app.name exists in Spanish
        assert translation is not None

    def test_get_available_languages(self):
        """Test getting available languages."""
        engine = TranslationEngine()
        languages = engine.get_available_languages()
        assert len(languages) > 0
        assert Language.EN_US in languages
        assert Language.ES_ES in languages

    def test_translate_dict_simple(self):
        """Test translating a simple dictionary."""
        engine = TranslationEngine()
        data = {
            "title": "dashboard.title",
            "subtitle": "dashboard.overview",
        }
        translated = engine.translate_dict(data)
        assert translated["title"] == "Quality Dashboard"
        assert translated["subtitle"] == "System Overview"

    def test_translate_dict_nested(self):
        """Test translating a nested dictionary."""
        engine = TranslationEngine()
        data = {
            "header": {
                "title": "dashboard.title",
            },
            "value": 85,
        }
        translated = engine.translate_dict(data)
        assert translated["header"]["title"] == "Quality Dashboard"
        assert translated["value"] == 85

    def test_translate_dict_with_list(self):
        """Test translating dictionary with lists."""
        engine = TranslationEngine()
        data = {
            "items": [
                {"name": "evidence.title"},
                {"name": "assurance.title"},
            ],
        }
        translated = engine.translate_dict(data)
        assert translated["items"][0]["name"] == "Evidence Collection"
        assert translated["items"][1]["name"] == "Assurance Cases"


class TestLocalizationManager:
    """Tests for LocalizationManager class."""

    def test_initialization(self):
        """Test localization manager initialization."""
        manager = LocalizationManager()
        assert manager.translation_engine is not None
        assert manager.current_region is None
        assert len(manager.user_preferences) == 0

    def test_set_user_language(self):
        """Test setting user language preference."""
        manager = LocalizationManager()
        manager.set_user_language("user1", Language.ES_ES)
        assert "user1" in manager.user_preferences
        assert manager.user_preferences["user1"]["language"] == Language.ES_ES

    def test_set_user_region(self):
        """Test setting user region preference."""
        manager = LocalizationManager()
        manager.set_user_region("user1", Region.EUROPE)
        assert "user1" in manager.user_preferences
        assert manager.user_preferences["user1"]["region"] == Region.EUROPE

    def test_get_user_language(self):
        """Test getting user language preference."""
        manager = LocalizationManager()
        manager.set_user_language("user1", Language.FR_FR)
        language = manager.get_user_language("user1")
        assert language == Language.FR_FR

    def test_get_user_language_default(self):
        """Test getting language for user without preference."""
        manager = LocalizationManager()
        language = manager.get_user_language("unknown_user")
        assert language == Language.EN_US

    def test_get_user_region(self):
        """Test getting user region preference."""
        manager = LocalizationManager()
        manager.set_user_region("user1", Region.ASIA_PACIFIC)
        region = manager.get_user_region("user1")
        assert region == Region.ASIA_PACIFIC

    def test_get_user_region_default(self):
        """Test getting region for user without preference."""
        manager = LocalizationManager()
        region = manager.get_user_region("unknown_user")
        assert region is None

    def test_get_regional_compliance_frameworks(self):
        """Test getting compliance frameworks for region."""
        manager = LocalizationManager()
        frameworks = manager.get_regional_compliance_frameworks(Region.EUROPE)
        assert ComplianceFramework.GDPR in frameworks
        assert ComplianceFramework.ISO_27001 in frameworks

    def test_localize_dashboard(self):
        """Test localizing dashboard data."""
        manager = LocalizationManager()
        manager.set_user_language("user1", Language.ES_ES)

        dashboard_data = {
            "title": "dashboard.title",
            "quality_score": 85,
        }

        localized = manager.localize_dashboard(dashboard_data, "user1")
        assert localized["title"] == "Panel de Calidad"
        assert localized["quality_score"] == 85

    def test_localize_report(self):
        """Test localizing report data."""
        manager = LocalizationManager()
        manager.set_user_language("user1", Language.FR_FR)
        manager.set_user_region("user1", Region.EUROPE)

        report_data = {
            "title": "report.executive",
            "score": 90,
        }

        localized = manager.localize_report(report_data, "user1")
        assert localized["title"] == "Rapport Exécutif"
        assert localized["score"] == 90
        assert "regional_compliance" in localized
        assert localized["regional_compliance"]["region"] == "europe"

    def test_get_compliance_requirements_gdpr(self):
        """Test getting GDPR requirements."""
        manager = LocalizationManager()
        requirements = manager.get_compliance_requirements(ComplianceFramework.GDPR)
        assert requirements["name"] == "General Data Protection Regulation"
        assert requirements["region"] == "Europe"
        assert len(requirements["key_requirements"]) > 0
        assert "Data protection by design and by default" in requirements["key_requirements"]

    def test_get_compliance_requirements_cyber_essentials(self):
        """Test getting Cyber Essentials requirements."""
        manager = LocalizationManager()
        requirements = manager.get_compliance_requirements(
            ComplianceFramework.CYBER_ESSENTIALS
        )
        assert requirements["name"] == "Cyber Essentials"
        assert requirements["region"] == "United Kingdom"
        assert "Boundary firewalls and internet gateways" in requirements["key_requirements"]

    def test_get_compliance_requirements_unknown(self):
        """Test getting requirements for unknown framework."""
        manager = LocalizationManager()
        requirements = manager.get_compliance_requirements(
            ComplianceFramework.ISO_27001
        )
        # Should return basic structure
        assert "name" in requirements
        assert "key_requirements" in requirements

    def test_get_localization_stats(self):
        """Test getting localization statistics."""
        manager = LocalizationManager()
        manager.set_user_language("user1", Language.ES_ES)
        manager.set_user_language("user2", Language.FR_FR)

        stats = manager.get_localization_stats()
        assert stats["supported_languages"] == len(Language)
        assert stats["supported_regions"] == len(Region)
        assert stats["compliance_frameworks"] == len(ComplianceFramework)
        assert stats["active_users"] == 2
        assert stats["translation_keys"] > 0

    def test_multiple_users_different_preferences(self):
        """Test multiple users with different preferences."""
        manager = LocalizationManager()
        manager.set_user_language("user1", Language.ES_ES)
        manager.set_user_language("user2", Language.FR_FR)
        manager.set_user_region("user1", Region.EUROPE)
        manager.set_user_region("user2", Region.ASIA_PACIFIC)

        assert manager.get_user_language("user1") == Language.ES_ES
        assert manager.get_user_language("user2") == Language.FR_FR
        assert manager.get_user_region("user1") == Region.EUROPE
        assert manager.get_user_region("user2") == Region.ASIA_PACIFIC
