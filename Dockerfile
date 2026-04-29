############ STAGE 1: 使用 devel 镜像编译 GROMACS ###############
FROM nvidia/cuda:12.8.0-devel-ubuntu22.04 AS gromacs-builder

ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"]

# 仅安装编译 GROMACS 所需工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    git \
    cmake \
    gcc \
    g++ \
    ssh \
    && rm -rf /var/lib/apt/lists/*

# 安装 Intel OneAPI（用于 MPI 编译）
RUN wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB \
    | gpg --dearmor | tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null
RUN echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | tee /etc/apt/sources.list.d/oneAPI.list
RUN apt-get update && apt-get install -y intel-oneapi-base-toolkit && rm -rf /var/lib/apt/lists/*

# 下载并编译 GROMACS
# RUN wget https://ftp.gromacs.org/gromacs/gromacs-2023.tar.gz
RUN mkdir -p -m 0700 ~/.ssh && \
    ssh-keyscan github.com >> ~/.ssh/known_hosts
RUN git config --global http.proxy $HTTP_PROXY && \
    git config --global https.proxy $HTTPS_PROXY && \
    git clone https://github.com/golab-ai/gromacs-fep.git
# RUN --mount=type=ssh git clone git@github.com:golab-ai/gromacs-fep.git

RUN echo hello
RUN source /opt/intel/oneapi/setvars.sh --force && \
    cd gromacs-fep && \
    mkdir build && cd build && \
    cmake .. \
        -DGMX_BUILD_OWN_FFTW=ON \
        -DREGRESSIONTEST_DOWNLOAD=OFF \
        -DCMAKE_INSTALL_PREFIX=/opt/gromacs \
        -DGMX_MPI=ON \
        -DCMAKE_C_COMPILER=/opt/intel/oneapi/mpi/2021.17/bin/mpicc \
        -DCMAKE_CXX_COMPILER=/opt/intel/oneapi/mpi/2021.17/bin/mpicxx \
        -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda \
        -DGMX_GPU=CUDA && \
    make -j 8 && make install

############### INSTALL LAMMPS ###############
RUN wget https://github.com/lammps/lammps/archive/refs/tags/stable_22Jul2025_update4.tar.gz
RUN apt-get update &&  apt-get install -y cmake  python3
RUN tar -xvf stable_22Jul2025_update4.tar.gz && \
    cd lammps-stable_22Jul2025_update4/  && \
    mkdir build-gpu  && \
    cd build-gpu   && \
    source /opt/intel/oneapi/setvars.sh  && \
    cmake -C ../cmake/presets/basic.cmake \
          -C ../cmake/presets/kokkos-cuda.cmake \
          -D CMAKE_INSTALL_PREFIX=/opt/lammps \
          -D PKG_KOKKOS=on \
          -D PKG_GPU=on \
          -D GPU_API=cuda \
          -D GPU_ARCH=sm_89 \
          -D Kokkos_ARCH_ADA89=ON \
          -D CMAKE_C_COMPILER=/opt/intel/oneapi/mpi/2021.17/bin/mpicc \
          -D CMAKE_CXX_COMPILER=/opt/intel/oneapi/mpi/2021.17/bin/mpicxx \
          -D PKG_KSPACE=on \
          -D PKG_MOLECULE=on \
          -D PKG_RIGID=on \
          -D PKG_CLASS2=on \
          -D PKG_EXTRA_PAIR=on \
          -D PKG_MC=on \
          ../cmake
RUN cd lammps-stable_22Jul2025_update4/build-gpu && source /opt/intel/oneapi/setvars.sh && make -j 8 && make install
 
 
############ STAGE 2: 基于 runtime 镜像打包其他功能 ###############
FROM nvidia/cuda:12.8.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/root/miniconda3/bin:${PATH}"
SHELL ["/bin/bash", "-c"]


RUN echo hello
RUN apt-get update
RUN apt-get install -y wget gpg-agent
RUN wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB \
    | gpg --dearmor | tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null
RUN echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | tee /etc/apt/sources.list.d/oneAPI.list
RUN apt-get update &&  apt install -y intel-oneapi-mkl intel-oneapi-mpi

# 从 builder 复制已编译的 GROMACS / LAMMPS
COPY --from=gromacs-builder /opt/gromacs /opt/gromacs
COPY --from=gromacs-builder /opt/lammps /opt/lammps

############ INSTALL BASE TOOLS ###############
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    git \
    vim \
    libgomp1


############ INSTALL MINICONDA ###############
ARG CONDA_INSTALLER=Miniconda3-py310_23.11.0-1-Linux-x86_64.sh
ARG CONDA_URL=https://repo.anaconda.com/miniconda/${CONDA_INSTALLER}
ARG CONDA_SHA256=6581658486be8e700d77e24eccafba586a0fbafafadcf73d35ab13eaee4b80b1
RUN wget --quiet ${CONDA_URL} -O /root/miniconda.sh && \
    echo "${CONDA_SHA256}  /root/miniconda.sh" | sha256sum -c - && \
    /bin/bash /root/miniconda.sh -b -p /root/miniconda3 && \
    rm /root/miniconda.sh && \
    /root/miniconda3/bin/conda init bash && \
    /root/miniconda3/bin/conda config --set auto_update_conda false

############# INSTALL OPENCODE-AI ###############
#RUN curl -fsSL https://opencode.ai/install | bash

############ INSTALL CONDA ENV HUNTIANLING ###############
COPY environment.yaml .
RUN conda env create -f environment.yaml

# Install RXNG
RUN conda create -n rxngraphormer python=3.10 -y
RUN git clone -b pytorch2 https://github.com/licheng-xu-echo/RXNGraphormer.git
RUN conda run -n rxngraphormer pip install torch==2.2.1 --index-url https://download.pytorch.org/whl/cu121 && \
    conda run -n rxngraphormer pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.2.0+cu121.html && \
    conda run -n rxngraphormer pip install modelscope rdkit==2024.3.2 ipykernel pandas python-box OpenNMT-py==1.2.0 torchdata==0.7.1 torch_geometric rxnmapper localmapper transformers==4.30.0 numpy==1.26.4 scikit-learn && \
    cd RXNGraphormer/ && conda run -n rxngraphormer pip install .

RUN conda clean -afy

# 配置环境：GROMACS 与 Intel OneAPI 从 builder 复制，路径已变更
RUN echo "source /opt/gromacs/bin/GMXRC" >> /root/.bashrc && \
    echo "source /opt/intel/oneapi/setvars.sh --force" >> /root/.bashrc && \
    echo "conda activate huntianling" >> /root/.bashrc

############ Craton  ############
RUN apt-get install -y ssh
RUN mkdir -p -m 0700 ~/.ssh && \
    ssh-keyscan github.com >> ~/.ssh/known_hosts
# ARG CRATON_COMMIT
# RUN echo "Craton commit: ${CRATON_COMMIT}"
# RUN --mount=type=ssh cd /opt && git clone git@github.com:golab-ai/craton.git
# COPY ./craton /opt/craton
RUN git clone https://github.com/golab-ai/craton.git 
RUN mv craton /opt/ && cd /opt/craton && conda run -n huntianling pip install -e .

############ Huntianling Skills ############
RUN apt install -y zip libxrender1 libxext6
# RUN curl -fsSL https://bun.sh/install | bash

############ INSTALL NGINX ###############
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    && rm -rf /var/lib/apt/lists/*

COPY opencode_canvas.conf /etc/nginx/conf.d/opencode_canvas.conf

## canvas service ##
COPY opencode_canvas/backend/requirements.txt .
RUN conda create -n canvas_api python=3.10 -y && \
    conda run -n canvas_api pip install --no-cache-dir \
    -r requirements.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ./ /app/huntianling

RUN chown -R www-data:www-data /app/huntianling/opencode_canvas/dist && \
    chmod -R 755 /app/huntianling/opencode_canvas/dist

## OPENCODE ##
# COPY ./opencode /app/service
# If you want the original version of opencode code, use the following command. 
# RUN curl -fsSL https://opencode.ai/install | bash

RUN rm -rf /var/lib/apt/lists/*

##### Addition ##### (should add to environment.yaml later)
# RUN conda run -n huntianling pip install modelscope 

### lampmps envi
# 配置环境：GROMACS 与 Intel OneAPI 从 builder 复制，路径已变更
RUN echo "source  /opt/lammps/etc/profile.d/lammps.sh" >> /root/.bashrc && \
    echo "export PATH=\"/opt/lammps/bin:$PATH\"" >> /root/.bashrc


RUN chmod +x /app/huntianling/start_all.sh
CMD ["/bin/bash", "/app/huntianling/start_all.sh"]

# 
