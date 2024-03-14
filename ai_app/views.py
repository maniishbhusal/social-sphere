from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import ChatConversation
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from dotenv import load_dotenv

from openai import OpenAI
from pathlib import Path

import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import os
from pygame import mixer

User = get_user_model()

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Instantiate mixer
mixer.init()

path = "ai_app/static/ai_app/audio/"


def index(request):
    if not request.user.is_authenticated:
        return redirect(reverse('user_login'))

    return render(request, 'ai_app/index.html')

# @login_required(login_url='login')


def artificialIntelligenceView(request):
    if not request.user.is_authenticated:
        return redirect(reverse('user_login'))

    # if request.method == 'POST':
    #     prompt = request.POST.get('prompt')
    #     user = request.user
    #     conversation = ChatConversation(user=user, prompt=prompt)
    #     conversation.save()
    #     return render(request, 'ai_app/artificial_intelligence.html', {'prompt': prompt})

        # return redirect(reverse('ai_app:ai_response', args=[prompt]))

    return render(request, 'ai_app/artificial_intelligence.html')


def recordAndRead(request):

    print("Message from client")
    # record audio and download
    # Sampling frequency
    freq = 44100

    # Recording duration
    duration = 5

    # Start recorder with the given values
    # of duration and sample frequency
    recording = sd.rec(int(duration * freq),
                       samplerate=freq, channels=2)

    # Record audio for the given number of seconds
    sd.wait()

    # This will convert the NumPy array to an audio
    # file with the given sampling frequency
    write(path+"recording.wav", freq, recording)

    # Transcribe the recorded audio using OpenAI Whisper API
    audio_file_path = path+"recording.wav"
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=open(audio_file_path, "rb")
    )

    print("Transcription obj...", transcript)
    # Get the transcription text
    transcription_text = transcript.text

    # # Use Chat API to give response of transcription_text
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": transcription_text}
        ]
    )

    chat_response = completion.choices[0].message.content
    print("Chat response...", chat_response)

    # Generates audio from the chat response of AI
    # speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="shimmer",
        input=chat_response
    )
    response.stream_to_file(path+"output.mp3")

    # read audio file
    mixer.music.load(path + "output.mp3")
    print("audio started playing...")
    mixer.music.play()

    # Return an HTTP response with the transcription text
    return JsonResponse({"query": transcription_text, "response": chat_response})
