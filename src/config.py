import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class ShadowConfig:
    """Konfiguracja Shadow Engine"""
    
    core_input: str = "../core/output/latest"
    shadow_output: str = "./output"
    data_path: str = "./data/shadow_neo_points.json"
    wallet: str = "0x8e504ebd3f1eaa45df87d398b7cbcb823592b324"
    
    invert_colors: bool = True
    mirror_x: bool = True
    mirror_y: bool = False
    reverse_animation: bool = True
    attractor_inversion: bool = True
    
    time_travel: bool = True
    time_offset_min: int = 3600
    time_offset_max: int = 86400
    
    image_quality: int = 95
    video_fps: int = 30
    vr_resolution: tuple = (4096, 2048)
    
    @classmethod
    def from_env(cls):
        return cls(
            core_input=os.getenv("CORE_INPUT", cls.core_input),
            shadow_output=os.getenv("SHADOW_OUTPUT", cls.shadow_output),
            wallet=os.getenv("WALLET", cls.wallet),
            time_travel=os.getenv("TIME_TRAVEL", "true").lower() == "true"
        )

config = ShadowConfig()
