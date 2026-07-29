"""
Time Travel Module - Symulacja podróży w czasie
"""

from datetime import datetime, timedelta
import random
import hashlib
import json
from typing import Dict, List

class TimeTravel:
    def __init__(self, engine):
        self.engine = engine
        self.config = engine.config
        self.timeline = []
    
    def warp_backward(self, base_time: datetime, intensity: float = 1.0) -> datetime:
        """Przenosi w przeszłość z zadaną intensywnością"""
        if not self.config.time_travel:
            return base_time
        
        max_offset = self.config.time_offset_max * intensity
        min_offset = self.config.time_offset_min * intensity
        
        offset = random.randint(int(min_offset), int(max_offset))
        warped_time = base_time - timedelta(seconds=offset)
        
        self.timeline.append({
            "original": base_time.isoformat(),
            "warped": warped_time.isoformat(),
            "offset_seconds": offset,
            "intensity": intensity
        })
        
        return warped_time
    
    def create_timeline_hash(self, data: Dict) -> str:
        """Tworzy hash osadzony w czasie"""
        content = json.dumps(data, sort_keys=True) + datetime.now().isoformat()
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def is_paradox(self, data: Dict) -> bool:
        """Sprawdza czy dane nie tworzą paradoksu czasowego"""
        # Wersja prosta - można rozbudować
        if 'shadow_timestamp' not in data:
            return False
        
        shadow_time = datetime.fromisoformat(data['shadow_timestamp'])
        now = datetime.now()
        
        # Jeśli cień jest z przyszłości -> paradoks
        if shadow_time > now:
            return True
        
        # Jeśli cień jest zbyt stary (>100 lat) -> paradoks
        if (now - shadow_time).days > 36500:
            return True
        
        return False
    
    def get_timeline_status(self) -> Dict:
        """Zwraca status osi czasu"""
        return {
            "total_jumps": len(self.timeline),
            "last_jump": self.timeline[-1] if self.timeline else None,
            "time_paradox_detected": any(
                self.is_paradox(t) for t in self.timeline
            ) if self.timeline else False
        }
