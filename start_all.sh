#!/bin/bash

# 先激活环境
source "$(conda info --base)/etc/profile.d/conda.sh" && conda activate huntianling

# 激活工具
source /opt/gromacs/bin/GMXRC && source /opt/intel/oneapi/setvars.sh --force

# 启动opencode（后台运行）
/app/huntianling/opencode-linux-x64/bin/opencode web --hostname 0.0.0.0 --port 3000 &

# 启动画布的前后端服务（后台运行）
/bin/bash /app/huntianling/opencode_canvas/start_drug_design.sh &

# 保底进程，防止容器退出
tail -f /dev/null &

# 保持脚本运行，防止容器退出
wait
