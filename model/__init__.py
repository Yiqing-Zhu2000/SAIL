from .language import SentenceEmbedding
from .vision import ImageEmbedding
from .vlm import VLContrastHead, VLContrastModel
from .loss import ClipLoss, SigLipLoss, BarlowTwinsLoss

from typing import Union, Optional
import torch
import os


def get_input_dtype(precision: str):
    input_dtype = None
    if precision in ("bf16", "pure_bf16"):
        input_dtype = torch.bfloat16
    elif precision in ("fp16", "pure_fp16"):
        input_dtype = torch.float16
    return input_dtype


def get_cast_dtype(precision: str):
    cast_dtype = None
    if precision == "bf16":
        cast_dtype = torch.bfloat16
    elif precision == "fp16":
        cast_dtype = torch.float16
    elif precision == "fp32":
        cast_dtype = torch.float32
    return cast_dtype


def create_model(
        text_model_name:Optional[str] = None, 
        vision_model_name:Optional[str] = None, 
        head_weights_path:Optional[str] = None,
        vision_dimesion:int = 1536,
        text_dimension:int = 768,
        target_dimension:int = 512,
        precision: str = 'fp32', 
        device: Union[str, torch.device] = 'cpu', 
        linear_type: str = 'linear',
        logit_scale: float = 10.0,
        logit_bias: float = -10.0,
        use_gmp: bool = False,
        gmp_groups: int = 512,
        test: bool = False,
):  
    if isinstance(device, str):
        device = torch.device(device)

    cast_dtype = get_cast_dtype(precision)
    if vision_model_name is not None and text_model_name is not None:
        model = VLContrastModel(text_model_name=text_model_name, vision_model_name=vision_model_name, target_dimension=target_dimension, vlhead_weights_path=head_weights_path,  linear_type=linear_type, cast_dtype=cast_dtype, use_gmp=use_gmp, gmp_groups=gmp_groups, test=test)
    else:
       model = VLContrastHead(vision_dimesion, text_dimension, target_dimension, linear_type=linear_type, cast_dtype=cast_dtype, logit_scale=logit_scale, logit_bias=logit_bias, use_gmp=use_gmp, gmp_groups=gmp_groups)
    model.to(device=device)
    return model


def create_loss(args):
    if args.siglip:
        print("Using SigLip loss")
        return SigLipLoss(
            rank=args.rank,
            world_size=args.world_size,
            diagonal_weight=args.diagonal_weight
        )
    elif args.barlowtwins:
        print("Using Barlow Twins loss")
        return BarlowTwinsLoss(
            rank=args.rank,
            world_size=args.world_size,
            lambda_param=args.lambda_param
        )
    else:
        print("Using Clip (infoNCE) loss")
        return ClipLoss(
            local_loss=args.local_loss,
            gather_with_grad=args.gather_with_grad,
            cache_labels=True,
            rank=args.rank,
            world_size=args.world_size,
            use_horovod=args.horovod,
        )
