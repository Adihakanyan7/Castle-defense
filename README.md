# Castle-defense
# Castle Defense: Protect Your Realm 🏰

Dive into an enchanting world where you command the defense of a castle against relentless waves of enemies. With strategic upgrades and tactical decisions, how long can you hold the fort?

## Game Overview 🎮

**Castle Defense** is a game of strategy and quick reflexes. Set against a beautifully designed backdrop, the game brings forth an immersive experience:

- **Start Menu**: The game welcomes players with a simple start menu, propelling them straight into the action.
- **Upgrades Galore**: Fortify your castle by enhancing its life and defense power. But that's not all! You can also add towers that automatically target and dispatch your adversaries.
- **Engaging Progression**: The game evolves with each stage. As you advance, you'll find enemies becoming faster, stronger, and trickier. However, every victory brings greater rewards!
- **Stunning Visuals**: A feast for the eyes! The background, the animated castle, the dynamically moving towers, and the relentless enemies—all craft a visual story. Each enemy type, with its unique walking, attack, and death animations, adds depth to the game narrative.
- **Unique Mechanics**: Firing mechanisms are intricately designed using mathematical illusions, ensuring realistic projectile trajectories. The player doesn't see a regular cursor; instead, they are greeted with a weapon sight, enhancing immersion.
- **Multiple Enemies**: With four distinct types of enemies, strategizing becomes crucial. Each enemy type has its strengths and weaknesses, ensuring the game remains challenging and engaging.
- **High Score System**: A competitive spirit is at the game's core. Beat your high score and set new benchmarks!

### Technical Highlights 💻

**Castle Defense** isn't just about engaging gameplay; it showcases a rich blend of technical prowess:

- **Core Libraries**: The game leans on the `pygame` library for its interactive interface and animations. With mathematics from the `math` library, enemy movements and tower shots are calculated to perfection.
- **Singleton Design Pattern**: The Game class uses a Singleton pattern, ensuring consistent access to game variables throughout.
- **Centralized Modifiers**: A separate `game_variables` module houses all game modifiers. Any changes to the game dynamics can be made here, avoiding the need to sift through code lines.
- **Abstract Base Classes**: Leveraging the power of Python's ABCs, the game establishes a blueprint for certain functionalities, ensuring uniformity and streamlined code architecture.

## Future Enhancements & Feedback 🚀💌

Eager to dive straight into the action without the hassles of setup? Hold tight! Future iterations of "Castle Defense" aim to deliver a direct executable download. This enhancement promises a seamless user experience, allowing players to get started with just a double click.

Moreover, your insights are our treasure! Whether you're a player battling your way through or a fellow developer examining the intricacies of our code, we welcome your feedback and suggestions. Each piece of advice, critique, or idea contributes significantly to refining and elevating "Castle Defense". Join us in this journey of constant improvement!

## Setup & Execution 🛠

Given that the game has been compiled into an executable, you don't need a Python environment to play:

1. Download the compiled game.
2. Double-click the executable to launch "Castle Defense".
3. On the initial run, the game will create a folder to store the high scores.

Join the defense, strategize, upgrade, and let's see how long you can protect the castle!
