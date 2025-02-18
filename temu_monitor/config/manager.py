# 移除对dotenv模块的依赖
class ConfigManager:
    def get(self, key):
        raise KeyError(f"Unknown configuration key: {key}")  # 如果调用此方法，抛出异常
