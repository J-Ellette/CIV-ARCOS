"""Enumeration - Enum builder

Enumeration type creator for development tasks.
Wrapper around Python's enum module.
"""

from enum import (
    Enum,
    IntEnum,
    Flag,
    IntFlag,
    auto,
    unique,
    EnumMeta
)
from typing import Any, Dict, List, Optional, Type, Union


class Enumeration:
    """
    Enumeration: Enum builder
    
    Provides utilities for creating enumeration types.
    """
    
    def __init__(self):
        """Initialize Enumeration"""
        self.created_enums = []
        self.lookup_count = 0
    
    def make(self,
             name: str,
             members: Union[List[str], Dict[str, Any]],
             enum_type: Type = Enum) -> Type:
        """
        Create an enum dynamically.
        
        Args:
            name: Enum name
            members: List of member names or dict of name->value
            enum_type: Base enum type (Enum, IntEnum, Flag, IntFlag)
            
        Returns:
            New enum type
        """
        if isinstance(members, list):
            # Create with auto() values
            members_dict = {m: auto() for m in members}
        else:
            members_dict = members
        
        # Create the enum
        new_enum = enum_type(name, members_dict)
        self.created_enums.append(new_enum)
        return new_enum
    
    def make_simple(self, name: str, *members: str) -> Type:
        """
        Create a simple enum with auto values.
        
        Args:
            name: Enum name
            *members: Member names
            
        Returns:
            New Enum type
        """
        return self.make(name, list(members), Enum)
    
    def make_int(self, name: str, members: Dict[str, int]) -> Type:
        """
        Create an IntEnum.
        
        Args:
            name: Enum name
            members: Dictionary of name->int value
            
        Returns:
            New IntEnum type
        """
        return self.make(name, members, IntEnum)
    
    def make_flag(self, name: str, *members: str) -> Type:
        """
        Create a Flag enum.
        
        Args:
            name: Enum name
            *members: Member names
            
        Returns:
            New Flag type
        """
        return self.make(name, list(members), Flag)
    
    def make_int_flag(self, name: str, members: Dict[str, int]) -> Type:
        """
        Create an IntFlag enum.
        
        Args:
            name: Enum name
            members: Dictionary of name->int value
            
        Returns:
            New IntFlag type
        """
        return self.make(name, members, IntFlag)
    
    def unique_decorator(self):
        """
        Get @unique decorator for enums.
        
        Returns:
            unique decorator
        """
        return unique
    
    def auto_value(self):
        """
        Get auto() function for enum values.
        
        Returns:
            auto function
        """
        return auto
    
    def get_members(self, enum_class: Type[Enum]) -> Dict[str, Enum]:
        """
        Get all members of an enum.
        
        Args:
            enum_class: Enum type
            
        Returns:
            Dictionary of name->member
        """
        return {member.name: member for member in enum_class}
    
    def get_member_names(self, enum_class: Type[Enum]) -> List[str]:
        """
        Get list of member names.
        
        Args:
            enum_class: Enum type
            
        Returns:
            List of member names
        """
        return [member.name for member in enum_class]
    
    def get_member_values(self, enum_class: Type[Enum]) -> List[Any]:
        """
        Get list of member values.
        
        Args:
            enum_class: Enum type
            
        Returns:
            List of member values
        """
        return [member.value for member in enum_class]
    
    def lookup_by_name(self, enum_class: Type[Enum], name: str) -> Optional[Enum]:
        """
        Lookup enum member by name.
        
        Args:
            enum_class: Enum type
            name: Member name
            
        Returns:
            Enum member or None
        """
        self.lookup_count += 1
        try:
            return enum_class[name]
        except KeyError:
            return None
    
    def lookup_by_value(self, enum_class: Type[Enum], value: Any) -> Optional[Enum]:
        """
        Lookup enum member by value.
        
        Args:
            enum_class: Enum type
            value: Member value
            
        Returns:
            Enum member or None
        """
        self.lookup_count += 1
        try:
            return enum_class(value)
        except ValueError:
            return None
    
    def is_member(self, obj: Any) -> bool:
        """
        Check if object is an enum member.
        
        Args:
            obj: Object to check
            
        Returns:
            True if enum member, False otherwise
        """
        return isinstance(obj, Enum)
    
    def get_name(self, member: Enum) -> str:
        """
        Get name of enum member.
        
        Args:
            member: Enum member
            
        Returns:
            Member name
        """
        return member.name
    
    def get_value(self, member: Enum) -> Any:
        """
        Get value of enum member.
        
        Args:
            member: Enum member
            
        Returns:
            Member value
        """
        return member.value
    
    def compare(self, member1: Enum, member2: Enum) -> bool:
        """
        Compare two enum members.
        
        Args:
            member1: First member
            member2: Second member
            
        Returns:
            True if equal, False otherwise
        """
        return member1 is member2
    
    def to_dict(self, enum_class: Type[Enum]) -> Dict[str, Any]:
        """
        Convert enum to dictionary.
        
        Args:
            enum_class: Enum type
            
        Returns:
            Dictionary of name->value
        """
        return {member.name: member.value for member in enum_class}
    
    def from_dict(self, name: str, data: Dict[str, Any]) -> Type:
        """
        Create enum from dictionary.
        
        Args:
            name: Enum name
            data: Dictionary of name->value
            
        Returns:
            New Enum type
        """
        return self.make(name, data, Enum)
    
    def extend(self,
               base_enum: Type[Enum],
               name: str,
               new_members: Dict[str, Any]) -> Type:
        """
        Create new enum extending existing enum.
        
        Args:
            base_enum: Base enum to extend
            name: New enum name
            new_members: New members to add
            
        Returns:
            New extended Enum type
        """
        # Get existing members
        existing = {member.name: member.value for member in base_enum}
        # Merge with new members
        all_members = {**existing, **new_members}
        return self.make(name, all_members, type(base_enum).__bases__[0])
    
    def has_member(self, enum_class: Type[Enum], name: str) -> bool:
        """
        Check if enum has member with name.
        
        Args:
            enum_class: Enum type
            name: Member name
            
        Returns:
            True if member exists, False otherwise
        """
        try:
            enum_class[name]
            return True
        except KeyError:
            return False
    
    def has_value(self, enum_class: Type[Enum], value: Any) -> bool:
        """
        Check if enum has member with value.
        
        Args:
            enum_class: Enum type
            value: Member value
            
        Returns:
            True if value exists, False otherwise
        """
        try:
            enum_class(value)
            return True
        except ValueError:
            return False
    
    def get_results(self) -> Dict[str, Any]:
        """Get processing results"""
        return {
            'enums_created': len(self.created_enums),
            'lookups_performed': self.lookup_count,
            'enum_names': [e.__name__ for e in self.created_enums]
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics"""
        return {
            'total_enums': len(self.created_enums),
            'total_lookups': self.lookup_count
        }
