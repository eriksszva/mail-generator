FROM python:3.12-slim

# install build dependencies termasuk Rust
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && . "$HOME/.cargo/env"

# set working directory
WORKDIR /app

# copy requirements dan install
COPY ../requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt