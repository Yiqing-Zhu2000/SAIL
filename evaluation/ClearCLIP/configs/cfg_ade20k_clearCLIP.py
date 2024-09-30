_base_ = './base_config.py'

# model settings
model = dict(
    name_path='/home/mila/q/qian.yang/Light_Align/evaluation/ClearCLIP/configs/cls_ade20k.txt'
)
# dataset settings
dataset_type = 'ADE20KDataset'
#Change this to your local path
data_root = '/home/mila/q/qian.yang/scratch/segmentation_datasets/ADEChallengeData2016'

test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='Resize', scale=(2048, 448), keep_ratio=True),
    dict(type='LoadAnnotations', reduce_zero_label=True),
    dict(type='PackSegInputs')
]

test_dataloader = dict(
    batch_size=1,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        data_prefix=dict(
            img_path='images/validation',
            seg_map_path='annotations/validation'),
        pipeline=test_pipeline))