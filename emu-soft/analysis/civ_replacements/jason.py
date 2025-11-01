"""Jason - JSON handler

JSON processor for development tasks.
Wrapper around Python's json module with enhanced error handling.
"""

import json
from typing import Any, Dict, List, Optional, Union, TextIO
from pathlib import Path


class Jason:
    """
    Jason: JSON processor
    
    Provides utilities to parse, validate, and serialize JSON.
    """
    
    def __init__(self):
        """Initialize Jason"""
        self.parse_count = 0
        self.serialize_count = 0
        self.errors = []
    
    def loads(self, 
              json_string: str, 
              strict: bool = True,
              **kwargs) -> Any:
        """
        Parse JSON from string.
        
        Args:
            json_string: JSON string to parse
            strict: Whether to use strict parsing
            **kwargs: Additional arguments for json.loads
            
        Returns:
            Parsed Python object
        """
        try:
            result = json.loads(json_string, strict=strict, **kwargs)
            self.parse_count += 1
            return result
        except json.JSONDecodeError as e:
            self.errors.append(str(e))
            raise
    
    def dumps(self, 
              obj: Any, 
              indent: Optional[int] = None,
              sort_keys: bool = False,
              ensure_ascii: bool = True,
              **kwargs) -> str:
        """
        Serialize object to JSON string.
        
        Args:
            obj: Object to serialize
            indent: Indentation level (None for compact)
            sort_keys: Whether to sort dictionary keys
            ensure_ascii: Whether to escape non-ASCII characters
            **kwargs: Additional arguments for json.dumps
            
        Returns:
            JSON string
        """
        try:
            result = json.dumps(
                obj, 
                indent=indent, 
                sort_keys=sort_keys,
                ensure_ascii=ensure_ascii,
                **kwargs
            )
            self.serialize_count += 1
            return result
        except (TypeError, ValueError) as e:
            self.errors.append(str(e))
            raise
    
    def load(self, file: Union[str, Path, TextIO], **kwargs) -> Any:
        """
        Load JSON from file.
        
        Args:
            file: File path or file object
            **kwargs: Additional arguments for json.load
            
        Returns:
            Parsed Python object
        """
        if isinstance(file, (str, Path)):
            with open(file, 'r', encoding='utf-8') as f:
                result = json.load(f, **kwargs)
        else:
            result = json.load(file, **kwargs)
        
        self.parse_count += 1
        return result
    
    def dump(self, 
             obj: Any, 
             file: Union[str, Path, TextIO],
             indent: Optional[int] = 2,
             sort_keys: bool = False,
             **kwargs):
        """
        Dump object to JSON file.
        
        Args:
            obj: Object to serialize
            file: File path or file object
            indent: Indentation level
            sort_keys: Whether to sort dictionary keys
            **kwargs: Additional arguments for json.dump
        """
        if isinstance(file, (str, Path)):
            with open(file, 'w', encoding='utf-8') as f:
                json.dump(obj, f, indent=indent, sort_keys=sort_keys, **kwargs)
        else:
            json.dump(obj, file, indent=indent, sort_keys=sort_keys, **kwargs)
        
        self.serialize_count += 1
    
    def validate(self, json_string: str) -> bool:
        """
        Validate if string is valid JSON.
        
        Args:
            json_string: String to validate
            
        Returns:
            True if valid JSON, False otherwise
        """
        try:
            json.loads(json_string)
            return True
        except json.JSONDecodeError:
            return False
    
    def prettify(self, 
                 json_string: str, 
                 indent: int = 2,
                 sort_keys: bool = False) -> str:
        """
        Format JSON string with indentation.
        
        Args:
            json_string: JSON string to format
            indent: Indentation level
            sort_keys: Whether to sort dictionary keys
            
        Returns:
            Formatted JSON string
        """
        obj = self.loads(json_string)
        return self.dumps(obj, indent=indent, sort_keys=sort_keys)
    
    def minify(self, json_string: str) -> str:
        """
        Minify JSON string (remove whitespace).
        
        Args:
            json_string: JSON string to minify
            
        Returns:
            Minified JSON string
        """
        obj = self.loads(json_string)
        return self.dumps(obj, indent=None, separators=(',', ':'))
    
    def merge(self, *json_objects: Dict) -> Dict:
        """
        Merge multiple JSON objects.
        
        Args:
            *json_objects: JSON objects to merge
            
        Returns:
            Merged dictionary
        """
        result = {}
        for obj in json_objects:
            if isinstance(obj, dict):
                result.update(obj)
        return result
    
    def diff(self, obj1: Any, obj2: Any) -> Dict[str, Any]:
        """
        Find differences between two JSON objects.
        
        Args:
            obj1: First object
            obj2: Second object
            
        Returns:
            Dictionary with differences
        """
        differences = {
            'added': [],
            'removed': [],
            'changed': []
        }
        
        if isinstance(obj1, dict) and isinstance(obj2, dict):
            keys1 = set(obj1.keys())
            keys2 = set(obj2.keys())
            
            differences['added'] = list(keys2 - keys1)
            differences['removed'] = list(keys1 - keys2)
            
            for key in keys1 & keys2:
                if obj1[key] != obj2[key]:
                    differences['changed'].append({
                        'key': key,
                        'old': obj1[key],
                        'new': obj2[key]
                    })
        
        return differences
    
    def get_results(self) -> Dict[str, Any]:
        """Get processing results"""
        return {
            'parsed': self.parse_count,
            'serialized': self.serialize_count,
            'errors': len(self.errors)
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics"""
        return {
            'total_operations': self.parse_count + self.serialize_count,
            'parse_operations': self.parse_count,
            'serialize_operations': self.serialize_count,
            'error_count': len(self.errors)
        }
    
    def get_errors(self) -> List[str]:
        """Get error history"""
        return self.errors.copy()
    
    def clear_errors(self):
        """Clear error history"""
        self.errors.clear()
