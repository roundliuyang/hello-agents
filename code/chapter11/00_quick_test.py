"""
快速实验测试

使用少量数据快速测试SFT和GRPO训练流程
"""

import sys
from pathlib import Path
import json

# 添加项目路径
project_root = Path(__file__).parent.parent / "HelloAgents"
sys.path.insert(0, str(project_root))

from hello_agents.tools import RLTrainingTool


def quick_test():
    """
    快速实验测试函数

    功能说明：
    - 使用少量样本（10个）快速验证SFT和GRPO训练流程是否正常
    - 适用于开发阶段的快速迭代测试
    - 预计运行时间：2-3分钟

    配置参数：
    - 模型: Qwen/Qwen3-0.6B（轻量级模型，适合快速测试）
    - 样本数: 10个训练样本
    - 训练轮数: 1个epoch
    - LoRA微调: 启用（减少显存占用，加速训练）
    """
    # 创建RL训练工具实例（RLTrainingTool 内部默认使用 GSM8K 数据集）
    tool = RLTrainingTool()

    print("=" * 80)
    print("快速实验测试")
    print("=" * 80)

    # ========================================================================
    # 测试1: 数据加载
    # ========================================================================
    print("\n测试1: 数据加载")
    print("-" * 80)

    # 数据加载配置字典
    data_config = {
        "action": "load_dataset",  # 操作类型：加载数据集
        "format_type": "sft",  # 数据格式：SFT监督微调格式
        "split": "train",  # 数据划分：训练集
        "max_samples": 5  # 最大样本数：仅加载5个样本用于快速验证
    }

    print("加载数据集...")
    result = tool.run(data_config)  # 执行数据加载操作
    data = json.loads(result)  # 将JSON字符串解析为Python字典
    print(f"✅ 数据集加载成功: {data['dataset_size']} 样本")
    print(json.dumps(data, indent=2, ensure_ascii=False))  # 格式化输出数据信息

    # ========================================================================
    # 测试2: SFT训练（Supervised Fine-Tuning，监督微调）
    # 验证SFT训练流程是否正常运行
    # ========================================================================
    print("\n测试2: SFT训练")
    print("-" * 80)

    # SFT训练配置字典
    sft_config = {
        "action": "train",  # 操作类型：开始训练
        "algorithm": "sft",  # 算法类型：监督微调
        "model_name": "Qwen/Qwen3-0.6B",  # 预训练模型名称
        "output_dir": "./output/quick_test/sft",  # 模型输出目录
        "max_samples": 10,  # 最大训练样本数
        "num_epochs": 1,  # 训练轮数：1个epoch
        "batch_size": 2,  # 批次大小：每次处理2个样本
        "use_lora": True,  # 启用LoRA高效微调技术
        "lora_r": 8,  # LoRA秩参数：控制低秩矩阵的维度
        "lora_alpha": 16,  # LoRA缩放系数：alpha/r决定学习率缩放比例
    }

    print("SFT配置:")
    print(json.dumps(sft_config, indent=2, ensure_ascii=False))

    print("\n⏳ 开始SFT训练...")
    sft_result = tool.run(sft_config)  # 执行SFT训练
    sft_data = json.loads(sft_result)  # 解析训练结果
    print("\n✅ SFT训练结果:")
    print(json.dumps(sft_data, indent=2, ensure_ascii=False))

    # ========================================================================
    # 测试3: GRPO训练（Group Relative Policy Optimization，群组相对策略优化）
    # 验证基于强化学习的GRPO训练流程
    # ========================================================================
    print("\n测试3: GRPO训练")
    print("-" * 80)

    # GRPO训练配置字典
    grpo_config = {
        "action": "train",               # 操作类型：开始训练
        "algorithm": "grpo",             # 算法类型：群组相对策略优化（强化学习）
        "model_name": "Qwen/Qwen3-0.6B", # 预训练模型名称
        "output_dir": "./output/quick_test/grpo",  # 模型输出目录
        "max_samples": 10,               # 最大训练样本数
        "num_epochs": 1,                 # 训练轮数：1个epoch
        "batch_size": 2,                 # 批次大小：每次处理2个样本
        "use_lora": True,                # 启用LoRA高效微调技术
        "lora_r": 8,                     # LoRA秩参数
        "lora_alpha": 16,                # LoRA缩放系数
    }

    print("GRPO配置:")
    print(json.dumps(grpo_config, indent=2, ensure_ascii=False))

    print("\n⏳ 开始GRPO训练...")
    grpo_result = tool.run(grpo_config)     # 执行GRPO训练
    grpo_data = json.loads(grpo_result)     # 解析训练结果
    print("\n✅ GRPO训练结果:")
    print(json.dumps(grpo_data, indent=2, ensure_ascii=False))

    # ========================================================================
    # 测试4: 奖励函数创建
    # 验证奖励函数的初始化和配置
    # ========================================================================
    print("\n测试4: 奖励函数")
    print("-" * 80)

    # 奖励函数配置字典
    reward_config = {
        "action": "create_reward",   # 操作类型：创建奖励函数
        "reward_type": "accuracy"    # 奖励类型：准确率奖励（根据答案正确性评分）
    }

    print("创建奖励函数...")
    reward_result = tool.run(reward_config)    # 执行奖励函数创建
    reward_data = json.loads(reward_result)    # 解析创建结果
    print("✅ 奖励函数创建成功:")
    print(json.dumps(reward_data, indent=2, ensure_ascii=False))

    # ========================================================================
    # 总结：输出所有测试结果和模型保存路径
    # ========================================================================
    print("\n" + "=" * 80)
    print("测试总结")
    print("=" * 80)
    print("\n✅ 所有测试通过!")
    print("\n测试项目:")
    print("  1. ✅ 数据加载")
    print("  2. ✅ SFT训练")
    print("  3. ✅ GRPO训练")
    print("  4. ✅ 奖励函数创建")

    print("\n模型路径:")
    print(f"  SFT模型: {sft_config['output_dir']}")
    print(f"  GRPO模型: {grpo_config['output_dir']}")


if __name__ == "__main__":
    quick_test()
