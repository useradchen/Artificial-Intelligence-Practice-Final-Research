#gemini輔助文本生成
import sys
import os
import gradio as gr
from indextts.infer import IndexTTS

from pydub import AudioSegment
import tempfile
import re

# 項目根目錄與模型設定
project_root = os.path.dirname(os.path.abspath(__file__))
tts_model_dir_abs = r'checkpoints'
tts_config_path_abs = r'checkpoints/config.yaml'

# 初始化 TTS 模型
tts_instance = None
print("正在初始化 IndexTTS 模型，請稍候...")
try:
    if not os.path.exists(tts_model_dir_abs):
        raise FileNotFoundError(f"模型目錄 '{tts_model_dir_abs}' 不存在！")
    if not os.path.exists(tts_config_path_abs):
        raise FileNotFoundError(f"配置文件 '{tts_config_path_abs}' 不存在！")
    tts_instance = IndexTTS(model_dir=tts_model_dir_abs, cfg_path=tts_config_path_abs)
    print("IndexTTS 模型初始化完成！")
except Exception as e:
    print(f"初始化 IndexTTS 模型時發生嚴重錯誤: {e}")

# 語音合成邏輯
def synthesize_speech_gradio(reference_audio_input, text_to_synthesize_input):
    if tts_instance is None:
        return None, "錯誤：TTS 模型未能初始化。"
    if not reference_audio_input:
        return None, "錯誤：請提供參考音訊。"
    if not text_to_synthesize_input:
        return None, "錯誤：請輸入文本。"

    segments = re.split(r"[，,、\s]+", text_to_synthesize_input)
    segments = [s.strip() for s in segments if s.strip()]
    output_audio_segments = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for idx, seg_text in enumerate(segments):
            seg_wav_path = os.path.join(tmpdir, f"seg_{idx}.wav")
            print(f"TTS子句({idx+1}): {seg_text}")
            try:
                tts_instance.infer(
                    reference_audio_input,
                    seg_text,
                    seg_wav_path
                )
                output_audio_segments.append(AudioSegment.from_wav(seg_wav_path))
            except Exception as e_synth:
                print(f"  合成錯誤（片段{idx+1}）: {e_synth}")
                return None, f"合成失敗（第{idx+1}段）：{e_synth}"

        combined_audio = output_audio_segments[0]
        silence = AudioSegment.silent(duration=50)
        for seg in output_audio_segments[1:]:
            combined_audio += silence + seg

        output_filename = "generated_gradio_live_output.wav"
        output_audio_abs_path = os.path.join(project_root, output_filename)
        combined_audio.export(output_audio_abs_path, format="wav")
        print("  合併並生成完成！")
        return output_audio_abs_path, f"合成成功！（共分段：{len(segments)} 段）"

# 啟動 Gradio 介面
if tts_instance is not None:

    # 範例音訊
    example_audio_1_path = r"audio/小小兵笑聲.mp3"
    example_audio_2_path = r"audio/豬哥亮.mp3"
    example_audio_3_path = r"audio/game.mp3"

    for path in [example_audio_1_path, example_audio_2_path, example_audio_3_path]:
        if not os.path.exists(path):
            print(f"警告: 範例音訊 '{path}' 未找到。對應的範例將沒有預設音訊。")

    with gr.Blocks(theme=gr.themes.Soft()) as iface:
        gr.Markdown("# IndexTTS 零樣本語音合成")
        gr.Markdown("上傳或錄製一段參考音訊，輸入文本（可含逗號、空格分段），然後點擊 '合成語音'。")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 1. 提供參考聲音")
                reference_audio_gradio = gr.Audio(
                    sources=["upload", "microphone"],
                    type="filepath",
                    label="上傳 .wav/.mp3 或進行錄音"
                )
            with gr.Column(scale=2):
                gr.Markdown("### 2. 輸入文本並合成")
                text_input_gradio = gr.Textbox(
                    lines=7,
                    label="要合成的文本 (Text to Synthesize)",
                    placeholder="大家好，AI技術已經發展到這樣匪夷所思的地步了！"
                )
                submit_button = gr.Button("合成語音 (Synthesize Speech)", variant="primary")

        with gr.Row():
            with gr.Column():
                gr.Markdown("### 3. 結果")
                output_audio_gradio = gr.Audio(label="生成的音訊 (Generated Audio)")
                status_textbox_gradio = gr.Textbox(label="狀態訊息 (Status)", interactive=False)

        submit_button.click(
            fn=synthesize_speech_gradio,
            inputs=[reference_audio_gradio, text_input_gradio],
            outputs=[output_audio_gradio, status_textbox_gradio]
        )

        gr.Examples(
            examples=[
                [example_audio_1_path, "We are the Minions. We are looking for a boss"],
                [example_audio_2_path, "我是豬哥亮 台灣要發達 票投謝欣達"],
                [example_audio_3_path, "大三下終於要結束了 好累"],
            ],
            inputs=[reference_audio_gradio, text_input_gradio],
            outputs=[output_audio_gradio, status_textbox_gradio],
            fn=synthesize_speech_gradio,
            cache_examples=False,
            label="範例 (Examples) - 點擊以載入"
        )

    print("\n準備啟動 Gradio 界面...")
    iface.launch(share=True, debug=True)
else:
    print("由於 TTS 模型未能初始化，無法啟動 Gradio 界面。")