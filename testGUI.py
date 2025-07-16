import tkinter as tk
import math
import numpy as np
import sounddevice as sd

# Set this to the index of your "Stereo Mix" or system audio input
DEVICE_INDEX = 34  # Make sure this matches your working input device

class SystemAudioVisualizer:
    def __init__(self, root, num_segments=60, radius=100, max_push=40):
        self.root = root
        self.num_segments = num_segments
        self.radius = radius
        self.max_push = max_push
        self.canvas_size = (radius + max_push + 20) * 2

        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg='black', highlightthickness=0)
        self.canvas.pack()

        self.center = self.canvas_size / 2
        self.segments = []
        self.audio_levels = np.zeros(num_segments)

        for i in range(num_segments):
            angle = 2 * math.pi * i / num_segments
            seg = self.canvas.create_line(0, 0, 0, 0, fill='cyan', width=3, capstyle=tk.ROUND)
            self.segments.append((seg, angle))

        # Use stereo input (2 channels)
        self.stream = sd.InputStream(
            device=DEVICE_INDEX,
            channels=2,
            samplerate=44100,
            blocksize=1024,
            callback=self.audio_callback
        )
        self.stream.start()

        self.animate()

    def audio_callback(self, indata, frames, time, status):
        # Average both stereo channels
        volume = np.linalg.norm(indata, axis=1)
        avg_volume = np.mean(volume)

        # Boost sensitivity and decay
        self.audio_levels *= 0.9
        for _ in range(3):
            idx = np.random.randint(0, self.num_segments)
            self.audio_levels[idx] = min(1.0, avg_volume * 50)  # Adjust multiplier if needed

    def animate(self):
        for i, (seg, angle) in enumerate(self.segments):
            push = self.audio_levels[i] * self.max_push
            x0 = self.center + self.radius * math.cos(angle)
            y0 = self.center + self.radius * math.sin(angle)
            x1 = self.center + (self.radius + push) * math.cos(angle)
            y1 = self.center + (self.radius + push) * math.sin(angle)
            self.canvas.coords(seg, x0, y0, x1, y1)

        self.root.after(30, self.animate)

# Create the window
root = tk.Tk()
root.title("System Audio Visualizer")
root.resizable(False, False)
root.configure(bg='black')

app = SystemAudioVisualizer(root)
root.mainloop()