from .whisper_node import WhisperNode
from .prompt_schedule_converter import PromptScheduleConverter

NODE_CLASS_MAPPINGS = { 
    "whisper_node" : WhisperNode,
    "prompt_schedule_converter" : PromptScheduleConverter
}

NODE_DISPLAY_NAME_MAPPINGS = {
     "whisper_node" : "Whisper Node",
     "prompt_schedule_converter" : "Prompt Schedule Converter"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']