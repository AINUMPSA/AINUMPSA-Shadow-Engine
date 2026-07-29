#!/usr/bin/env python3
"""
Generator assetów Shadow - JPG, GIF, MP4, VR
"""

from PIL import Image, ImageDraw, ImageFilter, ImageOps
import cv2
import numpy as np
from pathlib import Path
import logging
from typing import List, Dict
import subprocess
import json

logger = logging.getLogger(__name__)

class ShadowAssetGenerator:
    def __init__(self, engine):
        self.engine = engine
        self.config = engine.config
    
    def generate_jpg(self, points: List[Dict], output_path: str, size: int = 1024):
        img = self.engine.generate_preview(points, size)
        img.save(output_path, 'JPEG', quality=self.config.image_quality)
        logger.info(f"Wygenerowano JPG: {output_path}")
        return output_path
    
    def generate_gif(self, points: List[Dict], output_path: str, frames: int = 20, size: int = 512):
        images = []
        chunk_size = max(1, len(points) // frames)
        for i in range(frames):
            start = i * chunk_size
            end = min((i + 1) * chunk_size, len(points))
            chunk = points[start:end]
            frame = self.engine.generate_preview(chunk, size)
            if self.config.reverse_animation:
                frame = ImageOps.mirror(frame)
                frame = ImageOps.invert(frame)
            images.append(frame)
        if self.config.reverse_animation:
            images = images[::-1]
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
    
    def generate_mp4(self, points: List[Dict], output_path: str, duration: int = 10, size: int = 720):
        """Generuje MP4 z animacją"""
        fps = self.config.video_fps
        total_frames = duration * fps
        temp_dir = Path("/tmp/shadow_frames")
        temp_dir.mkdir(exist_ok=True)
        
        chunk_size = max(1, len(points) // total_frames)
        
        for i in range(total_frames):
            start = i * chunk_size
            end = min((i + 1) * chunk_size, len(points))
            chunk = points[start:end]
            frame = self.engine.generate_preview(chunk, size)
            if self.config.reverse_animation:
                frame = ImageOps.mirror(frame)
                frame = ImageOps.invert(frame)
            frame.save(temp_dir / f"frame_{i:04d}.jpg")
        
        # Użyj FFmpeg do stworzenia MP4
        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(fps),
            "-i", str(temp_dir / "frame_%04d.jpg"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            output_path
        ]
        subprocess.run(cmd, capture_output=True)
        
        # Wyczyść temp
        for f in temp_dir.glob("*.jpg"):
            f.unlink()
        temp_dir.rmdir()
        
        logger.info(f"Wygenerowano MP4: {output_path}")
        return output_path
    
    def generate_vr(self, points: List[Dict], output_path: str):
        """Generuje VR 360° (equirectangular)"""
        width, height = self.config.vr_resolution
        
        # Stwórz sferyczną mapę
        img = Image.new('RGB', (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        for point in points:
            # Konwersja na współrzędne sferyczne
            theta = point['x'] * 2 * np.pi
            phi = point['y'] * np.pi
            
            # Rzut na equirectangular
            u = (theta / (2 * np.pi)) * width
            v = (phi / np.pi) * height
            
            color = (int(point['r']), int(point['g']), int(point['b']))
            radius = int(abs(point['attractor']) * 2) + 1
            radius = min(radius, 10)
            
            draw.ellipse(
                [u-radius, v-radius, u+radius, v+radius],
                fill=color
            )
        
        # Dodaj efekt VR
        img = img.filter(ImageFilter.GaussianBlur(radius=1))
        img = ImageOps.autocontrast(img, cutoff=3)
        
        img.save(output_path)
        logger.info(f"Wygenerowano VR: {output_path}")
        return output_path
    
    def generate_all(self, points: List[Dict], output_dir: str, base_name: str = "shadow"):
        """Generuje wszystkie formaty"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # JPG
        self.generate_jpg(points, output_path / f"{base_name}.jpg")
        
        # GIF
        self.generate_gif(points, output_path / f"{base_name}.gif")
        
        # MP4
        self.generate_mp4(points, output_path / f"{base_name}.mp4")
        
        # VR
        self.generate_vr(points, output_path / f"{base_name}_vr.jpg")
        
        # JSON metadanych
        metadata = {
            "name": f"SHADOW #{base_name}",
            "description": "Lustrzane odbicie głównego silnika rezonansu",
            "image": f"{base_name}.jpg",
            "animation_url": f"{base_name}.mp4",
            "attributes": [
                {"trait_type": "Points", "value": len(points)},
                {"trait_type": "Time Travel", "value": str(self.config.time_travel)},
                {"trait_type": "Wallet", "value": self.config.wallet}
            ]
        }
        
        with open(output_path / f"{base_name}.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Wygenerowano wszystkie assety w: {output_dir}")
        return output_path
