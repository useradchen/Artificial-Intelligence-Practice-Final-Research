# IndexTTS: An Industrial-Level Controllable and Efficient Zero-Shot Text-To-Speech System

## Overview

This project explores the capabilities of **IndexTTS**, a zero-shot, industrial-grade text-to-speech (TTS) system. Our primary focus is on **inference** since the official training code is not publicly available. We evaluate its accuracy and speaker imitation performance using multiple benchmarks.

Our results show that IndexTTS performs exceptionally well in both Chinese and English speech synthesis, demonstrating great potential for practical applications—especially in emotional interaction and voice preservation.

> This work was conducted as part of the "AI Practice" course project at our university (Spring 2025, Group 3).

## 🔍 Motivation

Recent advances in speech synthesis have enabled AI to mimic familiar voices using just short samples. While this brings emotional benefits such as digitally recreating a deceased loved one’s voice, it also raises serious concerns like voice phishing and impersonation.

We aim to investigate both the potential and risks of zero-shot voice synthesis and assess the reliability and limitations of IndexTTS in realistic scenarios.

## 🛠️ Implementation

We based our implementation on the open-source [IndexTTS](https://github.com/index-tts/index-tts) repository. The following modules are used in the inference process:

- **Text Tokenizer**: BPE-based encoding for multilingual support (especially Chinese pinyin handling).
- **Speech Encoder**: Uses VQ-VAE with Finite Scalar Quantization to compress speech signals into discrete latent vectors.
- **Speech LLM**: A transformer-based model that uses text, speaker embeddings, and acoustic prompts to generate latent speech representations.
- **Speech Decoder**: Employs BigVGAN2 to directly synthesize high-fidelity audio from the latent vectors.

## 🧪 Experiment Results

We tested the model using 50 samples for each language (Chinese and English), both male and female speakers.

| Metric                  | Our Result | Paper Reference      |
|-------------------------|------------|-----------------------|
| **Chinese CER**         | 3.6%       | 1.3% ~ 7.0%           |
| **English WER**         | 1.51%      | 2.1% ~ 5.3%           |
| **Speaker Similarity**  | 73.72%     | 74.2% ~ 82.3%         |

- **CER** (Character Error Rate) was evaluated using [Paraformer ASR](https://github.com/lovemefan/paraformer-python/tree/main).
- **WER** (Word Error Rate) was evaluated using [Whisper Large v3](https://github.com/openai/whisper).
- **Speaker Similarity** used ERes2Net + cosine similarity.

Overall, the results validate that IndexTTS meets or outperforms the original benchmarks in most cases.

## 💡 Key Features

- 🗣️ **Zero-shot speaker cloning**: Mimic a target speaker using only one short reference audio clip.
- 🌍 **Multilingual support**: Works well in both Chinese and English.
- 🎛️ **Controllable emotion and tone** via reference speech and text.
- ⚡ **End-to-end efficient inference** using a unified and streamlined architecture.

## 🎬 Demo Showcase

You can access the audio and video demonstrations here:

- 🔉 [Audio samples](https://drive.google.com/drive/folders/10TqtE4uSk6UIGSZQt2q6OslWq6XmWGqq?usp=drive_link)
- 📹 [Result videos](https://drive.google.com/drive/folders/1-i_7N4QSvg9pE6Ayorieh8_cxgZMaTFB?usp=drive_link)

Highlights:

- 🟡 **Minions laughter (failed case)**: Failed to recreate due to unnatural, high-pitched frequencies.
- 🟢 **Taiwanese celebrity "Chu Ko-liang" voice clone**: Successfully reproduced voice even though the reference was in Taiwanese.
- 🔵 **Chinese gaming voice samples**: High fidelity due to matched dataset and accents.

## ⚠️ Limitations

- 📍 Text punctuation can lead to unnatural prosody.
- 🔊 Noisy or multi-speaker reference audio causes degraded output quality.
- 🎯 Model's stability is sensitive to input data cleanliness.

## 🚀 Usage Instructions

To run the demo with our Gradio interface:

1. **Clone the official IndexTTS repository**  
   Download the original project from GitHub:
   ```bash
   git clone https://github.com/index-tts/index-tts.git
   cd index-tts
   ```

2. **Place the demo script**  
Copy our [gradio_for_demo.py](gradio_for_demo/gradio_for_demo.py) file into the `index-tts` folder.

3. **Run the demo**  
Execute the script to launch a Gradio-based web interface:
```bash
python gradio_for_demo.py
```
This interface allows you to:
- Upload a reference audio sample.
- Input text in either Chinese or English.
- Generate synthesized speech in the style of the reference speaker.

Make sure all required dependencies are installed as specified in the original `index-tts` repo.


## 📎 Citation

If you refer to this project or use the data for your research, please cite:

```bibtex
@article{deng2025indextts,
  title={IndexTTS: An Industrial-Level Controllable and Efficient Zero-Shot Text-To-Speech System},
  author={Deng, Wei and others},
  journal={arXiv preprint arXiv:2502.05512},
  year={2025}
}
