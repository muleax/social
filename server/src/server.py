import logging
import db_connection
from db_schema import *
from aiohttp import web


async def index(request):
    return web.Response(text="Main page\n")


async def users(request):
    cursor = request.app.db.cursor()
    cursor.execute(f'select * from {USERS_TABLE}')
    records = cursor.fetchall()

    return web.Response(text=f"{str(records)}\n")


def create_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/users', users)


def app_factory(db_host, db_port, db_user, db_password):
    app = web.Application()

    async def on_startup(app):
        app.db = await db_connection.open_connection(db_host, db_port, db_user, db_password)

        if app.db:
            app.db.cursor().execute(f'use {DATABASE}')
            logging.info('Worker connected to db')
            create_routes(app)
        else:
            logging.info('Worker failed to connect to db')
            # TODO

    app.on_startup.append(on_startup)
    return app


logging.basicConfig(level=logging.DEBUG)
