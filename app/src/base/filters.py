async def is_chat_tag(message):
    check_at = message.text.startswith('@')
    if not check_at:
        await message.answer('Чат должен начинаться с @. Пример: @test')
    return check_at
