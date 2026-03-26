<a name="readme-top"></a>

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
  <img width="800" alt="passtui" src="https://github.com/user-attachments/assets/33da7043-206e-4849-9c5b-951d8ec432ca" />
</div>

---

## About The Project

`PassTUI` is a terminal user interface for [pass](https://www.passwordstore.org/) — the standard Unix password manager. It brings a keyboard-driven, visual experience to your encrypted password store without ever leaving the terminal.

If you live in the terminal and want a fast, intuitive way to manage your GPG-encrypted passwords, PassTUI is for you.

### Built With

![Python][python-shield]
![Textual][textual-shield]
![passpy][passpy-shield]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Features

- Browse your password store in a tree view
- Search / filter passwords in real time
- View and edit password entries in a built-in editor
- Copy password to clipboard with a single keystroke
- Copy username to clipboard with a single keystroke
- Copy any line to clipboard
- Create a new GPG key and password store
- Add new password entries
- Sync the password store with a remote Git repository
- Export your GPG key to a file
- Import a GPG key and re-encrypt the store

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Getting Started

### Prerequisites

`pass` relies on GPG to encrypt and decrypt passwords, so `gpg` must be installed on your system.

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

```bash
brew install gnupg
```

### Installation

Install PassTUI with [uv](https://docs.astral.sh/uv/)

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

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Usage

### Create a GPG Store

If you don't have a password store yet, PassTUI can create a GPG key and initialise the store for you in one step.

1. Launch PassTUI: `passtui`
2. Press `g` to open the **Create GPG Store** dialog
3. Fill in your **name**, **email**
4. Press `Enter` to confirm

PassTUI will generate a 4096-bit RSA GPG key and initialise the store at `~/.password-store` (or the path you provided).

> **Tip:** The store path defaults to `~/.password-store`. You can also set the `PASSWORD_STORE_DIR` environment variable to point to a different location before launching PassTUI.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

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

> **Tip:** The first line is always the password. PassTUI (and `pass`) will copy only the first line when you use the copy-password shortcut.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

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

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Sync with a Git Repository

PassTUI can push and pull your password store to/from a remote Git repository.

**First-time setup (new store)**

1. Press `s` to trigger a sync
2. When prompted, enter the remote repository URL (e.g., `git@github.com:user/passwords.git`)
3. PassTUI will initialise a Git repo, add the remote, and push

**Subsequent syncs (store already has Git)**

1. Press `s`
2. PassTUI will pull with rebase and then push automatically

> **Note:** This workflow is designed for stores that were created fresh. If your store was cloned from an existing remote, manage Git operations outside of PassTUI for the initial setup.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Export a GPG Key

Exporting your GPG key lets you back it up or transfer it to another machine.

1. Press `x` to open the **Export GPG Key** dialog
2. Enter your GPG key **passphrase**
3. Optionally enter a custom **output path** (defaults to `~/passtui/gpg-export.asc`)
4. Press `Enter` to export

The key will be saved as an ASCII-armored `.asc` file.

> **Warning:** Keep this file in a safe place. Anyone who has it and knows your passphrase can decrypt your passwords.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Import a GPG Key

Importing a GPG key allows you to move your password store to a new machine or add a new trusted key.

1. Press `z` to open the **Import GPG Key** dialog
2. Enter the **path** to the `.asc` key file (e.g., `~/passtui/gpg-export.asc`)
3. Press `Enter` to import

PassTUI will import the key, mark it as ultimately trusted, update the store's `.gpg-id`, and re-encrypt all entries with the new key.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

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

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Roadmap

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

See the [open issues](https://github.com/fjmoralesp/passtui/issues) for a full list of proposed features and known issues.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Contributing

Contributions, issues, and pull requests are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup instructions.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## License

Distributed under the GNU General Public License v3. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Contact

Francisco Morales — <fjmoralesp@outlook.com>

Project Link: [https://github.com/fjmoralesp/passtui](https://github.com/fjmoralesp/passtui)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

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
