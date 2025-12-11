# 🐍 Snake AI - Deep Reinforcement Learning #
# Beadandó feladat - Mesterséges Intelligencia és Neurális Hálózatok #
# Oktató: Gégény Dávid #

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red?style=for-the-badge&logo=pytorch)
![Pygame](https://img.shields.io/badge/Pygame-Game%20Engine-green?style=for-the-badge&logo=SDL)

Egy fejlett, önvezető Snake cselekvő, amely **Deep Q-Learning (DQN)** segítségével tanul meg játszani a nulláról. A projekt nemcsak a mesterséges intelligenciát demonstrálja, hanem egy teljesen egyedi játékmotort is tartalmaz részecske-effektekkel, dinamikus akadályokkal és valós idejű analitikával.

![Demo](/progress/demo.gif)

# 📋 Tartalomjegyzék
1. [Működés és Elmélet](#-hogyan-működik-az-elmélet)
2. [Funkciók](#-kiemelt-funkciók-features)
3. [Hardverkövetelmények](#hardver)
4. [Projekt Szerkezete](#-projekt-szerkezete)
5. [Telepítés](#-telepítés-és-futtatás)
6. [Jövőbeli Tervek](#tervek)

# 🧠 Hogyan működik? (Az elmélet) #

Az ágens a környezettel való interakció során tanul (Reinforcement Learning).
- **Állapottér (Input):** 11 bool érték (Veszély iránya, Alma iránya, Haladási irány).
- **Neurális Háló:** Feed-Forward hálózat (Input: 11 -> Rejtett: 256 -> Kimenet: 3).
- **Matematikai háttér:** A döntéshozatal alapja a **Bellman-egyenlet**:

$$Q(s, a) = r + \gamma \cdot \max(Q(s', a'))$$

Ahol az ágens maximalizálja a jövőbeli várható jutalmat ($r$) a jelenlegi állapot ($s$) és cselekvés ($a$) alapján.

# ✨ Kiemelt Funkciók (Features) #

* **💣 Dinamikus Környezet:** A pályán véletlenszerűen elhelyezett **aknák/bombák** vannak. Az AI megtanulja, hogy nem csak a fal veszélyes, hanem a statikus akadályok is.
* **✨ Particle System:** "Fizikai motor" a robbanásokhoz (lila részecskék aknáknál, piros az almánál).
* **📊 Heads-Up Display (HUD):** Valós idejű adatok a képernyőn:
    * Jelenlegi "Felfedezési ráta" (Epsilon).
    * AI állapota ("GONDOLKODIK" vs "FELFEDEZ").
* **🧠 Smart Reward Shaping:** Heurisztikus jutalmazás (+1/-1.5 pont közeledésért/távolodásért), ami drasztikusan felgyorsítja a tanulást.

## <a name="hardver"></a>🖥️ Hardverkövetelmények

A projekt optimalizálva van, hogy átlagos otthoni számítógépeken is hatékonyan fusson. Dedikált videókártya (GPU/CUDA) használata támogatott, de **nem szükséges**, mivel a neurális háló architektúrája rendkívül erőforrás-takarékos.

| Komponens | Minimum | Ajánlott |
| :--- | :--- | :--- |
| **Processzor (CPU)** | Dual Core 2.0 GHz | Quad Core 3.0 GHz+ (Intel i5 / Ryzen 5) |
| **Memória (RAM)** | 4 GB | 8 GB+ |
| **Videókártya (GPU)** | Integrált grafikus kártya | (Opcionális) |
| **Tárhely** | 100 MB szabad hely | 200 MB (modelleknek és logoknak) |
| **Rendszer** | Windows 10/11, Linux, macOS | Windows 10/11 |

**Megjegyzés:** A tanítás alapértelmezetten a **CPU-t** használja. Ilyen kis modellméretnél (Bemenet: 11 -> Rejtett: 256 -> Kimenet: 3) az adatok GPU-ra mozgatásának ideje (overhead) több időt venne igénybe, mint amennyi számítási előnyt nyerne vele.

# 📂 Projekt Szerkezete

A kód moduláris felépítésű a könnyebb karbantarthatóság és bővíthetőség érdekében:

      SnakeAI/
      ├── agent.py           # 🧠 A FŐPROGRAM. Ez köti össze a játékot a modellel.
      │                        (Tartalmazza a tanítási hurkot és a memóriát)
      ├── game.py            # 🎮 JÁTÉKMOTOR. A PyGame alapú környezet.
      │                        (Grafika, részecske-effektek, bombák logikája, HUD)
      ├── model.py           # 🕸️ NEURÁLIS HÁLÓ. A PyTorch DQN implementációja.
      │                        (Linear_QNet osztály és a Trainer logika)
      ├── helper.py          # 📊 VIZUALIZÁCIÓ. Valós idejű grafikonrajzoló (Matplotlib).
      ├── make_assets.py     # 🎨 GENERÁTOR. Script a képek és hangok legyártásához.
      ├── requirements.txt   # 📦 FÜGGŐSÉGEK. A szükséges Python csomagok listája.
      └── resources/         # 📁 ASSETEK. A generált .png és .wav fájlok helye.

# 🚀 Telepítés és Futtatás #

1. **Klónozd le a repót:**
   ```bash
   git clone [https://github.com/RodeMartin/Snake_AI_DeepLearning.git](https://github.com/RodeMartin/Snake_AI_DeepLearning.git)
   cd SnakeAI

2. **Telepítsd a függőségeket:**
   ```bash
   pip install -r requirements.txt

3. **Generáld le az asseteket:** 
A projekt tartalmaz egy scriptet, ami programozottan legyártja a képeket és hangokat, így nem kell külső fájlokat letölteni.
 
   ```bash
   python make_assets.py

4. **Indítsd el az AI-t:**
   ```bash
   python agent.py

A menüben válaszd a [T]-t a tanításhoz, vagy a [P]-t a lejátszáshoz.

📈 Teljesítmény
Az ágens általában **40-50 játék** után hagyja el a véletlenszerű mozgást. A 80. játék környékén már stabilan kerüli a bombákat és stratégiát alkalmaz.

## <a name="tervek"></a>🛣️ Jövőbeli Fejlesztési Tervek (Roadmap)

Bár a projekt jelenlegi formájában teljes, a következő fejlesztésekkel lehetne tovább növelni a hatékonyságot:

- [ ] **CNN (Convolutional Neural Network) bevezetése:** A jelenlegi 11 szenzor helyett a teljes képernyő-kép elemzése, hogy az AI "lásson", ne csak érzékeljen.
- [ ] **Hamiltonian Cycle:** Egy tökéletes, verhetetlen algoritmus implementálása összehasonlítási alapnak.
- [ ] **Többügynökös Rendszer (Multi-Agent):** Két kígyó versenyeztetése ugyanazon a pályán egymás ellen.
- [ ] **Online Ranglista:** A `stats.csv` felhőbe szinkronizálása.

# 👤 Szerző
**[Ródé Martin]**
* Egyetemi hallgató - [Tokaj-Hegyalja Egyetem - PTI]
* Neptun-kód: **DRPPXL**
* GitHub: [@RodeMartin](https://github.com/RodeMartin)

# 📄 Licenc
Ez a projekt az **MIT License** alatt áll - szabadon felhasználható és módosítható oktatási célokra.
                                                                                                                                                                                                                                                         **2025.11.24.**
