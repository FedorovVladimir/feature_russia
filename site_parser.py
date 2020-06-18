import requests
from bs4 import BeautifulSoup


class User:

    def __init__(self, name: str, count: int):
        self.name = name
        self.count = count

    def __str__(self):
        return f'{self.count} {self.name}'

    def __gt__(self, other):
        return self.count > other.count


def parse(max_count=None):
    url = 'https://доблестьалтая.рф/voiting'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    # получаем количество страниц
    count_pages = int(soup.find('div', class_='pagination').find_all('a')[-1].text)

    # обработка по одной странице
    users = []
    for i in range(count_pages):
        url = f'https://доблестьалтая.рф/voiting/?PAGEN_1={i + 1}'
        try:
            response = requests.get(url)
        except ConnectionError:
            return 'Не удалось получить доступ к сайту, попробуйте позже'
        soup = BeautifulSoup(response.text, 'lxml')
        cards = soup.find_all('div', class_='video_name')
        for card in cards:
            name = card.find_all('strong')[0].text
            try:
                count = int(card.find_all('span')[1].text)
                users.append(User(name, count))
            except ValueError:
                return 'Ожидалось число участников или ничего'

    users.sort(reverse=True)
    text = ''
    for i in range(len(users)):
        if i == max_count:
            break
        text += f'{str(users[i])}\n'

    return text


if __name__ == '__main__':
    print(parse())
