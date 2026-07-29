#!/usr/bin/env python3
"""
AINUMPSA – SHADOW ENGINE
Lustrzane odbicie głównego silnika rezonansu.
Odwraca wartości NEO: kolory, kąty, atraktory, geometrię.
"""

import json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import cv2
from pathlib import Path
import shutil
import hashlib
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple, Any, Optional
import logging

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='[SHADOW] %(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ShadowEngine:
    """
    Główny silnik transformacji Shadow.
    Przetwarza dane NEO i generuje odwrócone wizualizacje.
    """
    
    def __init__(self, config):
        self.config = config
        self.data = None
        self.transform_history = []
        
    def load_data(self, input_path: str) -> Dict:
        """Ładuje dane NEO z Core repo"""
        logger.info(f"Ładowanie danych z: {input_path}")
        
        try:
            # Szukaj najnowszych danych
            input_dir = Path(input_path)
            
            # Obsługa różnych formatów wejściowych
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
            # Fallback: wygeneruj testowe dane
            self.data = self._generate_test_data()
            return self.data
    
    def _generate_test_data(self) -> Dict:
        """Generuje testowe dane NEO jeśli brak wejścia"""
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
        """
        ODWROCONA TRANSFORMACJA NEO
        Lustrzane odbicie każdego parametru
        """
        transformed = point.copy()
        
        # 1. ODWROCONE KOLORY
        if self.config.invert_colors:
            transformed['r'] = 255 - point['r']
            transformed['g'] = 255 - point['g']
            transformed['b'] = 255 - point['b']
        
        # 2. ODWROCONA GEOMETRIA (lustro)
        if self.config.mirror_x:
            transformed['x'] = 1 - point['x']
        if self.config.mirror_y:
            transformed['y'] = 1 - point['y']
        
        # 3. ODWROCONY KĄT
        transformed['angle'] = -point['angle']
        
        # 4. ODWROCONY ATRAKTOR (1/x z zabezpieczeniem)
        if self.config.attractor_inversion:
            attr = point['attractor']
            if abs(attr) < 0.001:
                transformed['attractor'] = 1000.0
            else:
                transformed['attractor'] = 1.0 / attr
        
        # 5. ODWROCONA INTENSYWNOŚĆ
        transformed['intensity'] = 1 - point['intensity']
        
        # Dodaj znacznik shadow
        transformed['shadow_timestamp'] = self._shadow_time()
        transformed['shadow_hash'] = self._generate_hash(transformed)
        
        return transformed
    
    def _shadow_time(self) -> str:
        """Cofnięty czas - symulacja podróży w przeszłość"""
        if not self.config.time_travel:
            return datetime.now().isoformat()
        
        offset = random.randint(
            self.config.time_offset_min,
            self.config.time_offset_max
        )
        shadow_time = datetime.now() - timedelta(seconds=offset)
        return shadow_time.isoformat()
    
    def _generate_hash(self, data: Dict) -> str:
        """Generuje unikalny hash dla transformacji"""
        content = json.dumps(data, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def process_all(self) -> Dict:
        """Przetwarza wszystkie punkty NEO na Shadow"""
        if not self.data or 'points' not in self.data:
            self.load_data(self.config.core_input)
        
        logger.info(f"Przetwarzanie {len(self.data['points'])} punktów...")
        
        shadow_points = []
        for point in self.data['points']:
            shadow_point = self.transform_point(point)
            shadow_points.append(shadow_point)
        
        # Zbuduj wynik
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
        """Zapisuje przetworzone dane Shadow"""
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Nazwa pliku z cofniętym czasem
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
        """Generuje podgląd wizualizacji Shadow"""
        img = Image.new('RGB', (size, size), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        for point in points:
            # Współrzędne
            x = int(point['x'] * size)
            y = int(point['y'] * size)
            
            # Kolor (odwrócony już w transform)
            color = (
                int(point['r']),
                int(point['g']),
                int(point['b'])
            )
            
            # Rozmiar punktu (od atraktora)
            radius = int(abs(point['attractor']) * 3) + 1
            radius = min(radius, 20)  # limit
            
            draw.ellipse(
                [x-radius, y-radius, x+radius, y+radius],
                fill=color
            )
        
        # Dodaj efekt poświaty dla stylu Shadow
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        img = ImageOps.autocontrast(img, cutoff=5)
        
        return img

# ============================================
# INTERFEJS WIZUALNY – GENEROWANIE ASSETÓW
# ============================================

class ShadowAssetGenerator:
    """Generuje JPG, GIF, MP4, VR z danych Shadow"""
    
    def __init__(self, engine: ShadowEngine):
        self.engine = engine
        self.config = engine.config
    
    def generate_jpg(self, points: List[Dict], output_path: str, size: int = 1024):
        """Generuje obraz JPG"""
        img = self.engine.generate_preview(points, size)
        img.save(output_path, 'JPEG', quality=self.config.image_quality)
        logger.info(f"Wygenerowano JPG: {output_path}")
        return output_path
    
    def generate_gif(self, points: List[Dict], output_path: str, 
                     frames: int = 20, size: int = 512):
        """Generuje animowany GIF z odwróconą sekwencją"""
        images = []
        
        # Podziel punkty na klatki
        chunk_size = max(1, len(points) // frames)
        
        for i in range(frames):
            start = i * chunk_size
            end = min((i + 1) * chunk_size, len(points))
            chunk = points[start:end]
            
            # Generuj klatkę
            frame = self.engine.generate_preview(chunk, size)
            
            # Odwróć klatkę dla efektu "cofania"
            if self.config.reverse_animation:
                frame = ImageOps.mirror(frame)
                frame = ImageOps.invert(frame)
            
            images.append(frame)
        
        # Zapisz GIF z animacją wstecz
        if self.config.reverse_animation:
            images = images[::-1]  # Odtwarzanie od tyłu
        
        images[0].save(
            output_path,
            save_all=True,
            append_images=images[1:],
            duration=100,
            loop=0,
            optimize=True
        )
        logger.info(f"Wygenerowano GIF: {output_path}")
        return output_path
    
    def
