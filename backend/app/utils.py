import base64

def encode_byte(text):
  encoded_bytes = base64.b64encode(text.encode("utf-8"))
  return encoded_bytes

def decode_byte(text):
  decoded_bytes = base64.b64decode(text)
  decoded_content = decoded_bytes.decode("utf-8")
  return decoded_content