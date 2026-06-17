"""
自动运行 ResNet50 和 Loss_Dice_Heavy 实验
"""
import subprocess
import time
import sys
from pathlib import Path

def run_experiment(config_path, name):
    """运行单个实验"""
    print(f"\n{'='*60}")
    print(f"开始实验: {name}")
    print(f"配置文件: {config_path}")
    print(f"{'='*60}\n")

    start_time = time.time()

    cmd = [sys.executable, "scripts/train.py", "--config", config_path]
    result = subprocess.run(cmd, cwd=Path(__file__).parent)

    elapsed = time.time() - start_time
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)

    print(f"\n{'='*60}")
    print(f"实验 {name} 完成!")
    print(f"耗时: {hours}小时 {minutes}分钟")
    print(f"{'='*60}\n")

    return result.returncode == 0

def main():
    experiments = [
        ("configs/ablations/resnet50.yaml", "ResNet50"),
        ("configs/ablations/loss_dice_heavy.yaml", "Loss_Dice_Heavy"),
    ]

    print("="*60)
    print("消融实验自动化脚本")
    print("="*60)

    total_start = time.time()

    for config_path, name in experiments:
        success = run_experiment(config_path, name)
        if not success:
            print(f"警告: {name} 实验可能未成功完成")

    total_elapsed = time.time() - total_start
    hours = int(total_elapsed // 3600)
    minutes = int((total_elapsed % 3600) // 60)

    print("\n" + "="*60)
    print("所有实验完成!")
    print(f"总耗时: {hours}小时 {minutes}分钟")
    print("="*60)

    print("\n实验结果汇总:")
    results_dir = Path("outputs")
    for name in ["ablation_resnet50", "ablation_loss_dice_heavy"]:
        result_path = results_dir / name / "history.csv"
        if result_path.exists():
            print(f"  {name}: 已完成")

if __name__ == "__main__":
    main()
