# 🦝 Raccoon Café: Brew & Serve ☕
[![Athena Award Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Faward.athena.hackclub.com%2Fapi%2Fbadge)](https://award.athena.hackclub.com?utm_source=readme)

Welcome to **Raccoon Café**, a cozy pixel-art game where you're the barista at the cutest café in town — and your customers? Adorable raccoons with a serious love for coffee!

---

## 🎮 Gameplay

In **Raccoon Café**, your job is to keep your furry visitors happy by:

- Brewing coffee with the coffee machine ☕  
- Dragging fresh cups to the raccoon that appears 🐾  
- Cleaning up with the trash bin 🗑️  
- Ringing the cash register for a satisfying ka-ching 💸  
- Watching for sparkles ✨ when your coffee hits the spot!

Each raccoon appears with a random coffee order (1–3 cups). Serve them right, and they’ll gleefully waddle away, making room for the next guest. With randomized raccoon sprites, no two visits feel quite the same.

---

## 🖼️ Features

- 🎨 Wholesome, hand-picked pixel art assets  
- 🐾 Three unique raccoon sprites selected randomly  
- ☕ Drag-and-drop coffee mechanic  
- 🧼 Trash bin interaction and cleanup  
- 💬 Animated dialogue box with visual cues  
- 🎵 Relaxing jazz background music  
- ✨ Sparkle effect when coffee is delivered correctly  
- 🖱️ Custom mouse cursors for added charm  
- 🎚️ Sound effects for all major interactions (click, sparkle, register, raccoon entry)

---

## 🛠️ How to Run

1. Make sure you have Python 3.x installed.
2. Install Pygame by running:
   ```bash
   pip install pygame
3. Run the game from your terminal or IDE:
   ```bash
   python main.py
   
---

## ⚠️ Challenges

- **Custom mouse cursor**: Hiding the default system cursor and replacing it with a responsive pixel-art one was tricky, especially when syncing click states.
- **Raccoon sprite randomness**: The raccoon now randomly selects one of three sprites each time it enters, instead of changing unpredictably mid-game.
- **Smooth transitions**: Creating believable movement for the raccoon entering and exiting the café, while syncing sound and dialogue timing.
- **Polishing interactions**: Adding sound, hover effects, and click feedback for the register, coffee machine, and trash can — all while keeping things intuitive and cute.

---

## 🧠 What I Learned

- How to organize a multi-file Python game using `main.py`, `cafe.py`, `coffee.py`, and a shared `game_state.py`
- Implementing drag-and-drop mechanics with smooth mouse tracking and collision detection
- Managing sprite layers so that objects like coffee cups appear in the correct visual order
- Creating timed animations (like steam and sparkle effects) using frame intervals
- Adding interactivity to UI elements with hover highlights and sounds (trash, register, coffee machine)
- Using Pygame’s sound system to play simultaneous effects and loop background music
- Debugging subtle visual issues like cursor alignment, positioning offsets, and animation timing

## 💖 Made With

- [Python](https://www.python.org/)
- [Pygame](https://www.pygame.org/)
- Coffee, chaos, and cozy vibes ☕
