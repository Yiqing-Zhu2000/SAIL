# follow import things added by yiqing
import sys
sys.path.append(".")

from transformers import AutoModel, AutoConfig, AutoTokenizer
from transformers.models.auto.configuration_auto import CONFIG_MAPPING
from transformers.models.auto.modeling_auto import MODEL_MAPPING
from transformers.models.auto.tokenization_auto import TOKENIZER_MAPPING
from transformers.tokenization_utils_base import PreTrainedTokenizerBase

# 导入你自己的配置和模型
from loadPreModels.nvidia.NV_Embed_v2.configuration_nvembed import NVEmbedConfig
from loadPreModels.nvidia.NV_Embed_v2.modeling_nvembed import NVEmbedModel

# 注册 config 和 model
CONFIG_MAPPING.register("nvembed", NVEmbedConfig)
MODEL_MAPPING.register(NVEmbedConfig, NVEmbedModel)

# 注册 dummy tokenizer（绕开 HuggingFace 要求）
class DummyTokenizer(PreTrainedTokenizerBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def _tokenize(self, text): return text.split()
    def _convert_token_to_id(self, token): return 0
    def _convert_id_to_token(self, index): return "<dummy>"
    def convert_tokens_to_string(self, tokens): return " ".join(tokens)

TOKENIZER_MAPPING.register(NVEmbedConfig, DummyTokenizer)

#######################

from model import create_model
from PIL import Image
import torch

# Path to the downloaded checkpoint
checkpoint_path = "./checkpoint/sail_dinov2l_nv2.pt"

# Create the model, change the text_model to `Alibaba-NLP/gte-large-en-v1.5` if use sail_dinov2_gte
# models are from local, so need ./xxx
model = create_model(
    text_model_name="./loadPreModels/nvidia/NV_Embed_v2",
    vision_model_name="./loadPreModels/facebook/dinov2-large",
    head_weights_path=checkpoint_path,
    target_dimension=1024,
)
model.eval()  # Set model to evaluation mode

# Prepare images and texts
image_processor = model.image_processor
texts = ["a dog", "a cat"]
dog_image = Image.open("asset/dog.jpg").convert("RGB")
cat_image = Image.open("asset/cat.jpg").convert("RGB")
images = image_processor(images=[dog_image, cat_image], return_tensors="pt")

# Generate features and probabilities
with torch.no_grad():
    image_features = model.encode_image(images, normalize=True)
    text_features = model.encode_text(texts, text_list=texts, normalize=True)
text_probs = (100.0 * image_features @ text_features.T).softmax(dim=-1)

# Print the label probabilities
print("Label probs:", text_probs)