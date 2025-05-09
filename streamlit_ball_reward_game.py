import streamlit as st
import random

# ----------- Setup Section -----------
users = ["User1", "User2", "User3"]
selected_user = st.selectbox("👤 Select User", users)

# Initialize state for each user
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

for user in users:
    if user not in st.session_state.user_data:
        st.session_state.user_data[user] = {
            'coins': 0,
            'games_to_play': 0,
            'games_played': 0,
            'drawn_balls': [],
            'loan_taken': False,
            'loan_amount': 0,
            'revenue': 0,
            'payout': 0,
            'results': []
        }

user_state = st.session_state.user_data[selected_user]

# ----------- UI Section -----------
st.title("🎲 Ball Reward Game")

ball_emoji = {"Red": "🔴", "Blue": "🔵"}
source_bag = ['Red'] * 4 + ['Blue'] * 2
st.markdown("### 🎒 Transparent Bag")
st.markdown(" ".join([ball_emoji[color] for color in source_bag]))

if user_state['games_to_play'] == 0:
    num_games = st.selectbox("🎮 How many games do you want to play?", [5, 10, 15, 20], key=selected_user)
    entry_fee = num_games * 10

    if user_state['coins'] < entry_fee:
        loan_amount = entry_fee - user_state['coins']
        user_state['coins'] += loan_amount
        user_state['loan_taken'] = True
        user_state['loan_amount'] += loan_amount
        st.info(f"💰 Loan of {loan_amount} coins given to {selected_user} to start the game.")

    user_state['games_to_play'] = num_games
    user_state['games_played'] = 0
    user_state['drawn_balls'] = []
    user_state['results'] = []
    st.success(f"🎮 {num_games} games set for {selected_user}")

# ----------- Play Button Logic -----------
if st.button("▶️ Play", key=f"play_{selected_user}"):
    if user_state['games_played'] >= user_state['games_to_play']:
        st.warning("🎮 You've already played all your games. Click Reset to start over.")
    else:
        # Check if user has coins; lend if needed
        if user_state['coins'] < 10:
            user_state['coins'] += 10
            user_state['loan_taken'] = True
            user_state['loan_amount'] += 10
            st.info(f"💸 {selected_user} has insufficient coins. Loaned 10 coins.")

        drawn = random.sample(source_bag, 4)
        red = drawn.count('Red')
        blue = drawn.count('Blue')

        reward = 0
        if red == 4:
            reward = 50
        elif red in [1, 2, 3]:
            reward = 5

        user_state['coins'] += (reward - 10)  # 10 coin entry fee
        user_state['revenue'] += 10
        user_state['payout'] += reward
        user_state['games_played'] += 1
        user_state['drawn_balls'].append(drawn)

        result_str = (
            f"Game {user_state['games_played']}: "
            + " ".join([ball_emoji[c] for c in drawn])
            + f" → Reward: {'🏆 50 coins' if reward == 50 else '🥈 5 coins' if reward == 5 else '❌ No reward'}"
        )
        user_state['results'].append(result_str)
        st.success(result_str)
        st.info(f"🎯 {selected_user}'s coins: {user_state['coins']}")

# ----------- Show All Results So Far -----------
if user_state['results']:
    st.markdown("## 🧾 Game Results So Far")
    for res in user_state['results']:
        st.write(res)

# ----------- Profit Summary (Only on Click) -----------
if st.button("👑 Show Owner Profit Summary"):
    st.markdown("### 💼 Game Owner Profit Summary")
    total_revenue = user_state['revenue']
    total_payout = user_state['payout']
    net_profit = total_revenue - total_payout
    st.write(f"Total Revenue from {selected_user}: {total_revenue} coins")
    st.write(f"Total Payout to {selected_user}: {total_payout} coins")
    st.write(f"Net Profit from {selected_user}: {net_profit} coins")

# ----------- Reset Game Button (Only Resets Game Round) -----------
if st.button("🔁 Reset Game", key=f"reset_{selected_user}"):
    user_state['games_to_play'] = 0
    user_state['games_played'] = 0
    user_state['drawn_balls'] = []
    user_state['results'] = []
    st.success(f"✅ Game reset for {selected_user}. Coin balance and profit summary are preserved.")
