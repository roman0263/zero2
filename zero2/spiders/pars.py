import scrapy

class SvetSpider(scrapy.Spider):
    name = "svet"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def parse(self, response):
        # Извлекаем все блоки с товарами
        products = response.css('div._Ud0k')  # Уточните селектор, если он отличается

        # Проходим по каждому товару
        for product in products:
            # Извлекаем название
            name = product.css('div.lsooF span::text').get()
            # Извлекаем цену и очищаем её от лишних символов
            price = product.css('div.pY3d2 span::text').get()
            if price:
                price = price.replace('руб.', '').replace(' ', '').strip()  # Удаляем "руб." и пробелы
            # Извлекаем ссылку и делаем её абсолютной
            url = product.css('a').attrib.get('href')
            if url:
                url = response.urljoin(url)  # Преобразуем в полный URL

            # Возвращаем данные, если все поля заполнены
            if name and price and url:
                yield {
                    'name': name,
                    'price': price,
                    'url': url
                }
            else:
                # Логируем пропущенный элемент, если данные неполные
                self.logger.warning(f"Пропущен элемент: name={name}, price={price}, url={url}")

        # Обработка нескольких страниц
        # Ищем ссылку на следующую страницу
        next_page = response.css('a.PaginationLink[data-testid="item"]::attr(href)').getall()
        if next_page:
            # Предположим, что последний элемент в списке — это следующая страница
            next_page_url = next_page[-1]  # Берём последний элемент
            yield response.follow(next_page_url, callback=self.parse)