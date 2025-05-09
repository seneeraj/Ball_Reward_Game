import streamlit as st
import random

# ----------------- Initial Setup -----------------

# Initialize user list and game state store
if 'users' not in st.session_state:
    st.session_state.users = ['User1', 'User2', 'User3']

if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        user: {
            'coins': 100,
            'games_to_play': 0,
            'games_played': 0,
            'loan_taken': False,
            'loan_amount': 0,
            'revenue': 0,
            'payout': 0,
            'drawn_balls': [],
        } for user in st.session_state.users
    }

# Owner summary
if 'owner_profit' not in st.session_state:
    st.session_state.owner_profit = {
        'total_revenue': 0,
        'total_payout': 0,
        'total_loans': 0
    }

# ----------------- User Selection -----------------
st.title("🎲 Ball Reward Game")
selected_user = st.selectbox("👤 Choose a player", st.session_state.users)

user_state = st.session_state.user_data[selected_user]

# ----------------- Game Setup -----------------
if user_state['games_to_play'] == 0 and user_state['games_played'] == 0:
    num_games = st.selectbox("🎮 How many games do you want to play?", [5, 10, 15, 20], key=f"select_{selected_user}")
    entry_fee = num_games * 10

    if user_state['coins'] < entry_fee:
        loan_amount = entry_fee - user_state['coins']
        user_state['coins'] += loan_amount
        user_state['loan_taken'] = True
        user_state['loan_amount'] += loan_amount
        st.info(f"💰 Loan of {loan_amount} coins given to {selected_user} to start the game.")

    user_state['coins'] -= entry_fee
    user_state['games_to_play'] = num_games
    user_state['revenue'] += entry_fee
    st.success(f"🎮 {num_games} games set for {selected_user}")

# ----------------- Game Play -----------------
if user_state['games_played'] < user_state['games_to_play']:
    if st.button("🎯 Play Next Round"):
        reward = random.choice([0, 5, 5, 5, 0, 0, 10, 0, 0, 100])  # Rare jackpot
        user_state['coins'] += reward
        user_state['payout'] += reward
        user_state['drawn_balls'].append(reward)
        user_state['games_played'] += 1

        st.write(f"🎲 Result: You won {reward} coins!")
        st.write(f"💰 Current Balance: {user_state['coins']} coins")

        if user_state['games_played'] == user_state['games_to_play']:
            st.success("✅ You've completed all selected games.")
else:
    st.info("🎮 You've already played all your games. Click Reset to start over.")

# ----------------- Show Drawn Balls -----------------
if user_state['drawn_balls']:
    st.write("📜 Game Results:", user_state['drawn_balls'])

# ----------------- Reset Game Button -----------------
if st.button("🔁 Reset Game"):
    # Do not reset coins and cumulative profit
    user_state['games_to_play'] = 0
    user_state['games_played'] = 0
    user_state['drawn_balls'] = []
    user_state['loan_taken'] = False
    user_state['loan_amount'] = 0

    # Update owner summary
    st.session_state.owner_profit['total_revenue'] += user_state['revenue']
    st.session_state.owner_profit['total_payout'] += user_state['payout']
    st.session_state.owner_profit['total_loans'] += user_state['loan_amount']

    # Reset only current game's revenue/payout (not total profit)
    user_state['revenue'] = 0
    user_state['payout'] = 0

    st.success(f"🔁 Game reset for {selected_user}. You can start a new round!")

# ----------------- Display User Status -----------------
st.markdown("---")
st.subheader("📊 User Status")
st.write(f"🧍 Player: {selected_user}")
st.write(f"💰 Coins: {user_state['coins']}")
st.write(f"🎮 Games Played: {user_state['games_played']} / {user_state['games_to_play']}")
if user_state['loan_taken']:
    st.warning(f"🏦 Loan Taken: {user_state['loan_amount']} coins")

# ----------------- Owner Profit Summary (Hidden unless clicked) -----------------
if st.checkbox("📈 Show Owner Profit Summary"):
    profit = st.session_state.owner_profit['total_revenue'] - st.session_state.owner_profit['total_payout'] - st.session_state.owner_profit['total_loans']
    st.subheader("💼 Owner Profit Summary")
    st.write(f"💵 Total Revenue Collected: {st.session_state.owner_profit['total_revenue']} coins")
    st.write(f"💸 Total Payout Given: {st.session_state.owner_profit['total_payout']} coins")
    st.write(f"🏦 Total Loans Given: {st.session_state.owner_profit['total_loans']} coins")
    st.success(f"📊 Total Profit: {profit} coins")

