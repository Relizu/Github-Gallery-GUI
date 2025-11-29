# GitHub Gallery GUI

**GitHub Gallery GUI** is an Arabic GitHub clone with a simple and intuitive interface. It allows you to log in, browse repositories, edit content, add new repositories, and download repositories. all from a desktop GUI.  

This project was created for qimma hackthon, and this `README.md` was written inside the app itself.  

---

## Features

- Login to GitHub accounts  
- Browse user repositories in a gallery-style interface  
- Edit repository content  
- Add new repositories  
- Download repositories locally  

---

## Technologies Used

- Python 3.x  
- [PySide6](https://pypi.org/project/PySide6/) (for GUI)  
- [PyGithub](https://pypi.org/project/PyGithub/) (GitHub API)  
- Requests library  
- Markdown and Base64 handling  

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Relizu/Github-Gallery-GUI
cd Github-Gallery-GUI
```
Install dependencies (make sure you have Python 3.x installed):
```bash
pip install PySide6 PyGithub requests markdown matplotlib keyring
```

## Usage

Run the application:
```bash
python Main.py
```

## Disclaimer

This application allows you to edit and manage GitHub repositories. Every change you make is committed, so nothing is permanently lost and can be undone using Git or GitHub’s interface.  

While the app cannot delete entire repositories, please be careful with your actions. I am **not responsible** for any unintended changes to repository content.
