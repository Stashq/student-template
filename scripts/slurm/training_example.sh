#!/bin/bash
#SBATCH --job-name=unet_training
#SBATCH --time=5:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=clara
#SBATCH --gres=gpu:v100:1
#SBATCH --mem=24G
#SBATCH --cpus-per-task=4
#SBATCH -o /home/sc.uni-leipzig.de/<uni_login>/logs/%x.out-%j

source .venv/bin/activate

python src/runs/train/unet.py
