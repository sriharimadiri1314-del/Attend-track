# 🎓 Attendance Tracker — III B.Tech CSE-AI

> Daily & Weekly Attendance Tracker for **III B.Tech CSE – Artificial Intelligence**
> Academic Year: **2026-27 | I Semester**

## 🌐 Live Site
**[https://sriharimadiri1314-del.github.io/Attend-track/](https://sriharimadiri1314-del.github.io/Attend-Track/)**

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎓 Roll Number Login | Enter roll number in `2473A31___` format |
| 📅 Full Semester Schedule | Weeks 1–16 + I MID + II MID |
| ✅ Period-wise Absence Marking | Click P1–P4 to mark absent periods |
| 📊 Live Attendance % | Daily and overall percentage calculated in real-time |
| 💾 Auto-Save | Data saved in browser localStorage per roll number |
| 📥 Download JSON | Rich backup with full weekly breakdown + summary |
| 📊 Download CSV | Excel-friendly report with per-day attendance detail |
| 📤 Import Backup | Restore attendance from a previously downloaded JSON |
| 🔄 Reset | Clear all data for a roll number |
| 🌙 Dark Theme | Glassmorphism UI with animated background |

---

## 🚀 How to Use

1. Open the live site
2. Enter your roll number (last 3 digits — prefix `2473A31` is fixed)
3. Click any **P1, P2...** button to mark yourself **absent** for that period
4. Click **💾 Save** to persist your data
5. Use **📊 Download CSV** to export to Excel for your records

---

## 💾 Data Storage

Data is stored in the browser's **localStorage**, keyed by roll number:
```
attendance_2473A31042  ← per-student data
roll_number_list       ← list of all roll numbers used
```

> ⚠️ Download a JSON backup regularly to avoid data loss if you clear browser cache.

---

## 🛠 Tech Stack

- Pure **HTML + CSS + JavaScript** (no frameworks, no dependencies)
- **Google Fonts** — Outfit typeface
- **localStorage** for persistence
- Deployed via **GitHub Pages**

---

*Built with ❤️ for III B.Tech CSE-AI students*
