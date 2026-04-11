[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL3 License][license-shield]][license-url]

<div align="center">
  <h3 align="center">PassTUI</h3>
  <p align="center">
    The TUI for <strong>pass</strong> — the standard Unix password manager.
  </p>
  <img width="800" alt="passtui" src="https://github.com/user-attachments/assets/07f4b435-ad19-4128-852f-e6b5ee78a265" />
</div>

---

## About

`PassTUI` is a terminal UI for [pass](https://www.passwordstore.org/), the standard Unix password manager. It gives you a keyboard-driven, visual way to browse and manage your GPG-encrypted password store without ever leaving the terminal.

If you live in the terminal and want a faster, more intuitive way to work with your passwords, this is for you.

### Built With

![Python][python-shield]
![Textual][textual-shield]
![passpy][passpy-shield]

---

## Features

- Browse your password store in a tree view
- Search and filter passwords in real time
- View and edit password entries in a built-in editor
- Copy the password to clipboard with a single keystroke
- Copy the username to clipboard with a single keystroke
- Copy any line to clipboard
- Create a new GPG key and password store from scratch
- Add new password entries
- Sync the password store with a remote Git repository
- Export your GPG key to a file
- Import a GPG key and re-encrypt the store

---

## Getting Started

### Prerequisites

`pass` relies on GPG for encryption, so `gpg` needs to be installed on your system.

**Ubuntu / Debian**

```bash
sudo apt install gnupg
```

**CentOS / Fedora**

```bash
sudo yum install gnupg
```

**openSUSE**

```bash
sudo zypper install gpg2
```

**Gentoo**

```bash
emerge --ask app-crypt/gnupg
```

**Arch**

```bash
sudo pacman -Syu gnupg
```

**macOS**

> macOS doesn't ship with a default GPG setup. There's a script that handles the most common configuration, but if it doesn't work for your setup you'll need to install the prerequisites manually.

```bash
curl -LsSf https://raw.githubusercontent.com/fjmoralesp/passtui/main/scripts/install.sh | sh
```

<details>
  <summary>Click to see manual installation instructions</summary>

1. Install gnupg and pinentry-mac: `brew install gnupg pinentry-mac`
2. Create the keyring folder: `gpg -k`
3. Configure pinentry: `echo "pinentry-program $(brew --prefix)/bin/pinentry-mac" > "$HOME/.gnupg/gpg-agent.conf"`
4. Add GPG terminal detection to your shell config (~/.zshrc or ~/.bashrc): `export GPG_TTY=$(tty)`
5. Create a gpg2 binary symlink: `ln -s "$(which gpg)" "$(brew --prefix)/bin/gpg2"`
6. Restart the GPG agent: `gpgconf --kill gpg-agent`

</details>

### Installation

PassTUI is installed via [uv](https://docs.astral.sh/uv/).

Install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install passtui:

```bash
uv tool install --python 3.14 passtui
```

Then launch it:

```bash
passtui
```

---

## Usage

### Create a GPG Store

If you don't have a password store yet, PassTUI can create the GPG key and initialise everything for you in one step.

1. Launch PassTUI: `passtui`
2. Press `g` to open the **Create GPG Store** dialog
3. Fill in your **name** and **email**
4. Press `Enter` to confirm

PassTUI will generate a 4096-bit RSA key and initialise the store at `~/.password-store` (or wherever `PASSWORD_STORE_DIR` points).

> **Tip:** You can set the `PASSWORD_STORE_DIR` environment variable before launching PassTUI to use a different store location.

### Add a New Password

1. Press `n` to open a blank entry in the editor
2. Fill in your password, username, URL, and any extra notes following the template:

   ```
   (your password)
   Username: your-username
   Url: https://example.com
   ```

3. Press `Ctrl+S` to save
4. When prompted, enter the path for the new entry (e.g., `email/gmail`)

> **Tip:** The first line is always the password. PassTUI (and `pass`) will only copy the first line when you use the copy-password shortcut.

### View an Existing Password

1. Navigate the tree with `j` / `k` (or arrow keys)
2. Expand a folder with `Enter`
3. Select an entry — its decrypted contents will appear in the editor panel on the right
4. Press `e` to move focus to the editor
5. From the editor you can:
   - Press `c` to copy the **password** to the clipboard
   - Press `b` to copy the **username** to the clipboard
   - Press `y` to copy the **current line** to the clipboard
   - Press `i` to enter edit mode and make changes
   - Press `Ctrl+S` to save any edits

### Sync with a Git Repository

PassTUI can push and pull your password store to/from a remote Git repository.

**First-time setup (new store)**

1. Press `s` to trigger a sync
2. When prompted, enter the remote repository URL (e.g., `git@github.com:user/passwords.git`)
3. PassTUI will initialise a Git repo, add the remote, and push

**Subsequent syncs (store already has Git)**

1. Press `s`
2. PassTUI will pull with rebase and then push automatically

> **Note:** This workflow is designed for stores created fresh. If your store was cloned from an existing remote, handle the initial Git setup outside of PassTUI.

### Export a GPG Key

Exporting your GPG key lets you back it up or move it to another machine.

1. Press `x` to open the **Export GPG Key** dialog
2. Enter your GPG key **passphrase**
3. Optionally enter a custom **output path** (defaults to `~/passtui/gpg-export.asc`)
4. Press `Enter` to export

The key will be saved as an ASCII-armored `.asc` file.

> **Warning:** Keep this file somewhere safe. Anyone with access to it and your passphrase can decrypt your passwords.

### Import a GPG Key

Importing a GPG key lets you move your password store to a new machine or add a new trusted key.

1. Press `z` to open the **Import GPG Key** dialog
2. Enter the **path** to the `.asc` key file (e.g., `~/passtui/gpg-export.asc`)
3. Press `Enter` to import

PassTUI will import the key, mark it as ultimately trusted, update the store's `.gpg-id`, and re-encrypt all entries.

---

## Keybindings

### Global

| Key | Action                   |
| --- | ------------------------ |
| `/` | Focus the search bar     |
| `n` | Add a new password entry |
| `e` | Focus the editor panel   |
| `t` | Focus the password tree  |
| `s` | Sync with Git            |
| `g` | Create a new GPG Store   |
| `x` | Export GPG key           |
| `z` | Import GPG key           |

### Password Tree (`T` panel)

| Key       | Action                       |
| --------- | ---------------------------- |
| `j` / `↓` | Move cursor down             |
| `k` / `↑` | Move cursor up               |
| `h`       | Scroll left                  |
| `l`       | Scroll right                 |
| `Enter`   | Expand folder / select entry |
| `c`       | Copy password to clipboard   |
| `b`       | Copy username to clipboard   |

### Editor (`E` panel)

| Key      | Action                         |
| -------- | ------------------------------ |
| `i`      | Enter edit mode                |
| `Escape` | Cancel / exit edit mode        |
| `j`      | Move cursor down               |
| `k`      | Move cursor up                 |
| `h`      | Move cursor left               |
| `l`      | Move cursor right              |
| `c`      | Copy password to clipboard     |
| `b`      | Copy username to clipboard     |
| `y`      | Copy current line to clipboard |
| `Ctrl+S` | Save changes                   |

---

## Roadmap

- [x] Route all passphrase prompts through `pinentry` for better security
- [ ] Config file
- [ ] Vi motions for password editor
- [ ] Custom keybindings
- [ ] Imports
  - [ ] 1Password txt or 1pif data
  - [ ] KeePass KeepassX XML / CSV data
  - [ ] Figaro's Password Manager XML data
  - [ ] LastPass CSV data
  - [ ] Ked Password Manager data
  - [ ] Revelation Password Manager data
  - [ ] Password Gorilla data
  - [ ] PWSafe data
  - [ ] KWallet data
  - [ ] Roboform data
  - [ ] password-exporter data
  - [ ] pwsafe data

See the [open issues](https://github.com/fjmoralesp/passtui/issues) for a full list of proposed features and known bugs.

---

## Contributing

Contributions, issues, and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup instructions.

---

## License

Distributed under the GNU General Public License v3. See `LICENSE` for more information.

---

## Contact

Francisco Morales — <fjmoralesp@outlook.com>

Project Link: [https://github.com/fjmoralesp/passtui](https://github.com/fjmoralesp/passtui)

---

[contributors-shield]: https://img.shields.io/github/contributors/fjmoralesp/passtui?style=for-the-badge
[contributors-url]: https://github.com/fjmoralesp/passtui/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/fjmoralesp/passtui?style=for-the-badge
[forks-url]: https://github.com/fjmoralesp/passtui/network/members
[stars-shield]: https://img.shields.io/github/stars/fjmoralesp/passtui?style=for-the-badge
[stars-url]: https://github.com/fjmoralesp/passtui/stargazers
[issues-shield]: https://img.shields.io/github/issues/fjmoralesp/passtui?style=for-the-badge
[issues-url]: https://github.com/fjmoralesp/passtui/issues
[license-shield]: https://img.shields.io/github/license/fjmoralesp/passtui?style=for-the-badge
[license-url]: https://github.com/fjmoralesp/passtui/blob/main/LICENSE
[python-shield]: https://img.shields.io/badge/Python-gray?style=for-the-badge&logo=python
[textual-shield]: https://img.shields.io/badge/Textual-gray?style=for-the-badge&logo=python
[passpy-shield]: https://img.shields.io/badge/passpy-gray?style=for-the-badge&logo=gnuprivacyguard
