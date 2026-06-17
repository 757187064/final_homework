"""
监控 ResNet50 训练，完成后自动启动 Loss_Dice_Heavy
"""
import subprocess
import time
import sys
from pathlib import Path

def check_resnet50_complete():
    """检查 ResNet50 是否完成"""
    history_path = Path("outputs/ablation_resnet50/history.csv")
    if not history_path.exists():
        return False

    with history_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    if len(lines) < 2:
        return False

    # 获取最后一个 epoch
    last_line = lines[-1].strip()
    if not last_line:
        return False

    parts = last_line.split(",")
    if len(parts) >= 2:
        last_epoch = int(parts[0])
        total_epochs = 25
        return last_epoch >= total_epochs

    return False

def run_loss_dice_heavy():
    """运行 Loss_Dice_Heavy 实验"""
    print("\n" + "="*60)
    print("ResNet50 完成! 开始 Loss_Dice_Heavy 实验...")
    print("="*60 + "\n")

    start_time = time.time()

    cmd = [sys.executable, "scripts_train.py", "--config", "configs_optimization_loss_dice_heavy.yaml"]
    result = subprocess.run(cmd, cwd=Path(__file__).parent)

    elapsed = time.time() - start_time
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)

    print("\n" + "="*60)
    print("Loss_Dice_Heavy 实验完成!")
    print(f"耗时: {hours}小时 {minutes}分钟")
    print("="*60)

    return result.returncode == 0

def main():
    print("监控脚本已启动...")
    print("等待 ResNet50 训练完成 (25 epochs)...")

    check_interval = 60  # 每60秒检查一次
    max_wait_hours = 4  # 最多等待4小时

    start_time = time.time()
    max_wait_seconds = max_wait_hours * 3600

    while True:
        if check_resnet50_complete():
            print("\n检测到 ResNet50 训练完成!")
            run_loss_dice_heavy()
            print("\n所有实验完成!")
            break

        elapsed = time.time() - start_time
        if elapsed > max_wait_seconds:
            print("\n超时，停止监控")
            break

        # 获取当前进度
        history_path = Path("outputs/ablation_resnet50/history.csv")
        if history_path.exists():
            with history_path.open("r", encoding="utf-8") as f:
                lines = f.readlines()
            if len(lines) > 1:
                last_line = lines[-1].strip()
                if last_line:
                    parts = last_line.split(",")
                    if len(parts) >= 2:
                        current_epoch = int(parts[0])
                        print(f"\r当前进度: Epoch {current_epoch}/25, 已等待 {int(elapsed//60)} 分钟", end="")

        time.sleep(check_interval)

if __name__ == "__main__":
    main()

