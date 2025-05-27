import sys
import traceback
from datetime import datetime
from aiohttp import web
from botbuilder.core import (
    TurnContext,
    CloudAdapter,
    ConfigurationBotFrameworkAuthentication
)
from botbuilder.schema import Activity, ActivityTypes
from bot import MyBot
from config import DefaultConfig

CONFIG = DefaultConfig()

# Autenticación con CloudAdapter
bot_authentication = ConfigurationBotFrameworkAuthentication(
    app_id=CONFIG.APP_ID,
    app_password=CONFIG.APP_PASSWORD,
    tenant_id=CONFIG.APP_TENANT_ID
)

adapter = CloudAdapter(bot_authentication)

# Manejo de errores
async def on_error(context: TurnContext, error: Exception):
    print(f"\n [on_turn_error] {error}", file=sys.stderr)
    traceback.print_exc()

    await context.send_activity("El bot encontró un error.")
    if context.activity.channel_id == "emulator":
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=str(error),
            value_type="https://www.botframework.com/schemas/error",
        )
        await context.send_activity(trace_activity)

adapter.on_turn_error = on_error

# Instancia del bot
bot = MyBot()

# Ruta de mensajes
async def messages(req: web.Request) -> web.Response:
    if "application/json" in req.headers.get("Content-Type", ""):
        body = await req.json()
    else:
        return web.Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")

    response = await adapter.process_activity(activity, auth_header, bot.on_turn)
    return web.json_response(data=response.body, status=response.status) if response else web.Response(status=201)

# Servidor
app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    try:
        web.run_app(app, host="0.0.0.0", port=CONFIG.PORT)
    except Exception as error:
        raise error
