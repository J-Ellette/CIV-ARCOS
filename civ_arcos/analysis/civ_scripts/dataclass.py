"""DataClass - Data structure builder

Structured data type creator for development tasks.
Wrapper around Python's dataclasses module.
"""

from dataclasses import (
    dataclass, 
    field, 
    fields,
    asdict,
    astuple,
    replace,
    is_dataclass,
    Field,
    FrozenInstanceError,
    InitVar,
    MISSING
)
from typing import Any, Dict, List, Optional, Type, Tuple


class DataClass:
    """
    DataClass: Data structure builder
    
    Provides utilities for creating structured data types using dataclasses.
    """
    
    def __init__(self):
        """Initialize DataClass"""
        self.created_classes = []
        self.instance_count = 0
    
    def make(self,
             name: str,
             fields: List[Tuple[str, type]],
             frozen: bool = False,
             order: bool = False) -> Type:
        """
        Create a dataclass dynamically.
        
        Args:
            name: Class name
            fields: List of (field_name, field_type) tuples
            frozen: Whether instances should be immutable
            order: Whether to generate ordering methods
            
        Returns:
            New dataclass type
        """
        # Create class with __annotations__
        annotations = {field_name: field_type for field_name, field_type in fields}
        
        cls_dict = {
            '__annotations__': annotations
        }
        
        # Create the class
        cls = type(name, (), cls_dict)
        
        # Apply dataclass decorator
        cls = dataclass(frozen=frozen, order=order)(cls)
        
        self.created_classes.append(cls)
        return cls
    
    def decorator(self,
                  init: bool = True,
                  repr: bool = True,
                  eq: bool = True,
                  order: bool = False,
                  unsafe_hash: bool = False,
                  frozen: bool = False):
        """
        Get dataclass decorator with options.
        
        Args:
            init: Generate __init__ method
            repr: Generate __repr__ method
            eq: Generate __eq__ method
            order: Generate ordering methods
            unsafe_hash: Generate __hash__ method
            frozen: Make instances immutable
            
        Returns:
            Dataclass decorator
        """
        return dataclass(
            init=init,
            repr=repr,
            eq=eq,
            order=order,
            unsafe_hash=unsafe_hash,
            frozen=frozen
        )
    
    def field(self,
              default=MISSING,
              default_factory=MISSING,
              init: bool = True,
              repr: bool = True,
              hash: Optional[bool] = None,
              compare: bool = True,
              metadata: Optional[Dict] = None) -> Field:
        """
        Create a dataclass field with options.
        
        Args:
            default: Default value
            default_factory: Function to generate default
            init: Include in __init__
            repr: Include in __repr__
            hash: Include in __hash__
            compare: Include in comparison methods
            metadata: Field metadata
            
        Returns:
            Field object
        """
        return field(
            default=default,
            default_factory=default_factory,
            init=init,
            repr=repr,
            hash=hash,
            compare=compare,
            metadata=metadata
        )
    
    def to_dict(self, instance: Any, dict_factory: type = dict) -> Dict:
        """
        Convert dataclass instance to dictionary.
        
        Args:
            instance: Dataclass instance
            dict_factory: Type to use for dictionary
            
        Returns:
            Dictionary representation
        """
        return asdict(instance, dict_factory=dict_factory)
    
    def to_tuple(self, instance: Any, tuple_factory: type = tuple) -> Tuple:
        """
        Convert dataclass instance to tuple.
        
        Args:
            instance: Dataclass instance
            tuple_factory: Type to use for tuple
            
        Returns:
            Tuple representation
        """
        return astuple(instance, tuple_factory=tuple_factory)
    
    def get_fields(self, class_or_instance: Any) -> Tuple[Field, ...]:
        """
        Get fields from dataclass.
        
        Args:
            class_or_instance: Dataclass type or instance
            
        Returns:
            Tuple of Field objects
        """
        return fields(class_or_instance)
    
    def replace(self, instance: Any, **changes) -> Any:
        """
        Create new instance with modified fields.
        
        Args:
            instance: Dataclass instance
            **changes: Fields to change
            
        Returns:
            New instance with changes
        """
        self.instance_count += 1
        return replace(instance, **changes)
    
    def is_dataclass(self, obj: Any) -> bool:
        """
        Check if object is a dataclass.
        
        Args:
            obj: Object to check
            
        Returns:
            True if dataclass, False otherwise
        """
        return is_dataclass(obj)
    
    def make_simple(self,
                    class_name: str,
                    **field_types: type) -> Type:
        """
        Create a simple dataclass with named fields.
        
        Args:
            class_name: Class name
            **field_types: Keyword arguments mapping field names to types
            
        Returns:
            New dataclass type
        """
        fields_list = [(fname, ftype) for fname, ftype in field_types.items()]
        return self.make(class_name, fields_list)
    
    def make_from_dict(self,
                       name: str,
                       data: Dict[str, Any],
                       frozen: bool = False) -> Type:
        """
        Create dataclass from dictionary with type inference.
        
        Args:
            name: Class name
            data: Dictionary with example values
            frozen: Whether instances should be immutable
            
        Returns:
            New dataclass type
        """
        fields_list = [(key, type(value)) for key, value in data.items()]
        return self.make(name, fields_list, frozen=frozen)
    
    def validate_instance(self, instance: Any) -> bool:
        """
        Validate that instance matches its dataclass definition.
        
        Args:
            instance: Dataclass instance
            
        Returns:
            True if valid, False otherwise
        """
        if not self.is_dataclass(instance):
            return False
        
        for f in self.get_fields(instance):
            if not hasattr(instance, f.name):
                return False
        
        return True
    
    def get_field_names(self, class_or_instance: Any) -> List[str]:
        """
        Get list of field names from dataclass.
        
        Args:
            class_or_instance: Dataclass type or instance
            
        Returns:
            List of field names
        """
        return [f.name for f in self.get_fields(class_or_instance)]
    
    def get_field_types(self, class_or_instance: Any) -> Dict[str, type]:
        """
        Get dictionary of field types from dataclass.
        
        Args:
            class_or_instance: Dataclass type or instance
            
        Returns:
            Dictionary mapping field names to types
        """
        return {f.name: f.type for f in self.get_fields(class_or_instance)}
    
    def get_results(self) -> Dict[str, Any]:
        """Get processing results"""
        return {
            'classes_created': len(self.created_classes),
            'instances_created': self.instance_count,
            'class_names': [cls.__name__ for cls in self.created_classes]
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics"""
        return {
            'total_classes': len(self.created_classes),
            'total_instances': self.instance_count
        }
