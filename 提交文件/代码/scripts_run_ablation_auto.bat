@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ============================================
echo 关键消融实验批量运行脚本
echo ============================================
echo.

set EXPERIMENTS[0]=configs_baseline.yaml
set EXPERIMENTS[1]=configs_ablation_no_augmentation.yaml
set EXPERIMENTS[2]=configs_optimization_aug_very_strong.yaml
set EXPERIMENTS[3]=configs_optimization_efficientnet_b3.yaml
set EXPERIMENTS[4]=configs_optimization_loss_dice_heavy.yaml

set EXP_NAMES[0]=Baseline
set EXP_NAMES[1]=No_Augmentation
set EXP_NAMES[2]=Strong_Augmentation
set EXP_NAMES[3]=EfficientNet_B3
set EXP_NAMES[4]=Loss_Dice_Heavy

set TOTAL=5
set CURRENT=0

for /L %%i in (0,1,4) do (
    set idx=%%i
    echo [%%i+1/!TOTAL!] 运行 !EXP_NAMES[%%i]!...
    echo 开始时间: !date! !time!
    
    python scripts_train.py --config !EXPERIMENTS[%%i]!
    
    if !ERRORLEVEL! NEQ 0 (
        echo !EXP_NAMES[%%i]! 训练失败！
        echo 继续下一个实验...
    ) else (
        echo !EXP_NAMES[%%i]! 完成！
    )
    echo.
)

echo ============================================
echo 所有消融实验完成！
echo 汇总结果...
echo ============================================
echo.

python -c "
import pandas as pd
import os
import json
from datetime import datetime

results = []
experiments = [
    ('Baseline', 'outputs/baseline_unet_resnet34'),
    ('No_Augmentation', 'outputs/ablation_no_augmentation'),
    ('Strong_Augmentation', 'outputs/ablation_strong_augmentation'),
    ('EfficientNet_B3', 'outputs/ablation_efficientnet_b3'),
    ('Loss_Dice_Heavy', 'outputs/ablation_loss_dice_heavy')
]

for name, path in experiments:
    history_path = f'{path}/history.csv'
    config_path = f'{path}/config.yaml'
    
    if os.path.exists(history_path):
        df = pd.read_csv(history_path)
        best_idx = df['val_dice'].idxmax()
        best_dice = df.loc[best_idx, 'val_dice']
        best_epoch = df.loc[best_idx, 'epoch']
        final_dice = df.iloc[-1]['val_dice']
        final_epoch = len(df)
    else:
        best_dice = 'N/A'
        best_epoch = 'N/A'
        final_dice = 'N/A'
        final_epoch = 'N/A'
    
    results.append({
        'experiment': name,
        'best_dice': best_dice,
        'best_epoch': best_epoch,
        'final_dice': final_dice,
        'total_epochs': final_epoch
    })

results_df = pd.DataFrame(results)
print('\n消融实验结果汇总：')
print('=' * 70)
print(results_df.to_string(index=False))
print('=' * 70)

# 保存为CSV
results_df.to_csv('outputs/ablation_results_summary.csv', index=False)
print('\n结果已保存到: outputs/ablation_results_summary.csv')
"

echo.
echo 按任意键退出...
pause >nul

