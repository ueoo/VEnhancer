<div align="center">

<h1>VEnhancer: Generative Space-Time Enhancement<br>for Video Generation</h1>

<div>
    <a href='https://scholar.google.com/citations?user=GUxrycUAAAAJ&hl=zh-CN' target='_blank'>Jingwen He</a>,&emsp;
    <a href='https://tianfan.info' target='_blank'>Tianfan Xue</a>,&emsp;
    <a href='https://github.com/ChrisLiu6' target='_blank'>Dongyang Liu</a>,&emsp;
    <a href='https://github.com/0x3f3f3f3fun' target='_blank'>Xinqi Lin</a>,&emsp;
</div>
    <a href='https://gaopengcuhk.github.io' target='_blank'>Peng Gao</a>,&emsp;
    <a href='https://scholar.google.com/citations?user=GMzzRRUAAAAJ&hl=en' target='_blank'>Dahua Lin</a>,&emsp;
    <a href='https://scholar.google.com/citations?user=gFtI-8QAAAAJ&hl=en' target='_blank'>Yu Qiao</a>,&emsp;
    <a href='https://wlouyang.github.io' target='_blank'>Wanli Ouyang</a>,&emsp;
    <a href='https://liuziwei7.github.io' target='_blank'>Ziwei Liu</a>
<div>
</div>
<div>
    The Chinese University of Hong Kong,&emsp;Shanghai Artificial Intelligence Laboratory,&emsp; 
</div>
<div>
    
</div>
<div>
 S-Lab, Nanyang Technological University&emsp; 
</div>

<div>
    <h4 align="center">
        <a href="https://vchitect.github.io/VEnhancer-project/" target='_blank'>
        <img src="https://img.shields.io/badge/🐳-Project%20Page-blue">
        </a>
        <a href="https://arxiv.org/abs/2407.07667" target='_blank'>
        <img src="https://img.shields.io/badge/arXiv-2312.06640-b31b1b.svg">
        </a>
        <a href="https://youtu.be/QMR_5weifGg" target='_blank'>
        <img src="https://img.shields.io/badge/Demo%20Video-%23FF0000.svg?logo=YouTube&logoColor=white">
        <!-- </a>
        <img src="https://api.infinitescript.com/badgen/count?name="> -->
    </h4>
</div>

<strong>VEnhancer, a generative space-time enhancement framework that can improve the existing T2V results. </strong>

<table class="center">
  <tr>
    <td colspan="1">input</td>
    <td colspan="1">+VEnhancer</td>
  </tr>
  <tr>
  <td>
    <img src=assets/input_raccoon_4.gif width="380">
  </td>
  <td>
    <img src=assets/out_raccoon_4.gif width="380">
  </td>
  </tr>
  <tr>
  <td>
    <img src=assets/input_fish.gif width="380">
  </td>
  <td>
    <img src=assets/out_fish.gif width="380">
  </td>
  </tr>

  

</table>

:open_book: For more visual results, go checkout our <a href="https://vchitect.github.io/VEnhancer-project/" target="_blank">project page</a>


---

</div>



## 🔥🔥 News
We have enhanced some T2V results from [CogVideoX](https://github.com/THUDM/CogVideo)🤗. (This checkpoint is not the released one!) 
<div align="center">
  <video src="https://github.com/user-attachments/assets/d6ba4ebe-a970-4db1-ade1-03bfa8e52a20" width="80%" controls autoplay></video>
  <video src="https://github.com/user-attachments/assets/bf97116e-2fbc-4e29-b559-4fe08dc65c02" width="80%" controls autoplay></video>
  <p>A detailed wooden toy ship with intricately carved masts and sails is seen gliding smoothly over a plush, blue carpet that mimics the waves of the sea. The ship's hull is painted a rich brown, with tiny windows. The carpet, soft and textured, provides a perfect backdrop, resembling an oceanic expanse. Surrounding the ship are various other toys and children's items, hinting at a playful environment. The scene captures the innocence and imagination of childhood, with the toy ship's journey symbolizing endless adventures in a whimsical, indoor setting.</p>
</div>

<div align="center">
  <video src="https://github.com/user-attachments/assets/ff59dc10-b674-4ec5-ae7f-7c1ee3c638e1" width="80%" controls autoplay></video>
  <video src="https://github.com/user-attachments/assets/faebf7bb-5a33-4cd5-84ca-768d384dfe94" width="80%" controls autoplay></video>
  <p>The camera follows behind a white vintage SUV with a black roof rack as it speeds up a steep dirt road surrounded by pine trees on a steep mountain slope, dust kicks up from its tires, the sunlight shines on the SUV as it speeds along the dirt road, casting a warm glow over the scene. The dirt road curves gently into the distance, with no other cars or vehicles in sight. The trees on either side of the road are redwoods, with patches of greenery scattered throughout. The car is seen from the rear following the curve with ease, making it seem as if it is on a rugged drive through the rugged terrain. The dirt road itself is surrounded by steep hills and mountains, with a clear blue sky above with wispy clouds.</p>
</div>


## 🔥 Update
- [2024.08.18] 😸 Support enhancement for **abitrary long videos** (by spliting the videos into muliple chunks with overlaps); Fewer sampling steps (15) are enabled without obvious quality loss by setting `--solver_mode 'fast'` in the script command; Use **temporal VAE** to reduce video flickering.
- [2024.07.28] 🔥 Inference code and pretrained video enhancement model are released.
- [2024.07.10] 🤗 This repo is created.

## 🎬 Overview
VEnhancer achieves spatial super-resolution, temporal super-resolution (frame interpolation), and video refinement in a **unified framework**.
It is flexible to adapt to different upsampling factors (e.g., 1x~8x) for either spatial or temporal super-resolution. Besides, it provides flexible control to modify the refinement strength for handling diversified video artifacts. 

It follows ControlNet and copies the architecures and weights of multi-frame encoder and middle block of a pretrained video diffusion model to build a trainable condition network. 
This **video ControlNet** accepts both low-resolution key frames and full frames of noisy latents as inputs. 
Also, the noise level $\sigma$ regarding noise augmentation and downscaling factor $s$ serve as additional network conditioning through our proposed **video-aware conditioning** apart from timestep $t$ and prompt $c_{text}$. 
![overall_structure](assets/venhancer_arch.png)


## :gear: Installation
```shell
# clone this repo
git clone https://github.com/Vchitect/VEnhancer.git
cd VEnhancer

# create environment
conda create -n venhancer python=3.10
conda activate venhancer
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2
pip install -r requirements.txt
```
Note that ffmpeg command should be enabled. If you have sudo access, then you can install it using the following command:
```shell
sudo apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
```

## :dna: Pretrained Models
| Model Name | Description | HuggingFace | BaiduNetdisk  |
| :---------: | :----------: | :----------: | :----------: | 
| venhancer_paper.pth  | video enhancement model, paper version | [download](https://huggingface.co/jwhejwhe/VEnhancer/resolve/main/venhancer_paper.pt) | [download](https://pan.baidu.com/s/15t20RGvEHqJOMmhA_zRLiA?pwd=cpsd)|

## 💫 Inference 
1) Download the VEnhancer model and then put the checkpoint in the `VEnhancer/ckpts` directory. (optional as it can be done automatically)
2) run the following command.
```bash
  bash run_VEnhancer.sh
```
In `run_VEnhancer.sh`, `up_scale` is the upsampling factor ($1\sim8$) for spatial super-resolution; `target_fps` is your expected target fps (default is 24); `noise_aug` is the noise level ($0\sim300$) regarding noise augmentation. 

### Gradio
The same functionality is also available as a gradio demo
``` shell
python gradio_app.py
```


## BibTeX
If you use our work in your research, please cite our publication:
```
@article{he2024venhancer,
  title={VEnhancer: Generative Space-Time Enhancement for Video Generation},
  author={He, Jingwen and Xue, Tianfan and Liu, Dongyang and Lin, Xinqi and Gao, Peng and Lin, Dahua and Qiao, Yu and Ouyang, Wanli and Liu, Ziwei},
  journal={arXiv preprint arXiv:2407.07667},
  year={2024}
}
```

## 🤗 Acknowledgements
Our codebase builds on [modelscope](https://github.com/modelscope/modelscope). 
Thanks the authors for sharing their awesome codebases! 

## 📧 Contact
If you have any questions, please feel free to reach us at `hejingwenhejingwen@outlook.com`.
