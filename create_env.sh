#!/bin/bash
#SBATCH --account=def-skrishna
#SBATCH --gres=gpu:1       # Request GPU "generic resources"
#SBATCH --cpus-per-task=4  # Cores proportional to GPUs: 6 on Cedar, 16 on Graham.
#SBATCH --mem=16000M       # Memory proportional to GPUs: 32000 Cedar, 64000 Graham.
#SBATCH --time=0-00:30
#SBATCH --output=sailEnvTest2-%j.out
#SBATCH --mail-user=yiqing.zhu2@mail.mcgill.ca
#SBATCH --mail-type=BEGIN,END,FAIL

module load python/3.10  # Make sure to choose a version that suits your application
module load arrow/15.0.1
# remember to use the last zip file
cp ~/projects/rrg-skrishna/yzhu439/SAIL/Tmp.zip $SLURM_TMPDIR
unzip $SLURM_TMPDIR/Tmp.zip -d $SLURM_TMPDIR/

# Use my requirements_CC.txt and install my upload pycocoevalcap package
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install --no-index --upgrade pip
pip install --no-index -r ~/projects/rrg-skrishna/yzhu439/SAIL/requirements_CC.txt
pip install --no-index cython nltk
pip install --no-index --find-links=$SLURM_TMPDIR/my_packages pycocoevalcap

# # change current layer to Tmp
# # here as I use zip -r Tmp.zip my_packages requirements_CC.txt
# cd $SLURM_TMPDIR
# python train_bert.py
# # copy the output_model store back to my local place 
# cp -r output_model_CC ~/projects/rrg-skrishna/yzhu439/766Project_CCTest/