#!/bin/bash

echo "Starting GPG2 installation and configuration..."

if ! command -v brew &>/dev/null; then
  echo "Homebrew not found. Please install it first at https://brew.sh/"
  exit 1
fi

echo "Installing gnupg and pinentry-mac..."
brew install gnupg pinentry-mac </dev/null

GPG_DIR="$HOME/.gnupg"
[[ ! -d "$GPG_DIR" ]] && mkdir -m 700 "$GPG_DIR"

BREW_PREFIX=$(brew --prefix)
AGENT_CONF="$GPG_DIR/gpg-agent.conf"

echo "Configuring gpg-agent.conf..."
echo "pinentry-program $BREW_PREFIX/bin/pinentry-mac" >"$AGENT_CONF"

SHELL_PROFILE=""
if [[ "$SHELL" == *"zsh"* ]]; then
  SHELL_PROFILE="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
  SHELL_PROFILE="$HOME/.bashrc"
fi

if [ -n "$SHELL_PROFILE" ]; then
  if ! grep -q "GPG_TTY" "$SHELL_PROFILE"; then
    echo "Adding GPG_TTY to $SHELL_PROFILE..."
    echo "export GPG_TTY=$(tty)" >>"$SHELL_PROFILE"
  fi
fi

gpgconf --kill gpg-agent
gpg -k &>/dev/null

if ! command -v gpg2 &>/dev/null; then
  echo "gpg2 not found, creating symlink..."
  ln -s "$(which gpg)" "$BREW_PREFIX/bin/gpg2"
fi

echo "Installing passtui"
curl -LsSf https://astral.sh/uv/install.sh | sh

uv tool install --python 3.14 passtui

echo "Installation complete!"
echo "Please run: source $SHELL_PROFILE"
echo "OR, restart your terminal"
