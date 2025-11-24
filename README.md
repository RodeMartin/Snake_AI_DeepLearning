# 🐍 Snake AI - Deep Reinforcement Learning #

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red?style=for-the-badge&logo=pytorch)
![Pygame](https://img.shields.io/badge/Pygame-Game%20Engine-green?style=for-the-badge&logo=SDL)

Egy fejlett, önvezető Snake cselekvő, amely **Deep Q-Learning (DQN)** segítségével tanul meg játszani a nulláról. A projekt nemcsak a mesterséges intelligenciát demonstrálja, hanem egy teljesen egyedi játékmotort is tartalmaz részecske-effektekkel, dinamikus akadályokkal és valós idejű analitikával.

![Demo](/progress/demo.png)

# 🧠 Hogyan működik? (Az elmélet) #

Az ágens a környezettel való interakció során tanul (Reinforcement Learning).
- **Állapottér (Input):** 11 bool érték (Veszély iránya, Alma iránya, Haladási irány).
- **Neurális Háló:** Feed-Forward hálózat (Input: 11 -> Rejtett: 256 -> Kimenet: 3).
- **Matematikai háttér:** A döntéshozatal alapja a **Bellman-egyenlet**:

$$Q(s, a) = r + \gamma \cdot \max(Q(s', a'))$$

Ahol az ágens maximalizálja a jövőbeli várható jutalmat ($r$) a jelenlegi állapot ($s$) és cselekvés ($a$) alapján.

# ✨ Kiemelt Funkciók (Features) #

* **💣 Dinamikus Környezet:** A pályán véletlenszerűen elhelyezett **aknák/bombák** vannak. Az AI megtanulja, hogy nem csak a fal veszélyes, hanem a statikus akadályok is.
* **✨ Particle System:** Saját fejlesztésű fizikai motor a robbanásokhoz (lila részecskék aknáknál, piros az almánál).
* **📊 Heads-Up Display (HUD):** Valós idejű adatok a képernyőn:
    * Jelenlegi "Felfedezési ráta" (Epsilon).
    * AI állapota ("GONDOLKODIK" vs "FELFEDEZ").
* **🧠 Smart Reward Shaping:** Heurisztikus jutalmazás (+1/-1.5 pont közeledésért/távolodásért), ami drasztikusan felgyorsítja a tanulást.

# 🚀 Telepítés és Futtatás #

1. **Klónozd le a repót:**
   ```bash
   git clone [https://github.com/RodeMartin/SnakeAI.git](https://github.com/RodeMartin/SnakeAI.git)
   cd SnakeAI

2. **Telepítsd a függőségeket:**

pip install -r requirements.txt

3. **Generáld le az asseteket:** 
A projekt tartalmaz egy scriptet, ami programozottan legyártja a képeket és hangokat, így nem kell külső fájlokat letölteni.

python make_assets.py

4. **Indítsd el az AI-t:**

python agent.py

A menüben válaszd a [T]-t a tanításhoz, vagy a [P]-t a lejátszáshoz.

📈 Teljesítmény
Az ágens általában **40-50 játék** után hagyja el a véletlenszerű mozgást. A 80. játék környékén már stabilan kerüli a bombákat és stratégiát alkalmaz.