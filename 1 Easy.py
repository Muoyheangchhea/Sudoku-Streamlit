import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Easy Difficulty")
st.sidebar.header("Easy Difficulty")
st.sidebar.warning("Before moving on to the next difficulty, please make sure that the timer is stopped")
st.sidebar.warning("If the puzzle doesn't change after you switch difficulty, please click on the Reset button.")


def is_valid_sudoku(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    sub_grids = [set() for _ in range(9)]

    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num == 0:
                return False

            subgrid_index = (i // 3) * 3 + j // 3

            if num in rows[i] or num in cols[j] or num in sub_grids[subgrid_index]:
                return False

            rows[i].add(num)
            cols[j].add(num)
            sub_grids[subgrid_index].add(num)

    return True


def is_safe(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num:
            return False

    for x in range(9):
        if grid[x][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    return True


def solve_sudoku(grid, row, col):
    width = 9
    if row == width - 1 and col == width:
        return True

    if col == width:
        row += 1
        col = 0

    if grid[row][col] > 0:
        return solve_sudoku(grid, row, col + 1)
    for num in range(1, width + 1, 1):
        if is_safe(grid, row, col, num):
            grid[row][col] = num
            if solve_sudoku(grid, row, col + 1):
                return True
        grid[row][col] = 0
    return False


def display_board(board):
    for i in range(9):
        cols = st.columns(9)
        if (i + 1) % 3 == 0 and i + 1 != 9:
            st.write("<hr style='border: 1px solid black; margin: 0;'>", unsafe_allow_html=True)
        for j in range(9):
            if board[i][j] == 0:
                value = cols[j].number_input("", min_value=0, max_value=9, step=1, key=f"{i}{j}", format="%d",
                                             label_visibility="collapsed", on_change=update_board, args=(i, j))
            else:
                cols[j].markdown(f"<div style='display:flex;align-items:center;justify-content:center;height:38px;'>"
                                 f"{board[i][j]}</div>", unsafe_allow_html=True)


def update_board(row, col):
    value = st.session_state[f"{row}{col}"]
    st.session_state.board[row][col] = value


if 'running' not in st.session_state:
    st.session_state.running = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'elapsed_time' not in st.session_state:
    st.session_state.elapsed_time = 0


def start_timer():
    if st.session_state.start_time is None:  # First start
        st.session_state.start_time = time.time()
    else:  # Resume
        st.session_state.start_time = time.time() - st.session_state.elapsed_time
    st.session_state.running = True


def stop_timer():
    if st.session_state.running:
        st.session_state.elapsed_time = time.time() - st.session_state.start_time
    st.session_state.running = False


def reset_timer():
    st.session_state.elapsed_time = 0
    st.session_state.start_time = None
    st.session_state.running = False


def submit_message(num):
    if num == 1:
        st.sidebar.success("Congratulations, you have solved the Sudoku!")
    else:
        st.sidebar.warning("Sorry, the solution you provided is incorrect.")


def main():
    st.title("Sudoku Game")
    st.write("Fill in the numbers to complete the Sudoku puzzle.")
    # Initial Sudoku board
    initial_board = np.array([
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ])
    if 'board' not in st.session_state:
        st.session_state.board = initial_board.copy()

    board = st.session_state.board
    display_board(board)

    def switch_to_solution():
        if solve_sudoku(board, 0, 0):
            st.session_state.board = board

    def switch_to_reset():
        if solve_sudoku(board, 0, 0):
            reset_timer()
        st.session_state.board = initial_board.copy()

    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

    with col1:
        if st.button('Start') and not st.session_state.running:
            start_timer()

    with col2:
        if st.button("Stop") and st.session_state.running:
            stop_timer()

    with col3:
        if st.button("Reset", on_click=switch_to_reset):
            pass

    with col4:
        if st.button("Submit"):
            if is_valid_sudoku(board):
                submit_message(1)
                if st.session_state.running:
                    stop_timer()
            else:
                submit_message(2)
    with col5:
        if st.button("Solve for me", on_click=switch_to_solution):
            st.sidebar.success("The Sudoku is now solved")
            if st.session_state.running:
                stop_timer()

    timer_display = st.empty()

    while st.session_state.running:
        elapsed_time = time.time() - st.session_state.start_time
        timer_display.write(f'Elapsed time: {elapsed_time:.0f} seconds')
        time.sleep(1)

    if not st.session_state.running:
        timer_display.write(f'Elapsed time: {st.session_state.elapsed_time:.0f} seconds')


if __name__ == "__main__":
    main()
