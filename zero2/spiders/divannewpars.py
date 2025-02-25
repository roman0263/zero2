import scrapy

class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/divany-i-kresla"]

    def parse(self, response):
        # Извлекаем все блоки с диванами
        divans = response.css('div._Ud0k')

        # Проходим по каждому дивану
        for divan in divans:
            # Извлекаем название
            name = divan.css('div.lsooF span::text').get()
            # Извлекаем цену и очищаем её от лишних символов
            price = divan.css('div.pY3d2 span::text').get()
            if price:
                price = price.replace('руб.', '').strip()  # Удаляем "руб." и лишние пробелы
            # Извлекаем ссылку и делаем её абсолютной
            url = divan.css('a').attrib.get('href')
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