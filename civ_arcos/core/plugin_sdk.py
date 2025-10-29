"""
Plugin Development Kit (PDK) for CIV-ARCOS.

Provides SDK and templates for third-party plugin development:
- Base classes for plugin development
- Plugin scaffolding and templates
- Development utilities
- Documentation generation
"""

from typing import Any, Dict, List, Optional, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import os


@dataclass
class PluginMetadata:
    """Plugin metadata structure."""

    plugin_id: str
    name: str
    version: str
    author: str
    description: str
    plugin_type: str  # "collector", "metric", "compliance", "visualization"
    permissions: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


class BasePlugin(ABC):
    """
    Base class for all CIV-ARCOS plugins.

    All plugins must inherit from this class and implement required methods.
    """

    def __init__(self, metadata: PluginMetadata):
        """
        Initialize plugin with metadata.

        Args:
            metadata: Plugin metadata
        """
        self.metadata = metadata
        self.initialized = False
        self.config = {}

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """
        Initialize the plugin with configuration.

        Args:
            config: Configuration dictionary

        Returns:
            True if initialization successful, False otherwise
        """
        pass

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute main plugin functionality.

        Returns:
            Plugin execution result
        """
        pass

    def validate(self) -> tuple[bool, str]:
        """
        Validate plugin state and configuration.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.initialized:
            return False, "Plugin not initialized"
        return True, ""

    def get_info(self) -> Dict[str, Any]:
        """
        Get plugin information.

        Returns:
            Plugin metadata dictionary
        """
        return {
            "id": self.metadata.plugin_id,
            "name": self.metadata.name,
            "version": self.metadata.version,
            "author": self.metadata.author,
            "description": self.metadata.description,
            "type": self.metadata.plugin_type,
            "initialized": self.initialized,
        }


class CollectorPlugin(BasePlugin):
    """
    Base class for evidence collector plugins.

    Collector plugins gather evidence from external sources.
    """

    def __init__(self, metadata: PluginMetadata):
        """Initialize collector plugin."""
        super().__init__(metadata)
        if metadata.plugin_type != "collector":
            raise ValueError("Plugin type must be 'collector'")

    @abstractmethod
    def collect(self, source: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Collect evidence from source.

        Args:
            source: Source identifier
            **kwargs: Additional parameters

        Returns:
            List of evidence items
        """
        pass

    def execute(self, *args, **kwargs) -> Any:
        """Execute collector plugin."""
        source = kwargs.pop("source", "")
        return self.collect(source, **kwargs)


class MetricPlugin(BasePlugin):
    """
    Base class for custom metric plugins.

    Metric plugins calculate custom quality or performance metrics.
    """

    def __init__(self, metadata: PluginMetadata):
        """Initialize metric plugin."""
        super().__init__(metadata)
        if metadata.plugin_type != "metric":
            raise ValueError("Plugin type must be 'metric'")

    @abstractmethod
    def calculate(self, evidence: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate metrics from evidence.

        Args:
            evidence: Evidence data

        Returns:
            Dictionary of metric_name -> value
        """
        pass

    def execute(self, *args, **kwargs) -> Any:
        """Execute metric plugin."""
        evidence = kwargs.get("evidence", {})
        return self.calculate(evidence)


class CompliancePlugin(BasePlugin):
    """
    Base class for compliance check plugins.

    Compliance plugins verify adherence to standards and regulations.
    """

    def __init__(self, metadata: PluginMetadata):
        """Initialize compliance plugin."""
        super().__init__(metadata)
        if metadata.plugin_type != "compliance":
            raise ValueError("Plugin type must be 'compliance'")

    @abstractmethod
    def check_compliance(
        self,
        project_data: Dict[str, Any],
        standard: str,
    ) -> Dict[str, Any]:
        """
        Check compliance against standard.

        Args:
            project_data: Project data to check
            standard: Compliance standard identifier

        Returns:
            Compliance check results
        """
        pass

    def execute(self, *args, **kwargs) -> Any:
        """Execute compliance plugin."""
        project_data = kwargs.get("project_data", {})
        standard = kwargs.get("standard", "")
        return self.check_compliance(project_data, standard)


class VisualizationPlugin(BasePlugin):
    """
    Base class for visualization plugins.

    Visualization plugins create custom charts and reports.
    """

    def __init__(self, metadata: PluginMetadata):
        """Initialize visualization plugin."""
        super().__init__(metadata)
        if metadata.plugin_type != "visualization":
            raise ValueError("Plugin type must be 'visualization'")

    @abstractmethod
    def render(self, data: Dict[str, Any], format: str = "html") -> str:
        """
        Render visualization.

        Args:
            data: Data to visualize
            format: Output format ("html", "svg", "json")

        Returns:
            Rendered visualization
        """
        pass

    def execute(self, *args, **kwargs) -> Any:
        """Execute visualization plugin."""
        data = kwargs.get("data", {})
        format_type = kwargs.get("format", "html")
        return self.render(data, format_type)


class PluginTemplate:
    """Plugin template generator for scaffolding new plugins."""

    TEMPLATES = {
        "collector": """
\"\"\"
{name} - Evidence Collector Plugin for CIV-ARCOS
{description}
\"\"\"

from civ_arcos.core.plugin_sdk import CollectorPlugin, PluginMetadata
from typing import Dict, List, Any


class {class_name}(CollectorPlugin):
    \"\"\"
    {name} collector plugin.
    
    Collects evidence from {source_description}.
    \"\"\"
    
    def __init__(self):
        metadata = PluginMetadata(
            plugin_id="{plugin_id}",
            name="{name}",
            version="1.0.0",
            author="{author}",
            description="{description}",
            plugin_type="collector",
            permissions=["evidence.write", "network.http"],
        )
        super().__init__(metadata)
    
    def initialize(self, config: Dict[str, Any]) -> bool:
        \"\"\"Initialize the collector.\"\"\"
        self.config = config
        # Add initialization logic here
        self.initialized = True
        return True
    
    def collect(self, source: str, **kwargs) -> List[Dict[str, Any]]:
        \"\"\"
        Collect evidence from source.
        
        Args:
            source: Source identifier
            **kwargs: Additional parameters
            
        Returns:
            List of evidence items
        \"\"\"
        evidence_items = []
        
        # TODO: Implement collection logic
        # Example:
        # data = fetch_from_source(source)
        # evidence_items.append({{
        #     "type": "metric",
        #     "source": self.metadata.plugin_id,
        #     "data": data,
        #     "timestamp": datetime.now().isoformat(),
        # }})
        
        return evidence_items


# Plugin factory function (required)
def create_plugin():
    \"\"\"Create and return plugin instance.\"\"\"
    return {class_name}()
""",
        "metric": """
\"\"\"
{name} - Metric Calculator Plugin for CIV-ARCOS
{description}
\"\"\"

from civ_arcos.core.plugin_sdk import MetricPlugin, PluginMetadata
from typing import Dict, Any


class {class_name}(MetricPlugin):
    \"\"\"
    {name} metric plugin.
    
    Calculates {metric_description}.
    \"\"\"
    
    def __init__(self):
        metadata = PluginMetadata(
            plugin_id="{plugin_id}",
            name="{name}",
            version="1.0.0",
            author="{author}",
            description="{description}",
            plugin_type="metric",
            permissions=["evidence.read"],
        )
        super().__init__(metadata)
    
    def initialize(self, config: Dict[str, Any]) -> bool:
        \"\"\"Initialize the metric calculator.\"\"\"
        self.config = config
        # Add initialization logic here
        self.initialized = True
        return True
    
    def calculate(self, evidence: Dict[str, Any]) -> Dict[str, float]:
        \"\"\"
        Calculate metrics from evidence.
        
        Args:
            evidence: Evidence data
            
        Returns:
            Dictionary of metric_name -> value
        \"\"\"
        metrics = {{}}
        
        # TODO: Implement metric calculation logic
        # Example:
        # metrics["custom_score"] = calculate_score(evidence)
        # metrics["quality_index"] = calculate_quality(evidence)
        
        return metrics


# Plugin factory function (required)
def create_plugin():
    \"\"\"Create and return plugin instance.\"\"\"
    return {class_name}()
""",
        "compliance": """
\"\"\"
{name} - Compliance Check Plugin for CIV-ARCOS
{description}
\"\"\"

from civ_arcos.core.plugin_sdk import CompliancePlugin, PluginMetadata
from typing import Dict, Any


class {class_name}(CompliancePlugin):
    \"\"\"
    {name} compliance plugin.
    
    Checks compliance with {standard_name}.
    \"\"\"
    
    def __init__(self):
        metadata = PluginMetadata(
            plugin_id="{plugin_id}",
            name="{name}",
            version="1.0.0",
            author="{author}",
            description="{description}",
            plugin_type="compliance",
            permissions=["evidence.read"],
        )
        super().__init__(metadata)
    
    def initialize(self, config: Dict[str, Any]) -> bool:
        \"\"\"Initialize the compliance checker.\"\"\"
        self.config = config
        # Add initialization logic here
        self.initialized = True
        return True
    
    def check_compliance(
        self,
        project_data: Dict[str, Any],
        standard: str,
    ) -> Dict[str, Any]:
        \"\"\"
        Check compliance against standard.
        
        Args:
            project_data: Project data to check
            standard: Compliance standard identifier
            
        Returns:
            Compliance check results
        \"\"\"
        results = {{
            "standard": standard,
            "compliant": False,
            "checks": [],
            "violations": [],
            "score": 0.0,
        }}
        
        # TODO: Implement compliance check logic
        # Example:
        # for requirement in get_requirements(standard):
        #     if check_requirement(project_data, requirement):
        #         results["checks"].append(requirement)
        #     else:
        #         results["violations"].append(requirement)
        
        return results


# Plugin factory function (required)
def create_plugin():
    \"\"\"Create and return plugin instance.\"\"\"
    return {class_name}()
""",
        "visualization": """
\"\"\"
{name} - Visualization Plugin for CIV-ARCOS
{description}
\"\"\"

from civ_arcos.core.plugin_sdk import VisualizationPlugin, PluginMetadata
from typing import Dict, Any


class {class_name}(VisualizationPlugin):
    \"\"\"
    {name} visualization plugin.
    
    Creates {visualization_description}.
    \"\"\"
    
    def __init__(self):
        metadata = PluginMetadata(
            plugin_id="{plugin_id}",
            name="{name}",
            version="1.0.0",
            author="{author}",
            description="{description}",
            plugin_type="visualization",
            permissions=["evidence.read"],
        )
        super().__init__(metadata)
    
    def initialize(self, config: Dict[str, Any]) -> bool:
        \"\"\"Initialize the visualizer.\"\"\"
        self.config = config
        # Add initialization logic here
        self.initialized = True
        return True
    
    def render(self, data: Dict[str, Any], format: str = "html") -> str:
        \"\"\"
        Render visualization.
        
        Args:
            data: Data to visualize
            format: Output format ("html", "svg", "json")
            
        Returns:
            Rendered visualization
        \"\"\"
        if format == "html":
            return self._render_html(data)
        elif format == "svg":
            return self._render_svg(data)
        elif format == "json":
            return self._render_json(data)
        else:
            raise ValueError(f"Unsupported format: {{format}}")
    
    def _render_html(self, data: Dict[str, Any]) -> str:
        \"\"\"Render as HTML.\"\"\"
        # TODO: Implement HTML rendering
        html = "<div><h2>{name}</h2><p>Data visualization here</p></div>"
        return html
    
    def _render_svg(self, data: Dict[str, Any]) -> str:
        \"\"\"Render as SVG.\"\"\"
        # TODO: Implement SVG rendering
        svg = "<svg><text>Visualization</text></svg>"
        return svg
    
    def _render_json(self, data: Dict[str, Any]) -> str:
        \"\"\"Render as JSON.\"\"\"
        import json
        return json.dumps(data, indent=2)


# Plugin factory function (required)
def create_plugin():
    \"\"\"Create and return plugin instance.\"\"\"
    return {class_name}()
""",
    }

    @classmethod
    def generate(
        cls,
        plugin_type: str,
        name: str,
        plugin_id: str,
        author: str,
        description: str,
        **kwargs,
    ) -> str:
        """
        Generate plugin code from template.

        Args:
            plugin_type: Type of plugin ("collector", "metric", "compliance", "visualization")
            name: Plugin name
            plugin_id: Unique plugin identifier
            author: Plugin author
            description: Plugin description
            **kwargs: Additional template parameters

        Returns:
            Generated plugin code
        """
        if plugin_type not in cls.TEMPLATES:
            raise ValueError(f"Unknown plugin type: {plugin_type}")

        # Generate class name from plugin name
        class_name = "".join(word.capitalize() for word in name.split())
        if not class_name.endswith("Plugin"):
            class_name += "Plugin"

        template_vars = {
            "name": name,
            "class_name": class_name,
            "plugin_id": plugin_id,
            "author": author,
            "description": description,
            "source_description": kwargs.get("source_description", "external sources"),
            "metric_description": kwargs.get("metric_description", "custom metrics"),
            "standard_name": kwargs.get("standard_name", "standards"),
            "visualization_description": kwargs.get(
                "visualization_description", "custom visualizations"
            ),
        }

        template = cls.TEMPLATES[plugin_type]
        return template.format(**template_vars)


class PluginScaffolder:
    """Creates complete plugin project structure."""

    def scaffold_plugin(
        self,
        output_dir: str,
        plugin_type: str,
        name: str,
        plugin_id: str,
        author: str,
        description: str,
        **kwargs,
    ) -> Dict[str, str]:
        """
        Create complete plugin project structure.

        Args:
            output_dir: Directory to create plugin in
            plugin_type: Type of plugin
            name: Plugin name
            plugin_id: Unique plugin identifier
            author: Plugin author
            description: Plugin description
            **kwargs: Additional parameters

        Returns:
            Dictionary of created files
        """
        # Create directory structure
        plugin_dir = os.path.join(output_dir, plugin_id)
        os.makedirs(plugin_dir, exist_ok=True)

        created_files = {}

        # Generate plugin code
        plugin_code = PluginTemplate.generate(
            plugin_type, name, plugin_id, author, description, **kwargs
        )
        plugin_file = os.path.join(plugin_dir, "plugin.py")
        with open(plugin_file, "w") as f:
            f.write(plugin_code)
        created_files["plugin.py"] = plugin_file

        # Generate manifest
        manifest = self._generate_manifest(
            plugin_type, name, plugin_id, author, description
        )
        manifest_file = os.path.join(plugin_dir, "manifest.json")
        with open(manifest_file, "w") as f:
            json.dump(manifest, f, indent=2)
        created_files["manifest.json"] = manifest_file

        # Generate README
        readme = self._generate_readme(name, description, plugin_type)
        readme_file = os.path.join(plugin_dir, "README.md")
        with open(readme_file, "w") as f:
            f.write(readme)
        created_files["README.md"] = readme_file

        # Generate tests
        test_code = self._generate_test(name, plugin_type)
        test_file = os.path.join(plugin_dir, "test_plugin.py")
        with open(test_file, "w") as f:
            f.write(test_code)
        created_files["test_plugin.py"] = test_file

        # Generate requirements.txt
        requirements = self._generate_requirements()
        req_file = os.path.join(plugin_dir, "requirements.txt")
        with open(req_file, "w") as f:
            f.write(requirements)
        created_files["requirements.txt"] = req_file

        return created_files

    def _generate_manifest(
        self,
        plugin_type: str,
        name: str,
        plugin_id: str,
        author: str,
        description: str,
    ) -> Dict[str, Any]:
        """Generate plugin manifest."""
        return {
            "plugin_id": plugin_id,
            "name": name,
            "version": "1.0.0",
            "author": author,
            "description": description,
            "type": plugin_type,
            "entry_point": "plugin.py",
            "permissions": ["evidence.read"],
            "dependencies": [],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    def _generate_readme(self, name: str, description: str, plugin_type: str) -> str:
        """Generate README.md."""
        return f"""# {name}

{description}

## Plugin Type

{plugin_type}

## Installation

```bash
# Copy plugin to CIV-ARCOS plugins directory
cp -r . /path/to/civ-arcos/plugins/{name.lower().replace(' ', '_')}
```

## Usage

```python
from plugin import create_plugin

plugin = create_plugin()
plugin.initialize({{}})
result = plugin.execute()
```

## Configuration

Add configuration options here.

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest test_plugin.py
```

## License

Specify your license here.
"""

    def _generate_test(self, name: str, plugin_type: str) -> str:
        """Generate test file."""
        class_name = "".join(word.capitalize() for word in name.split())
        if not class_name.endswith("Plugin"):
            class_name += "Plugin"

        return f'''"""
Tests for {name} plugin.
"""

import pytest
from plugin import create_plugin, {class_name}


def test_plugin_creation():
    """Test plugin can be created."""
    plugin = create_plugin()
    assert isinstance(plugin, {class_name})


def test_plugin_initialization():
    """Test plugin initialization."""
    plugin = create_plugin()
    result = plugin.initialize({{}})
    assert result is True
    assert plugin.initialized is True


def test_plugin_execution():
    """Test plugin execution."""
    plugin = create_plugin()
    plugin.initialize({{}})
    
    # TODO: Add specific tests for your plugin
    result = plugin.execute()
    assert result is not None


def test_plugin_validation():
    """Test plugin validation."""
    plugin = create_plugin()
    plugin.initialize({{}})
    
    is_valid, message = plugin.validate()
    assert is_valid is True


def test_plugin_info():
    """Test plugin info retrieval."""
    plugin = create_plugin()
    info = plugin.get_info()
    
    assert "id" in info
    assert "name" in info
    assert "version" in info
    assert info["type"] == "{plugin_type}"
'''

    def _generate_requirements(self) -> str:
        """Generate requirements.txt."""
        return """# Plugin dependencies
# Add your dependencies here

# Testing
pytest>=7.4.0
"""


class PluginDevelopmentGuide:
    """Generates comprehensive plugin development documentation."""

    @staticmethod
    def generate_guide() -> str:
        """Generate complete plugin development guide."""
        return """# CIV-ARCOS Plugin Development Guide

## Introduction

Welcome to the CIV-ARCOS Plugin Development Kit (PDK). This guide will help you create custom plugins to extend CIV-ARCOS functionality.

## Plugin Types

CIV-ARCOS supports four types of plugins:

### 1. Collector Plugins
Collect evidence from external sources (CI/CD systems, code repositories, etc.)

### 2. Metric Plugins
Calculate custom quality or performance metrics

### 3. Compliance Plugins
Verify adherence to standards and regulations

### 4. Visualization Plugins
Create custom charts and reports

## Getting Started

### Quick Start

```bash
# Create a new plugin
python -m civ_arcos.plugin_sdk scaffold \\
    --type collector \\
    --name "My Collector" \\
    --id my_collector \\
    --author "Your Name"
```

### Manual Setup

1. Create plugin directory
2. Implement plugin class inheriting from base class
3. Create manifest.json
4. Implement required methods
5. Test your plugin

## Plugin Structure

```
my_plugin/
├── plugin.py           # Main plugin code
├── manifest.json       # Plugin metadata
├── README.md          # Documentation
├── test_plugin.py     # Tests
└── requirements.txt   # Dependencies
```

## Base Classes

All plugins inherit from BasePlugin and implement:

- `initialize(config)` - Setup plugin with configuration
- `execute(*args, **kwargs)` - Main plugin functionality
- `validate()` - Validate plugin state

## Permissions

Plugins must declare required permissions:

- `evidence.read` - Read evidence data
- `evidence.write` - Create evidence
- `storage.read` - Read from storage
- `storage.write` - Write to storage
- `analysis.run` - Run analysis tools
- `network.http` - Make HTTP requests

## Best Practices

1. **Error Handling**: Always handle errors gracefully
2. **Validation**: Validate inputs before processing
3. **Documentation**: Document your plugin thoroughly
4. **Testing**: Write comprehensive tests
5. **Performance**: Consider performance implications
6. **Security**: Never expose sensitive data

## Examples

See the `examples/` directory for complete plugin examples.

## API Reference

Full API documentation available at: https://docs.civ-arcos.org/plugins

## Support

- GitHub Issues: https://github.com/civ-arcos/civ-arcos/issues
- Discussions: https://github.com/civ-arcos/civ-arcos/discussions
- Email: support@civ-arcos.org
"""


# Export main classes
__all__ = [
    "BasePlugin",
    "CollectorPlugin",
    "MetricPlugin",
    "CompliancePlugin",
    "VisualizationPlugin",
    "PluginMetadata",
    "PluginTemplate",
    "PluginScaffolder",
    "PluginDevelopmentGuide",
]
