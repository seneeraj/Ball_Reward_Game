import streamlit as st
import random

def draw_balls():
    return [random.choice(['Red', 'Blue']) for _ in range(4)]

def count_colors(balls):
    return balls.count('Red'), balls.count('Blue')

st.set_page_config(page_title="Ball Draw Game", page_icon="🎲")

st.title("🎯 Ball Draw Game")

entry_fee_per_game = 10
reward_4_red = 50
small_reward = 5

st.markdown("Choose how many games you want to play:")
games_to_play = st.selectbox("🎮 Number of Games", options=list(range(5, 105, 5)))

current_coins = st.number_input("💰 Enter how many coins you have in your coin pocket", min_value=0, step=1)

play_game = st.button("▶️ Play")

if play_game:
    total_required_coins = games_to_play * entry_fee_per_game
    borrowed_coins = 0

    if current_coins < total_required_coins:
        borrowed_coins = total_required_coins - current_coins
        st.warning(f"⚠️ You don’t have enough coins. Lending you {borrowed_coins} coins.")
        current_coins += borrowed_coins

    total_payout = 0
    game_results = []

    for game in range(1, games_to_play + 1):
        current_coins -= entry_fee_per_game
        balls = draw_balls()
        red, blue = count_colors(balls)

        if red == 4:
            reward = reward_4_red
            outcome = f"🎉 Game {game}: 4 Red balls! Reward: {reward} coins"
        elif red == 3 and blue == 1:
            reward = small_reward
            outcome = f"Game {game}: 3 Red, 1 Blue. Reward: {reward} coins"
        elif red == 2 and blue == 2:
            reward = small_reward
            outcome = f"Game {game}: 2 Red, 2 Blue. Reward: {reward} coins"
        elif red == 1 and blue == 3:
            reward = small_reward
            outcome = f"Game {game}: 1 Red, 3 Blue. Reward: {reward} coins"
        else:
            reward = 0
            outcome = f"Game {game}: All Blue. No reward."

        current_coins += reward
        total_payout += reward
        game_results.append(f"{outcome} | Balls: {balls} | Current Balance: {current_coins} coins")

    if borrowed_coins > 0:
        st.info(f"💸 Repaying borrowed coins: {borrowed_coins}")
        current_coins -= borrowed_coins

    with st.expander("📜 Game-by-Game Results"):
        for result in game_results:
            st.write(result)

    st.subheader("📊 Game Summary")
    st.write(f"Total Games Played: {games_to_play}")
    st.write(f"Total Entry Fee Paid: {games_to_play * entry_fee_per_game} coins")
    st.write(f"Total Rewards Earned: {total_payout} coins")
    st.write(f"Net Coin Balance in Pocket: {current_coins} coins")
