
import streamlit as st
import random

st.set_page_config(page_title="Ball Reward Game", layout="centered")

st.title("🎲 Ball Reward Game")
st.markdown("Play a game of chance! Earn coins based on the combination of red and blue balls drawn.")

# Sidebar for inputs
st.sidebar.header("Game Settings")

games_to_play = st.sidebar.selectbox("Select number of games to play:", options=[i for i in range(5, 101, 5)])
user_coins = st.sidebar.number_input("Enter your coin pocket balance:", min_value=0, value=0, step=1)

entry_fee_per_game = 10
reward_4_red = 50
small_reward = 5
total_required_coins = games_to_play * entry_fee_per_game

if 'game_started' not in st.session_state:
    st.session_state.game_started = False

if st.sidebar.button("Start Game"):
    st.session_state.game_started = True

if st.session_state.game_started:
    borrowed_coins = 0
    current_coins = user_coins

    if current_coins < total_required_coins:
        borrowed_coins = total_required_coins - current_coins
        st.warning(f"Not enough coins! Lending you {borrowed_coins} coins.")
        current_coins += borrowed_coins

    total_payout = 0
    st.subheader("🎮 Game Results")

    for game in range(1, games_to_play + 1):
        st.markdown(f"#### Game {game}")
        current_coins -= entry_fee_per_game
        balls = [random.choice(['Red', 'Blue']) for _ in range(4)]
        red = balls.count('Red')
        blue = balls.count('Blue')
        st.write(f"Balls drawn: {balls} -> Red: {red}, Blue: {blue}")

        if red == 4:
            reward = reward_4_red
            st.success(f"🎉 You got 4 Red balls! Reward: {reward} coins")
        elif red == 3 and blue == 1:
            reward = small_reward
            st.info(f"You got 3 Red and 1 Blue balls. Reward: {reward} coins")
        elif red == 2 and blue == 2:
            reward = small_reward
            st.info(f"You got 2 Red and 2 Blue balls. Reward: {reward} coins")
        elif red == 1 and blue == 3:
            reward = small_reward
            st.info(f"You got 1 Red and 3 Blue balls. Reward: {reward} coins")
        else:
            reward = 0
            st.warning("No reward. All 4 balls are Blue.")

        current_coins += reward
        total_payout += reward
        st.write(f"💰 Current Coin Pocket Balance: {current_coins} coins")

    if borrowed_coins > 0:
        st.info(f"💸 Repaying borrowed coins: {borrowed_coins}")
        current_coins -= borrowed_coins

    st.markdown("## 🧾 Player Summary")
    st.write(f"Total Games Played: {games_to_play}")
    st.write(f"Total Entry Fee Paid: {games_to_play * entry_fee_per_game} coins")
    st.write(f"Total Rewards Earned: {total_payout} coins")
    st.write(f"Net Coin Balance in Pocket: {current_coins} coins")

    st.markdown("---")
    st.markdown("## 📊 Game Owner Summary")
    revenue = games_to_play * entry_fee_per_game
    profit = revenue - total_payout
    st.write(f"Total Revenue: {revenue} coins")
    st.write(f"Total Payout: {total_payout} coins")
    st.write(f"Net Profit: {profit} coins")

    st.success("✅ Game Over! Thanks for playing.")
