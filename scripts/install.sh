#!/bin/bash

echo "Starting GPG2 installation and configuration..."

# 1. Install GPG and Pinentry-Mac via Homebrew
if ! command -v brew &>/dev/null; then
  echo "Homebrew not found. Please install it first at https://brew.sh/"
  exit 1
fi

echo "Installing gnupg and pinentry-mac..."
brew install gnupg pinentry-mac

# 2. Configure GPG Agent for macOS Keychain support
GPG_DIR="$HOME/.gnupg"
mkdir -m 700 -p "$GPG_DIR"

# Get the correct Homebrew prefix for Intel or Apple Silicon
BREW_PREFIX=$(brew --prefix)
AGENT_CONF="$GPG_DIR/gpg-agent.conf"

echo "Configuring gpg-agent.conf..."
echo "pinentry-program $BREW_PREFIX/bin/pinentry-mac" >"$AGENT_CONF"

# 3. Add GPG_TTY to shell profile (supports Zsh and Bash)
SHELL_PROFILE=""
if [[ "$SHELL" == *"zsh"* ]]; then
  SHELL_PROFILE="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
  SHELL_PROFILE="$HOME/.bash_profile"
fi

if [ -n "$SHELL_PROFILE" ]; then
  if ! grep -q "GPG_TTY" "$SHELL_PROFILE"; then
    echo "Adding GPG_TTY to $SHELL_PROFILE..."
    echo "export GPG_TTY=$(tty)" >>"$SHELL_PROFILE"
  fi
fi

# 4. Restart the agent to apply changes
gpgconf --kill gpg-agent
gpg -k &>/dev/null

if ! command -v gpg2 &>/dev/null; then
  echo "gpg2 not found, creating symlink..."
  ln -s "$(which gpg)" "$BREW_PREFIX/bin/gpg2"
fi

# 5. Install uv and passtuy
echo "Installing passtui"
curl -LsSf https://astral.sh/uv/install.sh | sh

uv tool install --python 3.14 passtui

echo "Installation complete!"
echo "Please run: source $SHELL_PROFILE"
echo "OR, restart your terminal"
