import telebot
import subprocess
import os

TOKEN = os.getenv("8542516357:AAEBpF7C6pIX2HdgPURKzCn1DWIcaM1dTOk")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    file_info = bot.get_file(message.video.file_id)
    data = bot.download_file(file_info.file_path)

    input_file = "input.mp4"
    output_file = "output_4k_h265.mp4"

    with open(input_file, "wb") as f:
        f.write(data)

    bot.reply_to(message, "🔄 Converting to H.265 + 4K (no ratio damage)…")

    # FFmpeg command (SAFE 4K upscale)
    subprocess.run([
        "ffmpeg", "-y",
        "-i", input_file,
        "-vf", "scale=3840:2160:force_original_aspect_ratio=decrease",
        "-c:v", "libx265",
        "-preset", "slow",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        output_file
    ])

    with open(output_file, "rb") as v:
        bot.send_video(message.chat.id, v, supports_streaming=True)

    os.remove(input_file)
    os.remove(output_file)

bot.polling()
