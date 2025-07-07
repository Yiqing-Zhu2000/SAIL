from huggingface_hub import snapshot_download
import os

# 本地保存路径
save_root = "./loadPreModels"
os.makedirs(save_root, exist_ok=True)

# 下载 dinov2-large 到指定路径，保留可识别路径名
snapshot_download(
    repo_id="facebook/dinov2-large",
    cache_dir=save_root,
    local_dir=os.path.join(save_root, "facebook/dinov2-large"),
    local_dir_use_symlinks=False
)

print("✅ vision model 'facebook/dinov2-large' downloaded to ./loadPreModels/facebook/dinov2-large")


# 创建父文件夹（如不存在）
os.makedirs(save_root, exist_ok=True)

# 下载模型并转换为可直接使用的目录结构
snapshot_download(
    repo_id="nvidia/NV-Embed-v2",
    cache_dir=save_root,  # 临时缓存区
    local_dir=os.path.join(save_root, "nvidia/NV-Embed-v2"),          # 最终保存结构
    local_dir_use_symlinks=False, # 拷贝真实文件，非软连接
   # trust_remote_code=True        # 允许加载自定义模型代码（该模型需要）
)
print("✅ text model 'nvidia/NV-Embed-v2' downloaded to ./loadPreModels/nvidia/NV-Embed-v2")
