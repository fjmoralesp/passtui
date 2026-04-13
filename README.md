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

`PassTUI` is a terminal UI for [pass](https://www.passwordstore.org/), the standard Unix password manager. Browse and manage your GPG-encrypted password store without leaving the terminal.

### Built With

![Python][python-shield]
![Textual][textual-shield]
![passpy][passpy-shield]

---

## Features

- Tree view for browsing your password store
- Real-time search and filter
- Built-in editor to view and edit entries
- Copy password, username, or any line to clipboard
- Create a GPG key and password store from scratch
- Add new password entries
- Sync with a remote Git repository
- Export and import GPG keys

---

## Getting Started

### Installation

**Linux**

> This script handles detection of your distro's package manager and the full setup. If it doesn't cover your case, see the manual steps below.

```bash
curl -LsSf https://raw.githubusercontent.com/fjmoralesp/passtui/main/scripts/install-linux.sh | sh
```

<details>
  <summary>Manual installation</summary>

**Ubuntu / Debian**

```bash
sudo apt install gnupg
```

**CentOS / Fedora**

```bash
sudo dnf install gnupg2
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

**Configure gpg**

1. Create the keyring folder: `gpg -k`
2. Add GPG terminal detection to your shell config (~/.zshrc or ~/.bashrc): `export GPG_TTY=$(tty)`

</details>

**macOS**

> macOS doesn't ship with GPG. The following script handles the common setup, but if it doesn't work for your case, see the manual steps below.

```bash
curl -LsSf https://raw.githubusercontent.com/fjmoralesp/passtui/main/scripts/install.sh | sh
```

<details>
  <summary>Manual installation</summary>

1. Install gnupg and pinentry-mac: `brew install gnupg pinentry-mac`
2. Create the keyring folder: `gpg -k`
3. Configure pinentry: `echo "pinentry-program $(brew --prefix)/bin/pinentry-mac" > "$HOME/.gnupg/gpg-agent.conf"`
4. Add GPG terminal detection to your shell config (~/.zshrc or ~/.bashrc): `export GPG_TTY=$(tty)`
5. Create a gpg2 binary symlink: `ln -s "$(which gpg)" "$(brew --prefix)/bin/gpg2"`
6. Restart the GPG agent: `gpgconf --kill gpg-agent`

</details>

### Installation without GPG

If you prefer to handle GPG yourself and only install PassTUI, make sure you have the following in place first:

- `gpg2`
- A `pinentry` program (e.g., `pinentry-curses`, `pinentry-gtk2`, `pinentry-mac`)

Then install via [uv](https://docs.astral.sh/uv/):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install --python 3.14 passtui
passtui
```

---

## Usage

### Create a GPG Store

No password store yet? PassTUI can generate the GPG key and set everything up in one go.

1. Launch PassTUI: `passtui`
2. Press `g` to open the **Create GPG Store** dialog
3. Fill in your **name** and **email**
4. Press `Enter`

A 4096-bit RSA key is generated and the store is initialised at `~/.password-store` (or wherever `PASSWORD_STORE_DIR` points).

> **Tip:** Set `PASSWORD_STORE_DIR` before launching if you want the store somewhere else.

### Add a New Password

1. Press `n` to open a blank entry in the editor
2. Fill in your details following this format:

   ```
   (your password)
   Username: your-username
   Url: https://example.com
   ```

3. Press `Ctrl+S` to save
4. Enter the path for the entry when prompted (e.g., `email/gmail`)

> **Tip:** The first line is always treated as the password — that's what `c` copies.

### View an Existing Password

1. Navigate the tree with `j` / `k` (or arrow keys)
2. Expand a folder or decrypt an entry with `Enter`
3. The decrypted contents appear in the editor panel on the right
4. From there:
   - `c` — copy **password**
   - `b` — copy **username**
   - `y` — copy **current line**
   - `i` — enter edit mode
   - `Ctrl+S` — save

### Sync with a Git Repository

**First time (new store)**

1. Press `s`
2. Enter the remote URL (e.g., `git@github.com:user/passwords.git`)
3. PassTUI initialises a Git repo, adds the remote, and pushes

**Already has Git**

1. Press `s`
2. PassTUI pulls with rebase, then pushes

> **Note:** If your store was cloned from an existing remote, manage the initial Git setup outside PassTUI.

### Export a GPG Key

1. Press `x` to open the **Export GPG Key** dialog
2. Optionally enter an **output path** (defaults to `~/passtui/gpg-export.asc`)
3. Press `Enter`

The key is saved as an ASCII-armored `.asc` file.

> Note: The GPG key **passphrase** will be requested using pinentry. **Warning:** Keep this file safe — anyone with it and your passphrase can decrypt your passwords.

### Import a GPG Key

1. Press `z` to open the **Import GPG Key** dialog
2. Enter the **path** to the `.asc` file (e.g., `~/passtui/gpg-export.asc`)
3. Press `Enter`

PassTUI imports the key and then locally signs it as fully trusted using one of your existing private keys. If you don't have one yet, **PassTUI** will create a new key first (you'll be asked for a passphrase using `pinentry` for it) and use that to sign the imported key.

The trust is local-only (a local signature), so it has no effect outside your machine. Once signed, PassTUI updates `.gpg-id` and re-encrypts all entries with the imported key.

> **Note:** The local signature is what tells GPG the key is trusted for encryption on this machine. It doesn't certify the key for anyone else.

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
