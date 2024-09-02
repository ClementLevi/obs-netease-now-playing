**Forked from [@NSLC/netease-now-playing 1](https://obsproject.com/forum/resources/netease-now-playing.1944/), but s/he didn't offer a repo and it contains bug in the latest release.**

---

A Python Script for Obtaining Song Titles/Artists from [NetEase Cloud Music] Based on Process Class Lookups

**Requirements:**
- Windows 10/11
- Python > 3.8.0
- win32gui latest
- Code:
```cmd
pip install pywin32
```
- Netease Music playing (background OK, minimize OK, tray NOT OK)

  
**Usage:**
1. Download this script
2. Set Your Python Path in OBS - Tool - Script - Python Settings
3. Add a Text (GDI+) source in your scene
4. Load the script, fill and change parameters as you like, set the source to the text added just now
5. (IF U CANT see the text source you like, refresh(reload) the script)
6. It should be working

![image](https://github.com/user-attachments/assets/0273bf1e-3e4c-46b9-9ff5-38b90866599b)
