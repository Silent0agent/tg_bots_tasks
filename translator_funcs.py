from deep_translator import GoogleTranslator


def translate_text(text, source='ru', target='en'):
    translated = GoogleTranslator(source=source, target=target).translate(text)
    return translated