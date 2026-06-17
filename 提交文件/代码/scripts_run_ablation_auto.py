#!/usr/bin/env python3
"""
消融实验自动执行脚本
自动运行所有消融实验并汇总结果
"""

import subprocess
import sys
import os
import pandas as pd
from datetime import datetime

# 实验配置
EXPERIMENTS = [
    ('Baseline', 'configs_baseline.yaml', 'outputs/baseline_unet_resnet34'),
    ('No_Augmentation', 'configs_ablation_no_augmentation.yaml', 'outputs/ablation_no_augmentation'),
    ('Strong_Augmentation', 'configs_optimization_aug_very_strong.yaml', 'outputs/ablation_strong_augmentation'),
    ('EfficientNet_B3', 'configs_optimization_efficientnet_b3.yaml', 'outputs/ablation_efficientnet_b3'),
    ('Loss_Dice_Heavy', 'configs_optimization_loss_dice_heavy.yaml', 'outputs/ablation_loss_dice_heavy'),
]

def run_experiment(name, config_path):
    """运行单个实验"""
    print(f"\n{'='*60}")
    print(f"[实验 {name}]")
    print(f"配置文件: {config_path}")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            ['python', 'scripts_train.py', '--config', config_path],
            check=True,
            text=True
        )
        print(f"\n[{name}] 训练完成!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[{name}] 训练失败: {e}")
        return False

def collect_results():
    """收集所有实验结果"""
    print("\n" + "="*60)
    print("收集实验结果...")
    print("="*60)
    
    results = []
    
    for name, _, output_path in EXPERIMENTS:
        history_path = os.path.join(output_path, 'history.csv')
        
        if os.path.exists(history_path):
            df = pd.read_csv(history_path)
            best_idx = df['val_dice'].idxmax()
            best_dice = df.loc[best_idx, 'val_dice']
            best_epoch = df.loc[best_idx, 'epoch']
            final_dice = df.iloc[-1]['val_dice']
            final_epoch = len(df)
            
            results.append({
                'experiment': name,
                'best_dice': f'{best_dice:.4f}',
                'best_epoch': int(best_epoch),
                'final_dice': f'{final_dice:.4f}',
                'total_epochs': int(final_epoch)
            })
            print(f"[{name}] Best Dice: {best_dice:.4f} (Epoch {best_epoch})")
        else:
            results.append({
                'experiment': name,
                'best_dice': 'N/A',
                'best_epoch': 'N/A',
                'final_dice': 'N/A',
                'total_epochs': 'N/A'
            })
            print(f"[{name}] 无结果文件")
    
    # 创建汇总DataFrame
    results_df = pd.DataFrame(results)
    
    # 打印汇总表
    print("\n" + "="*60)
    print("消融实验结果汇总")
    print("="*60)
    print(results_df.to_string(index=False))
    
    # 保存为CSV
    output_file = 'outputs/ablation_results_summary.csv'
    os.makedirs('outputs', exist_ok=True)
    results_df.to_csv(output_file, index=False)
    print(f"\n结果已保存到: {output_file}")
    
    # 保存为Markdown
    md_file = 'outputs/ablation_results_summary.md'
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# 消融实验结果汇总\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(results_df.to_markdown(index=False))
    print(f"Markdown已保存到: {md_file}")
    
    return results_df

def main():
    """主函数"""
    print("="*60)
    print("消融实验自动执行脚本")
    print("="*60)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"实验数量: {len(EXPERIMENTS)}")
    
    # 依次运行实验
    for i, (name, config_path, _) in enumerate(EXPERIMENTS):
        print(f"\n\n[{i+1}/{len(EXPERIMENTS)}] 准备运行: {name}")
        
        success = run_experiment(name, config_path)
        
        if not success:
            print(f"警告: {name} 训练失败，继续下一个实验...")
    
    # 收集并保存结果
    print("\n\n" + "="*60)
    print("所有实验完成!")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    collect_results()
    
    print("\n脚本执行完毕!")

if __name__ == '__main__':
    main()

