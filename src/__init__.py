import json
import hashlib
from pathlib import Path
from typing import Union, Dict, Any

class FileHandler:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
    
    def read_json(self, filename: str) -> Dict[str, Any]:
        path = self.base_path / filename
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def write_json(self, filename: str, data: Dict[str, Any]) -> None:
        path = self.base_path / filename
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def get_hash(self, filename: str) -> str:
        path = self.base_path / filename
        sha256 = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

class ConfigLoader:
    def __init__(self, config_file: str = "config.json"):
        self.handler = FileHandler()
        self.config_file = config_file
        self._config = None
    
    @property
    def config(self) -> Dict[str, Any]:
        if self._config is None:
            self._config = self.handler.read_json(self.config_file)
        return self._config
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)