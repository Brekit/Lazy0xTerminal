import random

import requests
from eth_account.messages import encode_defunct
from web3 import Web3

web3 = Web3()

def load_privates():
    with open('privates.txt', 'r') as f:
        return f.read().splitlines()


def analyze_response(word_guess_history, words):
    excluded_positions = {}

    for hist_item in word_guess_history:
        if hist_item['amountGuessed'] == 0:
            for index, letter in enumerate(hist_item['word']):
                excluded_positions[index] = letter

    def is_valid_word(word):
        for index, letter in enumerate(word):
            if index in excluded_positions and excluded_positions[index] == letter:
                return False
        for hist_item in word_guess_history:
            count = sum(hist_item['word'][index] == letter for index, letter in enumerate(word))
            if hist_item['amountGuessed'] != count:
                return False
        return True

    return [word for word in words if is_valid_word(word)]


def main():
    private_keys = load_privates()
    for private_key in private_keys:
        address = web3.eth.account.from_key(private_key).address
        print(f'Working with address: {address}')
        session = requests.Session()
        token = session.get(f'https://0xterminal.game/api/auth/token?address={address}').json()['token']
        signable_message = encode_defunct(text=token)
        sign = web3.eth.account.sign_message(signable_message=signable_message,
                                             private_key=private_key)
        session.post('https://0xterminal.game/api/auth/login', json={'address': address, 'signature': sign.signature.hex()})

        finish = False

        while not finish:
            last_game = session.get('https://0xterminal.game/api/game/last').json()
            if last_game.get('error') == 'Not Found' or last_game['status'] == 'WIN' or last_game['status'] == 'LOSE':
                print('Game finished, start new')
                game = session.post('https://0xterminal.game/api/game/create').json()
            else:
                game = last_game
            if game.get('message') == 'You have no games left today':
                print('You have no games left today')
                finish = True
            else:
                word = random.choice(analyze_response(game['wordGuessHistory'], game['words']))
                print(f'Choose word: {word}')
                session.post('https://0xterminal.game/api/game/move', json={"userGameId":game['userGameId'],"guessWord":word})


if __name__ == '__main__':
    main()





# Telegram: @megajid
# Telegram: @megajid
# Telegram: @megajid
# Telegram: @megajid
# Telegram: @megajid
# Telegram: @megajid
# Telegram: @megajid
# Telegram: @megajid
# Telegram: @megajid
# Telegram: @megajid
# Telegram: @megajid
# Telegram: @megajid
# Telegram: @megajid












