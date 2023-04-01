import pika
import whisper
import os
import numpy as np
import torch
import time
import mutagen
import text2emotion as te

from ..models import TranscriptResult, TemporaryAudio


def print_size_of_model(model):
    torch.save(model.state_dict(), "temp.p")
    size = os.path.getsize("temp.p")/1e6
    print('Size (MB):', size)
    os.remove('temp.p')
    return size

def time_model_evaluation(model, mel, options, audio_file):
    eval_start_time = time.time()
    # result = whisper.decode(model, mel, options)
    result = whisper.transcribe(model, audio_file) # , options)
    eval_end_time = time.time()
    eval_duration_time = eval_end_time - eval_start_time

    return [result["text"], str(eval_duration_time)]

def transcribe_main(audio_file, transcribed_audio_obj):
    audio_info = mutagen.File(audio_file).info
    print(f"Audio Length: {audio_info.length}")

    model_fp32 = whisper.load_model(
        name="base",
        device="cpu")

    quantized_model = torch.quantization.quantize_dynamic(
        model_fp32, {torch.nn.Linear}, dtype=torch.qint8
    )

    print_size_of_model(model_fp32)
    print_size_of_model(quantized_model)

    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)

    mel   = whisper.log_mel_spectrogram(audio).to(model_fp32.device)
    options = whisper.DecodingOptions(fp16=False)

    _, probs = quantized_model.detect_language(mel)
    lang_det = max(probs, key=probs.get)
    print(f"Detected language: {lang_det}")

    result = time_model_evaluation(quantized_model, mel, options, audio_file)
    emotions = te.get_emotion(result[0])

    result.append(str(emotions))

    transcribed_audio_obj.status = "Success"
    transcribed_audio_obj.transcribe_result = result[0]
    transcribed_audio_obj.sentiment_result = str(emotions)
    transcribed_audio_obj.translate_result = "None"
    transcribed_audio_obj.audio_info = audio_info.length
    transcribed_audio_obj.save()

    ID = transcribed_audio_obj.id

    print(f"Done Transcribing Data for ID {ID}...")

    return result

# Evaluate the INT8 BERT model after the dynamic quantization
def transcribeTextData(audio, audio_info, transcribed_audio_obj, obj_id, audio_id):

    try:
        if audio:
            audio_file = audio.temporary_file_path()
        else:
            audio_file = TemporaryAudio.objects.get(pk=audio_id).audio.path

        if not transcribed_audio_obj:
            transcribed_audio_obj = TranscriptResult.objects.get(pk=obj_id)

        result_all = transcribe_main(audio_file, transcribed_audio_obj)

        transcribe_result = result_all[0]
        compute_time = result_all[1]
        emotion = result_all[2]

        status_description = "Successful in transcribing result"

        context = {
                    "status" : "Success",
                    "audio_info" : audio_info,
                    "status_description" : status_description,
                    "transcribe_result" : transcribe_result,
                    "sentiment_result" : emotion,
                    "id": transcribed_audio_obj.id
                }

        audio_data_obj = TemporaryAudio.objects.get(pk=audio_id)
        audio_data_obj.audio.delete()
        audio_data_obj.delete()

        return context

    except Exception as e:
        print(f"Error: {e}")
        audio_data_obj = TemporaryAudio.objects.get(pk=audio_id)
        audio_data_obj.audio.delete()
        audio_data_obj.delete()

        transcribed_audio_obj = TranscriptResult.objects.get(pk=obj_id)

        transcribed_audio_obj.status = "Error"
        transcribed_audio_obj.save()

        context = {
                    "status" : "Error",
                    "audio_info" : audio_info,
                    "status_description" : "Failed to transcribe text",
                    "transcribe_result" : "None",
                }
        return context
