from msilib.schema import MsiDigitalCertificate
from turtle import color
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Producto(Item):
    titulo = Field()
    precio = Field()
    serie = Field()
    marca = Field()
    paraUso = Field()
    tamanoPantalla = Field()
    sistemaOperativo = Field()
    entradaInterfaz  = Field()
    fabricanteCPU = Field()
    tarjeta = Field()
    caracteristicasEspeciales = Field()
    color = Field()
    contenido = Field()
    descripcion = Field()
    moreInfo = Field()

class paginaCrawler(CrawlSpider):
    name = 'Amazon'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20
    }

    download_delay = 1

    allowed_domains = ['www.amazon.com/s?k=computadoras', 'www.amazon.com/-/es']

    start_urls = ['https://www.amazon.com/s?k=computadoras&rh=n%3A13896617011&__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss']

    rules = (
        #Paginación
        Rule(
            LinkExtractor(
                allow = r'&ref=sr_pg_'
            ), follow = True
        ),
        #Detalle de los productos
        Rule(
            LinkExtractor(
                allow = r'/-/es/'
            ), follow = True, callback='parse_items'
        ),
    )

    def parse_items(self, response):
        item = ItemLoader(Producto(), response)

        item.add_xpath('titulo', '//h1[@class="a-size-large a-spacing-none"]/span/text()')
        item.add_xpath('precio', '//div[@class="a-section a-spacing-micro"]/span/text()')
        item.add_xpath('serie', '//table[@class="a-normal a-spacing-micro"]/tr[@class="a-spacing-small po-model_name"]/span[@class="a-size-base"]/text()')
        item.add_xpath('marca', '//table[@class="a-normal a-spacing-micro"]/tr[@class="a-spacing-small po-brand"]/span[@class="a-size-base"]/text()')
        item.add_xpath('paraUso', '//table[@class="a-normal a-spacing-micro"]/tr[@class="a-spacing-small po-specific_uses_for_product"]/span[@class="a-size-base"]/text()')
        item.add_xpath('tamanoPantalla', '//table[@class="a-normal a-spacing-micro"]/tr[@class="a-spacing-small po-display.size"]/span[@class="a-size-base"]/text()')
        item.add_xpath('sistemaOperativo', '//table[@class="a-normal a-spacing-micro"]/tr[@class="a-spacing-small po-operating_system"]/span[@class="a-size-base"]/text()')
        item.add_xpath('entradaInterfaz', '//table[@class="a-normal a-spacing-micro"]/tr[@class="a-spacing-small po-human_interface_input"]/span[@class="a-size-base"]/text()')
        item.add_xpath('fabricanteCPU', '//table[@class="a-normal a-spacing-micro"]/tr[@class="a-spacing-small po-cpu_model.manufacturer"]/span[@class="a-size-base"]/text()')
        item.add_xpath('tarjeta', '//table[@class="a-normal a-spacing-micro"]/tr[@class="a-spacing-small po-graphics_description"]/span[@class="a-size-base"]/text()')
        item.add_xpath('caracteristicasEspeciales', '//table[@class="a-normal a-spacing-micro"]/tr[@class="a-spacing-small po-special_feature"]/span[@class="a-size-base"]/text()')
        item.add_xpath('color', '//table[@class="a-normal a-spacing-micro"]/tr[@class="a-spacing-small po-color"]/span[@class="a-size-base"]/text()')
        item.add_xpath('contenido', '//div[@class="a-section a-spacing-medium a-spacing-top-small"]/span/text()')
        item.add_xpath('descripcion', '//div[@id="productDescription"]/p/text()')
        item.add_xpath('imagen', '//div[@class="imgTagWrapper"]/img[@data-old-hires]')

        yield item.load_item()
