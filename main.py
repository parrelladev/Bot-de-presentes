from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from typing import Dict, List

lists: Dict[str, List[str]] = {
    'angelo': [],
    'aline': []
}

# Definir o diretório das listas de presentes
lists_directory = r'C:\Users\angel\OneDrive\Documentos\GitHub\Bot-de-presentes\listas\\'

# Definir os caminhos dos arquivos de lista
list_path = {
    'angelo': lists_directory + 'angelo.txt',
    'aline': lists_directory + 'aline.txt'
}

# Função para lidar com o comando /start
def start(update: Update, context: CallbackContext) -> None:
    """Envia uma mensagem de boas-vindas e exibe os botões para acessar as listas de presentes."""
    keyboard = [
        [InlineKeyboardButton("Lista de Angelo", callback_data='angelo')],
        [InlineKeyboardButton("Lista de Aline", callback_data='aline')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Bem-vindo(a) ao Bot de Presentes! Escolha uma das opções abaixo para acessar a lista de presentes desejada.', reply_markup=reply_markup)

# Função para lidar com o callback dos botões
def button_callback(update: Update, context: CallbackContext) -> None:
    """Redireciona para a função correspondente à opção selecionada."""
    query = update.callback_query
    query.answer()

    if query.data == 'angelo':
        angelo_list(update, context)
    elif query.data == 'aline':
        aline_list(update, context)

# Função para lidar com o comando /angelo
def angelo_list(update: Update, context: CallbackContext) -> None:
    """Exibe a lista de presentes de Angelo."""
    angelo_gifts = load_gifts(list_path['angelo'])
    if angelo_gifts:
        update.callback_query.message.reply_text('Lista de presentes de Angelo:\n' + '\n'.join(angelo_gifts))
    else:
        update.callback_query.message.reply_text('A lista de presentes de Angelo está vazia.')

# Função para lidar com o comando /aline
def aline_list(update: Update, context: CallbackContext) -> None:
    """Exibe a lista de presentes de Aline."""
    aline_gifts = load_gifts(list_path['aline'])
    if aline_gifts:
        update.callback_query.message.reply_text('Lista de presentes de Aline:\n' + '\n'.join(aline_gifts))
    else:
        update.callback_query.message.reply_text('A lista de presentes de Aline está vazia.')

# Função para carregar os presentes de um arquivo
def load_gifts(file_path: str) -> List[str]:
    """Carrega a lista de presentes de um arquivo."""
    try:
        with open(file_path, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Função para adicionar um item à lista de presentes
def add_gift(update: Update, context: CallbackContext) -> None:
    """Adiciona um item à lista de presentes."""
    user_id = update.message.from_user.id
    gift = update.message.text

    # Verifica a pasta selecionada pelo usuário
    if user_id == 767140900:  # ID do usuário Angelo
        add_gift_to_list(gift, list_path['angelo'], update)  # Adiciona à lista de Angelo
    elif user_id == 1655918277:  # ID do usuário Aline
        add_gift_to_list(gift, list_path['aline'], update)  # Adiciona à lista de Aline
    else:
        update.message.reply_text('Usuário inválido.')

# Função para adicionar um item à lista de presentes em um arquivo
def add_gift_to_list(gift: str, file_path: str, update: Update) -> None:
    """Adiciona um item à lista de presentes em um arquivo."""
    try:
        with open(file_path, 'a') as file:
            # Carrega os presentes existentes na lista
            gifts = load_gifts(file_path)
            
            # Verifica o próximo número da lista
            next_number = len(gifts) + 1
            
            # Constrói o item com o número
            item = f'{next_number}. {gift}'
            
            # Adiciona o item à lista
            file.write(item + '\n')
        
        update.message.reply_text('Item adicionado à lista de presentes.')
    except IOError:
        update.message.reply_text('Ocorreu um erro ao adicionar o item à lista de presentes.')

def main() -> None:
    """Função principal para executar o bot."""
    # Configurar o Token do bot
    updater = Updater('6282075752:AAHEL8zPMb26akk0Jp5n6M2SqPNBdXEjmGQ', use_context=True)

    # Obter o despachante para registrar os manipuladores
    dispatcher = updater.dispatcher

    # Registrar os manipuladores
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button_callback))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, add_gift))

    # Iniciar o bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from typing import Dict, List

lists: Dict[str, List[str]] = {
    'angelo': [],
    'aline': []
}

# Definir o diretório das listas de presentes
lists_directory = r'C:\Users\angel\OneDrive\Documentos\GitHub\Bot-de-presentes\listas\\'

# Definir os caminhos dos arquivos de lista
list_path = {
    'angelo': lists_directory + 'angelo.txt',
    'aline': lists_directory + 'aline.txt'
}

# Função para lidar com o comando /start
def start(update: Update, context: CallbackContext) -> None:
    """Envia uma mensagem de boas-vindas e exibe os botões para acessar as listas de presentes."""
    keyboard = [
        [InlineKeyboardButton("Lista de Angelo", callback_data='angelo')],
        [InlineKeyboardButton("Lista de Aline", callback_data='aline')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Bem-vindo(a) ao Bot de Presentes! Escolha uma das opções abaixo para acessar a lista de presentes desejada.', reply_markup=reply_markup)

# Função para lidar com o callback dos botões
def button_callback(update: Update, context: CallbackContext) -> None:
    """Redireciona para a função correspondente à opção selecionada."""
    query = update.callback_query
    query.answer()

    if query.data == 'angelo':
        angelo_list(update, context)
    elif query.data == 'aline':
        aline_list(update, context)

# Função para lidar com o comando /angelo
def angelo_list(update: Update, context: CallbackContext) -> None:
    """Exibe a lista de presentes de Angelo."""
    angelo_gifts = load_gifts(list_path['angelo'])
    if angelo_gifts:
        update.callback_query.message.reply_text('Lista de presentes de Angelo:\n' + '\n'.join(angelo_gifts))
    else:
        update.callback_query.message.reply_text('A lista de presentes de Angelo está vazia.')

# Função para lidar com o comando /aline
def aline_list(update: Update, context: CallbackContext) -> None:
    """Exibe a lista de presentes de Aline."""
    aline_gifts = load_gifts(list_path['aline'])
    if aline_gifts:
        update.callback_query.message.reply_text('Lista de presentes de Aline:\n' + '\n'.join(aline_gifts))
    else:
        update.callback_query.message.reply_text('A lista de presentes de Aline está vazia.')

# Função para carregar os presentes de um arquivo
def load_gifts(file_path: str) -> List[str]:
    """Carrega a lista de presentes de um arquivo."""
    try:
        with open(file_path, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Função para adicionar um item à lista de presentes
def add_gift(update: Update, context: CallbackContext) -> None:
    """Adiciona um item à lista de presentes."""
    user_id = update.message.from_user.id
    gift = update.message.text

    # Verifica a pasta selecionada pelo usuário
    if user_id == 767140900:  # ID do usuário Angelo
        add_gift_to_list(gift, list_path['angelo'], update)  # Adiciona à lista de Angelo
    elif user_id == 987654321:  # ID do usuário Aline
        add_gift_to_list(gift, list_path['aline'], update)  # Adiciona à lista de Aline
    else:
        update.message.reply_text('Usuário inválido.')

# Função para adicionar um item à lista de presentes em um arquivo
def add_gift_to_list(gift: str, file_path: str, update: Update) -> None:
    """Adiciona um item à lista de presentes em um arquivo."""
    try:
        with open(file_path, 'a') as file:
            # Carrega os presentes existentes na lista
            gifts = load_gifts(file_path)
            
            # Verifica o próximo número da lista
            next_number = len(gifts) + 1
            
            # Constrói o item com o número
            item = f'{next_number}. {gift}'
            
            # Adiciona o item à lista
            file.write(item + '\n')
        
        update.message.reply_text('Item adicionado à lista de presentes.')
    except IOError:
        update.message.reply_text('Ocorreu um erro ao adicionar o item à lista de presentes.')

def main() -> None:
    """Função principal para executar o bot."""
    # Configurar o Token do bot
    updater = Updater('6282075752:AAHEL8zPMb26akk0Jp5n6M2SqPNBdXEjmGQ', use_context=True)

    # Obter o despachante para registrar os manipuladores
    dispatcher = updater.dispatcher

    # Registrar os manipuladores
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button_callback))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, add_gift))

    # Iniciar o bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
