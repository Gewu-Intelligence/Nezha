import os
import csv
from admet_ai import ADMETModel
import argparse

def run():
    parser = argparse.ArgumentParser(description="run docking")
    parser.add_argument("--smiles_file", type=str, help="smiles")
    parser.add_argument("--output_dir",default="admet",help="")
    args = parser.parse_args()
    #smiles_list = ["CCO", "c1ccccc1", "CC(=O)Oc1ccccc1C(=O)O"] # 乙醇、苯、阿司匹林

    with open(args.smiles_file) as inf:
        lines = inf.readlines()
    smiles_list = [line.strip() for line in lines]

    output_dir = args.output_dir

    os.makedirs(f"{output_dir}",exist_ok=True)

    # 1. 初始化模型 (第一次运行会下载预训练权重)
    model = ADMETModel()

    # 2. 准备 SMILES 列表
    

    # 3. 进行预测
    # model.predict 接受单个 SMILES 或 SMILES 列表
    results = model.predict(smiles=smiles_list)

    # 4. 查看结果
    # 结果是一个 Pandas DataFrame，包含了数十种 ADMET 指标
    print(results.head())

    # 5. 保存结果
    results.to_csv(f"{output_dir}/admet_predictions.csv", index=False)

if __name__ == "__main__":
    run()