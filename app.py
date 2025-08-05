import streamlit as st
import random
import time

st.set_page_config(page_title="Hand Cricket", page_icon="🏏", layout="centered")

def initialize_game():
    """Sets up the initial state for a new game."""
    st.session_state.clear() 
    st.session_state.game_stage = "toss_choice"
    st.session_state.user_score = 0
    st.session_state.computer_score = 0
    st.session_state.target = 0
    st.session_state.who_is_batting = None
    st.session_state.toss_winner = None
    st.session_state.game_over = False
    st.session_state.last_user_choice = "-"
    st.session_state.last_computer_choice = "-"
    st.session_state.wickets_down = False
    st.session_state.message = ""
    st.session_state.message_type = "default"


def display_scoreboard():
    """Displays the current scores and target if applicable."""
    col1, col2 = st.columns(2)
    col1.metric("Your Score", f"{st.session_state.user_score}")
    col2.metric("Computer's Score", f"{st.session_state.computer_score}")
    
    if st.session_state.target > 0:
        st.info(f"**Target to Win: {st.session_state.target}**")

def display_last_ball():
    """Shows the choices from the last ball played."""
    st.write("---")
    col1, col2 = st.columns(2)
    col1.write(f"**You Played:** `{st.session_state.last_user_choice}`")
    col2.write(f"**Computer Played:** `{st.session_state.last_computer_choice}`")
    st.write("---")

def display_message():
    """Displays the outcome of the last ball."""
    if st.session_state.message:
        if st.session_state.message_type == "success":
            st.success(st.session_state.message)
        elif st.session_state.message_type == "warning":
            st.warning(st.session_state.message)
        elif st.session_state.message_type == "error":
            st.error(st.session_state.message)
        else:
            st.info(st.session_state.message)

# --- Game Logic Functions ---

def handle_toss(user_toss_choice):
    """Handles the coin toss logic."""
    user_num = st.session_state.last_user_choice
    comp_num = random.randint(1, 6)
    st.session_state.last_computer_choice = comp_num
    
    total = user_num + comp_num
    result = "even" if total % 2 == 0 else "odd"

    if user_toss_choice.lower() == result:
        st.session_state.toss_winner = "user"
        st.session_state.message = f"It's {total} ({result}). You won the toss!"
        st.session_state.message_type = "success"
        st.session_state.game_stage = "bat_or_bowl_choice"
    else:
        st.session_state.toss_winner = "computer"
        st.session_state.message = f"It's {total} ({result}). The computer won the toss."
        st.session_state.message_type = "warning"
        # Computer makes a choice
        computer_decision = random.choice(["batting", "bowling"])
        st.session_state.who_is_batting = "computer" if computer_decision == "batting" else "user"
        st.session_state.game_stage = "playing"
        st.session_state.message += f" and chose to **{computer_decision}**."

def handle_play(user_choice):
    """Handles the main game logic for one ball."""
    computer_choice = random.randint(1, 6)
    st.session_state.last_user_choice = user_choice
    st.session_state.last_computer_choice = computer_choice

    # Check for OUT
    if user_choice == computer_choice:
        st.session_state.wickets_down = True
        st.session_state.message = "OUT! Wicket Down!"
        st.session_state.message_type = "error"
        
        # If first innings, set the target and switch sides
        if st.session_state.target == 0:
            if st.session_state.who_is_batting == "user":
                st.session_state.target = st.session_state.user_score + 1
                st.session_state.who_is_batting = "computer"
            else: # Computer was batting
                st.session_state.target = st.session_state.computer_score + 1
                st.session_state.who_is_batting = "user"
            st.session_state.wickets_down = False # Reset for next innings
        else: # Second innings is over
            st.session_state.game_over = True
        return

    # If not out, add runs
    if st.session_state.who_is_batting == "user":
        st.session_state.user_score += user_choice
        st.session_state.message = f"You scored {user_choice} runs!"
        st.session_state.message_type = "success"
    else: # Computer is batting
        st.session_state.computer_score += computer_choice
        st.session_state.message = f"Computer scored {computer_choice} runs."
        st.session_state.message_type = "info"

    # Check for win in second innings
    if st.session_state.target > 0:
        if st.session_state.user_score >= st.session_state.target or st.session_state.computer_score >= st.session_state.target:
            st.session_state.game_over = True


# --- Main App ---

st.title("🏏 Hand Cricket Game")

# Initialize the game if it's not already started
if "game_stage" not in st.session_state:
    initialize_game()

# --- STAGE 1: TOSS ---
if st.session_state.game_stage == "toss_choice":
    st.header("The Toss")
    st.write("Choose a number and then select Even or Odd.")
    
    cols = st.columns(6)
    for i in range(1, 7):
        with cols[i-1]:
            if st.button(str(i), key=f"toss_num_{i}"):
                st.session_state.last_user_choice = i
    
    if isinstance(st.session_state.last_user_choice, int):
        st.info(f"You chose: **{st.session_state.last_user_choice}**. Now call the toss.")
        
        toss_col1, toss_col2 = st.columns(2)
        if toss_col1.button("Even", use_container_width=True):
            handle_toss("even")
        if toss_col2.button("Odd", use_container_width=True):
            handle_toss("odd")

# --- STAGE 2: USER DECIDES TO BAT OR BOWL ---
if st.session_state.game_stage == "bat_or_bowl_choice":
    display_message()
    st.header("What do you want to do?")
    col1, col2 = st.columns(2)
    if col1.button("🏏 Bat First", use_container_width=True):
        st.session_state.who_is_batting = "user"
        st.session_state.game_stage = "playing"
    if col2.button("🥎 Bowl First", use_container_width=True):
        st.session_state.who_is_batting = "computer"
        st.session_state.game_stage = "playing"

# --- STAGE 3: PLAYING THE GAME ---
if st.session_state.game_stage == "playing" and not st.session_state.game_over:
    # Display whose turn it is
    if st.session_state.who_is_batting == "user":
        st.header("You are Batting")
    else:
        st.header("You are Bowling")

    display_scoreboard()
    display_last_ball()
    display_message()

    st.write("**Choose your number (1-6):**")
    cols = st.columns(6)
    for i in range(1, 7):
        with cols[i-1]:
            if st.button(str(i), key=f"play_num_{i}", use_container_width=True):
                handle_play(i)
                # Rerun to update the UI immediately after a button press
                st.rerun()

# --- STAGE 4: GAME OVER ---
if st.session_state.game_over:
    display_scoreboard()
    display_last_ball()
    st.header("Game Over!")

    # Determine winner
    if st.session_state.user_score > st.session_state.computer_score:
        st.balloons()
        st.success("🎉 Congratulations! You won the match! 🎉")
    elif st.session_state.computer_score > st.session_state.user_score:
        st.error("Better luck next time! The Computer won.")
    else:
        st.warning("It's a TIE! What a close match!")

# --- PLAY AGAIN BUTTON ---
# This button will appear at all stages after the toss
if st.session_state.game_stage != "toss_choice":
    if st.button("🔄 Play Again"):
        initialize_game()
        st.rerun()
