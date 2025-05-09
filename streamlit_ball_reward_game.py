import streamlit as st
import random

# Initialize session state
if 'coins' not in st.session_state:
    st.session_state.coins = 0
if 'loan_taken' not in st.session_state:
    st.session_state.loan_taken = False
if 'revenue' not in st.session_state:
    st.session_state.revenue = 0
if 'payout' not in st.session_state:
    st.session_state.payout = 0
if 'drawn_balls' not in st.session_state:
    st.session_state.drawn_balls = []
if 'games_to_play' not in st.session_state:
    st.session_state.games_to_play = 0
if 'games_played' not in st.session_state:
    st.session_state.games_played = 0
if 'entry_fee_per_game' not in st.session_state:
    st.session_state.entry_fee_per_game = 10

st.title("🎲 Ball Reward Game")

ball_emoji = {"Red": "🔴", "Blue": "🔵"}
source_bag = ['Red'] * 4 + ['Blue'] * 2
st.markdown("### 🎒 Transparent Bag (Click Play to draw 4 balls)")
st.markdown(" ".join([ball_emoji[color] for color in source_bag]))

# Step 1: Choose number of games
if st.session_state.games_to_play == 0:
    num_games = st.selectbox("🎮 How many games do you want to play?", [5, 10, 15, 20])
    entry_fee_per_game = 10
    total_fee = num_games * entry_fee_per_game

    if st.button("💥 Start Game"):
        if st.session_state.coins < total_fee:
            if not st.session_state.loan_taken:
                st.session_state.coins += total_fee
                st.session_state.loan_taken = True
                st.info(f"💰 You've been lent {total_fee} coins to start playing.")
        st.session_state.games_to_play = num_games
        st.session_state.games_played = 0
        st.session_state.drawn_balls = []
        st.session_state.entry_fee_per_game = entry_fee_per_game
        st.success("🎮 Game started! Click ▶️ Play to draw balls.")

# Step 2: Play game one at a time
if st.session_state.games_to_play > 0 and st.session_state.games_played < st.session_state.games_to_play:
    if st.button("▶️ Play"):
        drawn = random.sample(source_bag, 4)
        st.session_state.drawn_balls.append(drawn)

        red = drawn.count('Red')
        blue = drawn.count('Blue')
        reward = 0

        if red == 4:
            reward = 50
        elif (red == 3 and blue == 1) or (red == 2 and blue == 2) or (red == 1 and blue == 3):
            reward = 5

        # Update game stats
        st.session_state.revenue += st.session_state.entry_fee_per_game
        st.session_state.payout += reward
        st.session_state.coins += (reward - st.session_state.entry_fee_per_game)
        st.session_state.games_played += 1

# Step 3: Show game results
if st.session_state.drawn_balls:
    st.markdown("## 🎯 Game Results So Far")
    for i, balls in enumerate(st.session_state.drawn_balls):
        red = balls.count("Red")
        reward_str = (
            "🏆 50 coins" if red == 4 else
            "🥈 5 coins" if red in [1, 2, 3] else
            "❌ No reward"
        )
        st.write(f"Game {i+1}: " + " ".join([ball_emoji[color] for color in balls]) + f" → Reward: {reward_str}")
    st.success(f"💰 Your total coins now: {st.session_state.coins}")

# Step 4: Summary
if st.session_state.games_played == st.session_state.games_to_play and st.session_state.games_to_play > 0:
    st.info("🎉 All games played! Start a new session to play again.")
    if st.button("🔁 Reset Game"):
        st.session_state.games_to_play = 0
        st.session_state.games_played = 0
        st.session_state.drawn_balls = []

with st.expander("👑 Show Game Owner Profit Summary"):
    st.markdown("### 📊 Profit Summary")
    st.write(f"Total Revenue: {st.session_state.revenue} coins")
    st.write(f"Total Payout: {st.session_state.payout} coins")
    st.write(f"Net Profit: {st.session_state.revenue - st.session_state.payout} coins")
