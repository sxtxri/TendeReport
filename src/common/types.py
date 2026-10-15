from enum import StrEnum

TenderId = int
DivisionId = int
DivisionName = str
SearchQueryId = int


# TODO(sxtxri): точно на этом уровне их хранить?
class ScrapperEndpoint(StrEnum):
    GOV_BUDGET_SUBSIDIES = "https://promote.budget.gov.ru"
    ROSELTORG = "https://www.roseltorg.ru/"
    TEK_TORG = "https://kim.tektorg.ru/"
    SIBUR_SRM = "https://srm.sibur.ru/"
    RTS_TENDER = "https://www.rts-tender.ru/"
    ETP_GPB = "http://etp.gpb.ru"
    GAZPROM_NEFT_ZAKUPKI = "https://zakupki.gazprom-neft.ru/tenderix"
    GISP = "https://gisp.gov.ru/mainpage/"
    ROSTORGI = "https://rostorgi1.ru/"
    SBERBANK_AST = "https://www.sberbank-ast.ru/Default.aspx"
    ROSTENDER = "https://rostender.info/"
    ENERGYBASE = "https://energybase.ru/tender/catalog/industrial-catalysts"
    PHOSAGRO_SERVICES = "https://etpreg.phosagro.ru/services/111280-4/"
    PHOSAGRO_TENDERS = "https://etpreg.phosagro.ru/tenders/?PAGEN_2=2"
    BIDZAAR = "https://hello.bidzaar.com/"
    METAL_IT = "https://etp.metal-it.ru/frame/index.html"
    RND_MARKET = "https://rnd.sk.ru/lk/executor"
    GAZPROM_NEFT_EP = "https://swd1.gazprom-neft.ru/irj/portal"
    B2B_CENTER = "https://www.b2b-center.ru/market/?is_p_data=223"
    GAZPROM_NEFT_EFFECT = "https://effect.gazprom-neft.ru"
