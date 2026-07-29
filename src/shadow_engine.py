#!/usr/bin/env python3
"""
AINUMPSA – SHADOW ENGINE
Lustrzane odbicie głównego silnika rezonansu.
"""

import json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import cv2
from pathlib import Path
import hashlib
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple, Any, Optional
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[SHADOW] %(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ShadowEngine:
    def __init__(self, config):
        self.config = config
        self.data = None
        self.transform_history = []
        
    def load_data(self, input_path: str) -> Dict:
        logger.info(f"Ładowanie danych z: {input_path}")
        try:
            input_dir = Path(input_path)
            json_files = list(input_dir.glob("*.json"))
            if not json_files:
                raise FileNotFoundError(f"Brak plików JSON w {input_path}")
            latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
            with open(latest_file, 'r') as f:
                self.data = json.load(f)
            logger.info(f"Załadowano {len(self.data)} punktów NEO")
            return self.data
        except Exception as e:
            logger.error(f"Błąd ładowania danych: {e}")
            self.data = self._generate_test_data()
            return self.data
    
    def _generate_test_data(self) -> Dict:
        logger.warning("Generowanie testowych danych NEO...")
        points = []
        for i in range(100):
            points.append({
                'x': random.random(),
                'y': random.random(),
                'z': random.random(),
                'r': random.randint(0, 255),
                'g': random.randint(0, 255),
                'b': random.randint(0, 255),
                'angle': random.uniform(-180, 180),
                'attractor': random.uniform(0.1, 3.0),
                'intensity': random.uniform(0.0, 1.0),
                'timestamp': datetime.now().isoformat()
            })
        return {'points': points, 'meta': {'version': 'shadow_test'}}
    
    def transform_point(self, point: Dict) -> Dict:
        transformed = point.copy()
        if self.config.invert_colors:
            transformed['r'] = 255 - point['r']
            transformed['g'] = 255 - point['g']
            transformed['b'] = 255 - point['b']
        if self.config.mirror_x:
            transformed['x'] = 1 - point['x']
        if self.config.mirror_y:
            transformed['y'] = 1 - point['y']
        transformed['angle'] = -point['angle']
        if self.config.attractor_inversion:
            attr = point['attractor']
            if abs(attr) < 0.001:
                transformed['attractor'] = 1000.0
            else:
                transformed['attractor'] = 1.0 / attr
        transformed['intensity'] = 1 - point['intensity']
        transformed['shadow_timestamp'] = self._shadow_time()
        transformed['shadow_hash'] = self._generate_hash(transformed)
        return transformed
    
    def _shadow_time(self) -> str:
        if not self.config.time_travel:
            return datetime.now().isoformat()
        offset = random.randint(
            self.config.time_offset_min,
            self.config.time_offset_max
        )
        shadow_time = datetime.now() - timedelta(seconds=offset)
        return shadow_time.isoformat()
    
    def _generate_hash(self, data: Dict) -> str:
        content = json.dumps(data, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def process_all(self) -> Dict:
        if not self.data or 'points' not in self.data:
            self.load_data(self.config.core_input)
        
        logger.info(f"Przetwarzanie {len(self.data['points'])} punktów...")
        shadow_points = []
        for point in self.data['points']:
            shadow_point = self.transform_point(point)
            shadow_points.append(shadow_point)
        
        result = {
            'shadow_points': shadow_points,
            'meta': {
                'original': self.data.get('meta', {}),
                'shadow_engine': {
                    'version': '1.0.0',
                    'timestamp': self._shadow_time(),
                    'transformations': {
                        'invert_colors': self.config.invert_colors,
                        'mirror_x': self.config.mirror_x,
                        'mirror_y': self.config.mirror_y,
                        'reverse_animation': self.config.reverse_animation,
                        'attractor_inversion': self.config.attractor_inversion
                    }
                },
                'wallet': self.config.wallet,
                'total_points': len(shadow_points)
            }
        }
        
        self.transform_history.append({
            'timestamp': datetime.now().isoformat(),
            'points': len(shadow_points),
            'hash': self._generate_hash(result)
        })
        
        return result
    
    def save_shadow_data(self, result: Dict, output_path: str):
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        if self.config.time_travel:
            timestamp = result['meta']['shadow_engine']['timestamp'].replace(':', '-')
            filename = f"shadow_neo_{timestamp}.json"
        else:
            filename = "shadow_neo_latest.json"
        filepath = output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(result, f, indent=2)
        logger.info(f"Zapisano dane Shadow: {filepath}")
        return filepath
    
    def generate_preview(self, points: List[Dict], size: int = 1024) -> Image.Image:
        img = Image.new('RGB', (size, size), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        for point in points:
            x = int(point['x'] * size)
            y = int(point['y'] * size)
            color = (int(point['r']), int(point['g']), int(point['b']))
            radius = int(abs(point['attractor']) * 3) + 1
            radius = min(radius, 20)
            draw.ellipse(
                [x-radius, y-radius, x+radius, y+radius],
                fill=color
            )
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        img = ImageOps.autocontrast(img, cutoff=5)
        return img
