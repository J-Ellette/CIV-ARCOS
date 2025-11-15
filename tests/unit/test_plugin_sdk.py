"""
Tests for Plugin SDK.
"""

import pytest
import tempfile
import os
from civ_arcos.core.plugin_sdk import (
    BasePlugin,
    CollectorPlugin,
    MetricPlugin,
    CompliancePlugin,
    VisualizationPlugin,
    PluginMetadata,
    PluginTemplate,
    PluginScaffolder,
    PluginDevelopmentGuide,
)


class TestPluginMetadata:
    """Tests for plugin metadata."""
    
    def test_metadata_creation(self):
        """Test plugin metadata creation."""
        metadata = PluginMetadata(
            plugin_id="test_plugin",
            name="Test Plugin",
            version="1.0.0",
            author="Test Author",
            description="A test plugin",
            plugin_type="collector",
            permissions=["evidence.read"],
            dependencies=[],
        )
        
        assert metadata.plugin_id == "test_plugin"
        assert metadata.name == "Test Plugin"
        assert metadata.plugin_type == "collector"


class TestCollectorPlugin:
    """Tests for collector plugin base class."""
    
    def test_collector_plugin_creation(self):
        """Test collector plugin creation."""
        metadata = PluginMetadata(
            plugin_id="test_collector",
            name="Test Collector",
            version="1.0.0",
            author="Test",
            description="Test",
            plugin_type="collector",
        )
        
        class TestCollector(CollectorPlugin):
            def initialize(self, config):
                self.initialized = True
                return True
            
            def collect(self, source, **kwargs):
                return [{"data": "test"}]
        
        plugin = TestCollector(metadata)
        assert isinstance(plugin, CollectorPlugin)
        assert plugin.metadata.plugin_type == "collector"
    
    def test_collector_plugin_initialization(self):
        """Test collector plugin initialization."""
        metadata = PluginMetadata(
            plugin_id="test_collector",
            name="Test Collector",
            version="1.0.0",
            author="Test",
            description="Test",
            plugin_type="collector",
        )
        
        class TestCollector(CollectorPlugin):
            def initialize(self, config):
                self.config = config
                self.initialized = True
                return True
            
            def collect(self, source, **kwargs):
                return [{"data": "test"}]
        
        plugin = TestCollector(metadata)
        result = plugin.initialize({"key": "value"})
        
        assert result is True
        assert plugin.initialized is True
        assert plugin.config["key"] == "value"
    
    def test_collector_plugin_execution(self):
        """Test collector plugin execution."""
        metadata = PluginMetadata(
            plugin_id="test_collector",
            name="Test Collector",
            version="1.0.0",
            author="Test",
            description="Test",
            plugin_type="collector",
        )
        
        class TestCollector(CollectorPlugin):
            def initialize(self, config):
                self.initialized = True
                return True
            
            def collect(self, source, **kwargs):
                return [{"source": source, "data": "test"}]
        
        plugin = TestCollector(metadata)
        plugin.initialize({})
        result = plugin.execute(source="test_source")
        
        assert len(result) > 0
        assert result[0]["source"] == "test_source"
    
    def test_collector_wrong_type_raises_error(self):
        """Test that wrong plugin type raises error."""
        metadata = PluginMetadata(
            plugin_id="test_collector",
            name="Test Collector",
            version="1.0.0",
            author="Test",
            description="Test",
            plugin_type="metric",  # Wrong type
        )
        
        class TestCollector(CollectorPlugin):
            def initialize(self, config):
                return True
            
            def collect(self, source, **kwargs):
                return []
        
        with pytest.raises(ValueError, match="Plugin type must be 'collector'"):
            TestCollector(metadata)


class TestMetricPlugin:
    """Tests for metric plugin base class."""
    
    def test_metric_plugin_creation(self):
        """Test metric plugin creation."""
        metadata = PluginMetadata(
            plugin_id="test_metric",
            name="Test Metric",
            version="1.0.0",
            author="Test",
            description="Test",
            plugin_type="metric",
        )
        
        class TestMetric(MetricPlugin):
            def initialize(self, config):
                self.initialized = True
                return True
            
            def calculate(self, evidence):
                return {"score": 85.0}
        
        plugin = TestMetric(metadata)
        assert isinstance(plugin, MetricPlugin)
    
    def test_metric_plugin_calculation(self):
        """Test metric plugin calculation."""
        metadata = PluginMetadata(
            plugin_id="test_metric",
            name="Test Metric",
            version="1.0.0",
            author="Test",
            description="Test",
            plugin_type="metric",
        )
        
        class TestMetric(MetricPlugin):
            def initialize(self, config):
                self.initialized = True
                return True
            
            def calculate(self, evidence):
                coverage = evidence.get("coverage", 0)
                return {"quality_score": coverage * 0.5}
        
        plugin = TestMetric(metadata)
        plugin.initialize({})
        result = plugin.execute(evidence={"coverage": 90})
        
        assert "quality_score" in result
        assert result["quality_score"] == 45.0


class TestCompliancePlugin:
    """Tests for compliance plugin base class."""
    
    def test_compliance_plugin_creation(self):
        """Test compliance plugin creation."""
        metadata = PluginMetadata(
            plugin_id="test_compliance",
            name="Test Compliance",
            version="1.0.0",
            author="Test",
            description="Test",
            plugin_type="compliance",
        )
        
        class TestCompliance(CompliancePlugin):
            def initialize(self, config):
                self.initialized = True
                return True
            
            def check_compliance(self, project_data, standard):
                return {"compliant": True}
        
        plugin = TestCompliance(metadata)
        assert isinstance(plugin, CompliancePlugin)
    
    def test_compliance_plugin_check(self):
        """Test compliance plugin checking."""
        metadata = PluginMetadata(
            plugin_id="test_compliance",
            name="Test Compliance",
            version="1.0.0",
            author="Test",
            description="Test",
            plugin_type="compliance",
        )
        
        class TestCompliance(CompliancePlugin):
            def initialize(self, config):
                self.initialized = True
                return True
            
            def check_compliance(self, project_data, standard):
                return {
                    "standard": standard,
                    "compliant": project_data.get("coverage", 0) >= 80,
                    "score": 85.0,
                }
        
        plugin = TestCompliance(metadata)
        plugin.initialize({})
        result = plugin.execute(
            project_data={"coverage": 85},
            standard="ISO27001"
        )
        
        assert result["standard"] == "ISO27001"
        assert result["compliant"] is True


class TestVisualizationPlugin:
    """Tests for visualization plugin base class."""
    
    def test_visualization_plugin_creation(self):
        """Test visualization plugin creation."""
        metadata = PluginMetadata(
            plugin_id="test_viz",
            name="Test Visualization",
            version="1.0.0",
            author="Test",
            description="Test",
            plugin_type="visualization",
        )
        
        class TestVisualization(VisualizationPlugin):
            def initialize(self, config):
                self.initialized = True
                return True
            
            def render(self, data, format="html"):
                return f"<div>{data}</div>"
        
        plugin = TestVisualization(metadata)
        assert isinstance(plugin, VisualizationPlugin)
    
    def test_visualization_plugin_render(self):
        """Test visualization plugin rendering."""
        metadata = PluginMetadata(
            plugin_id="test_viz",
            name="Test Visualization",
            version="1.0.0",
            author="Test",
            description="Test",
            plugin_type="visualization",
        )
        
        class TestVisualization(VisualizationPlugin):
            def initialize(self, config):
                self.initialized = True
                return True
            
            def render(self, data, format="html"):
                if format == "html":
                    return f"<div>{data['value']}</div>"
                elif format == "svg":
                    return f"<svg>{data['value']}</svg>"
                return str(data)
        
        plugin = TestVisualization(metadata)
        plugin.initialize({})
        
        html = plugin.execute(data={"value": "test"}, format="html")
        assert "<div>test</div>" == html
        
        svg = plugin.execute(data={"value": "test"}, format="svg")
        assert "<svg>test</svg>" == svg


class TestPluginTemplate:
    """Tests for plugin template generation."""
    
    def test_generate_collector_template(self):
        """Test collector plugin template generation."""
        code = PluginTemplate.generate(
            "collector",
            "Test Collector",
            "test_collector",
            "Test Author",
            "A test collector plugin",
        )
        
        assert "CollectorPlugin" in code
        assert "test_collector" in code
        assert "Test Collector" in code
        assert "def collect" in code
    
    def test_generate_metric_template(self):
        """Test metric plugin template generation."""
        code = PluginTemplate.generate(
            "metric",
            "Test Metric",
            "test_metric",
            "Test Author",
            "A test metric plugin",
        )
        
        assert "MetricPlugin" in code
        assert "test_metric" in code
        assert "def calculate" in code
    
    def test_generate_compliance_template(self):
        """Test compliance plugin template generation."""
        code = PluginTemplate.generate(
            "compliance",
            "Test Compliance",
            "test_compliance",
            "Test Author",
            "A test compliance plugin",
        )
        
        assert "CompliancePlugin" in code
        assert "test_compliance" in code
        assert "def check_compliance" in code
    
    def test_generate_visualization_template(self):
        """Test visualization plugin template generation."""
        code = PluginTemplate.generate(
            "visualization",
            "Test Visualization",
            "test_viz",
            "Test Author",
            "A test visualization plugin",
        )
        
        assert "VisualizationPlugin" in code
        assert "test_viz" in code
        assert "def render" in code
    
    def test_template_has_factory_function(self):
        """Test that templates include factory function."""
        code = PluginTemplate.generate(
            "collector",
            "Test",
            "test",
            "Author",
            "Description",
        )
        
        assert "def create_plugin()" in code
    
    def test_invalid_plugin_type(self):
        """Test that invalid plugin type raises error."""
        with pytest.raises(ValueError, match="Unknown plugin type"):
            PluginTemplate.generate(
                "invalid_type",
                "Test",
                "test",
                "Author",
                "Description",
            )


class TestPluginScaffolder:
    """Tests for plugin scaffolder."""
    
    def test_scaffold_plugin(self):
        """Test complete plugin scaffolding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            scaffolder = PluginScaffolder()
            
            created_files = scaffolder.scaffold_plugin(
                tmpdir,
                "collector",
                "Test Collector",
                "test_collector",
                "Test Author",
                "A test plugin",
            )
            
            # Check that files were created
            assert "plugin.py" in created_files
            assert "manifest.json" in created_files
            assert "README.md" in created_files
            assert "test_plugin.py" in created_files
            assert "requirements.txt" in created_files
            
            # Check plugin directory exists
            plugin_dir = os.path.join(tmpdir, "test_collector")
            assert os.path.isdir(plugin_dir)
            
            # Check plugin file exists and has content
            plugin_file = created_files["plugin.py"]
            assert os.path.isfile(plugin_file)
            with open(plugin_file, "r") as f:
                content = f.read()
                assert "CollectorPlugin" in content
    
    def test_manifest_generation(self):
        """Test manifest file generation."""
        scaffolder = PluginScaffolder()
        manifest = scaffolder._generate_manifest(
            "collector",
            "Test Plugin",
            "test_plugin",
            "Test Author",
            "Test description",
        )
        
        assert manifest["plugin_id"] == "test_plugin"
        assert manifest["name"] == "Test Plugin"
        assert manifest["type"] == "collector"
        assert manifest["version"] == "1.0.0"
        assert "created_at" in manifest
    
    def test_readme_generation(self):
        """Test README generation."""
        scaffolder = PluginScaffolder()
        readme = scaffolder._generate_readme(
            "Test Plugin",
            "A test plugin",
            "collector",
        )
        
        assert "Test Plugin" in readme
        assert "collector" in readme
        assert "Installation" in readme
        assert "Usage" in readme
    
    def test_test_file_generation(self):
        """Test test file generation."""
        scaffolder = PluginScaffolder()
        test_code = scaffolder._generate_test("Test Plugin", "collector")
        
        assert "def test_plugin_creation" in test_code
        assert "def test_plugin_initialization" in test_code
        assert "pytest" in test_code


class TestPluginDevelopmentGuide:
    """Tests for plugin development guide."""
    
    def test_guide_generation(self):
        """Test development guide generation."""
        guide = PluginDevelopmentGuide.generate_guide()
        
        assert "Plugin Development Guide" in guide
        assert "Plugin Types" in guide
        assert "Getting Started" in guide
        assert "Best Practices" in guide
        assert len(guide) > 500  # Should be comprehensive


class TestBasePlugin:
    """Tests for base plugin functionality."""
    
    def test_plugin_info(self):
        """Test plugin info retrieval."""
        metadata = PluginMetadata(
            plugin_id="test",
            name="Test",
            version="1.0.0",
            author="Author",
            description="Description",
            plugin_type="collector",
        )
        
        class TestPlugin(CollectorPlugin):
            def initialize(self, config):
                self.initialized = True
                return True
            
            def collect(self, source, **kwargs):
                return []
        
        plugin = TestPlugin(metadata)
        info = plugin.get_info()
        
        assert info["id"] == "test"
        assert info["name"] == "Test"
        assert info["type"] == "collector"
        assert "initialized" in info
    
    def test_plugin_validation_uninitialized(self):
        """Test validation fails for uninitialized plugin."""
        metadata = PluginMetadata(
            plugin_id="test",
            name="Test",
            version="1.0.0",
            author="Author",
            description="Description",
            plugin_type="collector",
        )
        
        class TestPlugin(CollectorPlugin):
            def initialize(self, config):
                self.initialized = True
                return True
            
            def collect(self, source, **kwargs):
                return []
        
        plugin = TestPlugin(metadata)
        is_valid, message = plugin.validate()
        
        assert is_valid is False
        assert "not initialized" in message.lower()
    
    def test_plugin_validation_initialized(self):
        """Test validation passes for initialized plugin."""
        metadata = PluginMetadata(
            plugin_id="test",
            name="Test",
            version="1.0.0",
            author="Author",
            description="Description",
            plugin_type="collector",
        )
        
        class TestPlugin(CollectorPlugin):
            def initialize(self, config):
                self.initialized = True
                return True
            
            def collect(self, source, **kwargs):
                return []
        
        plugin = TestPlugin(metadata)
        plugin.initialize({})
        is_valid, message = plugin.validate()
        
        assert is_valid is True
        assert message == ""
