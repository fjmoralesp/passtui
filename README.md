# PassTUI

**The TUI for pass**

`PassTUI` is a Text-based user interface for `pass` [The standard unix password manager](https://www.passwordstore.org)

## Installation

`pass` relies on the `gpg` command-line tool to encrypt and decrypt passwords, so `gpg` must be installed on your system to use `PassTUI`.

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

**MacOS**

```bash
brew install gnupg
```

## Roadmap

- [ ] Config file
- [ ] Vi motions for password editor
- [ ] Custom Keybindings
- [ ] Imports
  - [ ] 1Password txt or 1pif data
  - [ ] keepass KeepassX XML data, CSV data
  - [ ] Figaro's Password Manager XML data
  - [ ] Lastpass CSV data
  - [ ] Ked Password Manager data
  - [ ] Revelation Password Manager data
  - [ ] Password Gorilla data
  - [ ] PWSafe data
  - [ ] KWallet data
  - [ ] Roboform data
  - [ ]  password-exporter data
  - [ ] pwsafe data
