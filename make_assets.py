import wave
import math
import struct
import os
from PIL import Image, ImageDraw

# mappa 
if not os.path.exists('resources'):
    os.makedirs('resources')

# kepek generalasa
def create_rect(color, filename):
    img = Image.new('RGBA', (20, 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 19, 19], fill=color, outline=(0,0,0))
    img.save(f'resources/{filename}')

def create_apple():
    img = Image.new('RGBA', (20, 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([1, 1, 18, 18], fill=(255, 50, 50), outline=(100, 0, 0))
    draw.line([10, 1, 10, 5], fill=(0, 255, 0), width=2)
    img.save('resources/apple.png')

def create_head():
    img = Image.new('RGBA', (20, 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 19, 19], fill=(0, 200, 0), outline=(0,100,0))
    draw.rectangle([2, 4, 18, 8], fill=(0, 0, 0)) 
    draw.line([20, 10, 24, 10], fill=(255, 0, 0), width=2)
    img.save('resources/head.png')

# hangok generalasa
def create_sound(filename, frequency, duration, volume=0.5, type='sine'):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    
    with wave.open(f'resources/{filename}', 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(n_samples):
            t = i / sample_rate
            if type == 'sine':
                value = int(volume * 32767.0 * math.sin(2.0 * math.pi * frequency * t))
            elif type == 'noise':
                import random
                value = int(volume * 32767.0 * (random.random()*2-1))
            elif type == 'saw':
                value = int(volume * 32767.0 * (2 * (t * frequency - math.floor(t * frequency + 0.5))))
            
            # Decay
            value = int(value * (1 - i/n_samples))
            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)

print("Generálás folyamatban...")

# kepek
try:
    create_rect((0, 255, 0), 'body.png')
    create_apple()
    create_head()
    print("- Képek OK")
except ImportError:
    print("HIBA: Kell a Pillow! (pip install Pillow)")

# hangok
try:
    create_sound('eat.wav', 880, 0.1, type='sine') # high pitch
    create_sound('die.wav', 100, 0.5, type='saw')  # low pitch
    print("- Hangok OK")
except Exception as e:
    print(f"HIBA a hangoknál: {e}")