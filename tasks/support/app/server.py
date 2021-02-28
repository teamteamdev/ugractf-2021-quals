#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import hmac
import os
import sys

import aiogram
import aiohttp.web as web
import aiosqlite

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.webhook import AnswerCallbackQuery, AnswerInlineQuery, SendMessage

BASE_DIR = os.path.dirname(__file__)
STATE_DIR = sys.argv[1] if len(sys.argv) >= 2 else BASE_DIR

TOKEN_SECRET = b'sensation-absorption-satisfied-depressed-correction'
TOKEN_SALT_SIZE = 16
FLAG_SECRET = b'sculpture-generation-manufacture-execution-personality'
FLAG_SALT_SIZE = 12

HOST = 'https://support.q.2021.ugractf.ru'
BOT_TOKEN = '1627682255:AAEpdi_Xi-cvMCRO-Tl9D_7FzasSsz_j2bw'
WEBHOOK_PATH = f'/{hashlib.sha512(BOT_TOKEN.encode()).hexdigest()}'


def verify_token(token):
    return hmac.new(
        TOKEN_SECRET,
        token[:-TOKEN_SALT_SIZE].encode(),
        'sha256'
    ).hexdigest()[:TOKEN_SALT_SIZE] == token[-TOKEN_SALT_SIZE:]


def get_secret(token):
    return hmac.new(FLAG_SECRET, token.encode(), 'sha256').hexdigest()[:FLAG_SALT_SIZE]


def database_path(user_id):
    return os.path.join(STATE_DIR, f'{user_id}.sqlite')


def database_exists(user_id):
    return os.path.exists(database_path(user_id))


async def init_database(user_id, token):
    if database_exists(user_id):
        return

    async with aiosqlite.connect(database_path(user_id)) as db:
        await db.execute('''CREATE TABLE accounts (
            id integer primary key autoincrement not null,
            fio varchar(200) not null,
            account varchar(22) not null,
            codeword varchar(50) not null
        )''')
        await db.execute('''CREATE TABLE questions (
            id integer primary key autoincrement not null,
            question varchar(400) not null,
            answer varchar(400) not null
        )''')
        await db.execute(f'''INSERT INTO accounts VALUES
            (1, 'Травкин Самсон Сигизмундович', '42305978110456367807', 'conception'),
            (2, 'Борщёва Юнона Елизаровна', '42504156510177573015', 'socialist'),
            (3, 'Койначёнока Эльвира Юлиевна', '40805156210453758160', 'transparent'),
            (4, 'Бакаринцев Мирослав Капитонович', '42302810910859896336', 'recommendation'),
            (5, 'Гагарин Евсей Куприянович', '40803840810980764854', 'economics'),
            (6, 'Цейдлерин Леонид Саввевич', '40803980110033560174', 'destruction'),
            (7, 'Кравчука Виктория Семеновна', '40804810710036338322', 'professional'),
            (8, 'Швечикова Фаина Марковна', '40801978910035922897', 'community'),
            (9, 'Кудрявцев Тимофей Дмитриевич', '40802156610855387415', 'depressed'),
            (10, 'Гриневеца Ольга Брониславовна', '40805810210292238244', 'respectable'),
            (11, 'Ерохина Ника Романовна', '42502980810985306576', 'attractive'),
            (12, 'Батурина Эмилия Алексеевна', '42502978910670158633', 'contradiction'),
            (13, 'Дябин Григорий Сигизмундович', '42303810810673461305', 'challenge'),
            (14, 'Янутан Ярослав Фролович', '42304980610036211231', 'ugra_'),
            (15, 'Таначёв Рюрик Данилевич', '42504344810675574017', 'you_'),
            (16, 'Шашлов Емельян Адамович', '40805810510039540714', 'can_'),
            (17, 'Копцева Антонина Алексеевна', '42503344710985126558', 'do_'),
            (18, 'Брежнев Мирон Чеславович', '42302810410859722719', 'sqli_'),
            (19, 'Беломестныха Елизавета Серафимовна', '42305156210988580460', 'in_'),
            (20, 'Шентерякова Злата Елизаровна', '42502810510525037362', 'telegram_'),
            (21, 'Ванзин Ростислав Фролович', '40802840810679010034', 'too_'),
            (22, 'Ялбачев Гавриил Захарович', '40802344110457877093', '{get_secret(token)}'),
            (23, 'Кропанин Игорь Иванович', '42503840410031231137', 'community'),
            (24, 'Драчёва Ирина Станиславовна', '42303980810031411884', 'extraterrestrial'),
            (25, 'Кичеев Демьян Чеславович', '42304810310298252739', 'freighter'),
            (26, 'Стаина Алла Юлиевна', '42503840910293336656', 'dependence'),
            (27, 'Краснова Дина Федотовна', '42504980010171348856', 'beginning'),
            (28, 'Ивазова Виктория Брониславовна', '42304810110453721691', 'wisecrack'),
            (29, 'Янечко Евдоким Семенович', '40804344610521867983', 'miscarriage'),
            (30, 'Власова Клара Серафимовна', '42304840510176502625', 'nationalism'),
            (31, 'Кочергова Вероника Тимуровна', '42505810310453305076', 'admission'),
            (32, 'Бендлин Архип Модестович', '42505156110983773132', 'background'),
            (33, 'Коллерова Альбина Брониславовна', '42304156410036094761', 'lifestyle'),
            (34, 'Казаринова Альбина Серафимовна', '42504840110179975055', 'administration'),
            (35, 'Теплухин Осип Назарович', '40801810910178902319', 'agreement'),
            (36, 'Моргунова Виктория Святославовна', '42301840910913527944', 'qualification'),
            (37, 'Поникарова Анастасия Леонидовна', '42301840910451959607', 'compliance'),
            (38, 'Жиленкова Ксения Трофимовна', '40803344010523599304', 'temperature'),
            (39, 'Тимошкин Потап Эрнестович', '42502980510292716963', 'civilization'),
            (40, 'Жутова Наталия Иларионовна', '42503344810298918743', 'accessible'),
            (41, 'Сюкосева Светлана Игоревна', '42501810910291441118', 'establish'),
            (42, 'Кирилишен Лев Ефремович', '42304810910014871929', 'leftovers'),
            (43, 'Хлопонин Тимур Ираклиевич', '42303344810527374051', 'manufacture'),
            (44, 'Каргина Ева Родионовна', '40803344810529992814', 'understand'),
            (45, 'Лашманова Злата Фомевна', '42301840810173890025', 'hypothesis')
        ''')

        await db.execute('''INSERT INTO questions VALUES
            (1, 'Что такое Ugra Pay?', 'Ugra Pay — это международная платёжная система, которая создана специалистами НКО «Югорские платёжные решения» с использованием северных технологий и высоких стандартов информационной и физической безопасности. С Ugra Pay вам доступны не только покупки, но и снятие наличных.'),
            (2, 'Что такое «Платежная система»?', 'Ответ Раздел 2(1)(i) Закона о PSS 2007 определяет платежную систему как систему, которая позволяет производить платеж между плательщиком и получателем, включая клиринговые, платежные или расчетные услуги или все из них, но не включает фондовая биржа (раздел 34 Закона о PSS 2007 года гласит, что его положения не будут применяться к фондовым биржам или клиринговым корпорациям, созданным при фондовых биржах). Далее для пояснения указывается, что «платежная система» включает в себя системы, позволяющие выполнять операции с кредитными картами, операции с дебетовыми картами, операции со смарт-картами, операции по переводу денег или аналогичные операции. Все системы (за исключением фондовых бирж и клиринговых корпораций, созданных на базе фондовых бирж), осуществляющие клиринговые, расчетные или платежные операции, или все они считаются платежными системами. Все организации, использующие такие системы, будут называться поставщиками систем. Также все организации, работающие с системами денежных переводов, карточными платежными системами или аналогичными системами, подпадают под определение поставщика системы. Чтобы решить, управляет ли конкретная организация платежной системой, она должна выполнять либо клиринговую, либо расчетную, либо платежную функцию, либо все и то.'),
            (3, 'Почему Ugra Pay так называется?', 'А сами-то не догадываетесь?'),
            (4, 'Какие карты бывают?', 'Карты Ugra Pay эмитирует ключевой партнёр международной платёжной системы «Ugra Pay» — микропредприятие по выдаче микрокредитов АО «Югорские деньги». Они выпускают карту «Ugra Pay» уровня «Классическая». Уточнить условия выпуска и обслуживания этого типа карты вы можете в отделении банка или по телефону горячей линии.'),
            (5, 'Что такое UgraSMS?', 'НКО «Югорские платёжные решения» со всей ответственностью подходит к вашим сбережениям. Вы можете с уверенностью сказать, что ваши деньги — это наши деньги. Поэтому для дополнительной защиты от платежей в сети «Интернет», а также IPX и других, разработана инновационная технология UgraSMS, не имеющая аналогов. Чтобы подтвердить операцию по карте «Ugra Pay», вам нужно будет ввести на специализированном «платёжном шлюзе» шестизначный код, полученный в СМС-сообщении или в личном кабинете Банка-Партнёра.'),
            (6, 'Где я могу отслеживать актуальные кэшбэки за оплату?', ''),
            (7, 'Я могу использовать карту «Ugra Pay»? Это безопасно?', 'Да, это абсолютно безопасно. Карта «Ugra Pay» защищена от любых попыток платежей — её титановый корпус, семидюймовый размер и вес от 982 («Классическая») до 1117 грамм («Премиальная») сочетает в себе высокие эстетические качества, современную магнитную ленту класса C2 для быстрого проведения и антивандальные возможности'),
            (8, 'Что делать, если деньги не пришли?', 'На этапе разработки, тестирования, внедрения и использования продукции МПС «Ugra Pay» возможны различные т.н. случайные воздействия на счета клиентов, приводящие к некорректному исполнению операций. Мы рекомендуем в таких случаях повторить операцию.'),
            (9, 'Что такое QR-код?', 'QR-код МПС — это зашифрованное графическое изображение, при расшифровке которого становится доступна вся необходимая информация. Благодаря графической защите платежная информация зашифрована и защищена от прочтения без специальных программных средств, которые имеются в декодере QR-кода.'),
            (10, 'Я могу использовать мобильные приложения для оплаты картой «Ugra Pay»?', 'Для оплаты с помощью карты «Ugra Pay» в мобильном приложении сделайте следующее.\\n\\n1. Откройте карту MasterCard в вашем банке.\\n2. Осуществите перевод денежных средств на данную карту.\\n3. Используйте приложение Google Pay или приложение Apple Pay для совершения платежа.'),
            (11, 'Как я могу вернуть кешбек?', 'Чтобы вернуть кешбек обратно, необходимо обратиться с заявлением к оператору кешбека — АО «Национальная система получения кешбека» с указанием суммы кешбека и причины возврата кешбека. В течение 60 рабочих дней указанная в заявлении сумма будет списана с вашей карты.'),
            (12, 'Могу ли я получить карту дистанционно?', 'Все карты «Ugra Pay» выпускаются в двух обличиях: физическом и виртуальном. С помощью виртуальной карты вы сможете совершать операции исключительно в сетях Интернет и т.п.. Выпуск каждого обличия карты производится совершенно бесплатно, однако, в целях вашей безопасности мы рекомендуем вам выпускать только виртуальную опцию карты с помощью веб-сайта Эмитетнта.'),
            (13, 'Я могу получить бесконтактную карту «Ugra Pay»?', 'Да, карта «Мир» оформляется в виртуальном варианте, и вам не придётся с ней контактировать.'),
            (14, 'Сколько стоит обслуживание карты «Ugra Pay»?', 'Стоимость обслуживания устанавливается банком-Эмитентом самостоятельно без уведомления НКО «Югорские платёжные решения» в рамках установленых минимальных розничных цен. С вопросами об условиях эмиссии платёжных средств обращайтесь в финансовую организацию.'),
            (15, 'Как и где я могу получить карту «Ugra Pay»?', 'Карта Ugra Pay доступна к выдаче в оффлайн- и интернет-представительствах всех банков-партнёров НКО «Югорские платёжные решения».'),
            (16, 'Действует ли карта «Ugra Pay» за пределами Югры?', 'Да, за пределами Югры вы можете оплачивать товары и услуги в сети Интернет. Для оплаты с помощью карты «Ugra Pay» в магазинах сделайте следующее.\\n\\n1. Откройте карту MasterCard в вашем банке.\\n2. Осуществите перевод денежных средств на данную карту.\\n3. Используйте данную карту для совершения платежа.'),
            (17, 'Как защищена карта «Ugra Pay»?', 'Каждая карта «Ugra Pay» имеет все защитные элементы, которые обеспечивают безопасность платежей и оберегают вас от мошенников. Это логотип платёжной системы «Ugra Pay», голограмма «Ugra Pay», логотип и название банка-эмитента, серия и номер карты, видимые только в ультрафиолетовом свете, код подразделения, подпись держателя карты, код дополнительной идентификации клиента.\n\nКроме того, «Ugra Pay» — это международная платёжная система. Ваши деньги всегда будут в полной безопасности под защитой югорских технологий обеспечения безопасности.'),
            (18, 'Предоставляется ли страхование моих средств?', 'Да. Все ваши средства на 100% застрахованы платёжной системой и банком-Эмитентом от расходования.')
        ''')

        await db.commit()


def get_database_connection(user_id):
    return aiosqlite.connect(database_path(user_id))


def wrap_if(text, predicate):
    if predicate:
        return f'[{text}]'
    else:
        return text


def truncate(text):
    if len(text) < 40:
        return text
    return text[:40] + "..."


def build_bot(app):
    # pylint: disable=unused-variable

    bot = aiogram.Bot(token=BOT_TOKEN)
    dp = aiogram.Dispatcher(bot)
    dp.middleware.setup(LoggingMiddleware())

    async def get_page(user_id, page=1):
        keyboard = aiogram.types.InlineKeyboardMarkup()

        async with get_database_connection(user_id) as db:
            async with db.execute(f'SELECT question FROM questions ORDER BY id LIMIT 6 OFFSET {(page - 1) * 6}') as cursor:
                async for row in cursor:
                    keyboard.row(
                        aiogram.types.InlineKeyboardButton(
                            text=row[0],
                            callback_data=row[0][:32]
                        )
                    )

        keyboard.row(*[
            aiogram.types.InlineKeyboardButton(
                text=wrap_if(f'{opage * 6 - 5}–{opage * 6}', page == opage),
                callback_data=f'page:{opage}'
            )
            for opage in range(1, 4)
        ])

        return keyboard


    @dp.inline_handler()
    async def search(inline_query: aiogram.types.InlineQuery):
        if not inline_query.query:
            return AnswerInlineQuery(
                inline_query.id,
                []
            )

        user_id = inline_query.from_user.id

        if not database_exists(user_id):
            return AnswerInlineQuery(
                inline_query.id,
                [],
                is_personal=True,
                cache_time=3,
                switch_pm_text='Авторизуйтесь с персональной ссылкой'
            )

        results = []
        try:
            async with get_database_connection(user_id) as db:
                print(inline_query.query.encode(), flush=True)
                async with db.execute('SELECT * FROM questions WHERE question LIKE \'%' + inline_query.query + '%\' LIMIT 50') as cursor:
                    async for row in cursor:
                        if len(results) == 50:
                            break

                        results.append(aiogram.types.InlineQueryResultArticle(
                            id=f'{user_id}-{row[0]}',
                            title=row[1],
                            input_message_content=aiogram.types.InputTextMessageContent(
                                f'\u2753 *{row[1]}*\n\n\U0001F4AC {row[2]}',
                                parse_mode='Markdown'
                            ),
                            reply_markup=aiogram.types.InlineKeyboardMarkup(inline_keyboard=[[
                                aiogram.types.InlineKeyboardButton(
                                    text='\U0001F44D Спасибо!',
                                    callback_data='like'
                                )
                            ]]),
                            description=truncate(row[2])
                        ))
        except aiosqlite.OperationalError:
            pass

        return AnswerInlineQuery(
            inline_query.id,
            results,
            is_personal=True,
            cache_time=20
        )


    @dp.callback_query_handler()
    async def navigate(callback_query: aiogram.types.CallbackQuery):
        user_id = callback_query.from_user.id

        if callback_query.data == 'like':
            return AnswerCallbackQuery(
                callback_query.id,
                text='Ваше мнение очень важно для нас!',
                show_alert=True
            )

        if callback_query.data.startswith('page:'):
            try:
                page = int(callback_query.data[5:])
            except ValueError:
                return AnswerCallbackQuery(
                    callback_query.id,
                    text='Нет такой страницы',
                    show_alert=True
                )

            questions = await get_page(user_id, page)

            try:
                await bot.edit_message_text(
                    'Выберите интересующий вас вопрос:',
                    user_id,
                    callback_query.message.message_id,
                    reply_markup=questions
                )
            except aiogram.utils.exceptions.MessageNotModified:
                pass
        else:
            async with get_database_connection(user_id) as db:
                async with db.execute('SELECT * FROM questions WHERE question LIKE \'' + callback_query.data + '%\' LIMIT 1') as cursor:
                    async for row in cursor:
                        await bot.edit_message_text(
                            f'\u2753 *{row[1]}*\n\n\U0001F4AC {row[2]}',
                            user_id,
                            callback_query.message.message_id,
                            parse_mode='Markdown',
                            reply_markup=aiogram.types.InlineKeyboardMarkup(inline_keyboard=[
                                [aiogram.types.InlineKeyboardButton(
                                    text='\U0001F44D Спасибо!',
                                    callback_data='like'
                                )],
                                # [aiogram.types.InlineKeyboardButton(
                                #     text='\U0001F501 Поделиться',
                                #     switch_inline_query=row[1]
                                # )]
                            ])
                        )

        return AnswerCallbackQuery(callback_query.id)


    @dp.message_handler()
    async def echo(message: aiogram.types.Message):
        user_id = message.from_user.id

        if message.get_command() == '/start' and message.get_args() != '':
            try:
                token = message.get_args()
            except ValueError:
                return SendMessage(
                    user_id,
                    'Пожалуйста, используйте вашу персональную ссылку для входа.'
                )

            if not verify_token(token):
                return SendMessage(
                    user_id,
                    'Ваша персональная ссылка устарела. Обратитесь в центр Клиентской Поддержки.'
                )

            await init_database(user_id, token)

            text = 'Добро пожаловать в Департамент клиентской поддержки! Выберите интересующий вас вопрос:'
        else:
            text = 'К сожалению, все операторы отсутствуют. Ваш вопрос очень важен для нас, поэтому ответ на него наверняка найдётся ниже:'

        if not database_exists(user_id):
            return SendMessage(
                user_id,
                'Пожалуйста, используйте вашу персональную ссылку для входа.'
            )

        questions = await get_page(user_id)

        return SendMessage(
            user_id,
            text,
            reply_markup=questions
        )


    async def startup(_):
        await bot.set_webhook(f'{HOST}{WEBHOOK_PATH}')

    async def shutdown(_):
        await bot.delete_webhook()

    aiogram.utils.executor.set_webhook(
        dp,
        WEBHOOK_PATH,
        on_startup=startup,
        on_shutdown=shutdown,
        skip_updates=True,
        web_app=app
    )


def start():
    app = web.Application()
    build_bot(app)

    if os.environ.get('DEBUG') == 'F':
        web.run_app(app, host='0.0.0.0', port=31337)
    else:
        web.run_app(app, path=os.path.join(STATE_DIR, 'support.sock'))


if __name__ == '__main__':
    start()
