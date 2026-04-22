FROM condaforge/mambaforge

# Avoid interactive prompts (tzdata, etc.)
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV MAMBA_NO_BANNER=1

# System dependencies
RUN apt-get update && apt-get install -y \
    git \
    openjdk-17-jdk \
    wget \
    unzip \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

COPY environment.yml /tmp/environment.yml

    
RUN mamba env create -f /tmp/environment.yml

# Activate by default
ENV CONDA_DEFAULT_ENV=risk
ENV PATH=/opt/conda/envs/risk/bin:$PATH

RUN python -m ipykernel install --name risk --display-name "Python (risk)"

# Default shell
SHELL ["/bin/bash", "-c"]
RUN echo "conda activate risk" >> ~/.bashrc
