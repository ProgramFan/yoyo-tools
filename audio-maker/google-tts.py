#!/usr/bin/env python3
#

import argparse
from google.cloud import texttospeech as tts


def create_audio(text, audio, ssml=False, speed=1.0):
    with open(text) as f:
        content = f.read()
    client = tts.TextToSpeechClient()
    if ssml:
        synthesis_input = tts.SynthesisInput(ssml=content)
    else:
        synthesis_input = tts.SynthesisInput(text=content)
    voice = tts.VoiceSelectionParams(language_code="en-US",
                                     name="en-US-Wavenet-F",
                                     ssml_gender=tts.SsmlVoiceGender.FEMALE)
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3,
                                   speaking_rate=speed)
    response = client.synthesize_speech(input=synthesis_input,
                                        voice=voice,
                                        audio_config=audio_config)
    with open(audio, "wb") as out:
        out.write(response.audio_content)
        print(f'Successfully converted "{text}" to "{audio}"')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("TEXT", help="Text file to convert")
    parser.add_argument("OUTPUT", help="Output file name")
    parser.add_argument("--ssml",
                        action="store_true",
                        help="Treat the input as SSML text")
    parser.add_argument("--speed",
                        type=float,
                        default=1.0,
                        help="Reading speed (default: %(default)s)")
    args = parser.parse_args()

    create_audio(args.TEXT, args.OUTPUT, args.ssml, args.speed)


if __name__ == "__main__":
    main()
