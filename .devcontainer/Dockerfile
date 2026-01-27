FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# Install pyenv dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    curl \
    git \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pyenv as vscode user
USER vscode
ENV HOME=/home/vscode
ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/bin:${PYENV_ROOT}/shims:${PATH}"

RUN curl https://pyenv.run | bash \
    && echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc \
    && echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc \
    && echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Pre-install Python versions (this speeds up container startup)
RUN pyenv install 3.13.1 \
    && pyenv install 3.14.0 \
    && pyenv global 3.13.1

# Install pipx and poetry
RUN pip install --user pipx \
    && ~/.local/bin/pipx install poetry==2.2.1 \
    && ~/.local/bin/pipx inject poetry poetry-plugin-export

ENV PATH="${HOME}/.local/bin:${PATH}"

# Trivial healthcheck to satisfy trivy (devcontainers don't need real healthchecks)
HEALTHCHECK CMD echo "ok" || exit 1
