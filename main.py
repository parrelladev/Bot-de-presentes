import requests
import telebot
from telebot import types
from typing import Dict, List
import re

lists: Dict[str, List[str]] = {
    'angelo': [],
    'aline': []
}

# Definir o diretório do arquivo main
main_directory = './'

# Definir o diretório das listas de presentes
lists_directory = main_directory + 'listas/'

# Definir os caminhos dos arquivos de lista
list_path = {
    'angelo': lists_directory + 'angelo.txt',
    'aline': lists_directory + 'aline.txt'
}

bot_token = '6282075752:AAHEL8zPMb26akk0Jp5n6M2SqPNBdXEjmGQ'

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start(message):
    """Envia uma mensagem de boas-vindas e exibe os botões para acessar as listas de presentes."""
    keyboard = types.InlineKeyboardMarkup()
    angelo_button = types.InlineKeyboardButton('Lista de Ângelo', callback_data='angelo')
    aline_button = types.InlineKeyboardButton('Lista de Aline', callback_data='aline')
    keyboard.add(angelo_button, aline_button)
    bot.send_message(message.chat.id, 'Bem-vindo(a) ao Bot de Presentes! 🎁\n\nEscolha uma lista para acessar.', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def button_callback(call):
    """Redireciona para a função correspondente à opção selecionada."""
    if call.data == 'angelo':
        angelo_list(call.message)
    elif call.data == 'aline':
        aline_list(call.message)

def angelo_list(message):
    """Exibe a lista de presentes de Angelo."""
    angelo_gifts = load_gifts(list_path['angelo'])
    if angelo_gifts:
        bot.send_message(message.chat.id, 'Lista de presentes de Ângelo:\n' + '\n'.join(angelo_gifts))
    else:
        bot.send_message(message.chat.id, 'A lista de presentes de Ângelo está vazia.')

def aline_list(message):
    """Exibe a lista de presentes de Aline."""
    aline_gifts = load_gifts(list_path['aline'])
    if aline_gifts:
        bot.send_message(message.chat.id, 'Lista de presentes de Aline:\n' + '\n'.join(aline_gifts))
    else:
        bot.send_message(message.chat.id, 'A lista de presentes de Aline está vazia.')

def load_gifts(file_path):
    """Carrega a lista de presentes de um arquivo."""
    try:
        with open(file_path, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

def shorten_url(url):
    """Encurta uma URL usando a API do encurtador.dev."""
    api_endpoint = 'https://api.encurtador.dev/encurtamentos'
    payload = {'url': url}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_endpoint, json=payload, headers=headers)

    if response.status_code == 200 or response.status_code == 201:
        data = response.json()
        return data['urlEncurtada']
    else:
        return None

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Manipula as mensagens enviadas pelo usuário."""
    user_id = message.from_user.id
    command = message.text.lower()

    if user_id == 767140900:  # ID do usuário Angelo
        if command.startswith('/remove '):
            item_number = command.split('/remove ')[1]
            delete_item_from_list(item_number, list_path['angelo'], message)
        else:
            add_gift_to_list(command, list_path['angelo'], message)
    elif user_id == 1655918277:  # ID do usuário Aline
        if command.startswith('/remove '):
            item_number = command.split('/remove ')[1]
            delete_item_from_list(item_number, list_path['aline'], message)
        else:
            add_gift_to_list(command, list_path['aline'], message)
    else:
        bot.send_message(message.chat.id, 'Usuário inválido.')

def add_gift_to_list(gift, file_path, message):
    """Adiciona um item à lista de presentes em um arquivo."""
    try:
        with open(file_path, 'a') as file:
            # Carrega os presentes existentes na lista
            gifts = load_gifts(file_path)

            # Verifica o próximo número da lista
            next_number = len(gifts) + 1

            # Verifica se é um link
            if gift.startswith('http://') or gift.startswith('https://'):
                shortened_url = shorten_url(gift)
                if shortened_url:
                    gift = shortened_url
            else:
                # Extrai a URL do texto usando expressão regular
                url_match = re.search(r'(https?://\S+)', gift)
                if url_match:
                    url = url_match.group(0)
                    shortened_url = shorten_url(url)
                    if shortened_url:
                        gift = gift.replace(url, shortened_url)

            # Constrói o item com o número
            item = f'{next_number}. {gift}'

            # Adiciona o item à lista
            file.write(item + '\n')

        bot.send_message(message.chat.id, 'Item adicionado à lista de presentes.')

        # Exibe a lista atualizada ao usuário
        if 'angelo' in file_path:
            angelo_list(message)
        elif 'aline' in file_path:
            aline_list(message)
    except IOError:
        bot.send_message(message.chat.id, 'Ocorreu um erro ao adicionar o item à lista de presentes.')


def delete_item_from_list(item_number, file_path, message):
    """Deleta um item da lista de presentes em um arquivo."""
    try:
        with open(file_path, 'r') as file:
            gifts = file.read().splitlines()

        if len(gifts) >= int(item_number):
            del gifts[int(item_number) - 1]  # Remove o item da lista

            # Atualiza os números da lista
            for i in range(int(item_number), len(gifts) + 1):
                parts = gifts[i - 1].split('. ')
                parts[0] = str(i)
                gifts[i - 1] = '. '.join(parts)

            with open(file_path, 'w') as file:
                file.write('\n'.join(gifts))  # Escreve a lista atualizada no arquivo
                file.write('\n')  # Adiciona uma nova linha vazia

            bot.send_message(message.chat.id, 'Item removido da lista de presentes.')
        else:
            bot.send_message(message.chat.id, 'Item inválido. Verifique o número do item na lista.')
    except IOError:
        bot.send_message(message.chat.id, 'Ocorreu um erro ao remover o item da lista de presentes.')

bot.polling()