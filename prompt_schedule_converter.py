import re

class PromptScheduleConverter:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text_with_timestamps": ("STRING",),  # Subtitle text in custom timestamp format
                "fps": ("FLOAT",),                    # Frames per second
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("formatted_text",)
    FUNCTION = "convert_time_to_frame"
    CATEGORY = "Schedulizer"

    def convert_time_to_frame(self, text_with_timestamps, fps):
        # Define the pattern for extracting time ranges and text
        text_pattern = r'\[(\d+\.\d+)s - (\d+\.\d+)s\] (.+)'  # Capture non-empty text after time range
        
        # Find all matches for start time, end time, and associated text
        matches = re.findall(text_pattern, text_with_timestamps)
        
        # Check if any matches were found
        if not matches:
            print("No valid matches found in input.")
            return {"ui": {"text": "No valid input detected."}, "result": ("No valid input detected.",)}

        formatted_text = []
        last_text = None  # Track the last text to avoid duplicates
        first_entry = True  # Track if we're adding the first entry
        
        # Loop over each matched time range and text
        for start_time, end_time, line in matches:
            # Convert start time to frame number
            start_frame = self.time_to_frames(start_time, fps)
            
            # Ensure the text is stripped of excess whitespace
            line = line.strip()
            
            # Check if this is the first entry
            if first_entry:
                # Always set the first entry to frame "0"
                formatted_text.append(f'"0" : "{line}"')
                last_text = line  # Update last_text to the current line
                first_entry = False  # Disable the first entry flag
                continue  # Skip to the next loop iteration
            
            # Only add the frame-text pair if the text has changed
            if line != last_text:
                formatted_text.append(f'"{start_frame}" : "{line}"')
                last_text = line  # Update last_text to the current line

        # Join all frame-text pairs with line breaks, adding a comma after each except the last
        formatted_output = ",\n".join(formatted_text)
        
        # Return formatted output
        return {"ui": {"text": formatted_output}, "result": (formatted_output,)}
    
    def time_to_frames(self, time_str, fps):
        # Convert time string (ss.s) to frame count
        return int(float(time_str) * fps)