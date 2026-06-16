from utils.sound_utils import SoundHelper

if __name__ == "__main__":
    file = "data/raw/DSP1.wav"
    signal_threshold = -45
    y, sr = SoundHelper.load_sound(file)
    m_noise, m_signal, std_dev_file = SoundHelper.extract_sdt(y, sr)

    thresholds = [-50, -42, -38, -32]
    
    for threshold in thresholds:
        SoundHelper.calculate_sdt_probabilities(
            m_noise,
            m_signal,
            std_dev_file,
            threshold
        )
    