#!/bin/bash

set -euo pipefail

echo "Starting GPG installation and configuration..."

detect_package_manager() {
  if command -v apt &>/dev/null; then
    echo "apt"
  elif command -v dnf &>/dev/null; then
    echo "dnf"
  elif command -v yum &>/dev/null; then
    echo "yum"
  elif command -v pacman &>/dev/null; then
    echo "pacman"
  elif command -v zypper &>/dev/null; then
    echo "zypper"
  elif command -v emerge &>/dev/null; then
    echo "emerge"
  else
    echo ""
  fi
}

install_gnupg() {
  local pkg_manager="$1"

  echo "Installing gnupg..."
  case "$pkg_manager" in
  apt) sudo apt-get install -y gnupg ;;
  dnf) sudo dnf install -y gnupg2 ;;
  yum) sudo yum install -y gnupg2 ;;
  pacman) sudo pacman -Syu --noconfirm gnupg ;;
  zypper) sudo zypper install -y gpg2 ;;
  emerge) sudo emerge --ask=n app-crypt/gnupg ;;
  esac
}

configure_gpg_dir() {
  local gpg_dir="$HOME/.gnupg"
  [[ ! -d "$gpg_dir" ]] && mkdir -m 700 "$gpg_dir"
  gpg -k &>/dev/null
}

configure_shell_profile() {
  local shell_profile=""

  if [[ "$SHELL" == *"zsh"* ]]; then
    shell_profile="$HOME/.zshrc"
  elif [[ "$SHELL" == *"bash"* ]]; then
    shell_profile="$HOME/.bashrc"
  fi

  if [[ -n "$shell_profile" ]]; then
    if ! grep -q "GPG_TTY" "$shell_profile"; then
      echo "Adding GPG_TTY to $shell_profile..." >&2
      echo 'export GPG_TTY=$(tty)' >>"$shell_profile"
    fi
  fi

  echo "$shell_profile"
}

install_passtui() {
  echo "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh

  echo "Installing passtui..."
  uv tool install --python 3.14 passtui
}

main() {
  local pkg_manager
  pkg_manager="$(detect_package_manager)"

  if [[ -z "$pkg_manager" ]]; then
    echo "No supported package manager found. Please install gnupg manually."
    exit 1
  fi

  echo "Detected package manager: $pkg_manager"

  if ! command -v gpg &>/dev/null; then
    install_gnupg "$pkg_manager"
  else
    echo "gpg already installed, skipping."
  fi

  configure_gpg_dir

  gpgconf --kill gpg-agent

  local shell_profile
  shell_profile="$(configure_shell_profile)"

  install_passtui

  echo "Installation complete!"
  if [[ -n "$shell_profile" ]]; then
    echo "Please run: source $shell_profile"
    echo "OR, restart your terminal"
  fi
}

main
