import whisper
import os
import folder_paths
import uuid
import torchaudio


class WhisperNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio": ("AUDIO",),
                "model": (["base", "tiny", "small", "medium", "large", "large-v2"],),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("text", "text_with_timestamps")
    FUNCTION = "whisper_node"
    CATEGORY = "Schedulizer"

    def whisper_node(self, audio, model):
        # Save audio bytes to file
        temp_dir = folder_paths.get_temp_directory()
        os.makedirs(temp_dir, exist_ok=True)
        audio_save_path = os.path.join(temp_dir, f"{uuid.uuid1()}.wav")
        torchaudio.save(audio_save_path, audio['waveform'].squeeze(0), audio["sample_rate"])

        # Transcribe using Whisper
        model = whisper.load_model(model)
        result = model.transcribe(audio_save_path, word_timestamps=True)

        # Extract plain text and timestamped text
        plain_text = result["text"].strip()
        text_with_timestamps = "\n".join(
            f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text'].strip()}"
            for segment in result['segments']
        )

        return plain_text, text_with_timestamps
