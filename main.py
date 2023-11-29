import hydra
from omegaconf import DictConfig

@hydra.main(version_base=None, config_path=".", config_name="config.yaml")
def main(cfg: DictConfig):
  print(cfg.cohere.api_key)

if __name__ == "__main__":
  main()