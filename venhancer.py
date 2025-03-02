import os

import torch

from easydict import EasyDict
from huggingface_hub import hf_hub_download

from inference_utils import (
    adjust_resolution,
    collate_fn,
    load_video,
    make_mask_cond,
    preprocess,
    save_video,
    tensor2vid,
)
from video_to_video.utils.logger import get_logger
from video_to_video.utils.seed import setup_seed
from video_to_video.video_to_video_model import VideoToVideo


logger = get_logger()


class VEnhancer:
    def __init__(
        self, result_dir="./results/", model_path="", solver_mode="fast", steps=15, guide_scale=7.5, s_cond=8
    ):
        if not model_path:
            self.download_model()
            assert os.path.exists(self.model_path), "Error: checkpoint Not Found!"
        else:
            self.model_path = model_path
        logger.info(f"checkpoint_path: {self.model_path}")

        self.result_dir = result_dir
        os.makedirs(self.result_dir, exist_ok=True)

        model_cfg = EasyDict(__name__="model_cfg")
        model_cfg.model_path = self.model_path
        self.model = VideoToVideo(model_cfg)

        steps = 15 if solver_mode == "fast" else steps
        self.solver_mode = solver_mode
        self.steps = steps
        self.guide_scale = guide_scale
        self.s_cond = s_cond

    def enhance_a_video(self, video_path, prompt, up_scale=4, target_fps=24, noise_aug=300):

        logger.info(f"input video path: {video_path}")
        text = prompt
        logger.info(f"text: {text}")
        caption = text + self.model.positive_prompt

        input_frames, input_fps = load_video(video_path)
        in_f_num = len(input_frames)
        logger.info(f"input frames length: {in_f_num}")
        logger.info(f"input fps: {input_fps}")
        interp_f_num = max(round(target_fps / input_fps) - 1, 0)
        interp_f_num = min(interp_f_num, 8)
        target_fps = input_fps * (interp_f_num + 1)
        logger.info(f"target_fps: {target_fps}")

        video_data = preprocess(input_frames)
        _, _, h, w = video_data.shape
        logger.info(f"input resolution: {(h, w)}")
        target_h, target_w = adjust_resolution(h, w, up_scale)
        logger.info(f"target resolution: {(target_h, target_w)}")

        mask_cond = make_mask_cond(in_f_num, interp_f_num)
        mask_cond = torch.Tensor(mask_cond).long()

        noise_aug = min(max(noise_aug, 0), 300)
        logger.info(f"noise augmentation: {noise_aug}")
        logger.info(f"scale s is set to: {self.s_cond}")

        pre_data = {"video_data": video_data, "y": caption}
        pre_data["mask_cond"] = mask_cond
        pre_data["s_cond"] = self.s_cond
        pre_data["interp_f_num"] = interp_f_num
        pre_data["target_res"] = (target_h, target_w)
        pre_data["t_hint"] = noise_aug

        total_noise_levels = 900
        setup_seed(666)

        with torch.no_grad():
            data_tensor = collate_fn(pre_data, "cuda:0")
            output = self.model.test(
                data_tensor,
                total_noise_levels,
                steps=self.steps,
                solver_mode=self.solver_mode,
                guide_scale=self.guide_scale,
                noise_aug=noise_aug,
            )

        output = tensor2vid(output)
        file_name = f"{text}.mp4"
        save_video(output, self.result_dir, file_name, fps=target_fps)
        return os.path.join(self.result_dir, file_name)

    def download_model(self):
        REPO_ID = "jwhejwhe/VEnhancer"
        filename = "venhancer_paper.pt"
        ckpt_dir = "/data/Dynamics/VEnhacer_ckpts/"
        os.makedirs(ckpt_dir, exist_ok=True)
        local_file = os.path.join(ckpt_dir, filename)
        if not os.path.exists(local_file):
            logger.info(f"Downloading the VEnhancer checkpoint...")
            hf_hub_download(repo_id=REPO_ID, filename=filename, local_dir=ckpt_dir)
        self.model_path = local_file
