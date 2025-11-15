"""PathFinder - Path utility

Path handler for development tasks.
Wrapper around Python's pathlib module with enhanced functionality.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Iterator
import os
import shutil


class PathFinder:
    """
    PathFinder: Path handler
    
    Provides utilities to handle file paths and operations.
    """
    
    def __init__(self):
        """Initialize PathFinder"""
        self.operations = []
        self.operation_count = 0
    
    def path(self, *args) -> Path:
        """
        Create a Path object.
        
        Args:
            *args: Path components
            
        Returns:
            Path object
        """
        return Path(*args)
    
    def join(self, *parts: Union[str, Path]) -> Path:
        """
        Join path components.
        
        Args:
            *parts: Path parts to join
            
        Returns:
            Joined Path object
        """
        result = Path(parts[0])
        for part in parts[1:]:
            result = result / part
        self.operation_count += 1
        return result
    
    def exists(self, path: Union[str, Path]) -> bool:
        """Check if path exists"""
        return Path(path).exists()
    
    def is_file(self, path: Union[str, Path]) -> bool:
        """Check if path is a file"""
        return Path(path).is_file()
    
    def is_dir(self, path: Union[str, Path]) -> bool:
        """Check if path is a directory"""
        return Path(path).is_dir()
    
    def is_absolute(self, path: Union[str, Path]) -> bool:
        """Check if path is absolute"""
        return Path(path).is_absolute()
    
    def absolute(self, path: Union[str, Path]) -> Path:
        """Get absolute path"""
        return Path(path).absolute()
    
    def resolve(self, path: Union[str, Path]) -> Path:
        """Resolve path (make absolute and resolve symlinks)"""
        return Path(path).resolve()
    
    def parent(self, path: Union[str, Path]) -> Path:
        """Get parent directory"""
        return Path(path).parent
    
    def name(self, path: Union[str, Path]) -> str:
        """Get file/directory name"""
        return Path(path).name
    
    def stem(self, path: Union[str, Path]) -> str:
        """Get file name without extension"""
        return Path(path).stem
    
    def suffix(self, path: Union[str, Path]) -> str:
        """Get file extension"""
        return Path(path).suffix
    
    def suffixes(self, path: Union[str, Path]) -> List[str]:
        """Get all file extensions"""
        return Path(path).suffixes
    
    def parts(self, path: Union[str, Path]) -> tuple:
        """Get path components as tuple"""
        return Path(path).parts
    
    def mkdir(self, 
              path: Union[str, Path], 
              parents: bool = False,
              exist_ok: bool = False):
        """
        Create directory.
        
        Args:
            path: Directory path
            parents: Create parent directories if needed
            exist_ok: Don't raise error if directory exists
        """
        Path(path).mkdir(parents=parents, exist_ok=exist_ok)
        self.operations.append(('mkdir', str(path)))
        self.operation_count += 1
    
    def touch(self, path: Union[str, Path], exist_ok: bool = True):
        """
        Create empty file.
        
        Args:
            path: File path
            exist_ok: Don't raise error if file exists
        """
        Path(path).touch(exist_ok=exist_ok)
        self.operations.append(('touch', str(path)))
        self.operation_count += 1
    
    def unlink(self, path: Union[str, Path], missing_ok: bool = False):
        """
        Remove file.
        
        Args:
            path: File path
            missing_ok: Don't raise error if file doesn't exist
        """
        Path(path).unlink(missing_ok=missing_ok)
        self.operations.append(('unlink', str(path)))
        self.operation_count += 1
    
    def rmdir(self, path: Union[str, Path]):
        """Remove empty directory"""
        Path(path).rmdir()
        self.operations.append(('rmdir', str(path)))
        self.operation_count += 1
    
    def rename(self, path: Union[str, Path], target: Union[str, Path]) -> Path:
        """
        Rename file or directory.
        
        Args:
            path: Source path
            target: Target path
            
        Returns:
            New Path object
        """
        result = Path(path).rename(target)
        self.operations.append(('rename', f"{path} -> {target}"))
        self.operation_count += 1
        return result
    
    def replace(self, path: Union[str, Path], target: Union[str, Path]) -> Path:
        """
        Replace file or directory (overwrite if exists).
        
        Args:
            path: Source path
            target: Target path
            
        Returns:
            New Path object
        """
        result = Path(path).replace(target)
        self.operations.append(('replace', f"{path} -> {target}"))
        self.operation_count += 1
        return result
    
    def copy(self, src: Union[str, Path], dst: Union[str, Path]):
        """
        Copy file.
        
        Args:
            src: Source file path
            dst: Destination path
        """
        shutil.copy2(src, dst)
        self.operations.append(('copy', f"{src} -> {dst}"))
        self.operation_count += 1
    
    def copytree(self, src: Union[str, Path], dst: Union[str, Path]):
        """
        Copy directory tree.
        
        Args:
            src: Source directory path
            dst: Destination path
        """
        shutil.copytree(src, dst)
        self.operations.append(('copytree', f"{src} -> {dst}"))
        self.operation_count += 1
    
    def move(self, src: Union[str, Path], dst: Union[str, Path]):
        """
        Move file or directory.
        
        Args:
            src: Source path
            dst: Destination path
        """
        shutil.move(src, dst)
        self.operations.append(('move', f"{src} -> {dst}"))
        self.operation_count += 1
    
    def listdir(self, path: Union[str, Path] = '.') -> List[str]:
        """
        List directory contents.
        
        Args:
            path: Directory path
            
        Returns:
            List of names
        """
        return [p.name for p in Path(path).iterdir()]
    
    def glob(self, path: Union[str, Path], pattern: str) -> List[Path]:
        """
        Find files matching pattern.
        
        Args:
            path: Directory path
            pattern: Glob pattern
            
        Returns:
            List of matching paths
        """
        return list(Path(path).glob(pattern))
    
    def rglob(self, path: Union[str, Path], pattern: str) -> List[Path]:
        """
        Recursively find files matching pattern.
        
        Args:
            path: Directory path
            pattern: Glob pattern
            
        Returns:
            List of matching paths
        """
        return list(Path(path).rglob(pattern))
    
    def walk(self, path: Union[str, Path]) -> Iterator[tuple]:
        """
        Walk directory tree (like os.walk).
        
        Args:
            path: Directory path
            
        Yields:
            Tuples of (dirpath, dirnames, filenames)
        """
        for root, dirs, files in os.walk(path):
            yield (root, dirs, files)
    
    def read_text(self, path: Union[str, Path], encoding: str = 'utf-8') -> str:
        """
        Read text file.
        
        Args:
            path: File path
            encoding: Text encoding
            
        Returns:
            File contents
        """
        return Path(path).read_text(encoding=encoding)
    
    def read_bytes(self, path: Union[str, Path]) -> bytes:
        """
        Read binary file.
        
        Args:
            path: File path
            
        Returns:
            File contents
        """
        return Path(path).read_bytes()
    
    def write_text(self, 
                   path: Union[str, Path], 
                   data: str,
                   encoding: str = 'utf-8'):
        """
        Write text file.
        
        Args:
            path: File path
            data: Text data
            encoding: Text encoding
        """
        Path(path).write_text(data, encoding=encoding)
        self.operations.append(('write_text', str(path)))
        self.operation_count += 1
    
    def write_bytes(self, path: Union[str, Path], data: bytes):
        """
        Write binary file.
        
        Args:
            path: File path
            data: Binary data
        """
        Path(path).write_bytes(data)
        self.operations.append(('write_bytes', str(path)))
        self.operation_count += 1
    
    def size(self, path: Union[str, Path]) -> int:
        """Get file size in bytes"""
        return Path(path).stat().st_size
    
    def mtime(self, path: Union[str, Path]) -> float:
        """Get modification time"""
        return Path(path).stat().st_mtime
    
    def cwd(self) -> Path:
        """Get current working directory"""
        return Path.cwd()
    
    def home(self) -> Path:
        """Get user home directory"""
        return Path.home()
    
    def expanduser(self, path: Union[str, Path]) -> Path:
        """Expand ~ in path"""
        return Path(path).expanduser()
    
    def get_results(self) -> Dict[str, Any]:
        """Get processing results"""
        return {
            'operations_performed': self.operation_count,
            'recent_operations': self.operations[-10:]  # Last 10 operations
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics"""
        operation_types = {}
        for op_type, _ in self.operations:
            operation_types[op_type] = operation_types.get(op_type, 0) + 1
        
        return {
            'total_operations': self.operation_count,
            'operation_types': operation_types
        }
    
    def clear_history(self):
        """Clear operation history"""
        self.operations.clear()
        self.operation_count = 0
