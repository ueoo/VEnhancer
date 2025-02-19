from argparse import ArgumentParser, Namespace

from venhancer import VEnhancer
from video_to_video.utils.logger import get_logger


logger = get_logger()


def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument("--input_path", required=True, type=str, help="input video path")
    parser.add_argument("--save_dir", type=str, default="results", help="save directory")
    parser.add_argument("--model_path", type=str, default="", help="model path")
    parser.add_argument("--prompt", type=str, default="a good video", help="prompt")

    parser.add_argument("--cfg", type=float, default=7.5)
    parser.add_argument("--solver_mode", type=str, default="fast", help="fast | normal")
    parser.add_argument("--steps", type=int, default=15)

    parser.add_argument("--noise_aug", type=int, default=200, help="noise augmentation")
    parser.add_argument("--target_fps", type=int, default=24)
    parser.add_argument("--up_scale", type=float, default=4)
    parser.add_argument("--s_cond", type=float, default=8)

    return parser.parse_args()


def main():

    args = parse_args()

    input_path = args.input_path
    prompt = args.prompt
    model_path = args.model_path
    save_dir = args.save_dir

    noise_aug = args.noise_aug
    up_scale = args.up_scale
    target_fps = args.target_fps
    s_cond = args.s_cond

    steps = args.steps
    solver_mode = args.solver_mode
    guide_scale = args.cfg

    assert solver_mode in ("fast", "normal")

    venhancer = VEnhancer(
        result_dir=save_dir,
        model_path=model_path,
        solver_mode=solver_mode,
        steps=steps,
        guide_scale=guide_scale,
        s_cond=s_cond,
    )

    venhancer.enhance_a_video(input_path, prompt, up_scale, target_fps, noise_aug)


if __name__ == "__main__":
    main()
