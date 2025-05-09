import streamlit as st
import random

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

st.title("🎲 Ball Reward Game")

ball_emoji = {"Red": "🔴", "Blue": "🔵"}
source_bag = ['Red'] * 4 + ['Blue'] * 2
st.markdown("### 🎒 Transparent Bag (Click Play to draw 4 balls)")
st.markdown(" ".join([ball_emoji[color] for color in source_bag]))

num_games = st.selectbox("🎮 How many games do you want to play?", [5, 10, 15, 20])
entry_fee_per_game = 10
min_required_coins = num_games * entry_fee_per_game

if st.session_state.coins < min_required_coins:
    if not st.session_state.loan_taken:
        st.session_state.coins += min_required_coins
        st.session_state.loan_taken = True
        st.info(f"💰 You've been lent {min_required_coins} coins to start playing.")

if st.button("▶️ Play"):
    st.session_state.drawn_balls.clear()

    for game in range(num_games):
        drawn = random.sample(source_bag, 4)
        st.session_state.drawn_balls.append(drawn)

        red = drawn.count('Red')
        blue = drawn.count('Blue')
        reward = 0

        if red == 4:
            reward = 50
        elif (red == 3 and blue == 1) or (red == 2 and blue == 2) or (red == 1 and blue == 3):
            reward = 5

        st.session_state.revenue += entry_fee_per_game
        st.session_state.payout += reward
        st.session_state.coins += (reward - entry_fee_per_game)

    st.markdown("## 🎯 Game Results")
    for i, balls in enumerate(st.session_state.drawn_balls):
        red = balls.count("Red")
        blue = balls.count("Blue")
        reward_str = (
            "🏆 50 coins" if red == 4 else
            "🥈 5 coins" if red in [1, 2, 3] else
            "❌ No reward"
        )
        st.write(f"Game {i+1}: " + " ".join([ball_emoji[color] for color in balls]) + f" → Reward: {reward_str}")

    st.success(f"💰 Your total coins now: {st.session_state.coins}")

with st.expander("👑 Show Game Owner Profit Summary"):
    st.markdown("### 📊 Profit Summary")
    st.write(f"Total Revenue: {st.session_state.revenue} coins")
    st.write(f"Total Payout: {st.session_state.payout} coins")
    st.write(f"Net Profit: {st.session_state.revenue - st.session_state.payout} coins")
