import requests
from eth_account.messages import encode_defunct
from web3 import Web3

web3 = Web3()

def main():
    invite_code = input('Enter invite code: ')
    account = web3.eth.account.create()
    address = account.address
    private_key = account.key.hex()
    session = requests.Session()
    token = session.get(f'https://0xterminal.game/api/auth/token?address={address}').json()['token']
    signable_message = encode_defunct(text=token)
    sign = web3.eth.account.sign_message(signable_message=signable_message,
                                         private_key=private_key)
    login = session.post('https://0xterminal.game/api/auth/login',
                         json={'address': address, 'signature': sign.signature.hex(), "inviteCode": invite_code})
    if login.json()['message'] == 'Invite code is already used':
        print('Invite code is already used')
        return
    else:
        with open('privates.txt', 'a') as f:
            f.write(f"{private_key}\n")
        print('Account saved to privates.txt')
        with open('accounts.txt', 'a') as f:
            f.write(f"{address} {private_key} {invite_code}\n")
        print('Account saved to accounts.txt')

if __name__ == '__main__':
    main()
