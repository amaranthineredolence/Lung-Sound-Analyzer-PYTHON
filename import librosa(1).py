import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy import signal
import simpleaudio as sa

# Initialize Tkinter app
app = tk.Tk()
app.title("Audio Processing App")

# Global variables
sample_rate = 0
audio_data = np.array([])
filtered_audio_data = np.array([])
effected_audio_data = np.array([])
is_filtered = False
is_effected = False

# Function to open a sound file
def open_file():
    global sample_rate, audio_data, is_filtered, is_effected
    
    file_path = filedialog.askopenfilename(filetypes=[("Wave files", "*.wav")])
    if file_path:
        sample_rate, audio_data = wavfile.read(file_path)
        audio_data = audio_data[:, 0]  # Select the first channel if it's a stereo file
        is_filtered = False
        is_effected = False
        
        # Clear the previous graph, if any
        plt.clf()
        
        # Plot the waveform
        plt.plot(audio_data)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Audio Waveform')
        plt.show()

# Function to apply audio filters
def apply_filters():
    global filtered_audio_data, is_filtered, is_effected
    
    # Apply the filters to the audio data
    # Replace this with your own implementation of filtering
    
    # Design the filter
    filter_type = "lowpass"  # Replace with the desired filter type: lowpass, highpass, bandpass, or notch
    cutoff_freq = 2000  # Replace with the desired cutoff frequency in Hz
    filter_order = 4  # Replace with the desired filter order
    
    # Normalize the cutoff frequency
    normalized_cutoff_freq = 2 * cutoff_freq / sample_rate
    
    # Apply the selected filter
    if filter_type == "lowpass":
        b, a = signal.butter(filter_order, normalized_cutoff_freq, btype="lowpass", analog=False)
    elif filter_type == "highpass":
        b, a = signal.butter(filter_order, normalized_cutoff_freq, btype="highpass", analog=False)
    elif filter_type == "bandpass":
        # Replace with the desired bandpass parameters
        lower_cutoff = 1000
        upper_cutoff = 4000
        normalized_lower_cutoff = 2 * lower_cutoff / sample_rate
        normalized_upper_cutoff = 2 * upper_cutoff / sample_rate
        b, a = signal.butter(filter_order, [normalized_lower_cutoff, normalized_upper_cutoff], btype="bandpass", analog=False)
    elif filter_type == "notch":
        # Replace with the desired notch filter parameters
        notch_freq = 3000
        normalized_notch_freq = 2 * notch_freq / sample_rate
        b, a = signal.iirnotch(normalized_notch_freq, Q=1)
    else:
        print("Invalid filter type.")
        return
    
    # Apply the filter to the audio data
    filtered_audio_data = signal.lfilter(b, a, audio_data)
    is_filtered = True
    is_effected = False
    
    # Clear the previous graph, if any
    plt.clf()
    
    # Plot the processed waveform
    plt.plot(filtered_audio_data)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Processed Audio Waveform')
    plt.show()

# Function to apply audio effects
def apply_effects():
    global effected_audio_data, is_effected, is_filtered
    
    # Apply the effects to the audio data
    # Replace this with your own implementation of audio effects
    
    # Apply equalization
    equalized_audio_data = audio_data * 1.2  # Placeholder, increase the amplitude by 20%
    
    # Apply dynamic range compression
    compressed_audio_data = np.clip(equalized_audio_data, -1000, 1000)  # Placeholder, clip values between -1000 and 1000
    
    # Apply noise reduction
    noise_reduced_audio_data = compressed_audio_data * 0.8  # Placeholder, decrease the amplitude by 20%
    
    # Apply reverberation removal
    reverberation_removed_audio_data = noise_reduced_audio_data * 0.5  # Placeholder, decrease the amplitude by 50%
    
    effected_audio_data = reverberation_removed_audio_data
    is_effected = True
    is_filtered = False
    
    # Clear the previous graph, if any
    plt.clf()
    
    # Plot the processed waveform
    plt.plot(effected_audio_data)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Processed Audio Waveform')
    plt.show()

# Function to play the final audio
def play_audio():
    global audio_data, filtered_audio_data, effected_audio_data, is_filtered, is_effected
    
    if is_effected:
        audio_to_play = effected_audio_data
    elif is_filtered:
        audio_to_play = filtered_audio_data
    else:
        audio_to_play = audio_data
    
    if len(audio_to_play) > 0:
        sa.play_buffer(audio_to_play.astype(np.int16), 1, 2, sample_rate)
    else:
        print("No audio data to play.")

# Function to recover the audio to its original state
def recover_audio():
    global audio_data, filtered_audio_data, effected_audio_data, is_filtered, is_effected
    
    audio_data = audio_data.copy()  # Restore original audio data
    filtered_audio_data = np.array([])  # Clear filtered audio data
    effected_audio_data = np.array([])  # Clear effected audio data
    is_filtered = False
    is_effected = False
    
    # Clear the previous graph, if any
    plt.clf()
    
    # Plot the waveform
    plt.plot(audio_data)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Audio Waveform')
    plt.show()

# Button to open a sound file
open_button = tk.Button(app, text="Open File", command=open_file)
open_button.pack()

# Button to apply filters
filter_button = tk.Button(app, text="Apply Filters", command=apply_filters)
filter_button.pack()

# Button to apply effects
effect_button = tk.Button(app, text="Apply Effects", command=apply_effects)
effect_button.pack()

# Button to play the final audio
play_button = tk.Button(app, text="Play Audio", command=play_audio)
play_button.pack()

# Button to recover the audio to its original state
recover_button = tk.Button(app, text="Recover Audio", command=recover_audio)
recover_button.pack()

# Run the Tkinter event loop
app.mainloop()
