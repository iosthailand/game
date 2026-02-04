import wave
import struct
import math
import os

def generate_beep(filename, freq=440, duration=0.1, volume=0.5):
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with wave.open(filename, 'w') as f:
        f.setnchannels(1) # Mono
        f.setsampwidth(2) # 2 bytes per sample
        f.setframerate(sample_rate)
        
        for i in range(num_samples):
            # Simple sine wave with decay
            decay = 1.0 - (i / num_samples)
            value = int(volume * decay * 32767.0 * math.sin(2.0 * math.pi * freq * i / sample_rate))
            data = struct.pack('<h', value)
            f.writeframesraw(data)

if __name__ == "__main__":
    audio_dir = os.path.join(os.path.dirname(__file__), 'assets', 'audio')
    
    # Shoot: High-to-low frequency sweep
    generate_beep(os.path.join(audio_dir, 'shoot.wav'), freq=880, duration=0.15)
    
    # Hit: Low-pitch thud
    generate_beep(os.path.join(audio_dir, 'hit.wav'), freq=220, duration=0.2)
    
    print("Sounds generated in assets/audio/")
