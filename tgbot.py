import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Инициализация поля
board = [' ' for _ in range(9)]
current_player = 'X'

def display_board():
    return f"{board[0]}|{board[1]}|{board[2]}\n-+-+-\n{board[3]}|{board[4]}|{board[5]}\n-+-+-\n{board[6]}|{board[7]}|{board[8]}"

def check_winner():
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in winning_combinations:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global board, current_player
    board = [' ' for _ in range(9)]
    current_player = 'X'
    await update.message.reply_text("Игра началась! Используйте /move 1-9 чтобы продать душу неграм.\n" + display_board())

async def move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_player
    try:
        position = int(context.args[0]) - 1
        if board[position] == ' ':
            board[position] = current_player
            winner = check_winner()
            if winner:
                await update.message.reply_text(f"Игрок {winner} даун!\n{display_board()}")
                return
            elif ' ' not in board:
                await update.message.reply_text("ебать вы дауны!\n" + display_board())
                return

            current_player = 'O'
            bot_move()
            winner = check_winner()
            if winner:
                await update.message.reply_text(f"Игрок {winner} даун!\n{display_board()}")
            elif ' ' not in board:
                await update.message.reply_text("ебать вы дауны!\n" + display_board())
            else:
                current_player = 'X'
                await update.message.reply_text(display_board())
        else:
            await update.message.reply_text("Ты даун? Сюда нельзя ставить.")
    except (IndexError, ValueError):
        await update.message.reply_text("Ой долбоеб, используй /move 1-9.")

def bot_move():
    available_positions = [i for i, x in enumerate(board) if x == ' ']
    if available_positions:
        position = random.choice(available_positions)
        board[position] = 'O'

def main():
    application = Application.builder().token('YOUR_BOT_TOKEN').build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('move', move))
    application.run_polling()

if __name__ == '__main__':
    main()
