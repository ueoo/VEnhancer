export PATH=/mnt/petrelfs/share_data/hejingwen/ffmpeg-4.3.2-amd64-static/:$PATH
srun -p video-aigc-1 --gres=gpu:1 --job-name=SRI  \
python enhance_a_video.py \
--up_scale 4 --target_fps 24 --noise_aug 250 \
--solver_mode 'fast' --steps 15 \
--input_path prompts/astronaut.mp4 \
--prompt 'An astronaut flying in space, featuring a steady and smooth perspective' \
--save_dir 'results/' \