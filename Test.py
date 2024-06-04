import streamlit as st
import copy
import time

st.set_page_config(page_title="Play Sudoku", page_icon="🎮")


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


def save_game(board):
    with open('saved_game.txt', 'w') as file:
        for row in board:
            file.write(' '.join(map(str, row)) + '\n')


def load_game():
    with open('saved_game.txt', 'r') as file:
        board = [line.strip().split() for line in file]
    return board


def add_css():
    st.markdown(
        """
        <style>
        .sudoku-table td {
            border: 1px solid #000;
            text-align: center;
            width: 50px;
            height: 50px;
        }
        .sudoku-table .top { border-top: 3px solid #000; }
        .sudoku-table .left { border-left: 3px solid #000; }
        .sudoku-table .bottom { border-bottom: 3px solid #000; }
        .sudoku-table .right { border-right: 3px solid #000; }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_board_with_borders(board):
    html = "<table class='sudoku-table'>"
    for i, row in enumerate(board):
        html += "<tr>"
        for j, cell in enumerate(row):
            cell_class = []
            if i % 3 == 0:
                cell_class.append("top")
            if j % 3 == 0:
                cell_class.append("left")
            if i == 8:
                cell_class.append("bottom")
            if j == 8:
                cell_class.append("right")
            class_attr = " ".join(cell_class)
            html += f"<td class='{class_attr}'>{cell if cell != 0 else ''}</td>"
        html += "</tr>"
    html += "</table>"
    return html


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


def display_input_boxes(board):
    for i in range(9):
        cols = st.columns(9, gap='small')
        for j in range(9):
            value = board[i][j]
            if initial_board[i][j] != 0:
                cols[j].markdown(f"<div style='display:flex;align-items:center;justify-content:center;height:38px;'>"
                                 f"{value}</div>", unsafe_allow_html=True)
            else:
                new_value = cols[j].text_input(f"Cell {i+1},{j+1}:small_red_triangle_down:", str(value) if value != 0 else "", key=f"{i},{j}", max_chars=1)
                if new_value.isdigit() and 1 <= int(new_value) <= 9:
                    board[i][j] = int(new_value)
                elif new_value.isdigit() and int(new_value) <= 0:
                    st.warning("Value must be greater than 0.")
                elif new_value == "":
                    board[i][j] = 0


initial_board = [
    [0, 0, 0, 6, 0, 0, 4, 0, 0],
    [7, 0, 0, 0, 0, 3, 6, 0, 0],
    [0, 0, 0, 0, 9, 1, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 5, 0, 1, 8, 0, 0, 0, 3],
    [0, 0, 0, 3, 0, 6, 0, 4, 5],
    [0, 4, 0, 2, 0, 0, 0, 6, 0],
    [9, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 1, 0, 0]
]


def main():
    st.title("Sudoku Game")

    board_input = copy.deepcopy(initial_board)

    st.write("Fill in the blank spaces correctly to solve it.")

    board_display = st.empty()

    display_input_boxes(board_input)

    st.sidebar.subheader("Actions")
    timer_display = st.sidebar.empty()

    if st.sidebar.button("Start Timer") and not st.session_state.running:
        start_timer()

    if st.sidebar.button("Stop Timer") and st.session_state.running:
        stop_timer()

    if st.sidebar.button("Submit"):
        if is_valid_sudoku(board_input):
            st.sidebar.success("Congratulations, you have solved the Sudoku.")
            if st.session_state.running:
                stop_timer()
        else:
            st.sidebar.warning("Sorry, the solution you provided was incorrect.")

    if st.sidebar.button("Solve for me"):
        if solve_sudoku(board_input, 0, 0):
            st.sidebar.success("Sudoku is now solved.")
            if st.session_state.running:
                stop_timer()

    if st.sidebar.button("Reset Board"):
        reset_timer()
        board_input = copy.deepcopy(initial_board)

    if st.sidebar.button("Save Game"):
        save_game(board_input)
        st.sidebar.success("Game saved successfully.")

    if st.sidebar.button("Load Game"):
        loaded_board = load_game()
        add_css()
        sudoku_html = render_board_with_borders(loaded_board)
        st.sidebar.markdown(sudoku_html, unsafe_allow_html=True)

    add_css()
    board_display.markdown(render_board_with_borders(board_input), unsafe_allow_html=True)

    while st.session_state.running:
        elapsed_time = time.time() - st.session_state.start_time
        timer_display.subheader(f'Elapsed time: {elapsed_time:.0f} seconds')
        time.sleep(1)

    if not st.session_state.running:
        timer_display.subheader(f'Elapsed time: {st.session_state.elapsed_time:.0f} seconds')


if __name__ == "__main__":
    main()
