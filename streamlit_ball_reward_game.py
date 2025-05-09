import streamlit as st
import random

# Initialize session state if not already initialized
if 'users' not in st.session_state:
    st.session_state.users = {
        'user1': {'coins': 60, 'games_played': 0, 'loan_taken': False, 'revenue': 0, 'payout': 0},
        'user2': {'coins': 60, 'games_played': 0, 'loan_taken': False, 'revenue': 0, 'payout': 0}
    }
if 'games_to_play' not in st.session_state:
    st.session_state.games_to_play = 0

# User selection dropdown
user = st.selectbox("🎮 Select your user", list(st.session_state.users.keys()))

# Display selected user's information
st.markdown(f"### User: {user}")
st.markdown(f"💰 Coins: {st.session_state.users[user]['coins']}")
st.markdown(f"🎮 Games Played: {st.session_state.users[user]['games_played']}")

# Ask how many games the user wants to play
num_games = st.selectbox("🎮 How many games do you want to play?", [5, 10, 15, 20])
entry_fee_per_game = 10
min_required_coins = num_games * entry_fee_per_game

# Check if the user has enough coins to play
if st.session_state.users[user]['coins'] < min_required_coins:
    if not st.session_state.users[user]['loan_taken']:
        loan_amount = min_required_coins - st.session_state.users[user]['coins']
        st.session_state.users[user]['coins'] += loan_amount
        st.session_state.users[user]['loan_taken'] = True
        st.info(f"💰 You've been lent {loan_amount} coins to start playing.")

# Button to play games
if st.button("▶️ Play"):
    if st.session_state.users[user]['coins'] <= 0:
        st.warning("😔 You don't have enough coins to play! Please reset the game.")
    else:
        # Proceed with the game logic
        for i in range(num_games):
            if st.session_state.users[user]['coins'] <= 0:
                st.warning("😔 You ran out of coins! Please reset the game.")
                break

            # Update games played
            st.session_state.users[user]['games_played'] += 1

            # Track drawn balls for the current round
            drawn_balls = random.sample(['Red'] * 4 + ['Blue'] * 2, 4)
            red = drawn_balls.count('Red')
            blue = drawn_balls.count('Blue')
            reward = 0

            if red == 4:
                reward = 50
            elif red == 3 and blue == 1:
                reward = 5

            # Update the user's coins based on the reward and entry fee
            st.session_state.users[user]['coins'] += (reward - entry_fee_per_game)
            st.session_state.users[user]['revenue'] += entry_fee_per_game
            st.session_state.users[user]['payout'] += reward

            # Display the result of the current game
            st.markdown(f"Game {st.session_state.users[user]['games_played']}: " +
                        " ".join([f"🔴" if ball == "Red" else "🔵" for ball in drawn_balls]) +
                        f" → Reward: {reward if reward > 0 else '❌ No reward'}")
            st.markdown(f"💰 Your total coins now: {st.session_state.users[user]['coins']}")

# Display the profit summary
st.markdown("### 📊 Profit Summary")
total_revenue = sum(user_data['revenue'] for user_data in st.session_state.users.values())
total_payout = sum(user_data['payout'] for user_data in st.session_state.users.values())
net_profit = total_revenue - total_payout
st.write(f"Total Revenue: {total_revenue} coins")
st.write(f"Total Payout: {total_payout} coins")
st.write(f"Net Profit: {net_profit} coins")

# Reset button (when user is done playing and wants to reset the game)
if st.button("🔁 Reset Game"):
    if st.session_state.users[user]['coins'] <= 0:
        st.session_state.users[user]['coins'] = 60  # Reset the user's coins
        st.session_state.users[user]['games_played'] = 0  # Reset games played
        st.session_state.users[user]['loan_taken'] = False  # Reset loan status
        st.session_state.users[user]['revenue'] = 0  # Reset revenue
        st.session_state.users[user]['payout'] = 0  # Reset payout
        st.success(f"✅ Game for {user} has been reset. You can start a new round!")
    else:
        st.warning("❌ You can't reset the game until you run out of coins or manually stop playing.")
