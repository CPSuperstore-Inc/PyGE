# import aubio
import numpy as num
import pyaudio

from PyGE.Globals.GlobalVariable import set_var


def frequency_monitor(unit="Hz", silence=-40):
    """
    WARNING: Temporarily Disabled!
    Monitors the frequency (pitch) of the audio input.
    WARNING: DO NOT CALL IN MAIN THREAD!!!
    :param unit: the unit to measure the pitch in (default is "Hz" - Hertz)
    :param silence: The silence threashold (default is -40db)
    """
    raise NotImplementedError("Due to some compatability issues, this method has been temporarily disabled...")
    # # constants
    # buffer_size = 2048
    # channels = 1
    # pyaudio_format = pyaudio.paFloat32
    # method = "default"
    # sample_rate = 44100
    # hop_size = buffer_size // 2
    # period_size_in_frame = hop_size
    #
    # # Initiating PyAudio object.
    # pa = pyaudio.PyAudio()
    # # Open the microphone stream.
    # mic = pa.open(
    #     format=pyaudio_format,
    #     channels=channels,
    #     rate=sample_rate,
    #     input=True,
    #     frames_per_buffer=period_size_in_frame
    # )
    #
    # # Initiating Aubio's pitch detection object.
    # detection = aubio.pitch(method, buffer_size,
    #     hop_size, sample_rate)
    # # Set unit.
    # detection.set_unit(unit)
    # # Frequency under -40 dB will considered
    # # as a silence.
    # detection.set_silence(silence)
    #
    # while True:
    #     # Always listening to the microphone.
    #     data = mic.read(period_size_in_frame)
    #     # Convert into number that Aubio understand.
    #     samples = num.fromstring(data, dtype=aubio.float_type)
    #     # Finally get the pitch.
    #     set_var("current_pitch", detection(samples)[0])
