import tkinter as tk
from tkinter import filedialog, ttk
import os
import whisperx
import time
import threading
import sys
from pathlib import Path

def get_ffmpeg_path():
    """
    Determine the path to ffmpeg.exe.
    If running as a bundled executable, it will be extracted to a temporary folder (sys._MEIPASS).
    Otherwise, it is expected to be in the "resources" subfolder relative to this script.
    """
    if getattr(sys, 'frozen', False):  # Running as compiled executable
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "resources", "ffmpeg.exe")

def check_ffmpeg():
    """
    Check if ffmpeg.exe exists at the expected location.
    """
    ffmpeg_path = get_ffmpeg_path()
    if not os.path.exists(ffmpeg_path):
        print(f"Error: ffmpeg.exe not found at {ffmpeg_path}. Please ensure it is included and in the proper location.")
        sys.exit(1)

def format_timestamp(seconds: float) -> str:
    """
    Convert seconds (float) into an [HH:MM] timestamp string.
    For example, 300 seconds becomes "[00:05]".
    """
    minutes, _ = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"[{int(hours):02d}:{int(minutes):02d}]"

class TranscriptionThread(threading.Thread):
    """
    This thread performs transcription in the background so the GUI stays responsive.
    """
    def __init__(self, file_path, progress_callback, completion_callback):
        super().__init__()
        self.file_path = file_path
        self.progress_callback = progress_callback
        self.completion_callback = completion_callback

    def run(self):
        try:
            start_time = time.time()
            
            # Load the WhisperX model (tiny.en) using CPU with int8 compute type.
            model = whisperx.load_model(
                "tiny.en",
                device="cpu",
                compute_type="int8",
                language="en"
            )

            # Load audio and compute its duration (assuming 16kHz sample rate)
            audio = whisperx.load_audio(self.file_path)
            sample_rate = 16000
            duration = len(audio) / sample_rate

            # Generate timestamps every 5 minutes (300 seconds)
            timestamps = []
            current = 300  # Starting at 5 minutes
            while current <= duration:
                timestamps.append(current)
                current += 300

            # Transcribe the audio; result has a 'segments' list with 'start' and 'text' keys.
            result = model.transcribe(audio, batch_size=8)
            segments = result['segments']

            # Build output text with inserted timestamps.
            output = []
            timestamp_index = 0
            segment_index = 0

            # (Optional) Insert an initial timestamp if you want one at time 0.
            if timestamps and timestamps[0] == 0:
                output.append(f"{format_timestamp(0)}\n")
                timestamp_index += 1

            while segment_index < len(segments) and timestamp_index < len(timestamps):
                seg_start = segments[segment_index]['start']
                if seg_start >= timestamps[timestamp_index]:
                    # Insert a timestamp on its own line before this segment.
                    output.append(f"\n{format_timestamp(timestamps[timestamp_index])}\n")
                    timestamp_index += 1
                else:
                    # Append the segment text.
                    output.append(segments[segment_index]['text'] + " ")
                    segment_index += 1
                    self.progress_callback(segment_index / len(segments))
                    
            # Append any remaining segments.
            while segment_index < len(segments):
                output.append(segments[segment_index]['text'] + " ")
                segment_index += 1
                self.progress_callback(segment_index / len(segments))

            # Append any leftover timestamps after the last segment.
            while timestamp_index < len(timestamps):
                output.append(f"\n{format_timestamp(timestamps[timestamp_index])}\n")
                timestamp_index += 1

            # Save the transcript to a file with _transcript appended to the original file name.
            base = os.path.splitext(self.file_path)[0]
            output_path = f"{base}_transcript.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("".join(output).strip())

            self.completion_callback(True, output_path, time.time() - start_time)

        except Exception as e:
            self.completion_callback(False, str(e), 0)

def transcribe_audio():
    def select_file():
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio files", "*.mp3 *.wav *.flac *.ogg *.m4a")]
        )
        if file_path:
            start_processing(file_path)

    def start_processing(file_path):
        progress_bar.start()
        status_label.config(text="Processing...", fg="black")
        
        def completion_handler(success, result, processing_time):
            progress_bar.stop()
            if success:
                status_label.config(
                    text=f"Success! Transcript saved to:\n{result}\nProcessing time: {processing_time:.1f}s",
                    fg="darkgreen"
                )
            else:
                status_label.config(text=f"Error: {result}", fg="red")

        # Start transcription in a separate thread to keep the GUI responsive.
        thread = TranscriptionThread(
            file_path,
            lambda p: root.after(50, update_progress, p),
            lambda s, r, t: root.after(50, completion_handler, s, r, t)
        )
        thread.start()

    def update_progress(value):
        progress_bar['value'] = value * 100

    # Build the Tkinter GUI.
    global root, progress_bar, status_label
    root = tk.Tk()
    root.title("Audio Transcriber")
    root.geometry("500x300")

    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(expand=True, fill="both")

    select_button = ttk.Button(
        main_frame,
        text="Select Audio File",
        command=select_file
    )
    select_button.pack(pady=10)

    progress_bar = ttk.Progressbar(
        main_frame,
        orient="horizontal",
        length=300,
        mode="determinate"
    )
    progress_bar.pack(pady=10)

    status_label = tk.Label(
        main_frame,
        text="Select an audio file to begin transcription",
        wraplength=400,
        justify="center",
        fg="gray50"
    )
    status_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    check_ffmpeg()  # Check for ffmpeg.exe before starting the application
    transcribe_audio()
