import pyttsx3 as pt
import os
# engine = pt.init()
# text = "hello samuel"
# engine.save_to_file(text,  "hiy.mp3")
# engine.runAndWait()
file_name = "hello.mp3"
pat = os.path.join(os.getcwd(), 'media/audio/'+file_name)
print(pat)