from transformers import AutoModel

# # 6.28 I tried this, it works!
# try:
#     model = AutoModel.from_pretrained("./loadPreModels/facebook/dinov2-large")
#     print("✅ 模型成功加载")
# except Exception as e:
#     print("❌ 加载失败：", e)

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


# OKK! GOOD!